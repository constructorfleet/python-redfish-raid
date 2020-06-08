from framework.usecases.UseCase import UseCase


class RetrieveModelFromCacheUseCase(UseCase):
    """Get model from cache if exists."""

    def __init__(self, model_cache):
        """Create a new use case for getting data models from cache."""
        super().__init__()
        self._model_cache = model_cache

    def __call__(self, id):
        """Get data model from cache by id if it exists."""
        return self._model_cache.get(id, None)
