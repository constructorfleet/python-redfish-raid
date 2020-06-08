from domain.models.ModelCache import ModelCache
from framework.usecases.UseCase import UseCase

_cache = ModelCache()


class GetModelCacheUseCase(UseCase):
    """Use case for getting cache for models."""

    def __init__(self):
        """Create use case for retrieving model cache."""
        super().__init__()

    def __call__(self):
        """Retrieve the model cache."""
        return _cache
