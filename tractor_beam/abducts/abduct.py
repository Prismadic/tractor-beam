import os
import requests
import importlib
from tractor_beam.utils.globals import _f, writeme, files
from tractor_beam.utils.config import Job
from .beacons import *
from tractor_beam.utils.quantum import AbductState

class Abduct:
    def __init__(self, conf: dict = None, job: Job = None, cb=None):
        try:
            self.state = AbductState(conf=conf.conf, job=job)
            self.cb = cb
            return _f('info', f'Abduct initialized\n{self.state}')
        except Exception as e:
            return _f('warn', f'no configuration loaded\n{e}')

    async def download(self, f: str=None):
        proj_path = os.path.join(self.state.conf.settings.proj_dir,self.state.conf.settings.name)            
        block_size = 1024
        
        _f('info',f"running job:\n{self.state.job}")
        headers = {
            "User-Agent": "PostmanRuntime/7.23.3",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        } if not hasattr(self.state.job.custom, "headers") \
            else self.state.job.custom['headers']
        f = f'{proj_path}/{self.state.job.url.split("/")[-1]}'
        if self.state.conf.role in ['watcher', 'server']: # a watcher and may have recursion
            module = importlib.import_module("tractor_beam.abducts.beacons."+self.state.job.beacon)
            watcher_class = getattr(module, 'Stream')
            watcher = watcher_class(self.state)
            filings = await watcher.run()
            self.state.data=filings
            _f('success', f'{len(self.state.data)} downloaded')
            return self.state
        elif self.state.job.types: # not a watcher, but does have recursion
            response = requests.get(self.state.job.url, stream=True, headers=headers, timeout=10)
            response.raise_for_status()
            safe = response.status_code==200
            _files = files(response.content, self.state.job.url, self.state.job.types)
            for _file in _files:
                f = f'{proj_path}/{_file.split("/")[-1]}'
                writeme(response.iter_content(block_size), f) if safe else _f('fatal',response.status_code), False
                self.state.data.append({"file":_file, "path":f'{os.path.join(proj_path,_file.split("/")[-1])}'})
                if self.cb: self.cb(self.state)
            _f('success', f'{len(_files)} downloaded')
            return self.state
        else: # just a simple URL
            response = requests.get(self.state.job.url, stream=True, headers=headers, timeout=10)
            safe = response.status_code==200
            writeme(response.content, f) if safe else _f('fatal',response.status_code)
            _f('success', '1 downloaded')
            self.state.data.append({"file":self.state.job.url, "path":f'{os.path.join(proj_path,self.state.job.url.split("/")[-1])}'})
            if self.cb: self.cb(self.state)
            return self.state