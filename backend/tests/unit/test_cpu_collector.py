"""Unit tests for CPU collector."""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agent.collectors import cpu


def test_collect_cpu_metrics():
    """Test CPU metrics collection."""
    metrics = cpu.collect_cpu_metrics()

    # Check required fields
    assert "overall_percent" in metrics
    assert "per_core_percent" in metrics
    assert "times" in metrics
    assert "load_average" in metrics
    assert "frequency" in metrics
    assert "count" in metrics

    # Check data types and ranges
    assert isinstance(metrics["overall_percent"], (int, float))
    assert 0 <= metrics["overall_percent"] <= 100

    assert isinstance(metrics["per_core_percent"], list)
    for core_pct in metrics["per_core_percent"]:
        assert 0 <= core_pct <= 100

    # Check CPU times
    times = metrics["times"]
    assert "user" in times
    assert "system" in times
    assert "idle" in times
    assert isinstance(times["user"], (int, float))
    assert isinstance(times["system"], (int, float))
    assert isinstance(times["idle"], (int, float))

    # Check CPU count
    count = metrics["count"]
    assert count["logical"] > 0
    assert count["physical"] > 0
    assert count["logical"] >= count["physical"]


def test_get_top_cpu_processes():
    """Test getting top CPU processes."""
    processes = cpu.get_top_cpu_processes(limit=5)

    assert isinstance(processes, list)
    assert len(processes) <= 5

    for proc in processes:
        assert "pid" in proc
        assert "name" in proc
        assert "cpu_percent" in proc
        assert isinstance(proc["pid"], int)
        assert isinstance(proc["name"], str)
        assert isinstance(proc["cpu_percent"], (int, float))


def test_get_top_cpu_processes_custom_limit():
    """Test getting top CPU processes with custom limit."""
    processes = cpu.get_top_cpu_processes(limit=3)

    assert isinstance(processes, list)
    assert len(processes) <= 3


def test_cpu_metrics_consistency():
    """Test that multiple collections return consistent data structures."""
    metrics1 = cpu.collect_cpu_metrics()
    metrics2 = cpu.collect_cpu_metrics()

    # Both should have the same keys
    assert set(metrics1.keys()) == set(metrics2.keys())

    # CPU count should be the same
    assert metrics1["count"] == metrics2["count"]
