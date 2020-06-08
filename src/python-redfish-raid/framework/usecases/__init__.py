from domain.usecases.api.ConnectUseCase import ConnectUseCase
from domain.usecases.api.DisconnectUseCase import DisconnectUseCase
from domain.usecases.api.RecurseApiUseCase import RecurseApiUseCase
from domain.usecases.models.CacheModelUseCase import CacheModelUseCase
from domain.usecases.models.GetCachedModelUseCase import GetCachedModelUseCase
from domain.usecases.models.GetModelCache import GetModelCacheUseCase


def get_connect_usecase(client):
    """Get connect use case."""
    return ConnectUseCase(client)


def get_disconnect_usecase(client):
    """Get disconnect use case."""
    return DisconnectUseCase(client)


def get_model_cache():
    """Get model cache use case."""
    return GetModelCacheUseCase()()


def get_cache_model_usecase():
    """Get use case for caching models."""
    return CacheModelUseCase(get_model_cache())


def get_model_cached_usecase():
    """Get use case for retrieving cached models."""
    return GetCachedModelUseCase(get_model_cache())


def get_recurse_api_usecase(client):
    """Get recurse api usecase."""
    return RecurseApiUseCase(client, get_model_cached_usecase(), get_cache_model_usecase())
