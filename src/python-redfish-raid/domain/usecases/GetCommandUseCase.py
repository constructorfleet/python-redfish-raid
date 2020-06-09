from framework.configs.Command import Command
from framework.usecases.UseCase import UseCase


class GetCommandUseCase(UseCase):
    """Use case for retrieving the command to execute."""

    def __init__(self):
        super().__init__()

    def __call__(self, flags):
        # TODO : More dynamic
        command = Command.SHOW_ALL
        if flags.nagios:
            command = Command.NAGIOS
        elif flags.show_pr:
            command = Command.SHOW_PATROL_READ
        elif flags.show_cc:
            command = Command.SHOW_CONSISTENCY_CHECK
        elif flags.show_bbu:
            command = Command.SHOW_BATTERY_BACKUP
        elif flags.show_enc:
            command = Command.SHOW_ENCLOSURE
        elif flags.show_disks:
            command = Command.SHOW_DISKS
        elif flags.show_logical:
            command = Command.SHOW_LOGICAL_VOLUMES

        if not command.is_implemented:
            raise NotImplementedError('Command %s is not yet implemented' % command.command_name)

        return command
