"""Reporting use cases."""
import abc

from framework.usecases.UseCase import UseCase


class ReportUseCase(abc.ABC):
    """Abstract base report use case."""

    def __init__(self, name):
        """Create a new reporting use case."""
        self.name = name
