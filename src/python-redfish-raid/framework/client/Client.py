import abc


class Client(abc.ABC):
    """Client abstract class."""

    @abc.abstractmethod
    def connect(self, host, username, password, **kwargs):
        """Initiate connection from client."""
        pass

    @abc.abstractmethod
    def get(self, path):
        """Get response for the specified path."""
        pass
