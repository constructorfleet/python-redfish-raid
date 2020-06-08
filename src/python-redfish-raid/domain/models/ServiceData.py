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
        for key, value in attrs.items():
            self[key] = value

    def __str__(self) -> str:
        return "(%s:%s) -> %s" % (self.data_type, self.id, super().__str__())
