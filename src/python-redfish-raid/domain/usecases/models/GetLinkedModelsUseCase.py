from const import ATTR_ID
from framework.usecases.UseCase import UseCase


class GetLinkedModelsUseCase(UseCase):
    """Retrieve linked models use case."""

    def __init__(self, get_cached_model):
        super().__init__()
        self._get_cached_model = get_cached_model

    def __call__(self, model):
        if isinstance(model, str):
            return self._get_cached_model(model)
        links = {}
        for key, value in model.items():
            if key == ATTR_ID:
                return self._get_cached_model(value)
            if isinstance(value, list):
                links[key] = [self(item) for item in value]
            elif isinstance(value, dict):
                links[key] = self(value)

        return links
