import abc


class ConfigLoader(abc.ABC):
    """Configuration loader."""

    @abc.abstractmethod
    def load(self, **kwargs):
        """Load configuration."""
        pass
