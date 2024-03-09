from .utils.globals import _f, check
import os, shutil
from tractor_beam.utils.config import Config
from tractor_beam.clone.replicator import Abduct
from tractor_beam.visits.sites import Records
from tractor_beam.laser.purify import Focus

class Beam:
    def __init__(self, config: str | dict = None):
        self.runs = []
        self.config = Config(config)
    def go(self):
        self.config.use()
        self.config.unbox()
        _f('wait', f'tractor beaming with "{self.config.conf["settings"]["name"]}"')
        copy = Abduct(self.config)
        r = Records(self.config)
        j = Focus(self.config)
        data = copy.download()
        r.create(data)
        r.write()
        j.process(data)
        if self.config and copy and r and j:
            _f('success', '🛸 done')
            self.runs.append({
                "config": self.config
                , "Abduct": copy
                , "Records": r
                , "Focus": j
                , "data": data
                , "status": 'complete'
            })
            return self.runs
            # handle missing or broken objects in the runs
    def destroy(self, confirm:str = None):
        if not check(os.path.join(self.config.conf['settings']['proj_dir'], self.config.conf['settings']['name'])):
            return _f('fatal', f'invalid path - {self.p}')
        if confirm==self.config.conf["settings"]["name"]:
            shutil.rmtree(os.path.join(self.config.conf['settings']['proj_dir'], self.config.conf['settings']['name'])), _f('warn', f'{confirm} destroyed')
        else:
            _f('fatal','you did not confirm - `tractor_beam.destroy("your_config_name")`')
