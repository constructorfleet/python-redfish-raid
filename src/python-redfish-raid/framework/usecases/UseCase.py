import abc
import logging


class UseCase(abc.ABC):
    """Base abstract class for use cases."""

    def __init__(self):
        """Initialize base use case class."""
        self._logger = logging.getLogger(self.__class__.__name__)

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        pass
