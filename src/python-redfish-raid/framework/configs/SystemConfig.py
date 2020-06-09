import abc


class SystemConfig(abc.ABC):
    """System configuration source."""

    @abc.abstractmethod
    def get_prefix(self, command):
        """Return the prefix for the given command."""
        pass

    @abc.abstractmethod
    def get_property(self, command):
        """Return the property for the given command."""
        pass

    @abc.abstractmethod
    def get_recurse(self, command):
        """Get whether or not to recurse the api given the specified command."""
        pass


