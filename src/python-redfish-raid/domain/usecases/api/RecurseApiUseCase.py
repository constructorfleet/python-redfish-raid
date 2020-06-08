from copy import deepcopy
import json
import re

from domain.models.ServiceData import ServiceData
from framework.usecases.UseCase import UseCase

ATTR_CONTEXT = '@odata.context'
ATTR_DATA_TYPE = '@odata.type'
ATTR_ID = '@odata.id'
ATTR_LINKS = 'Links'

_CACHE = {}
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
_WHITELIST_KEYWORDS = [
    'Storage',
    'Disk',
    'Drive',
    'Enclosure'
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

def _is_whitelisted(endpoint):
    for keyword in _WHITELIST_KEYWORDS:
        if keyword.lower() in endpoint.lower():
            return True
    return False


class RecurseApiUseCase(UseCase):
    """Recurse through api use case."""

    def __init__(self, client):
        """Instantiate a new instance of this use case."""
        super().__init__()
        self._client = client

    def __call__(self, endpoint):
        """Invoke the specified endpoint and recurse child properties."""
        try:
            if endpoint in _CACHE:
                print('Retreiving %s from cache' % endpoint)
                return _CACHE[endpoint]
            if _is_blacklisted(endpoint):
                return {}

            print('Retreiving %s' % endpoint)
            response = self._client.get(endpoint)
            id = _clear_key(response, ATTR_ID, endpoint)
            context = _clear_key(response, ATTR_CONTEXT, endpoint)
            data_type = _clear_key(response, ATTR_DATA_TYPE)

            links = _clear_key(response, ATTR_LINKS, {})

            populated_json = self._recurse_json(response)

            service_data = ServiceData(id, context, data_type, populated_json, links)
            _CACHE[endpoint] = service_data
            return service_data

        except Exception as err:
            self._logger.error(str(err))
            raise err

    def _recurse_json(self, json):
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
