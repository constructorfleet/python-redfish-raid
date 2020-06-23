from string import Formatter
import json
import jmespath

from framework.usecases.UseCase import UseCase


class KWArgFormatter(Formatter):
    def get_value(self, key, args, kwargs):
        if isinstance(key, str):
            try:
                return kwargs[key]
            except KeyError:
                return key
        else:
            return Formatter.get_value(key, args, kwargs)


class ShowReportUseCase(UseCase):
    """Show report use case."""

    def __init__(self, report_format):
        """Instantiate the show report use case for the given reports."""
        super().__init__()
        self._report_format = str(report_format) if report_format else None
        self._keyword_formatter = KWArgFormatter()

    def __call__(self, service_data):
        """Show reports from service data."""
        if not self._report_format:
            return json.dumps(service_data, indent=2, sort_keys=True)
        return self._keyword_formatter.format(self._report_format, **service_data)
