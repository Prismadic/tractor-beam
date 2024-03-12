import os, csv

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from tractor_beam.utils.globals import check_headers, dateme, _f, check
from tractor_beam.utils.config import Job

@dataclass
# The `RecordState` class in Python defines attributes for configuration, job information, and a list
# of data dictionaries.
class RecordState:
    conf: Optional[dict] = None
    job: Optional[dict] = None
    data: List[Dict[str, str]] = field(default_factory=list)

# The `Record` class in Python defines methods for initializing a record with configuration and job
# parameters, creating and writing data to a CSV file, and seeking specific data within the file.
class Record:
    def __init__(self, conf: dict = None, job: Job = None):
        """
        This Python function initializes a record with optional configuration and job parameters,
        handling exceptions and returning messages accordingly.
        
        :param conf: The `conf` parameter is a dictionary that is used to pass configuration settings or
        options to the `__init__` method of a class. It can contain key-value pairs that provide
        necessary information for initializing the object. In the code snippet you provided, the `conf`
        dictionary is used to initialize
        :type conf: dict
        :param job: The `job` parameter in the `__init__` method appears to be an instance of a `Job`
        class. It is likely used to provide information or configuration related to a specific job or
        task within the context of the class where this method is defined. The `job` parameter is
        expected
        :type job: Job
        :return: The code snippet provided is a part of a class constructor (`__init__` method) in
        Python. It seems to be attempting to initialize a `Record` object with a given configuration
        dictionary (`conf`) and a `Job` object (`job`).
        """
        self.headers = []
        try:
            self.state = RecordState(conf=conf.conf, job=job)
            return _f('info', f'Record initialized\n{self.state}')
        except Exception as e:
            return _f('warn', f'no configuration loaded\n{e}')

    def create(self, data: dict=None, o: bool = False):
        """
        This Python function creates a CSV file for storing visit data, with optional data input and
        error handling.
        
        :param data: The `data` parameter in the `create` method is a dictionary that contains the data
        to be written to a CSV file. If this parameter is provided, the method will use the data to
        create the CSV file
        :type data: dict
        :param o: The 'o' parameter in the `create` method is a boolean flag that indicates whether to
        overwrite an existing file. If `o` is set to `True`, the method will overwrite the existing file
        at the specified path. If `o` is set to `False` (the default value, defaults to False
        :type o: bool (optional)
        :return: If the condition `check(os.path.join(proj_path,'visits.csv')) and not o` is met, the
        function will return a warning message using the `_f` function with the message `f'{proj_path}
        exists'`. Otherwise, if the condition is not met, the function will create a new CSV file at the
        path `os.path.join(proj_path,'visits.csv')` and
        """
        proj_path = os.path.join(self.state.conf.settings.proj_dir,self.state.conf.settings.name)
        if check(os.path.join(proj_path,'visits.csv')) and not o:
            return _f('warn', f'{proj_path} exists')
        else:
            with open(os.path.join(proj_path,'visits.csv'), 'w') as _:
                io = csv.writer(_)
                if data is not None:
                    self.headers = check_headers(data)
                    self.state.data = data
                else:
                    _f('fatal','no data passed to visits')
                self.headers.append('ts')
                io.writerow(self.headers) if data is not None else _f('info', f'[{", ".join(self.headers)}] header used')
        _f('info', f'created {os.path.join(proj_path, "visits.csv")}')

    def seek(self, line: str | int = None, all: bool = False):
        """
        This Python function named `seek` reads a CSV file and searches for a specific line or value
        within the data, with options to return all data or a specific line.
        
        :param line: The `line` parameter in the `seek` method can be either a string or an integer. If
        it is a string, the method will search for that string within the data and return any matching
        entries. If it is an integer, the method will attempt to return the entry at that index in
        :type line: str | int
        :param all: The `all` parameter in the `seek` method is a boolean flag that determines whether
        to return all data from a file or not. If `all` is set to `True`, the method will return all
        data from the file specified by `self.proj_path`. If `all` is set, defaults to False
        :type all: bool (optional)
        :return: The `seek` method returns different results based on the input parameters:
        """
        if all:
            if line is not None:
                return _f('fatal','you have `line` and `all` set')
            with open(self.proj_path, 'r') as _:
                o = [x for x in csv.DictReader(_)]
                return o
        _ = [x for x in csv.DictReader(open(self.proj_path, 'r'))]
        if self.state.data is None:
            return _f('fatal', 'no data passed')
        if isinstance(line, int):
            try:
                return _[line]
            except Exception as e:
                _f('fatal', 'index error')
        if isinstance(line, str):
            _r = []
            for datum in _:
                if [x for x in datum.values() if line in x]:
                    _r.append(datum)
                _f('info', f'found {line} in data')
            return _r
        
    def write(self, o: bool = False, ts: bool = True, v: bool = False):
        """
        This function writes data to a CSV file, with options to overwrite or append, and provides
        feedback on the operation.
        
        :param o: The `o` parameter in the `write` method is a boolean flag that determines whether to
        overwrite the existing file (`'w+'`) or append to the existing file (`'a'`) when opening the
        file for writing. If `o` is `True`, the file will be opened in, defaults to False
        :type o: bool (optional)
        :param ts: The `ts` parameter in the `write` method is a boolean flag that determines whether to
        include a timestamp in the headers of the CSV file being written. If `ts` is `True` and the
        string 'ts' is not already in the list of headers, then the 'ts', defaults to True
        :type ts: bool (optional)
        :param v: The `v` parameter in the `write` method is a boolean flag that determines whether
        additional information should be displayed upon successful completion of writing data to a CSV
        file. If `v` is set to `True`, it will display the list of keys from the first data entry if
        available, otherwise, defaults to False
        :type v: bool (optional)
        """
        proj_path = os.path.join(self.state.conf.settings.proj_dir,self.state.conf.settings.name)
        self.headers.append('ts') if ts and 'ts' not in self.headers else None
        if check(proj_path):
            with open(os.path.join(proj_path,'visits.csv'), 'w+' if o else 'a') as _:
                io = csv.DictWriter(_) if isinstance(self.state.data, dict) else csv.writer(_)
                io.writerow(self.headers) if self.headers and o else None
                [dateme(x) for x in self.state.data]
                [io.writerow(x.values()) for x in self.state.data]
                _f('success', f'{list(self.state.data[0].keys())}' if v else f'{len(self.state.data)} written to {os.path.join(proj_path, "visits.csv")}')
        else:
            _f('fatal', 'path not found')