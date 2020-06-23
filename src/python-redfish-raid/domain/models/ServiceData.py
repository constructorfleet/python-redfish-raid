import json

DATA_TYPE_IGNORED = "Ignored Data Type"
DATA_TYPE_REFERENCE = "See Referenced ID"


class ServiceData(dict):
    """Service data class."""

    __slots__ = ['id', 'context', 'data_type', 'links']

    def __init__(self, id, context, api_data_type, attrs, links=None):
        """Instantiate a service data object."""
        super().__init__()
        self.id = id
        self.context = context
        self.data_type = api_data_type
        self.links = links or {}
        if attrs is not None and len(attrs.keys()) > 0:
            for key, value in attrs.items():
                self[key] = value

        self['@id'] = self.id
        self['@data_type'] = self.data_type
        if self.context:
            self['@context'] = self.context

    def __str__(self) -> str:
        return json.dumps(self, indent=2, sort_keys=True)


class IgnoredServiceDataType(ServiceData):
    """Ignored service data container."""

    def __init__(self, id):
        """Create an ignored service data model."""
        super().__init__(id, None, DATA_TYPE_IGNORED, {})


class ServiceDataReference(ServiceData):
    """Referenced service data container."""

    def __init__(self, id):
        """Create a placeholder indicating the service data model can be referenced elsewhere."""
        super().__init__(id, None, DATA_TYPE_REFERENCE, {})
