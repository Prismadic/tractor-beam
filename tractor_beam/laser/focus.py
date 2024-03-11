import chardet

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from tractor_beam.utils.tools import Strip
from tractor_beam.utils.globals import writeme, _f, check
from tractor_beam.utils.config import Job
import os

@dataclass
class FocusState:
    conf: Optional[dict] = None
    job: Optional[dict] = None
    data: List[Dict[str, str]] = field(default_factory=list)

class Focus:
    def __init__(self, conf: dict = None, job: Job = None):
        try:
            self.state = FocusState(conf=conf.conf, job=job)
            return _f('info', f'Abduct initialized\n{self.state}')
        except Exception as e:
            return _f('warn', f'no configuration loaded\n{e}')
        
    def process(self, data: dict=None):
        """
        The function processes a file by reading its contents, detecting the encoding, and performing
        specific actions based on the file type.
        :return: the result of the `writeme` function call, which is not shown in the provided code.
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

    def destroy(self, confirm: str = None):
        """
        The function `destroy` removes a file if the confirmation matches the file name.
        
        :param confirm: The `confirm` parameter is used to confirm the destruction of a file. It should
        be set to the name of the file that you want to destroy
        :return: a message indicating whether the file was successfully destroyed or not.
        """
        if not check(self.o):
            return _f('fatal', 'invalid path')
        if confirm==self.o.split('/')[-1]:
            os.remove(self.o), _f('warn', f'{confirm} destroyed from {self.o}')
        else:
            _f('fatal','you did not confirm - `Records.destroy(confirm="file_name")`')
        