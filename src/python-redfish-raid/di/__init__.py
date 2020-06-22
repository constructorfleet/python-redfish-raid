from domain.usecases.GetCommandUseCase import GetCommandUseCase
from domain.usecases.RunApplicationUseCase import RunApplicationUseCase
from domain.usecases.api.ConnectUseCase import ConnectUseCase
from domain.usecases.api.DisconnectUseCase import DisconnectUseCase
from domain.usecases.api.FilterOutputUseCase import FilterOutputCaseUseCase
from domain.usecases.api.GetApiClientUseCase import GetApiClientUseCase
from domain.usecases.api.InvokeApiUseCase import InvokeApiUseCase
from domain.usecases.configs.GetSystemConfigUseCase import GetSystemConfigUseCase
from domain.usecases.configs.LoadConfigurationUseCase import LoadConfigurationUseCase
from domain.usecases.models.AddModelToCacheUseCase import AddModelToCacheUseCase
from domain.usecases.models.CleanUpResultsUseCase import CleanUpResultsUseCase
from domain.usecases.models.GetModelCache import GetModelCacheUseCase
from domain.usecases.models.RetrieveModelFromCacheUseCase import RetrieveModelFromCacheUseCase


def get_load_configuration_usecase():
    """Get configuration loader use case."""
    return LoadConfigurationUseCase()


def get_system_configuration_usecase(load_config):
    """"Get system configuration use case."""
    return GetSystemConfigUseCase(load_config)


def get_command_use_case():
    """Get command use case."""
    return GetCommandUseCase()


def get_connect_usecase(client):
    """Get connect use case."""
    return ConnectUseCase(client)


def get_disconnect_usecase(client):
    """Get disconnect use case."""
    return DisconnectUseCase(client)


def get_model_cache():
    """Get model cache use case."""
    return GetModelCacheUseCase()()


def get_add_model_to_cache_usecase():
    """Get use case for caching models."""
    return AddModelToCacheUseCase(get_model_cache())


def get_retrieve_cached_model_usecase():
    """Get use case for retrieving cached models."""
    return RetrieveModelFromCacheUseCase(get_model_cache())


def get_api_client_usecase():
    """Get use case for creating api client."""
    return GetApiClientUseCase()


def get_filter_output_usecase(config, command):
    """Get use case for filtering api output."""
    json_queries = []
    for values in config.get_command_config(command):
        for value in values:
            if isinstance(value, dict) and value.get('json_queries'):
                json_queries = json_queries + value[json_queries]
                print(str(json_queries))

    if len(json_queries) == 0:
        print('No json queries')
        return None

    return FilterOutputCaseUseCase(json_queries)


def get_invoke_api_usecase(client, config, command):
    """Get invoke api usecase."""
    return InvokeApiUseCase(client,
                            get_retrieve_cached_model_usecase(),
                            get_add_model_to_cache_usecase(),
                            get_filter_output_usecase(config, command))


def get_clean_up_results_usecase(invoke_api,):
    """Get use case for cleaning up result set."""
    return CleanUpResultsUseCase(
        get_retrieve_cached_model_usecase(),
        invoke_api
    )


def get_run_application_usecase(api_type,
                                login_host,
                                login_account,
                                login_password,
                                flags,
                                **kwargs):
    """Get use case for running application."""
    client = get_api_client_usecase()(
        api_type,
        login_host,
        login_account,
        login_password,
        prefix=kwargs.get('api_prefix'))
    config = get_system_configuration_usecase(
        get_load_configuration_usecase()
    )(kwargs['system'])
    command = get_command_use_case()(flags)
    invoke_api = get_invoke_api_usecase(client, config, command.command_name)
    return RunApplicationUseCase(
        config,
        invoke_api,
        get_clean_up_results_usecase(invoke_api),
        get_connect_usecase(client),
        get_disconnect_usecase(client),
        command,
        **kwargs
    )
