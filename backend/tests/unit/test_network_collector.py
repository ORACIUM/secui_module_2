"""Unit tests for network collector."""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agent.collectors import network


def test_collect_network_metrics():
    """Test network metrics collection."""
    metrics = network.collect_network_metrics()

    # Check required fields
    assert "interfaces" in metrics
    assert "total" in metrics
    assert "connections" in metrics
    assert "addresses" in metrics

    # Check interfaces
    interfaces = metrics["interfaces"]
    assert isinstance(interfaces, dict)
    assert len(interfaces) > 0  # Should have at least one interface

    for interface_name, stats in interfaces.items():
        assert "bytes_sent" in stats
        assert "bytes_recv" in stats
        assert "packets_sent" in stats
        assert "packets_recv" in stats
        assert "errin" in stats
        assert "errout" in stats
        assert "dropin" in stats
        assert "dropout" in stats

        # Check data types
        assert isinstance(stats["bytes_sent"], int)
        assert isinstance(stats["bytes_recv"], int)
        assert stats["bytes_sent"] >= 0
        assert stats["bytes_recv"] >= 0

    # Check total stats
    total = metrics["total"]
    assert "bytes_sent" in total
    assert "bytes_recv" in total
    assert isinstance(total["bytes_sent"], int)
    assert isinstance(total["bytes_recv"], int)


def test_network_addresses():
    """Test network interface addresses."""
    metrics = network.collect_network_metrics()

    addresses = metrics["addresses"]
    assert isinstance(addresses, dict)

    for interface_name, addr_list in addresses.items():
        assert isinstance(addr_list, list)

        for addr in addr_list:
            assert "family" in addr
            assert "address" in addr


def test_calculate_bandwidth():
    """Test bandwidth calculation."""
    previous_net = {
        "eth0": {
            "bytes_sent": 1000000,
            "bytes_recv": 2000000,
        }
    }

    current_net = {
        "eth0": {
            "bytes_sent": 1500000,
            "bytes_recv": 2500000,
        }
    }

    interval = 5.0

    bandwidth = network.calculate_bandwidth(previous_net, current_net, interval)

    assert "eth0" in bandwidth
    assert bandwidth["eth0"]["bytes_sent_per_sec"] == 100000.0  # (1500000 - 1000000) / 5
    assert bandwidth["eth0"]["bytes_recv_per_sec"] == 100000.0  # (2500000 - 2000000) / 5
    assert bandwidth["eth0"]["mbps_sent"] == pytest.approx(0.8, rel=0.01)  # 100000 * 8 / 1_000_000
    assert bandwidth["eth0"]["mbps_recv"] == pytest.approx(0.8, rel=0.01)


def test_calculate_bandwidth_zero_interval():
    """Test bandwidth calculation with zero interval."""
    previous_net = {"eth0": {"bytes_sent": 1000000, "bytes_recv": 2000000}}
    current_net = {"eth0": {"bytes_sent": 1500000, "bytes_recv": 2500000}}

    bandwidth = network.calculate_bandwidth(previous_net, current_net, 0)

    assert bandwidth == {}


def test_calculate_bandwidth_none_values():
    """Test bandwidth calculation with None values."""
    bandwidth = network.calculate_bandwidth(None, None, 5.0)

    assert bandwidth == {}
