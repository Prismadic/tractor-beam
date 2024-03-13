import chardet

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from tractor_beam.utils.tools import Strip
from tractor_beam.utils.globals import writeme, _f, check
from tractor_beam.utils.config import Job
import os

@dataclass
# The `FocusState` class in Python defines attributes for configuration, job, and data storage.
class FocusState:
    conf: Optional[dict] = None
    job: Optional[dict] = None
    data: List[Dict[str, str]] = field(default_factory=list)

# The `Focus` class in Python initializes a `FocusState` object with configuration and job parameters,
# and processes data by reading, sanitizing, and writing files.
class Focus:
    def __init__(self, conf: dict = None, job: Job = None):
        """
        The function initializes a FocusState object with provided configuration and job parameters,
        returning an informational message if successful or a warning message if an exception occurs.
        
        :param conf: The `conf` parameter in the `__init__` method is expected to be a dictionary containing
        configuration settings. It is used to initialize the `FocusState` object with the configuration
        settings provided in the dictionary. If no `conf` dictionary is provided, the default value is set
        to `None
        :type conf: dict
        :param job: The `job` parameter in the `__init__` method is of type `Job`. It seems like it is used
        to initialize the `FocusState` object within the class
        :type job: Job
        :return: The code snippet is attempting to initialize an object of the `FocusState` class with the
        provided configuration (`conf`) and job parameters. If successful, it will return a formatted string
        containing information about the initialization process and the state of the object. If an exception
        occurs during the initialization, it will return a warning message indicating that no configuration
        was loaded and providing details about the exception that occurred.
        """
        try:
            self.state = FocusState(conf=conf.conf, job=job)
            return _f('info', f'Abduct initialized\n{self.state}')
        except Exception as e:
            return _f('warn', f'no configuration loaded\n{e}')
        
    def process(self, data: dict=None):
        """
        This Python function processes data by reading files, detecting encoding, sanitizing content,
        and writing cleaned output to new files.
        
        :param data: The `data` parameter in the `process` method is expected to be a dictionary
        containing information about files to be processed. Each item in the dictionary should have a
        'path' key pointing to the file location. The method reads the content of each file, detects its
        encoding, sanitizes the content
        :type data: dict
        :return: The `process` method returns the `self.state` object if the `data` parameter is
        provided and the `proj_path` passes the `check` function. If the `data` parameter is not
        provided or the `proj_path` check fails, it returns a call to the `_f` function with a message
        indicating a fatal error.
        """
        proj_path = os.path.join(self.state.conf.settings.proj_dir,self.state.conf.settings.name)
        if data and check(proj_path):
            for d in data:
                with open(d['path'], 'rb') as f:
                    _ = f.read()
                    enc = chardet.detect(_)['encoding']
                    if enc is None:
                        enc = 'utf-8'
                    try:
                        if d['path'].endswith('.xml'):
                            _t = Strip(copy=_.decode(enc)).sanitize(xml=True)
                        else:
                            _t = Strip(copy=_.decode(enc)).sanitize()
                        out = os.path.join('/'.join(d['path'].split('/')[:-1]), d['path'].split('/')[-1].split('.')[0]+'_cleaned.txt')
                        writeme(_t.encode(), out)
                        d['cleaned'] = out
                    except Exception as e:
                        d['cleaned'] = f"ERROR: {e}"
                        _f('fatal', f'markup encoding - {e} | {_}')
                    self.state.data.append(d)
            return self.state
        else:
            return _f('fatal', 'invalid path')
        