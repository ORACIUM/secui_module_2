"""Unit tests for disk collector."""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agent.collectors import disk


def test_collect_disk_metrics():
    """Test disk metrics collection."""
    metrics = disk.collect_disk_metrics()

    # Check required fields
    assert "partitions" in metrics
    assert "io_stats" in metrics
    assert "per_disk_io" in metrics

    # Check partitions
    partitions = metrics["partitions"]
    assert isinstance(partitions, list)
    assert len(partitions) > 0  # Should have at least one partition

    for partition in partitions:
        assert "device" in partition
        assert "mountpoint" in partition
        assert "fstype" in partition
        assert "total" in partition
        assert "used" in partition
        assert "free" in partition
        assert "percent" in partition

        # Check data types and ranges
        assert isinstance(partition["total"], int)
        assert isinstance(partition["used"], int)
        assert isinstance(partition["free"], int)
        assert isinstance(partition["percent"], (int, float))

        assert partition["total"] > 0
        assert partition["used"] >= 0
        assert partition["free"] >= 0
        assert 0 <= partition["percent"] <= 100

        # Check relationships
        assert partition["used"] <= partition["total"]
        assert partition["free"] <= partition["total"]


def test_disk_io_stats():
    """Test disk I/O statistics."""
    metrics = disk.collect_disk_metrics()

    io_stats = metrics["io_stats"]

    # May be None on some systems
    if io_stats:
        assert "read_count" in io_stats
        assert "write_count" in io_stats
        assert "read_bytes" in io_stats
        assert "write_bytes" in io_stats

        assert isinstance(io_stats["read_count"], int)
        assert isinstance(io_stats["write_count"], int)
        assert io_stats["read_count"] >= 0
        assert io_stats["write_count"] >= 0


def test_calculate_iops():
    """Test IOPS calculation."""
    previous_io = {
        "read_count": 1000,
        "write_count": 500,
    }

    current_io = {
        "read_count": 1100,
        "write_count": 550,
    }

    interval = 5.0

    iops = disk.calculate_iops(previous_io, current_io, interval)

    assert "read_iops" in iops
    assert "write_iops" in iops
    assert iops["read_iops"] == 20.0  # (1100 - 1000) / 5
    assert iops["write_iops"] == 10.0  # (550 - 500) / 5


def test_calculate_iops_zero_interval():
    """Test IOPS calculation with zero interval."""
    previous_io = {"read_count": 1000, "write_count": 500}
    current_io = {"read_count": 1100, "write_count": 550}

    iops = disk.calculate_iops(previous_io, current_io, 0)

    assert iops["read_iops"] == 0
    assert iops["write_iops"] == 0


def test_calculate_iops_none_values():
    """Test IOPS calculation with None values."""
    iops = disk.calculate_iops(None, None, 5.0)

    assert iops["read_iops"] == 0
    assert iops["write_iops"] == 0
