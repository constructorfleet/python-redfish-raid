from domain.usecases.reporting import ReportUseCase
from framework.usecases.UseCase import UseCase


class ReportEnclosureUseCase(UseCase, ReportUseCase):
    """Report enclosure data."""

    def __init__(self):
        super(ReportUseCase, self).__init__("Enclosures")
        super().__init__()

    def __call__(self, service_data):
        """Report enclosure information from service data."""
        pass
