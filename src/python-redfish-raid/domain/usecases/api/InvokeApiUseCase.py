from copy import deepcopy

from const import ATTR_ID, ATTR_CONTEXT, ATTR_DATA_TYPE
from domain.models.ServiceData import ServiceData, IgnoredServiceDataType, ServiceDataReference
from framework.usecases.UseCase import UseCase

_BLACKLIST_KEYWORDS = [
    # 'Fan',
    # 'DIMM',
    # 'Assembly',
    # 'Sensor',
    # 'Processor',
    #'Power',
    # 'PCIeFunction',
    # 'Thermal',
    # 'PCIeDevice',
    # 'PowerSupplies',
    # 'DellOSDeploymentService',
    # 'Memory',
    # 'JSON',
    # 'Certificates',
    # 'Software',
    # 'Logs',
    # 'Network',
    # 'Ethernet',
    # 'Jobs',
    # 'Accounts',
    # 'Users',
    # 'Sessions',
    # 'Bios',
    # 'BootOptions',
    # 'BootSources',
    # 'DellNumericSensor',
    # 'License',
    # 'Managers'
]

# Keep track of endpoints in stack heap to prevent circular recursion and heap exceptions
_ACTIVE_ENDPOINTS = []


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

    def __init__(self, client, retrieve_cached_model, add_model_to_cache):
        """Instantiate a new instance of this use case."""
        super().__init__()
        self._client = client
        self._retrieve_cached_model = retrieve_cached_model
        self._add_model_to_cache = add_model_to_cache
        self._recursion_depth = 0

    def __call__(self, endpoint, recurse):
        """Invoke the specified endpoint and recurse child properties if specified."""
        self._recursion_depth += 1
        results = self._invoke_api(endpoint, recurse)
        self._recursion_depth -= 1
        return results

    def _invoke_api(self, endpoint, recurse):
        if isinstance(recurse, int) and self._recursion_depth > (recurse + 1):
                return

        if not endpoint.startswith('/'):
            return endpoint  # Sanity check
        try:
            if not _is_blacklisted(endpoint):
                cached_model = self._retrieve_cached_model(endpoint)
                if cached_model or endpoint in _ACTIVE_ENDPOINTS:
                    return ServiceDataReference(endpoint)

                _ACTIVE_ENDPOINTS.append(endpoint)
                # print('Retrieving %s' % endpoint)
                response = self._client.get(endpoint)
                id = _clear_key(response, ATTR_ID, endpoint)
                context = _clear_key(response, ATTR_CONTEXT, endpoint)
                data_type = _clear_key(response, ATTR_DATA_TYPE)
                populated_json = response

                if recurse:
                    populated_json = self._recurse_json(response, recurse)

                cached_model = ServiceData(id, context, data_type, populated_json, {})
                _ACTIVE_ENDPOINTS.remove(endpoint)
            else:
                cached_model = IgnoredServiceDataType(endpoint)
            self._add_model_to_cache(cached_model)
            return cached_model

        except Exception as err:
            self._logger.error(str(err))
            raise err

    def _recurse_json(self, json, recurse):
        if isinstance(json, list):
            return [self._recurse_json(item, recurse) for item in json]
        if not isinstance(json, dict):
            return json

        json_copy = deepcopy(json)
        for key, value in json_copy.items():
            if key == ATTR_ID:
                return json if value in _ACTIVE_ENDPOINTS else self(value, recurse)

            if isinstance(value, dict):
                json[key] = self._recurse_json(value, recurse)
            elif isinstance(value, list):
                json[key] = [self._recurse_json(item, recurse) for item in value]

        return json
