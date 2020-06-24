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

    @functions.signature({'types': ['number']})
    def _func_fractional(self, value):
        return humanize.fractional(value)

    @functions.signature({'types': ['number']})
    def _func_scientific(self, value):
        return humanize.scientific(value)

    @functions.signature({'types': ['string']}, {'types': ['number']}, {'types': ['number']})
    def _func_substring(self, value, start_index=None, end_index=None):
        if start_index and end_index:
            start_index = max(0, int(start_index))
            end_index = min(len(value) - 1, int(end_index))
            return value[start_index:end_index]
        elif start_index:
            start_index = max(0, int(start_index))
            return value[start_index:]
        elif end_index:
            end_index = min(len(value) - 1, int(end_index))
            return value[:end_index]
        else:
            return value


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
                    [self._keyword_formatter.format(item_format, **self._sub_format(query.get('sub_formats'), item)) for item in filtered_json])
            else:
                response[key] = filtered_json
        return response

    def _sub_format(self, sub_formats, json_item):
        if sub_formats:
            for key, sub_format in sub_formats.items():
                if key not in json_item:
                    continue
                json_item[key] = ''.join(
                    [self._keyword_formatter.format(sub_format, **sub_item)
                     for sub_item
                     in json_item[key]])

        return json_item