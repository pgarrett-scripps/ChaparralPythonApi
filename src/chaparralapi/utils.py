from ping3 import ping
from . import constants

def _get_best_server(ips: list[str]) -> str:
    """
    Get the best server from a list of IPs based on ping time

    Args:
        ips (list[str]): List of IP addresses

    Returns:
        str: The best IP address
    """
    best_ip = None
    best_time = float('inf')

    for ip in ips:
        ping_time = ping(ip, timeout=2)
        if ping_time is not None and ping_time < best_time:
            best_time = ping_time
            best_ip = ip

    return best_ip

def get_best_chaparral_server() -> str:
    """
    Get the best Chaparral server based on ping time

    Returns:
        str: The best Chaparral server
    """
    servers = constants.CHAPARRAL_SERVERS
    return _get_best_server(servers)