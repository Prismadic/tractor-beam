import os, requests, importlib, time, csv

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from ..utils.globals import writeme, files, _f, check
from ..utils.config import Job
from ..clone.beacons import *

@dataclass
class AbductState:
    conf: Optional[dict] = None
    job: Optional[dict] = None
    data: List[Dict[str, str]] = field(default_factory=list)

class Abduct:
    def __init__(self, conf: dict = None, job: Job = None):
        try:
            self.state = AbductState(conf=conf.conf, job=job)
            return _f('info', f'Abduct initialized\n{self.state}')
        except Exception as e:
            return _f('warn', f'no configuration loaded\n{e}')

    def _fetch_to_write(self, attachment, headers, attachment_path, file_name, block_size, o=False):
        if os.path.exists(attachment_path) and not o:
            return _f('warn', f"File exists at {attachment_path}, and overwrite is disabled. Skipping download.")
        response = requests.get(attachment, stream=True, headers=headers)
        response.raise_for_status()
        try:
            writeme(response.iter_content(block_size), attachment_path)
            self.state.data.append({ "file": file_name, "path": attachment_path})
        except Exception as e:
            _f('fatal',e), False

    def download(self, o: bool=False, f: str=None):
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
        if self.state.conf.role == 'watcher': # a watcher and may have recursion
            module = importlib.import_module("tractor_beam.clone.beacons."+self.state.job.beacon)
            watcher_class = getattr(module, 'Stream')
            watcher = watcher_class(self.state.conf,self.state.job)
            filings = watcher.run()
            for filing in filings:
                filing_path = os.path.join(proj_path, filing['title'])
                if self.state.job.types: # has recursion
                    dedupe = [] # fix for multiple paths, same name
                    for attachment in filing['attachments']:
                        if attachment.split('/')[-1] not in dedupe:
                            dedupe.append(attachment.split('/')[-1])
                            time.sleep(0.5)
                            file_name = filing['title'].replace("/", "_") + '_' + attachment.split('/')[-1]
                            attachment_path = os.path.join(filing_path, file_name)
                            if check(os.path.join(self.state.conf.settings.proj_dir, "visits.csv")):
                                if not any(attachment_path == row[1] \
                                    for row in csv.reader(open(os.path.join(self.state.conf.settings.proj_dir, "visits.csv")))
                                ):
                                    self._fetch_to_write(attachment, headers, attachment_path, file_name, block_size, o)
                                else:
                                    _f('warn', f"filing exists in 🛸 project visits, skipping download\n{attachment_path}")
                            else:
                                self._fetch_to_write(attachment, headers, attachment_path, file_name, block_size, o)

                else:  # no recursion
                    self._fetch_to_write(attachment, headers, attachment_path, file_name, block_size, o)
            self._files=filings
            _f('success', f'{len(self._files)} downloaded')
            return self.state
        elif self.state.job.types: # not a watcher, but does have recursion
            response = requests.get(self.job['url'], stream=True, headers=headers)
            response.raise_for_status()
            safe = response.status_code==200
            _files = files(response.content, self.state.job['url'], self.state.job['types'])
            for _file in _files:
                f = f'{proj_path}/{_file.split("/")[-1]}'
                self.state.data.append({"file":_file, "path":f'{os.path.join(proj_path,_file.split("/")[-1])}'})
                writeme(response.iter_content(block_size), f) if safe else _f('fatal',response.status_code), False
            _f('success', f'{len(_files)} downloaded')
            return self.state
        else: # just a simple URL
            self.state.data.append({"file":self.job["url"], "path":f'{os.path.join(proj_path,self.job["url"].split("/")[-1])}'})
            writeme(response.content, f) if safe else _f('fatal',response.status_code)
            return self.state