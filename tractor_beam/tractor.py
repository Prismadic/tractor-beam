from .utils.globals import _f
from .utils.config import Config

from .clone.abduct import Abduct
from .visits.record import Record
from .laser.focus import Focus

import time
from multiprocessing import Pool, cpu_count

class Beam:
    def __init__(self, config: str | dict = None):
        self.runs = []
        self.config = Config(config)

    def _runner(self, job):
        copy = Abduct(self.config, job)
        f = Focus(self.config, job)
        r = Record(self.config, job)
        data = copy.download()
        p_data = f.process(data)
        r.create(p_data)
        r.write()
        if self.config and copy and r and f:
            _f('success', '🛸 done')
            self.runs.append({
                "config": self.config
                , "Abduct": copy
                , "Records": r
                , "Focus": f
                , "data": data
                , "status": 'complete'
            })
            return self.runs

    def job_with_delay(self, job):
        _f('warn', f'watching with {job.delay} delay')
        while True:
            self._runner(job)
            time.sleep(job.delay)

    def process_job(self, job):
        if hasattr(job, "delay"):
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