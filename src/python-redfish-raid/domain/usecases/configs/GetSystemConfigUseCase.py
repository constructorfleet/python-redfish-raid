from data.configs.DictSystemConfig import DictSystemConfig
from framework.usecases.UseCase import UseCase

_DEFAULT_CONFIG_DIRECTORY = "configs"


class GetSystemConfigUseCase(UseCase):
    """Get system configuration use case."""

    def __init__(self, load_config):
        """Create use case for providing system configuration."""
        super().__init__()
        self._load_config = load_config

    def __call__(self, system):
        """Get system configuration."""
        return DictSystemConfig(self._load_config(system))
