import os, csv
from tractor_beam.utils.globals import check_headers, dateme, _f, check
from tractor_beam.utils.config import Job

class Record:
    def __init__(self, conf: dict = None, job: Job = None):
        self.headers = []
        self.job = job
        self.conf = conf.conf
        self.data = []
        return _f('info', 'Records initialized') if conf else _f('warn', f'no configuration loaded')

    def create(self, data: dict=None, o: bool = False):
        proj_path = os.path.join(self.conf.settings.proj_dir,self.conf.settings.name)
        if check(os.path.join(proj_path,'visits.csv')) and not o:
            return _f('warn', f'{proj_path} exists')
        else:
            with open(os.path.join(proj_path,'visits.csv'), 'w') as _:
                io = csv.writer(_)
                if data is not None:
                    self.headers = check_headers(data[0])
                    self.data = data
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
        check_headers(self)
        _ = [x for x in csv.DictReader(open(self.proj_path, 'r'))]
        if self.data is None:
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
        proj_path = os.path.join(self.conf.settings.proj_dir,self.conf.settings.name)
        self.headers.append('ts') if ts and 'ts' not in self.headers else None
        if check(proj_path):
            with open(os.path.join(proj_path,'visits.csv'), 'w+' if o else 'a') as _:
                io = csv.DictWriter(_) if isinstance(self.data, dict) else csv.writer(_)
                io.writerow(self.headers) if self.headers and o else None
                [dateme(x) for x in self.data]
                [io.writerow(x.values()) for x in self.data]
                _f('success', f'{list(self.data[0].keys())}' if v else f'{len(self.data)} written to {os.path.join(proj_path, "visits.csv")}')
        else:
            _f('fatal', 'path not found')
            
    def destroy(self, confirm: str = None):
        if confirm==self.proj_path.split('/')[-1]:
            os.remove(self.proj_path), _f('warn', f'{confirm} destroyed from {self.proj_path}') 
        else:
            _f('fatal','you did not confirm - `Records.destroy(confirm="file_name")`')
        