from .utils.globals import _f, check, likethis
import os, shutil, time
from tractor_beam.utils.config import Config
from tractor_beam.clone.replicator import Abduct
from tractor_beam.visits.sites import Record
from tractor_beam.laser.purify import Focus
from multiprocessing import Pool, cpu_count

class Beam:
    def __init__(self, config: str | dict = None):
        self.runs = []
        self.config = Config(config)
        _ = likethis(self.config.conf)
        if not _[0]:
            _f('fatal', _[1])

    def _runner(self, job):
        copy = Abduct(self.config)
        f = Focus(self.config)
        r = Record(self.config)
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
        if "delay" in job:
            _f('warn', f'watching with {job["delay"]} delay')
            while True:
                self._runner(job)
                time.sleep(job["delay"])

    def process_job(self, job):
        if "delay" in job:
            self.job_with_delay(job)
        else:
            self._runner(job)

    def go(self, cb=None):
        self.config.use()
        self.config.unbox()
        _f('wait', f'tractor beaming with "{self.config.conf["settings"]["name"]}" project')

        jobs = self.config.conf['settings']['jobs']
        num_cores = cpu_count()
        num_jobs = len(jobs)
        _f('info', f"starting {num_jobs} jobs allocating {num_jobs/num_cores*100}% CPU total")
        num_processes = min(num_jobs, num_cores)
        immediate_jobs = [job for job in jobs if "delay" not in job]
        delayed_jobs = [job for job in jobs if "delay" in job]

        if immediate_jobs:
            with Pool(processes=num_processes) as pool:
                pool.map(self.process_job, immediate_jobs)

        for job in delayed_jobs:
            self.process_job(job)

    def destroy(self, confirm:str = None):
        if not check(os.path.join(self.config.conf['settings']['proj_dir'], self.config.conf['settings']['name'])):
            return _f('fatal', f'invalid path - {self.p}')
        if confirm==self.config.conf["settings"]["name"]:
            shutil.rmtree(os.path.join(self.config.conf['settings']['proj_dir'], self.config.conf['settings']['name'])), _f('warn', f'{confirm} destroyed')
        else:
            _f('fatal','you did not confirm - `tractor_beam.destroy("your_config_name")`')

