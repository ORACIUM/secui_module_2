"""Network metrics collector."""
import psutil
from typing import Dict, Any


def collect_network_metrics() -> Dict[str, Any]:
    """
    Collect network metrics including interface traffic and connection status.

    Returns:
        Dictionary containing network metrics
    """
    # Network I/O statistics per interface
    net_io = psutil.net_io_counters(pernic=True)
    interfaces = {}

    for interface_name, io_stats in net_io.items():
        interfaces[interface_name] = {
            "bytes_sent": io_stats.bytes_sent,
            "bytes_recv": io_stats.bytes_recv,
            "packets_sent": io_stats.packets_sent,
            "packets_recv": io_stats.packets_recv,
            "errin": io_stats.errin,
            "errout": io_stats.errout,
            "dropin": io_stats.dropin,
            "dropout": io_stats.dropout,
        }

    # Total network I/O
    net_io_total = psutil.net_io_counters(pernic=False)
    total_stats = {
        "bytes_sent": net_io_total.bytes_sent,
        "bytes_recv": net_io_total.bytes_recv,
        "packets_sent": net_io_total.packets_sent,
        "packets_recv": net_io_total.packets_recv,
        "errin": net_io_total.errin,
        "errout": net_io_total.errout,
        "dropin": net_io_total.dropin,
        "dropout": net_io_total.dropout,
    }

    # Network connections
    try:
        connections = psutil.net_connections(kind='inet')
        connection_stats = {
            "established": sum(1 for c in connections if c.status == 'ESTABLISHED'),
            "time_wait": sum(1 for c in connections if c.status == 'TIME_WAIT'),
            "close_wait": sum(1 for c in connections if c.status == 'CLOSE_WAIT'),
            "listen": sum(1 for c in connections if c.status == 'LISTEN'),
            "total": len(connections),
        }
    except (psutil.AccessDenied, PermissionError):
        # Requires elevated privileges on some systems
        connection_stats = None

    # Network interface addresses
    addresses = {}
    net_if_addrs = psutil.net_if_addrs()
    for interface_name, addr_list in net_if_addrs.items():
        addresses[interface_name] = []
        for addr in addr_list:
            addresses[interface_name].append({
                "family": str(addr.family),
                "address": addr.address,
                "netmask": addr.netmask,
                "broadcast": addr.broadcast,
            })

    return {
        "interfaces": interfaces,
        "total": total_stats,
        "connections": connection_stats,
        "addresses": addresses,
    }


def calculate_bandwidth(previous_net: Dict, current_net: Dict, interval: float) -> Dict[str, Dict[str, float]]:
    """
    Calculate bandwidth usage (bytes/s) based on two measurements.

    Args:
        previous_net: Previous network statistics
        current_net: Current network statistics
        interval: Time interval between measurements in seconds

    Returns:
        Dictionary containing bandwidth metrics per interface
    """
    if not previous_net or not current_net or interval <= 0:
        return {}

    bandwidth = {}

    for interface_name, current_stats in current_net.items():
        if interface_name in previous_net:
            prev_stats = previous_net[interface_name]

            bytes_sent_per_sec = (current_stats["bytes_sent"] - prev_stats["bytes_sent"]) / interval
            bytes_recv_per_sec = (current_stats["bytes_recv"] - prev_stats["bytes_recv"]) / interval

            bandwidth[interface_name] = {
                "bytes_sent_per_sec": max(0, bytes_sent_per_sec),
                "bytes_recv_per_sec": max(0, bytes_recv_per_sec),
                "mbps_sent": max(0, bytes_sent_per_sec * 8 / 1_000_000),  # Convert to Mbps
                "mbps_recv": max(0, bytes_recv_per_sec * 8 / 1_000_000),
            }

    return bandwidth
