import os, requests, importlib, time, csv

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from ..utils.globals import writeme, files, _f, check
from ..utils.config import Job
from ..clone.beacons import *

@dataclass
# The `AbductState` class in Python contains attributes for configuration, job, and data stored as a
# list of dictionaries.
class AbductState:
    conf: Optional[dict] = None
    job: Optional[dict] = None
    data: List[Dict[str, str]] = field(default_factory=list)

# The class `Abduct` in Python contains methods for initializing an object with configuration settings
# and job details, as well as for downloading files from URLs with options for handling different
# scenarios.
class Abduct:
    def __init__(self, conf: dict = None, job: Job = None):
        """
        The function initializes an Abduct object with a given configuration and job, handling
        exceptions if configuration loading fails.
        
        :param conf: The `conf` parameter in the `__init__` method is expected to be a dictionary
        containing configuration settings. It is used to initialize the `AbductState` object with the
        provided configuration settings. If no configuration is provided, the default value is set to
        `None`
        :type conf: dict
        :param job: The `job` parameter in the `__init__` method is of type `Job`. It is used as an
        input to initialize the `AbductState` object within the class
        :type job: Job
        :return: The code snippet provided is a part of a class constructor (`__init__` method) in
        Python.
        """
        try:
            self.state = AbductState(conf=conf.conf, job=job)
            return _f('info', f'Abduct initialized\n{self.state}')
        except Exception as e:
            return _f('warn', f'no configuration loaded\n{e}')

    def _fetch_to_write(self, attachment, headers, attachment_path, file_name, block_size, o=False):
        """
        This function fetches a file from a URL and writes it to a specified path, with options to
        overwrite existing files and handle exceptions.
        
        :param attachment: The `attachment` parameter is typically a URL pointing to the location of the
        file that needs to be fetched and written to the specified path. It could be a direct link to a
        file or a resource that needs to be downloaded
        :param headers: The `headers` parameter in the `_fetch_to_write` method is used to pass any
        additional HTTP headers that may be required for the request. These headers can include
        information such as authentication tokens, content type, user-agent, etc. They are sent along
        with the request to provide additional information to the
        :param attachment_path: The `attachment_path` parameter in the `_fetch_to_write` method is the
        path where the downloaded attachment file will be saved on the local file system. It is the
        location where the file will be written to after being downloaded from the provided URL
        (`attachment`)
        :param file_name: The `file_name` parameter in the `_fetch_to_write` method is used to specify
        the name of the file that will be saved to the `attachment_path`. It is a string that represents
        the name of the file being downloaded or written
        :param block_size: The `block_size` parameter in the `_fetch_to_write` function is used to
        specify the size of the data blocks to be read from the response stream and written to the file
        during the download process. It helps in controlling the amount of data read and written at a
        time, which can be useful
        :param o: The 'o' parameter in the function `_fetch_to_write` is a boolean flag that indicates
        whether to overwrite an existing file at the specified `attachment_path`. If `o` is set to
        `True`, the function will overwrite the file if it already exists. If `o` is set to, defaults to
        False (optional)
        :return: a tuple containing a log message and a boolean value. The log message is a warning if
        the file already exists at the specified path and overwrite is disabled, indicating that the
        download will be skipped. The boolean value is False, indicating that the download was not
        successful.
        """
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
        """
        This Python function downloads files from URLs, with options for handling different scenarios
        like recursion and watching for new files.
        
        :param o: The `o` parameter in the `download` method is a boolean parameter with a default value
        of `False`. It is used to specify whether the download operation should overwrite existing files
        or not. If `o` is set to `True`, the download operation will overwrite existing files, and if
        it, defaults to False
        :type o: bool (optional)
        :param f: The `f` parameter in the `download` method is used to specify the file path where the
        downloaded file will be saved. If `f` is not provided, the method will generate a file path
        based on the project path and the filename extracted from the URL
        :type f: str
        :return: The `self.state` object is being returned at the end of the `download` method.
        """
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
                else: # no recursion
                    self._fetch_to_write(attachment, headers, attachment_path, file_name, block_size, o)
            self._files=filings
            _f('success', f'{len(self._files)} downloaded')
            return self.state
        
        elif self.state.job.types: # not a watcher, but does have recursion
            response = requests.get(self.job['url'], stream=True, headers=headers)
            response.raise_for_status()
            safe = response.status_code==200
            _files = files(response.content, self.state.job.url, self.state.job.types)
            for _file in _files:
                f = f'{proj_path}/{_file.split("/")[-1]}'
                writeme(response.iter_content(block_size), f) if safe else _f('fatal',response.status_code), False
                self.state.data.append({"file":_file, "path":f'{os.path.join(proj_path,_file.split("/")[-1])}'})
            _f('success', f'{len(_files)} downloaded')
            return self.state
        else: # just a simple URL
            response = requests.get(self.state.job.url, stream=True, headers=headers)
            safe = response.status_code==200
            writeme(response.content, f) if safe else _f('fatal',response.status_code)
            _f('success', '1 downloaded')
            self.state.data.append({"file":self.state.job.url, "path":f'{os.path.join(proj_path,self.state.job.url.split("/")[-1])}'})
            return self.state