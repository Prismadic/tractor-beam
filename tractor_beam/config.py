import os, json, shutil
from .utils import _f, readthis, likethis, check

class Config:
    def __init__(self, conf: str | dict = None):
        if type(conf) in [dict, str]:
            self.conf = conf
        else:
            self.conf = _f('fatal', f'config not found - {conf}')
    def use(self):
        if isinstance(self.conf, str):
            _ = readthis(self.conf)
            _c = json.load(_)
            if likethis(_c):
                _f('success', f'config set from - {self.conf}')
                self.conf = _c
        elif isinstance(self.conf, dict):
            if likethis(self.conf):
                _f('success', f'config loaded from - {self.conf["settings"]["name"]}')
    def save(self):
        proj_path = os.path.join(self.conf['settings']['proj_dir'],self.conf['settings']['name'],'config.json')
        f = open(proj_path, 'w')
        json.dump(self.conf, f)
        return _f('info', f'config saved to - {"/".join(proj_path.split("/")[:-1])}')
    def unbox(self, o: bool = False):
        proj_path = os.path.join(self.conf["settings"]["proj_dir"],self.conf["settings"]["name"])
        if o and check(proj_path):
            shutil.rmtree(proj_path)
            os.mkdir(proj_path)
        elif not check(proj_path):
            os.mkdir(proj_path)
        else:
            return _f('fatal',f'exists - {proj_path}')
        self.save()
        return _f('success', f'unboxed! 🦢📦 - {proj_path} ')
    def create(self, config: dict = None):
        if likethis(config):
            _p = os.path.join(config["settings"]["proj_dir"],config["settings"]["name"])
            if check(_p):
                return _f('fatal',f'exists - {_p}')
            else:
                os.makedirs(_p)
                f = open(os.path.join(_p, 'config.json'), 'w')
                json.dump(config, f)
            _f('success', f'unboxed! 🦢📦 using - {_p} ')
            return _p
        else:
            return _f('fatal', 'your config schema does not match the requirements')
    def destroy(self, confirm: str = None):
        """
        The `destroy` function removes a file if the confirmation matches the file name.
        
        :param confirm: The `confirm` parameter is used to confirm the destruction of a file. It should
        be set to the name of the file that you want to destroy
        :type confirm: str
        :return: a message indicating whether the file was successfully destroyed or not.
        """
        """
        The function `destroy` removes a file if the confirmation matches the file name.
        
        :param confirm: The `confirm` parameter is used to confirm the destruction of a file. It should
        be set to the name of the file that you want to destroy
        :return: a message indicating whether the file was successfully destroyed or not.
        """
        if not check(self.p):
            return _f('fatal', f'invalid path - {self.p}')
        if confirm==self.c["settings"]["name"]:
            shutil.rmtree(self.p.replace('config.json','')), _f('warn', f'{confirm} destroyed')
        else:
            _f('fatal','you did not confirm - `Config.destroy(confirm="your_config_name")`')
        