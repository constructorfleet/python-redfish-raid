from framework.configs.SystemConfig import SystemConfig

_PREFIX = 'prefix'
_PROPERTY = 'property'
_RECURSE = 'recurse'


class DictSystemConfig(SystemConfig):
    """Dictionary based system configuration."""

    def __init__(self, config):
        if not isinstance(config, dict):
            raise TypeError('Expected configuration to be a dict.')
        self._config = config

    def get_prefix(self, command):
        return self._get_command_config(command).get(_PREFIX)

    def get_property(self, command):
        return self._get_command_config(command).get(_PROPERTY)

    def get_recurse(self, command):
        return self._get_command_config(command).get(_RECURSE, False)

    def _get_command_config(self, command):
        return self._config.get(command, {})
