import re
from jsonquery import processPath

from framework.usecases.UseCase import UseCase


class FilterOutputCaseUseCase(UseCase):
    """Filter api output."""

    def __init__(self, json_queries):
        """Create a use case for performing queries against the JSON responses."""
        super().__init__()
        self._json_queries = json_queries

    def __call__(self, service_data_json):
        """Perform Json Query/Select operations against the API responses."""
        if not isinstance(service_data_json, dict):
            return None
        response = {}
        for query in self._json_queries:
            response[query['result_key']] = processPath(service_data_json, query['jq'])
        return response
