"""CPU metrics collector."""
import psutil
from typing import Dict, List, Any


def collect_cpu_metrics() -> Dict[str, Any]:
    """
    Collect CPU metrics including overall usage, per-core usage, and load averages.

    Returns:
        Dictionary containing CPU metrics
    """
    # Overall CPU usage
    cpu_percent = psutil.cpu_percent(interval=1, percpu=False)

    # Per-core CPU usage
    cpu_percent_per_core = psutil.cpu_percent(interval=0, percpu=True)

    # CPU times (user, system, idle, iowait)
    cpu_times = psutil.cpu_times()

    # Load average (Linux/macOS only)
    try:
        load_avg_1, load_avg_5, load_avg_15 = psutil.getloadavg()
    except (AttributeError, OSError):
        # Windows doesn't support getloadavg
        load_avg_1 = load_avg_5 = load_avg_15 = None

    # CPU frequency
    try:
        cpu_freq = psutil.cpu_freq()
        freq_current = cpu_freq.current if cpu_freq else None
        freq_min = cpu_freq.min if cpu_freq else None
        freq_max = cpu_freq.max if cpu_freq else None
    except (AttributeError, RuntimeError):
        freq_current = freq_min = freq_max = None

    # CPU count
    cpu_count_logical = psutil.cpu_count(logical=True)
    cpu_count_physical = psutil.cpu_count(logical=False)

    return {
        "overall_percent": cpu_percent,
        "per_core_percent": cpu_percent_per_core,
        "times": {
            "user": cpu_times.user,
            "system": cpu_times.system,
            "idle": cpu_times.idle,
            "iowait": getattr(cpu_times, 'iowait', None),
        },
        "load_average": {
            "1min": load_avg_1,
            "5min": load_avg_5,
            "15min": load_avg_15,
        },
        "frequency": {
            "current": freq_current,
            "min": freq_min,
            "max": freq_max,
        },
        "count": {
            "logical": cpu_count_logical,
            "physical": cpu_count_physical,
        }
    }


def get_top_cpu_processes(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get top N processes by CPU usage.

    Args:
        limit: Number of processes to return

    Returns:
        List of dictionaries containing process information
    """
    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            pinfo = proc.info
            processes.append({
                "pid": pinfo['pid'],
                "name": pinfo['name'],
                "cpu_percent": pinfo['cpu_percent'] or 0,
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Sort by CPU usage and return top N
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return processes[:limit]
