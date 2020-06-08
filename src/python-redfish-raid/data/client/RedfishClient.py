import redfish
import json

from framework.client.Client import Client

ARG_PREFIX = 'prefix'
DEFAULT_PREFIX = '/redfish/v1'


class RedfishClient(Client):
    """Redfish client implementation."""

    def __init__(self, host, username, password, **kwargs):
        """Initialize a Redfish API client."""
        self._client = redfish.redfish_client(
            host,
            username,
            password,
            default_prefix=kwargs.get(ARG_PREFIX, DEFAULT_PREFIX))

    def connect(self, **kwargs):
        """Connect to Redfish using given credentials."""
        self._client.login()

    def get(self, path):
        """Get the response for the given api endpoint path."""
        response = self._client.get(path)
        return json.loads(response.read)

    def disconnect(self, **kwargs):
        """Disconnect client from host."""
        self._client.logout()
