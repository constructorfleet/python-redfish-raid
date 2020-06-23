from string import Formatter

import humanize
import jmespath
from jmespath import functions

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


class CustomFunctions(functions.Functions):
    @functions.signature({'types': ['number']})
    def _func_naturalsize(self, value):
        return humanize.naturalsize(value)


class FilterOutputCaseUseCase(UseCase):
    """Filter api output."""

    options = jmespath.Options(custom_functions=CustomFunctions())

    def __init__(self, json_filters):
        """Create a use case for performing queries against the JSON responses."""
        super().__init__()
        self._json_filters = json_filters
        self._keyword_formatter = KWArgFormatter()

    def __call__(self, service_data_json):
        """Perform Json Query/Select operations against the API responses."""
        if not isinstance(service_data_json, dict):
            return None
        response = {}
        for query in self._json_filters:
            key = query['key']
            filtered_json = jmespath.search(query['jq'], service_data_json, options=self.options)

            if 'format' in query:
                item_format = query['format']
                response[key] = ''.join(
                    [self._keyword_formatter.format(item_format, **item) for item in filtered_json])
            else:
                response[key] = filtered_json
        return response
