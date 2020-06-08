from framework.usecases.UseCase import UseCase


class AddModelToCacheUseCase(UseCase):
    """Add model to cache use case."""

    def __init__(self, model_cache):
        """Create use case for adding model to cache."""
        super().__init__()
        self._model_cache = model_cache

    def __call__(self, service_data_model):
        """Add service data model to cache."""
        self._model_cache[service_data_model.id] = service_data_model
