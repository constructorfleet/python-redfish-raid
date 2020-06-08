from framework.usecases.UseCase import UseCase


class ConnectUseCase(UseCase):
    """Connection use case."""

    def __init__(self, client):
        """Instantiate a use case for connecting to a server."""
        super().__init__()
        self.client = client

    def __call__(self, **kwargs):
        """Connect to host with given credentials."""
        try:
            self.client.connect()
        except Exception as err:
            self._logger.error("Connection error: %s", str(err))
            raise err  # Re-raise error
