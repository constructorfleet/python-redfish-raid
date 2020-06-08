from data.configs.YAMLConfigLoader import YAMLConfigLoader
from framework.usecases.UseCase import UseCase


class LoadConfigurationUseCase(UseCase):
    """Use case for loading configuration."""

    def __init__(self):
        """Create use case for configuration loading."""
        super().__init__()
        self._config_loader = YAMLConfigLoader()  # TODO: Dynamically build loader

    def __call__(self, system):
        """Load configuration."""
        return self._config_loader.load(system)
