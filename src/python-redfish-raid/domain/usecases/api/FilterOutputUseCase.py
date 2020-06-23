import jmespath
import humanize

from string import Formatter

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


class FilterOutputCaseUseCase(UseCase):
    """Filter api output."""

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
            filtered_json = jmespath.search(query['jq'], service_data_json)
            # print(filtered_json)
            # if 'transforms' in query:
            #     transforms = query[trans]
            #     for item in filtered_json:
            #         if item not in transforms:
            #             filtered_json
            #     filtered_json = [item if item not in transforms else humanize.__getattribute__(transforms[item])(item) for item in filtered_json]

            if 'format' in query:
                item_format = query['format']
                response[key] = ''.join([self._keyword_formatter.format(item_format, **item) for item in filtered_json])
            else:
                response[key] = filtered_json
        return response
