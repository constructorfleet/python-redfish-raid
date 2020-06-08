import abc


class Client(abc.ABC):
    """Client abstract class."""

    @abc.abstractmethod
    def connect(self, **kwargs):
        """Initiate connection from client."""
        pass

    @abc.abstractmethod
    def get(self, path):
        """Get response for the specified path."""
        pass

    @abc.abstractmethod
    def disconnect(self, **kwargs):
        """Disconnect from host."""
        pass
