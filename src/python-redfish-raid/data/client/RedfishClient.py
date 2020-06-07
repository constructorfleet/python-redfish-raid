import redfish

from framework.client.Client import Client

ARG_PREFIX = 'prefix'
DEFAULT_PREFIX = '/redfish/v1'


class RedfishClient(Client):
    """Redfish client implementation."""

    _client = None

    def connect(self, host, username, password, **kwargs):
        """Connect to Redfish using given credentials."""
        self._client = redfish.redfish_client(
            host,
            username,
            password,
            default_prefix=kwargs.get(ARG_PREFIX, DEFAULT_PREFIX))

        self._client.login()

    def get(self, path):
        """Get the response for the given api endpoint path."""
        return self._client.get(path)



