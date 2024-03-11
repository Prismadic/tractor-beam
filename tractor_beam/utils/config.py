import os
import json
import shutil
from dataclasses import asdict
from typing import Union
from tractor_beam.utils.globals import _f, check
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class CustomJob:
    func: Optional[str] = None
    headers: Optional[dict] = None
    types: Optional[list] = None

@dataclass
class Job:
    url: str
    types: Optional[List[str]] = None
    beacon: Optional[str] = None
    delay: Optional[float] = None
    custom: Optional[CustomJob] = None

class Settings:
    def __init__(self, name: str, proj_dir: str, jobs: List[Job]):
        if not name or not isinstance(name, str):
            raise ValueError("name must be a non-empty string")
        if not proj_dir or not isinstance(proj_dir, str):
            raise ValueError("proj_dir must be a non-empty string")
        if not jobs or not isinstance(jobs, list) or not all(isinstance(job, Job) for job in jobs):
            raise ValueError("jobs must be a non-empty list of Job instances")

        self.name = name
        self.proj_dir = proj_dir
        self.jobs = jobs

@dataclass
class Schema:
    role: str
    settings: Settings

class ConfigEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Job) or isinstance(obj, Settings):
            return self.to_serializable(obj)  # Reuse the to_serializable function
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
    def to_serializable(self, obj):
        if isinstance(obj, Job):
            return asdict(obj)
        elif isinstance(obj, Settings):
            # Assuming jobs is a list of Job instances
            return {"name": obj.name, "proj_dir": obj.proj_dir, "jobs": [self.to_serializable(job) for job in obj.jobs]}
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        else:
            return str(obj)  # Fallback for unsupported types
    
class Config:
    def __init__(self, conf: Union[str, dict, None] = None):
        self.load_conf(conf)

    def load_conf(self, conf):
        if isinstance(conf, str):
            try:
                with open(conf, 'r') as f:
                    conf_dict = json.load(f)
                    conf_instance = self.parse_conf(conf_dict)
                    if conf_instance:
                        self.conf = conf_instance
                        if self.conf and isinstance(self.conf, Schema):
                            _f('success', f'Config loaded from - {self.conf.settings.name}')
                        else:
                            _f('fatal', 'Failed to parse configuration')
                    else:
                        self.conf = None
                        _f('fatal', 'Failed to parse configuration from file')
            except (ValueError, json.JSONDecodeError):
                self.conf = None
            except FileNotFoundError:
                self.conf = None
        elif isinstance(conf, dict):
            conf_instance = self.parse_conf(conf)
            if conf_instance:
                self.conf = conf_instance
                _f('success', f'Config loaded from - {self.conf.settings.name}')
            else:
                self.conf = None
                _f('fatal', 'Failed to parse configuration from dictionary')
        else:
            self.conf = None
            _f('fatal', f'Config not found - {conf}')

        return self.conf

    def parse_conf(self, conf_dict: Dict[str, Any]) -> Schema:
        if not conf_dict.get("role") or not isinstance(conf_dict["role"], str):
            self.conf = None
            _f("fatal", "role must be a non-empty string")

        settings_dict = conf_dict["settings"]
        if not settings_dict.get("name") or not isinstance(settings_dict["name"], str):
            self.conf = None
            _f("fatal", "settings name must be a non-empty string")
        if not settings_dict.get("proj_dir") or not isinstance(settings_dict["proj_dir"], str):
            self.conf = None
            _f("fatal", "settings proj_dir must be a non-empty string")
        if not settings_dict.get("jobs") or not isinstance(settings_dict["jobs"], list):
            self.conf = None
            _f("fatal", "settings jobs must be a list")

        jobs_list = [Job(**job_dict) for job_dict in settings_dict["jobs"]]
        if not jobs_list:
            self.conf = None
            _f("fatal", "settings jobs list must not be empty")

        settings = Settings(name=settings_dict["name"],
                            proj_dir=settings_dict["proj_dir"],
                            jobs=jobs_list)
        return Schema(role=conf_dict["role"], settings=settings)
    
    def save(self):
        if self.conf:
            conf_path = os.path.join(self.conf.settings.proj_dir, self.conf.settings.name, 'config.json')
            try:
                with open(conf_path, 'w') as f:
                    json.dump(asdict(self.conf), f, cls=ConfigEncoder)
                _f('info', f'Config saved to - {conf_path}')
                return self.conf, conf_path
            except TypeError as e:
                _f('fatal', e)
                return None
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
        