from const import API_REDFISH
from data.client.RedfishClient import RedfishClient
from framework.usecases.UseCase import UseCase


class GetApiClientUseCase(UseCase):
    """Use case for creating the client implementation."""

    def __init__(self):
        """Create use case for building the api client."""
        super().__init__()

    def __call__(self, api_type, host, username, password, **kwargs):
        """Get client for specified api."""
        if api_type == API_REDFISH:
            return RedfishClient(host, username, password, prefix=kwargs.get('prefix'))
        raise Exception('Invalid api type %s' % api_type)
