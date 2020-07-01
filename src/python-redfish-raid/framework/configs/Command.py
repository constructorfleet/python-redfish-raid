from enum import Enum

from const import (
    COMMAND_NAGIOS,
    COMMAND_SHOW_ALL,
    COMMAND_SHOW_PR,
    COMMAND_SHOW_CC,
    COMMAND_SHOW_BBU,
    COMMAND_SHOW_ENC,
    COMMAND_SHOW_DISKS,
    COMMAND_SHOW_LOGICAL
)


class Command(Enum):
    """Available commands to execute."""
    NAGIOS = (COMMAND_NAGIOS, True)
    SHOW_ALL = (COMMAND_SHOW_ALL, True)
    SHOW_PATROL_READ = (COMMAND_SHOW_PR, True)
    SHOW_CONSISTENCY_CHECK = (COMMAND_SHOW_CC, True)
    SHOW_BATTERY_BACKUP = (COMMAND_SHOW_BBU, True)
    SHOW_ENCLOSURE = (COMMAND_SHOW_ENC, True)
    SHOW_DISKS = (COMMAND_SHOW_DISKS, True)
    SHOW_LOGICAL_VOLUMES = (COMMAND_SHOW_LOGICAL, True)

    def __init__(self, command_name, is_implemented):
        """Create a Command Enum."""
        self.command_name = command_name
        self.is_implemented = is_implemented
