from .utils import _f, check
import os, shutil
from tractor_beam.config import Config
from tractor_beam.copier import Copier
from tractor_beam.receipts import Receipts
from tractor_beam.janitor import Janitor

class tractor_beam:
    def __init__(self, config: str | dict = None):
        self.runs = []
        self.config = Config(config)
    def go(self):
        self.config.use()
        self.config.unbox()
        _f('wait', f'tractor beaming with "{self.config.conf["settings"]["name"]}"')
        copy = Copier(self.config)
        r = Receipts(self.config)
        j = Janitor(self.config)
        data = copy.download()
        print(data)
        r.create(data)
        r.write()
        j.process(data)
        if self.config and copy and r and j:
            _f('success', '🦢 done')
            self.runs.append({
                "config": self.config
                , "copier": copy
                , "receipts": r
                , "janitor": j
                , "data": data
                , "status": 'complete'
            })
            return {
                "config": self.config
                , "copier": copy
                , "receipts": r
                , "janitor": j
                , "data": data
                , "status": 'complete'
            }
            # handle missing or broken objects in the runs
    def destroy(self, confirm:str = None):
        if not check(os.path.join(self.config.conf['settings']['proj_dir'], self.config.conf['settings']['name'])):
            return _f('fatal', f'invalid path - {self.p}')
        if confirm==self.config.conf["settings"]["name"]:
            shutil.rmtree(os.path.join(self.config.conf['settings']['proj_dir'], self.config.conf['settings']['name'])), _f('warn', f'{confirm} destroyed')
        else:
            _f('fatal','you did not confirm - `tractor_beam.destroy("your_config_name")`')