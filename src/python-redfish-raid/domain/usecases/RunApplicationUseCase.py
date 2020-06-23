from framework.usecases.UseCase import UseCase


class RunApplicationUseCase(UseCase):
    """Use case for running the application."""

    def __init__(self,
                 system_configuration,
                 invoke_api,
                 clean_up_results,
                 show_report,
                 connect,
                 disconnect,
                 command,
                 **kwargs):
        super().__init__()
        self._system_configuration = system_configuration
        self._invoke_api = invoke_api
        self._clean_up_results = clean_up_results
        self._show_report = show_report
        self._connect = connect
        self._disconnect = disconnect
        self._command = command
        self._kwargs = kwargs

    def __call__(self):
        """Run application."""
        self._connect()
        try:
            results = self._invoke_api(
                self._system_configuration.get_prefix(
                    self._command
                ) or self._kwargs.get('api_prefix'),
                recurse=self._system_configuration.get_recurse(self._command))
            return self._show_report(
                self._clean_up_results(
                    results,
                    retrieve_linked_property=self._system_configuration.get_property(self._command)
                )
            )
        finally:
            self._disconnect()
