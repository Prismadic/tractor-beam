import os
import json
import shutil
from dataclasses import asdict
from typing import Union
from tractor_beam.utils.globals import _f, check
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
# The `CustomJob` class in Python defines attributes for a custom job, including a function, headers,
# and types.
class CustomJob:
    func: Optional[str] = None
    headers: Optional[dict] = None
    types: Optional[list] = None

@dataclass
# The class `Job` in Python defines attributes for a job, including URL, types, beacon, delay, and
# custom job information.
class Job:
    url: str
    types: Optional[List[str]] = None
    beacon: Optional[str] = None
    delay: Optional[float] = None
    custom: Optional[CustomJob] = None

# The `Settings` class in Python initializes an object with a project name, directory path, and a list
# of job instances, performing validation checks on the input parameters.
class Settings:
    def __init__(self, name: str, proj_dir: str, jobs: List[Job]):
        """
        The function `__init__` initializes an object with a name, project directory, and a list of job
        instances, performing validation checks on the input parameters.
        
        :param name: The `name` parameter is a string that represents the name of a project. It must be a
        non-empty string, otherwise a `ValueError` will be raised
        :type name: str
        :param proj_dir: proj_dir is a parameter that represents the project directory path where the
        project files are stored. It should be a non-empty string
        :type proj_dir: str
        :param jobs: The `jobs` parameter is expected to be a list of `Job` instances. The `__init__` method
        checks that `jobs` is a non-empty list where each element is an instance of the `Job` class. If any
        of these conditions are not met, a `ValueError
        :type jobs: List[Job]
        """
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
# The `Schema` class has two attributes, `role` of type `str` and `settings` of type `Settings`.
class Schema:
    role: str
    settings: Settings

# The `ConfigEncoder` class in Python provides custom serialization for `Job` and `Settings` objects
# by overriding the `default` method of `JSONEncoder` and implementing a `to_serializable` method.
class ConfigEncoder(json.JSONEncoder):
    def default(self, obj):
        """
        The function overrides the default method of the JSONEncoder class to handle custom
        serialization for Job and Settings objects.
        
        :param obj: The `obj` parameter in the `default` method is the object that needs to be
        serialized into a JSON-serializable format. The method checks if the object is an instance of
        either the `Job` class or the `Settings` class. If it is, it calls the `to_serial
        :return: The `default` method is returning the result of calling `self.to_serializable(obj)` if
        the `obj` is an instance of `Job` or `Settings`. Otherwise, it is letting the base class
        `json.JSONEncoder.default` method raise a `TypeError`.
        """
        if isinstance(obj, Job) or isinstance(obj, Settings):
            return self.to_serializable(obj)  # Reuse the to_serializable function
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
    def to_serializable(self, obj):
        """
        The function `to_serializable` converts objects into a serializable format, handling specific
        classes like Job and Settings.
        
        :param obj: The `to_serializable` method you provided is a custom serialization method that
        converts objects into a serializable format. The method checks the type of the input object
        `obj` and serializes it accordingly
        :return: The `to_serializable` method is returning a JSON serializable representation of the
        input object `obj`. If `obj` is an instance of the `Job` class, it returns the object as a
        dictionary using the `asdict` function. If `obj` is an instance of the `Settings` class, it
        returns a dictionary containing the name, project directory, and a list of serialized
        """
        if isinstance(obj, Job):
            return asdict(obj)
        elif isinstance(obj, Settings):
            # Assuming jobs is a list of Job instances
            return {"name": obj.name, "proj_dir": obj.proj_dir, "jobs": [self.to_serializable(job) for job in obj.jobs]}
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        else:
            return str(obj)  # Fallback for unsupported types
    
# The `Config` class in Python provides methods to load, parse, save, unbox, create, and destroy
# project configurations based on provided settings.
class Config:
    def __init__(self, conf: Union[str, dict, None] = None):
        """
        The function `__init__` initializes an object with a configuration parameter that can be a
        string, dictionary, or None.
        
        :param conf: The `conf` parameter in the `__init__` method can accept a string, a dictionary, or
        `None` as its value. This parameter is used to initialize the object with configuration settings
        :type conf: Union[str, dict, None]
        """
        self.load_conf(conf)

    def load_conf(self, conf):
        """
        The function `load_conf` loads a configuration from either a file or a dictionary, parses it,
        and returns the parsed configuration.
        
        :param conf: The `conf` parameter in the `load_conf` method can be either a string (representing
        a file path to a configuration file) or a dictionary (representing the configuration directly).
        The method first checks the type of `conf` and then proceeds to load and parse the configuration
        accordingly. If
        :return: The `load_conf` method returns the `self.conf` object after loading and parsing the
        configuration either from a file or a dictionary.
        """
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
        """
        The function `parse_conf` validates and parses a configuration dictionary to create a Schema
        object with role and settings information.
        
        :param conf_dict: conf_dict: A dictionary containing configuration settings for a specific role.
        It should have keys "role" (a non-empty string) and "settings" (a dictionary containing keys
        "name" (a non-empty string), "proj_dir" (a non-empty string), and "jobs" (a
        :type conf_dict: Dict[str, Any]
        :return: A Schema object is being returned with the role and settings parsed from the conf_dict
        parameter. The role is extracted directly from the conf_dict, while the settings are extracted
        from the "settings" key within the conf_dict. The settings include a name (extracted from "name"
        key), proj_dir (extracted from "proj_dir" key), and a list of jobs (extracted from "
        """
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
        """
        This function saves a configuration object to a JSON file.
        :return: The `save` method returns either the saved configuration object (`self.conf`) and the
        path where it was saved (`conf_path`), or it returns `None` if there was an error or if there
        was no configuration to save.
        """
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
        """
        The function `unbox` creates a project directory based on configuration settings, with an option
        to overwrite existing directory.
        
        :param overwrite: The `overwrite` parameter in the `unbox` method is a boolean flag that
        determines whether to overwrite an existing directory if it already exists. If `overwrite` is
        set to `True` and the directory at `proj_path` already exists, the method will delete the
        existing directory and create a, defaults to False
        :type overwrite: bool (optional)
        :return: The `unbox` method returns the result of the `self.save()` method.
        """
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
        """
        This Python function creates a project directory based on a provided configuration dictionary.
        
        :param config: The `config` parameter in the `create` method is a dictionary that contains
        configuration settings for a project. This method checks if the `config` parameter is provided,
        parses the configuration, creates a project directory based on the parsed settings, and writes
        the configuration to a `config.json` file in
        :type config: dict
        :return: either a success message indicating that the project has been successfully created and
        the configuration has been saved in a JSON file, or a fatal error message indicating that the
        project already exists or the provided config schema does not match the requirements.
        """
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
        """
        The function `destroy` deletes a directory if the confirmation matches the project name in the
        configuration settings.
        
        :param confirm: The `confirm` parameter in the `destroy` method is a string parameter that is
        used to confirm the destruction of a project directory. The method checks if the value of
        `confirm` matches the name of the project directory before proceeding with the deletion. If the
        confirmation matches, the project directory is deleted
        :type confirm: str
        :return: The function `destroy` will return a message based on the conditions provided in the
        code snippet. If the `confirm` parameter matches the project name in the configuration settings,
        it will delete the project directory and return a warning message that the project has been
        destroyed. If the `confirm` parameter does not match the project name, it will return a fatal
        error message indicating that the user did not confirm the
        """
        if not self.conf or not check(self.conf.settings.proj_dir):
            return _f('fatal', 'Invalid path or configuration not loaded')
        proj_path = os.path.join(self.conf.settings.proj_dir, self.conf.settings.name)
        if confirm == self.conf.settings.name:
            shutil.rmtree(proj_path)
            _f('warn', f'{confirm} destroyed')
        else:
            _f('fatal', 'You did not confirm - `Config.destroy(confirm="your_config_name")`')
        