"""Disk metrics collector."""
import psutil
from typing import Dict, List, Any


def collect_disk_metrics() -> Dict[str, Any]:
    """
    Collect disk metrics including usage and I/O statistics.

    Returns:
        Dictionary containing disk metrics
    """
    # Disk partitions and usage
    partitions = []
    for partition in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            partitions.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "opts": partition.opts,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
            })
        except (PermissionError, OSError):
            # Skip partitions we can't access
            continue

    # Disk I/O statistics
    try:
        disk_io = psutil.disk_io_counters(perdisk=False)
        io_stats = {
            "read_count": disk_io.read_count,
            "write_count": disk_io.write_count,
            "read_bytes": disk_io.read_bytes,
            "write_bytes": disk_io.write_bytes,
            "read_time": disk_io.read_time,
            "write_time": disk_io.write_time,
        } if disk_io else None
    except (AttributeError, RuntimeError):
        io_stats = None

    # Per-disk I/O statistics
    try:
        disk_io_per_disk = psutil.disk_io_counters(perdisk=True)
        per_disk_stats = {}
        if disk_io_per_disk:
            for disk_name, disk_stat in disk_io_per_disk.items():
                per_disk_stats[disk_name] = {
                    "read_count": disk_stat.read_count,
                    "write_count": disk_stat.write_count,
                    "read_bytes": disk_stat.read_bytes,
                    "write_bytes": disk_stat.write_bytes,
                    "read_time": disk_stat.read_time,
                    "write_time": disk_stat.write_time,
                }
    except (AttributeError, RuntimeError):
        per_disk_stats = None

    return {
        "partitions": partitions,
        "io_stats": io_stats,
        "per_disk_io": per_disk_stats,
    }


def calculate_iops(previous_io: Dict, current_io: Dict, interval: float) -> Dict[str, float]:
    """
    Calculate IOPS (I/O operations per second) based on two measurements.

    Args:
        previous_io: Previous I/O statistics
        current_io: Current I/O statistics
        interval: Time interval between measurements in seconds

    Returns:
        Dictionary containing IOPS metrics
    """
    if not previous_io or not current_io or interval <= 0:
        return {"read_iops": 0, "write_iops": 0}

    read_iops = (current_io["read_count"] - previous_io["read_count"]) / interval
    write_iops = (current_io["write_count"] - previous_io["write_count"]) / interval

    return {
        "read_iops": max(0, read_iops),
        "write_iops": max(0, write_iops),
    }
