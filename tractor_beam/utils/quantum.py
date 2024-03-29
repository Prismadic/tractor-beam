import platform
import psutil
from dataclasses import dataclass, field
from typing import Optional, List, Dict

from tractor_beam.visits.visit import VisitState
from tractor_beam.processor import ProcessState
from tractor_beam.utils.globals import _f

@dataclass
class AbductState:
    conf: Optional[dict] = None
    job: Optional[dict] = None
    data: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class HostInfo:
    platform: str
    platform_release: str
    platform_version: str
    architecture: str
    processor: str
    cpu_usage: float
    memory_usage: float
    disk_usage: Dict[str, psutil._common.sdiskusage]  # Disk usage by partition
    total_disk_io: psutil._common.sdiskio  # Total disk I/O statistics
    net_io_counters: psutil._common.snetio  # Network I/O statistics
    boot_time: float  # System boot time
    cpu_freq: Optional[psutil._common.scpufreq] = None  # CPU frequency
    cpu_physical_cores: Optional[int] = None  # Number of physical CPU cores
    cpu_total_cores: Optional[int] = None  # Total number of CPU cores
    virtual_memory: Optional[psutil.virtual_memory] = None  # Detailed virtual memory statistics
    swap_memory: Optional[psutil._common.sswap] = None  # Detailed swap memory statistics
    network_addresses: Dict[str, List[psutil._common.snicaddr]] = None  # Network interface addresses
    temperature_sensors: Dict[str, List[psutil._common.shwtemp]] = None  # Temperature sensors

@dataclass
class States:
    host: HostInfo = None
    abduct: List[AbductState] = field(default_factory=list) 
    visit: List[object] = field(default_factory=list) 
    process: List[object] = field(default_factory=list) 

class BeamState:
    def __init__(self):
        self.host_info: List[HostInfo] = [self.get_host_info()]
        self.states = States()

    def get_host_info(self) -> HostInfo:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk_usage = {part.mountpoint: psutil.disk_usage(part.mountpoint) for part in psutil.disk_partitions()}
        total_disk_io = psutil.disk_io_counters()
        net_io_counters = psutil.net_io_counters()
        boot_time = psutil.boot_time()
        
        # CPU frequency handling
        cpu_freq = None
        if hasattr(psutil, "cpu_freq"):
            try:
                freq = psutil.cpu_freq()
                if freq:  # Checking if the information is available
                    cpu_freq = {'current': freq.current, 'min': freq.min, 'max': freq.max}
            except Exception as e:
                _f("warn", f"Error retrieving CPU frequency: {e}")

        cpu_physical_cores = psutil.cpu_count(logical=False)
        cpu_total_cores = psutil.cpu_count(logical=True)
        virtual_memory = psutil.virtual_memory()
        swap_memory = psutil.swap_memory()
        network_addresses = {interface: addresses for interface, addresses in psutil.net_if_addrs().items()}
        temperature_sensors = psutil.sensors_temperatures() if hasattr(psutil, "sensors_temperatures") else None

        return HostInfo(
            platform=platform.system(),
            platform_release=platform.release(),
            platform_version=platform.version(),
            architecture=platform.machine(),
            processor=platform.processor(),
            cpu_usage=cpu_percent,
            memory_usage=memory.percent,
            disk_usage=disk_usage,
            total_disk_io=total_disk_io,
            net_io_counters=net_io_counters,
            boot_time=boot_time,
            cpu_freq=cpu_freq,
            cpu_physical_cores=cpu_physical_cores,
            cpu_total_cores=cpu_total_cores,
            virtual_memory=virtual_memory,
            swap_memory=swap_memory,
            network_addresses=network_addresses,
            temperature_sensors=temperature_sensors,
        )

    def abduct_state_update(self, state: AbductState = None) -> None:
        self.states.abduct.append(state)

    def visit_state_update(self, state: VisitState = None) -> None:
        self.states.visit.append(state)

    def visits_processor_state_update(self, state: ProcessState = None) -> None:
        self.states.process.append(state)

    def host_state_update(self) -> None:
        self.host_info.append(self.get_host_info())
