import os, csv

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from tractor_beam.utils.globals import check_headers, dateme, _f, check
from tractor_beam.utils.config import Job

@dataclass
class RecordState:
    conf: Optional[dict] = None
    job: Optional[dict] = None
    data: List[Dict[str, str]] = field(default_factory=list)

class Record:
    def __init__(self, conf: dict = None, job: Job = None):
        self.headers = []
        try:
            self.state = RecordState(conf=conf.conf, job=job)
            return _f('info', f'Record initialized\n{self.state}')
        except Exception as e:
            return _f('warn', f'no configuration loaded\n{e}')

    def create(self, data: dict=None, o: bool = False):
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