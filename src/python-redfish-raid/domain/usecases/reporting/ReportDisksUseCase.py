from domain.usecases.reporting import ReportUseCase
from framework.usecases.UseCase import UseCase


class ReportDisksUseCase(UseCase, ReportUseCase):
    """Physical disks reporting use case."""

    def __init__(self):
        UseCase.__init__(self)
        ReportUseCase.__init__(self, "Physical Disks")

    def __call__(self, *args, **kwargs):
        pass

