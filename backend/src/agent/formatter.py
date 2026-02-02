"""Output formatter for CLI display."""
import json
from typing import Dict, Any
from datetime import datetime


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes to human-readable format.

    Args:
        bytes_value: Number of bytes

    Returns:
        Formatted string (e.g., "1.5 GB")
    """
    if bytes_value is None:
        return "N/A"

    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def format_metrics_cli(metrics: Dict[str, Any]) -> str:
    """
    Format metrics for CLI output.

    Args:
        metrics: Dictionary containing all collected metrics

    Returns:
        Formatted string for display
    """
    lines = []
    lines.append("=" * 80)
    lines.append(f"System Metrics - {metrics['timestamp']}")
    lines.append("=" * 80)

    # CPU Metrics
    if 'cpu' in metrics:
        cpu = metrics['cpu']
        lines.append("\n[CPU]")
        lines.append(f"  Overall Usage: {cpu['overall_percent']:.1f}%")

        if cpu['load_average']['1min'] is not None:
            lines.append(f"  Load Average: {cpu['load_average']['1min']:.2f} (1m), "
                        f"{cpu['load_average']['5min']:.2f} (5m), "
                        f"{cpu['load_average']['15min']:.2f} (15m)")

        lines.append(f"  Cores: {cpu['count']['logical']} logical, {cpu['count']['physical']} physical")

        if cpu.get('per_core_percent'):
            core_usage = ', '.join([f"{p:.1f}%" for p in cpu['per_core_percent']])
            lines.append(f"  Per-core: {core_usage}")

    # Memory Metrics
    if 'memory' in metrics:
        mem = metrics['memory']
        phys = mem['physical']
        swap = mem['swap']

        lines.append("\n[Memory]")
        lines.append(f"  Physical: {format_bytes(phys['used'])} / {format_bytes(phys['total'])} ({phys['percent']:.1f}%)")
        lines.append(f"  Available: {format_bytes(phys['available'])}")

        if swap['total'] > 0:
            lines.append(f"  Swap: {format_bytes(swap['used'])} / {format_bytes(swap['total'])} ({swap['percent']:.1f}%)")

    # Disk Metrics
    if 'disk' in metrics:
        disk = metrics['disk']
        lines.append("\n[Disk]")

        for partition in disk['partitions']:
            lines.append(f"  {partition['mountpoint']} ({partition['device']}):")
            lines.append(f"    Usage: {format_bytes(partition['used'])} / {format_bytes(partition['total'])} ({partition['percent']:.1f}%)")
            lines.append(f"    Free: {format_bytes(partition['free'])}")

        if disk['io_stats']:
            io = disk['io_stats']
            lines.append(f"  I/O: Read {format_bytes(io['read_bytes'])}, Write {format_bytes(io['write_bytes'])}")

    # Network Metrics
    if 'network' in metrics:
        net = metrics['network']
        lines.append("\n[Network]")

        total = net['total']
        lines.append(f"  Total Traffic:")
        lines.append(f"    Sent: {format_bytes(total['bytes_sent'])} ({total['packets_sent']} packets)")
        lines.append(f"    Received: {format_bytes(total['bytes_recv'])} ({total['packets_recv']} packets)")
        lines.append(f"    Errors: {total['errin']} in, {total['errout']} out")
        lines.append(f"    Drops: {total['dropin']} in, {total['dropout']} out")

        if net['connections']:
            conn = net['connections']
            lines.append(f"  Connections: {conn['total']} total, {conn['established']} established")

    lines.append("=" * 80)
    return '\n'.join(lines)


def format_metrics_json(metrics: Dict[str, Any]) -> str:
    """
    Format metrics as JSON.

    Args:
        metrics: Dictionary containing all collected metrics

    Returns:
        JSON string
    """
    return json.dumps(metrics, indent=2, default=str)
