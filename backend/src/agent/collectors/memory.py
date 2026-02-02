"""Memory metrics collector."""
import psutil
from typing import Dict, Any


def collect_memory_metrics() -> Dict[str, Any]:
    """
    Collect memory metrics including physical and swap memory.

    Returns:
        Dictionary containing memory metrics
    """
    # Physical memory
    virtual_mem = psutil.virtual_memory()

    # Swap memory
    swap_mem = psutil.swap_memory()

    return {
        "physical": {
            "total": virtual_mem.total,
            "available": virtual_mem.available,
            "used": virtual_mem.used,
            "free": virtual_mem.free,
            "percent": virtual_mem.percent,
            "buffers": getattr(virtual_mem, 'buffers', None),
            "cached": getattr(virtual_mem, 'cached', None),
            "shared": getattr(virtual_mem, 'shared', None),
        },
        "swap": {
            "total": swap_mem.total,
            "used": swap_mem.used,
            "free": swap_mem.free,
            "percent": swap_mem.percent,
            "sin": swap_mem.sin,  # swap in
            "sout": swap_mem.sout,  # swap out
        }
    }


def get_memory_by_process(limit: int = 5) -> list:
    """
    Get top N processes by memory usage.

    Args:
        limit: Number of processes to return

    Returns:
        List of dictionaries containing process memory information
    """
    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'memory_percent']):
        try:
            pinfo = proc.info
            processes.append({
                "pid": pinfo['pid'],
                "name": pinfo['name'],
                "memory_mb": pinfo['memory_info'].rss / 1024 / 1024,  # Convert to MB
                "memory_percent": pinfo['memory_percent'],
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Sort by memory usage and return top N
    processes.sort(key=lambda x: x['memory_percent'], reverse=True)
    return processes[:limit]
