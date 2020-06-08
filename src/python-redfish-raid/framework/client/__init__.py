"""Client framework."""
from const import API_REDFISH
from data.client.RedfishClient import RedfishClient


def get_client(api_type, host, username, password, **kwargs):
    """Get client for specified api."""
    if api_type == API_REDFISH:
        return RedfishClient(host, username, password, prefix=kwargs.get('prefix'))
    raise Exception('Invalid api type %s' % api_type)
