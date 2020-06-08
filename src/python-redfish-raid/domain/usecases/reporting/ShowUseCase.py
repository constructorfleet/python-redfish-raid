import abc

from framework.usecases.UseCase import UseCase


class ShowReportUseCase(UseCase):
    """Show report use case."""

    def __init__(self, *reports):
        """Instantiate the show report use case for the given reports."""
        super().__init__()
        self._reports = reports

    def __call__(self, service_data):
        """Show reports from service data."""
        pass



