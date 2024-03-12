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
# The `State` class in Python contains a data attribute that is a list of `BeamState` objects.
class State:
    data: List[BeamState] = field(default_factory=list)

# The `Beam` class in Python defines methods for running jobs related to Abduct, Focus, and Record,
# handling both immediate and delayed jobs with configurable settings.
class Beam:
    def __init__(self, config: str | dict = None):
        """
        The function initializes an object with a list attribute, a configuration object, and a state
        object.
        
        :param config: The `config` parameter in the `__init__` method is used to initialize the object
        with configuration settings. It can be either a string or a dictionary. If a string is provided,
        it will be passed to the `Config` class to create a configuration object. If a dictionary is
        provided
        :type config: str | dict
        """
        self.runs = []
        self.config = Config(config)
        self.state = State()

    def _runner(self, job):
        """
        This Python function runs a series of tasks related to Abduct, Focus, and Record, updating
        states and data accordingly.
        
        :param job: It looks like the code snippet you provided is a method called `_runner` that takes
        two parameters: `self` and `job`. The method performs a series of operations using instances of
        classes `Abduct`, `Focus`, and `Record`, updates the state, downloads data, processes it,
        creates
        :return: The `_runner` method returns the `self.runs` list, which contains a dictionary with
        keys "config", "Abduct", "Records", "Focus", "data", and "status".
        """
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
        """
        The function `job_with_delay` runs a job repeatedly with a specified delay between each
        execution.
        
        :param job: It looks like the `job` parameter is an object that contains information about a
        specific job to be executed. This object seems to have a `delay` attribute that specifies the
        delay between each execution of the job. The `job_with_delay` function is designed to repeatedly
        execute the job using the `_
        """
        _f('warn', f'watching with {job.delay} delay')
        while True:
            self._runner(job)
            time.sleep(job.delay)

    def process_job(self, job):
        """
        The function `process_job` checks if a job has a delay and calls different methods based on the
        delay value.
        
        :param job: It looks like the code snippet you provided is a method called `process_job` that
        takes two parameters: `self` and `job`. The method checks if the `job` has a delay that is not
        None and greater than 0. If the delay meets the condition, it calls the `
        """
        if not job.delay == None and job.delay > 0:
            self.job_with_delay(job)
        else:
            self._runner(job)

    def go(self, cb=None):
        """
        The `go` function processes a list of jobs, allocating CPU resources based on the number of
        available cores and handling both immediate and delayed jobs.
        
        :param cb: The `cb` parameter in the `go` method is a callback function that can be passed as an
        argument. It is optional, meaning it has a default value of `None`. This callback function can
        be used to perform additional actions or handle events after certain operations are completed
        within the `go`
        """
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