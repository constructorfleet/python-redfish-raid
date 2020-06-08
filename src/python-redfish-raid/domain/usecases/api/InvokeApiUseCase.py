from copy import deepcopy

from const import ATTR_ID, ATTR_CONTEXT, ATTR_DATA_TYPE, ATTR_LINKS
from domain.models.ServiceData import ServiceData, IgnoredServiceData
from framework.usecases.UseCase import UseCase

_BLACKLIST_KEYWORDS = [
    'Fan',
    'DIMM',
    'Sensor',
    'Processor',
    'Power',
    'JSON',
    'Certificates',
    'Software',
    'Log',
    'Network'
]


def _clear_key(json_dict, key, default=None):
    if key not in json_dict:
        return default
    value = json_dict[key]
    del json_dict[key]
    return value


def _is_blacklisted(endpoint):
    for keyword in _BLACKLIST_KEYWORDS:
        if keyword.lower() in endpoint.lower():
            return True
    return False


class InvokeApiUseCase(UseCase):
    """Invoke api use case."""

    def __init__(self, client, get_cached_model, cache_model):
        """Instantiate a new instance of this use case."""
        super().__init__()
        self._client = client
        self._get_cached_model = get_cached_model
        self._cache_model = cache_model

    def __call__(self, endpoint, recurse=True):
        """Invoke the specified endpoint and recurse child properties if specified."""
        try:
            cached_model = self._get_cached_model(endpoint)
            if cached_model:
                print('Retrieving %s from cache' % endpoint)
                return cached_model
            if not _is_blacklisted(endpoint):
                print('Retrieving %s' % endpoint)
                response = self._client.get(endpoint)
                id = _clear_key(response, ATTR_ID, endpoint)
                context = _clear_key(response, ATTR_CONTEXT, endpoint)
                data_type = _clear_key(response, ATTR_DATA_TYPE)

                links = _clear_key(response, ATTR_LINKS, {})
                populated_json = response
                if recurse:
                    populated_json = self._recurse_json(response)

                cached_model = ServiceData(id, context, data_type, populated_json, links)
            else:
                cached_model = IgnoredServiceData(endpoint)
            self._cache_model(cached_model)
            return cached_model

        except Exception as err:
            self._logger.error(str(err))
            raise err

    def _recurse_json(self, json):
        if isinstance(json, list):
            return [self(item) for item in json]
        if not isinstance(json, dict):
            return json

        json_copy = deepcopy(json)
        for key, value in json_copy.items():
            if key == ATTR_ID:
                return self(value)

            if isinstance(value, dict):
                json[key] = self._recurse_json(value)
            elif isinstance(value, list):
                json[key] = [self._recurse_json(item) for item in value]

        return json
