from framework.usecases.UseCase import UseCase


class DisconnectUseCase(UseCase):
    """Use case for disconnecting client."""

    def __init__(self, client):
        super().__init__()
        self._client = client

    def __call__(self, **kwargs):
        self._client.disconnect(**kwargs)
