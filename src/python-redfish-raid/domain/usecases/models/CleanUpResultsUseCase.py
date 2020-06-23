from const import ATTR_LINKS
from domain.models.ServiceData import ServiceDataReference
from framework.usecases.UseCase import UseCase


class CleanUpResultsUseCase(UseCase):
    """Clean up results use case."""

    def __init__(self,
                 get_model_from_cache,
                 invoke_api,
                 filter_output):
        super().__init__()
        self._get_model_from_cache = get_model_from_cache
        self._invoke_api = invoke_api
        self._filter_output = filter_output

    def __call__(self, data, retrieve_linked_property=None):
        """Clean up result set of data models."""
        if retrieve_linked_property:
            results = data.get(ATTR_LINKS, {}).get(retrieve_linked_property)
        else:
            results = data

        if self._filter_output is not None:
            results = self._filter_output(results)

        if isinstance(results, list):
            results = self._process_list_of_models(results)
        elif isinstance(results, dict):
            new_data = {}
            for key, value in results.items():
                if isinstance(value, list):
                    new_data[key] = self._process_list_of_models(value)
                elif isinstance(value, ServiceDataReference):
                    new_data[key] = self._get_model_from_cache(value.id)
                else:
                    new_data[key] = value
            results = new_data

        return results

    def _process_list_of_models(self, model_list):
        return [self._get_model_from_cache(item.id)
                if isinstance(item, ServiceDataReference)
                else item
                for item in model_list]
