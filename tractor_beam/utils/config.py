import os
import json
import shutil
from dataclasses import asdict
from typing import Union
from tractor_beam.utils.globals import _f, check
from tractor_beam.utils.config_classes import Schema, parse_conf

class Config:
    def __init__(self, conf: Union[str, dict, None] = None):
        self.load_conf(conf)

    def load_conf(self, conf):
        if isinstance(conf, str):
            with open(conf, 'r') as f:
                conf_dict = json.load(f)
                conf_instance = parse_conf(conf_dict)
                if conf_instance:
                    self.conf = conf_instance
                    if self.conf and isinstance(self.conf, Schema):
                        _f('success', f'Config loaded from - {self.conf.settings.name}')
                    else:
                        _f('fatal', 'Failed to parse configuration')
                else:
                    self.conf = None
                    _f('fatal', 'Failed to parse configuration from file')
        elif isinstance(conf, dict):
            conf_instance = parse_conf(conf)
            if conf_instance:
                self.conf = conf_instance
                _f('success', f'Config loaded from - {self.conf.settings.name}')
            else:
                self.conf = None
                _f('fatal', 'Failed to parse configuration from dictionary')
        else:
            self.conf = None
            _f('fatal', 'Config not found - {conf}')

        return self.conf

    def save(self):
        if self.conf:
            proj_path = os.path.join(self.conf.settings.proj_dir, self.conf.settings.name, 'config.json')
            with open(proj_path, 'w') as f:
                json.dump(asdict(self.conf), f)
            _f('info', f'Config saved to - {proj_path}')
            return self.conf, proj_path
        else:
            _f('fatal', 'No configuration to save')
            return None

    def unbox(self, overwrite: bool = False):
        if not self.conf:
            return _f('fatal', 'Configuration is not loaded')
        proj_path = os.path.join(self.conf.settings.proj_dir, self.conf.settings.name)
        if overwrite and check(proj_path):
            shutil.rmtree(proj_path)
            os.makedirs(proj_path)
        elif not check(proj_path):
            os.makedirs(proj_path)
        else:
            _f('fatal', f'Exists - {proj_path}')
            return None
        _f('success', f'Unboxed! 🛸📦 - {proj_path}')
        return self.save()

    def create(self, config: dict = None):
        if config:
            parsed_config = self.parse_conf(config)
            if parsed_config:
                proj_path = os.path.join(parsed_config.settings.proj_dir, parsed_config.settings.name)
                if check(proj_path):
                    return _f('fatal', f'Exists - {proj_path}')
                os.makedirs(proj_path)
                with open(os.path.join(proj_path, 'config.json'), 'w') as f:
                    _f('success', f'Unboxed! 🛸📦 using - {proj_path}')
                    return json.dump(asdict(parsed_config), f)
            else:
                _f('fatal', 'Your config schema does not match the requirements')
                return None

    def destroy(self, confirm: str = None):
        if not self.conf or not check(self.conf.settings.proj_dir):
            return _f('fatal', 'Invalid path or configuration not loaded')
        proj_path = os.path.join(self.conf.settings.proj_dir, self.conf.settings.name)
        if confirm == self.conf.settings.name:
            shutil.rmtree(proj_path)
            _f('warn', f'{confirm} destroyed')
        else:
            _f('fatal', 'You did not confirm - `Config.destroy(confirm="your_config_name")`')
        