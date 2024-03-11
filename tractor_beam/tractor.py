from .utils.globals import _f
from .utils.config import Config
from .utils.quantum import BeamState

from .clone.abduct import Abduct
from .visits.record import Record
from .laser.focus import Focus

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

    def _runner(self, job):
        state = BeamState()

        a = Abduct(self.config, job)
        state.abduct_state_update(a.state)
        self.state.data.append(state) if a.state else _f("fatal", "`Abduct` did not report state!!")

        f = Focus(self.config, job)
        state.focus_state_update(f.state)
        self.state.data.append(state) if f.state else _f("fatal", "`Focus` did not report state!!")

        r = Record(self.config, job)
        state.record_state_update(r.state)
        self.state.data.append(state) if r.state else _f("fatal", "`Record` did not report state!!")

        a.download()
        f.process(a.state.data)
        r.create(f.state.data)
        r.write()
        
        if self.config and a and r and f:
            _f('success', '🛸 done')
            self.runs.append({
                "config": self.config
                , "Abduct": a
                , "Records": r
                , "Focus": f
                , "data": self.state.data
                , "status": 'complete'
            })
            return self.runs

    def job_with_delay(self, job):
        _f('warn', f'watching with {job.delay} delay')
        while True:
            self._runner(job)
            time.sleep(job.delay)

    def process_job(self, job):
        if not job.delay == None and job.delay > 0:
            self.job_with_delay(job)
        else:
            self._runner(job)

    def go(self, cb=None):
        self.config.unbox()
        _f('wait', f'tractor beaming with "{self.config.conf.settings.name}" project')

        jobs = self.config.conf.settings.jobs
        num_cores = cpu_count()
        num_jobs = len(jobs)
        _f('info', f"starting {num_jobs} jobs allocating {num_jobs/num_cores*100}% CPU total")
        num_processes = min(num_jobs, num_cores)
        immediate_jobs = [job for job in jobs if not hasattr(job, "delay")]
        delayed_jobs = [job for job in jobs if hasattr(job, "delay")]

        if immediate_jobs:
            with Pool(processes=num_processes) as pool:
                pool.map(self.process_job, immediate_jobs)

        for job in delayed_jobs:
            self.process_job(job)