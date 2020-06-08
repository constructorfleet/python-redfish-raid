from const import ATTR_ID
from framework.usecases.UseCase import UseCase


class GetLinkedModelsUseCase(UseCase):
    """Retrieve linked models use case."""

    def __init__(self, get_cached_model, invoke_api):
        super().__init__()
        self._get_cached_model = get_cached_model
        self._invoke_api = invoke_api

    def __call__(self, model):
        links = {}
        for key, value in model.links.items():
            if isinstance(value, dict):
                links[key] = self._process_link_dict(value)
            elif isinstance(value, list):
                links[key] = self._process_link_list(value)
        return links

    def _process_link_list(self, link_list):
        return [self._process_link_dict(link) for link in link_list]

    def _process_link_dict(self, link_dict):
        if not isinstance(link_dict, dict):
            return link_dict  # Sanity check
        object_id = link_dict.get(ATTR_ID)
        if not object_id:
            return link_dict
        cached_model = self._get_cached_model(object_id)
        if not cached_model:
            cached_model = self._invoke_api(object_id, recurse=False)
        return cached_model
