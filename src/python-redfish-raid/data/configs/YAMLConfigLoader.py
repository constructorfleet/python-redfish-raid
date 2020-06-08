import os
import yaml

from framework.configs.ConfigLoader import ConfigLoader


class YAMLConfigLoader(ConfigLoader):
    """YAML configuration file loader."""

    def load(self, system):
        """Load configuration for the given system."""
        file = 'configs/%s.yaml' % system.lower()
        if not os.path.exists(file):
            raise FileNotFoundError(file)

        with open(file) as file:
            return yaml.load(file, Loader=yaml.FullLoader)
