from tractor_beam.utils.globals import _f
from tractor_beam.utils.config import Config
from tractor_beam.utils.quantum import BeamState
from tractor_beam.abducts.abduct import Abduct
from tractor_beam.visits.visit import Visit
from tractor_beam.processor import VisitsProcessor

import time
from typing import List
from dataclasses import dataclass, field
from multiprocessing import Pool, cpu_count


@dataclass
class State:
    data: List[BeamState] = field(default_factory=list)


class Beam:
    def __init__(self, config: str | dict = None):
        self.runs = []
        self.config = Config(config)
        self.state = State()

    async def _runner(self, job, cb):
        state = BeamState()

        if 'abduct' in job.tasks:
            a = Abduct(self.config, job)
            await a.download()
            state.abduct_state_update(a.state)
            self.state.data.append(state) if a.state else _f(
                "fatal", "`Abduct` did not report state!!")
        else:
            a = None
        if 'visits' in job.tasks:
            v = Visit(self.config, job)
            v.create(a.state.data)
            v.write()
            state.visit_state_update(v.state)
            self.state.data.append(state) if v.state else _f(
                "fatal", "`Visit` did not report state!!")
        else:
            v = None
        if 'process' in job.tasks:
            p = VisitsProcessor(v.state, job)
            await p.process_visits()
            state.visits_processor_state_update(p.state)
            self.state.data.append(state) if p.state else _f(
                "fatal", "`VisitsProcessor` did not report state!!")
        else:
            p = None
        if self.config and a and v:
            _f('success', '🛸 done')
            self.runs.append({
                "config": self.config,
                "Abduct": a,
                "Visits": v,
                "Processor": p,
                "data": self.state.data,
                "status": 'complete'
            })
            if cb is not None:
                await cb(self.runs)
            else:
                return self.runs

    async def job_with_delay(self, job, cb):
        _f('warn', f'watching with {job.delay} delay')
        while True:
            await self._runner(job, cb=cb)
            time.sleep(job.delay)

    async def process_job(self, job, cb):
        if not job.delay == None and job.delay > 0:
            await self.job_with_delay(job, cb=cb)
        else:
            await self._runner(job, cb=cb)

    async def go(self, cb=None):
        self.config.unbox()
        _f('wait',
           f'tractor beaming with "{self.config.conf.settings.name}" project')

        jobs = self.config.conf.settings.jobs
        num_cores = cpu_count()
        num_jobs = len(jobs)
        _f('info',
           f"starting {num_jobs} jobs allocating {num_jobs/num_cores*100}% CPU total")
        num_processes = min(num_jobs, num_cores)
        immediate_jobs = [job for job in jobs if not hasattr(job, "delay")]
        delayed_jobs = [job for job in jobs if hasattr(job, "delay")]

        if immediate_jobs:
            with Pool(processes=num_processes) as pool:
                for job in immediate_jobs:
                    # Use apply_async instead of map to handle each job individually
                    pool.apply_async(self.process_job,
                                     args=(job, cb), callback=cb)

                # Wait for all tasks to complete
                pool.close()
                pool.join()

        for job in delayed_jobs:
            # Process delayed jobs outside the pool
            await self.process_job(job, cb=cb)
