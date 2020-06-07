from copy import deepcopy

from domain.models.ServiceData import ServiceData
from framework.usecases.UseCase import UseCase

ATTR_CONTEXT = '@odata.context'
ATTR_DATA_TYPE = '@odata.type'
ATTR_ID = '@odata.id'
ATTR_LINKS = 'Links'


def _clear_key(json, key, default=None):
    if key not in json:
        return default
    value = json[key]
    del json[key]
    return value


class RecurseApiUseCase(UseCase):
    """Recurse through api use case."""

    def __init__(self, client):
        """Instantiate a new instance of this use case."""
        super().__init__()
        self.client = client

    def __call__(self, endpoint):
        """Invoke the specified endpoint and recurse child properties."""
        try:
            response = self.client.get(endpoint)
            id = _clear_key(response, ATTR_ID, endpoint)
            context = _clear_key(response, ATTR_CONTEXT, endpoint)
            data_type = _clear_key(response, ATTR_DATA_TYPE)

            links = _clear_key(response, ATTR_LINKS, {})

            populated_json = self._recurse_json(response)

            return ServiceData(id, context, data_type, populated_json, links)
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
