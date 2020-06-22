import re
from jsonquery import processPath

from framework.usecases.UseCase import UseCase


class FilterOutputCaseUseCase(UseCase):
    """Filter api output."""

    def __init__(self, json_queries):
        """Create a use case for performing queries against the JSON responses."""
        super().__init__()
        self._json_queries = json_queries

    def __call__(self, service_data_json, endpoint):
        """Perform Json Query/Select operations against the API responses."""
        response = {}
        for key, value in service_data_json:
            if key.startswith('@'):
                response[key] = value
                continue
            for query_key, json_queries in self._get_json_queries_for_data(endpoint).items():
                print('Found json queries')
                results = []
                for json_query in json_queries:
                    results = results + processPath(value, json_query)
                response[query_key] = results
        print(str(response))
        return response

    def _get_json_queries_for_data(self, endpoint):
        json_queries = []
        for query_data in self._json_queries:
            matches = re.match(query_data.endpoint_regex, endpoint, re.RegexFlag.I)
            if matches:
                json_queries = json_queries
                json_queries[query_data['key']] = query_data

        return json_queries


