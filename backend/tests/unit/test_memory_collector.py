"""Unit tests for memory collector."""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agent.collectors import memory


def test_collect_memory_metrics():
    """Test memory metrics collection."""
    metrics = memory.collect_memory_metrics()

    # Check required fields
    assert "physical" in metrics
    assert "swap" in metrics

    # Check physical memory
    phys = metrics["physical"]
    assert "total" in phys
    assert "available" in phys
    assert "used" in phys
    assert "free" in phys
    assert "percent" in phys

    # Check data types and ranges
    assert isinstance(phys["total"], int)
    assert isinstance(phys["used"], int)
    assert isinstance(phys["available"], int)
    assert isinstance(phys["percent"], (int, float))

    assert phys["total"] > 0
    assert phys["used"] >= 0
    assert phys["available"] >= 0
    assert 0 <= phys["percent"] <= 100

    # Check relationships
    assert phys["used"] <= phys["total"]
    assert phys["available"] <= phys["total"]

    # Check swap memory
    swap = metrics["swap"]
    assert "total" in swap
    assert "used" in swap
    assert "free" in swap
    assert "percent" in swap

    assert isinstance(swap["total"], int)
    assert swap["total"] >= 0

    if swap["total"] > 0:
        assert 0 <= swap["percent"] <= 100


def test_get_memory_by_process():
    """Test getting processes by memory usage."""
    processes = memory.get_memory_by_process(limit=5)

    assert isinstance(processes, list)
    assert len(processes) <= 5

    for proc in processes:
        assert "pid" in proc
        assert "name" in proc
        assert "memory_mb" in proc
        assert "memory_percent" in proc
        assert isinstance(proc["pid"], int)
        assert isinstance(proc["name"], str)
        assert isinstance(proc["memory_mb"], (int, float))
        assert proc["memory_mb"] >= 0


def test_get_memory_by_process_custom_limit():
    """Test getting memory processes with custom limit."""
    processes = memory.get_memory_by_process(limit=3)

    assert isinstance(processes, list)
    assert len(processes) <= 3


def test_memory_metrics_consistency():
    """Test that physical memory total doesn't change."""
    metrics1 = memory.collect_memory_metrics()
    metrics2 = memory.collect_memory_metrics()

    # Total memory should be the same
    assert metrics1["physical"]["total"] == metrics2["physical"]["total"]
    assert metrics1["swap"]["total"] == metrics2["swap"]["total"]
