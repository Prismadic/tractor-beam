from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class Job:
    url: str
    types: Optional[List[str]] = None
    beacon: Optional[str] = None
    delay: Optional[float] = None
    custom: Optional[List[Dict[str, Any]]] = None

@dataclass
class Settings:
    name: str
    proj_dir: str
    jobs: List[Job]

@dataclass
class Schema:
    role: str
    settings: Settings

def parse_conf(conf_dict: Dict[str, Any]) -> Schema:
    settings_dict = conf_dict["settings"]
    jobs_list = [Job(**job_dict) for job_dict in settings_dict["jobs"]]
    settings = Settings(name=settings_dict["name"],
                        proj_dir=settings_dict["proj_dir"],
                        jobs=jobs_list)
    return Schema(role=conf_dict["role"], settings=settings)