import platform
import psutil
from dataclasses import dataclass, field
from typing import Optional, List, Dict

from ..clone.abduct import AbductState
from ..laser.focus import FocusState
from ..visits.record import RecordState
from ..utils.globals import _f

@dataclass
# This class `HostInfo` represents various system information attributes such as platform details, CPU
# and memory usage, disk and network I/O statistics, boot time, CPU frequency, core information,
# memory statistics, network addresses, and temperature sensors.
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
# The `States` class defines attributes for host information, abduction states, focus objects, and
# record objects.
class States:
    host: HostInfo = None
    abduct: List[AbductState] = field(default_factory=list) 
    focus: List[object] = field(default_factory=list) 
    record: List[object] = field(default_factory=list) 

# The `BeamState` class in Python manages host information and state updates for an abduction process.
class BeamState:
    def __init__(self):
        """
        The `__init__` function initializes an object with a list of `HostInfo` objects and a `States`
        object.
        """
        self.host_info: List[HostInfo] = [self.get_host_info()]
        self.states = States()

    def get_host_info(self) -> HostInfo:
        """
        This Python function retrieves various system information such as CPU usage, memory usage, disk
        usage, network information, and more.
        :return: The `get_host_info` function is returning an instance of the `HostInfo` class with
        various system information such as platform details, CPU usage, memory usage, disk usage,
        network information, CPU frequency, core counts, boot time, and temperature sensors (if
        available).
        """
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
        """
        This function updates the abduct state in a class instance.
        
        :param state: The `state` parameter in the `abduct_state_update` method is of type
        `AbductState`, which is a custom class or data structure used to represent the state of an
        abduction process. This parameter allows you to pass in an instance of `AbductState` to update
        the state of
        :type state: AbductState
        """
        self.states.abduct.append(state)

    def focus_state_update(self, state: FocusState = None) -> None:
        """
        The function `focus_state_update` appends a `FocusState` object to the `focus` list within the
        `states` attribute of an object.
        
        :param state: The `focus_state_update` method takes in a parameter `state` of type `FocusState`.
        This parameter is optional and can be set to `None`. The method appends the `state` to the
        `focus` list within the `states` attribute of the object
        :type state: FocusState
        """
        self.states.focus.append(state)

    def record_state_update(self, state: RecordState = None) -> None:
        """
        This function records a state update in a list within the 'states' attribute of the object.
        
        :param state: The `state` parameter in the `record_state_update` method is of type
        `RecordState`, which is a custom class or data structure used to represent the state of
        something in your program. This parameter allows you to pass in an instance of `RecordState` to
        update the record of states in
        :type state: RecordState
        """
        self.states.record.append(state)

    def host_state_update(self) -> None:
        """
        The function `host_state_update` appends host information to the `host_info` list.
        """
        self.host_info.append(self.get_host_info())
