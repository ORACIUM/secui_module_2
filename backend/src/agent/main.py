"""Main agent entry point for metric collection."""
import time
import logging
import argparse
import sys
from datetime import datetime
from typing import Dict, Any

from .config_loader import load_config, validate_config
from .formatter import format_metrics_cli, format_metrics_json
from .collectors import cpu, memory, disk, network


def setup_logging(config: Dict[str, Any]) -> logging.Logger:
    """
    Setup logging configuration.

    Args:
        config: Configuration dictionary

    Returns:
        Logger instance
    """
    log_level = getattr(logging, config['log_level'].upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(config['log_file'])
        ]
    )

    return logging.getLogger('agent')


def collect_all_metrics(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Collect all enabled metrics.

    Args:
        config: Configuration dictionary

    Returns:
        Dictionary containing all metrics with timestamp
    """
    metrics = {
        "timestamp": datetime.utcnow().isoformat(),
        "hostname": __import__('socket').gethostname(),
    }

    collectors_config = config.get('collectors', {})

    try:
        if collectors_config.get('cpu', True):
            metrics['cpu'] = cpu.collect_cpu_metrics()
            metrics['top_cpu_processes'] = cpu.get_top_cpu_processes(
                limit=config.get('top_processes_limit', 5)
            )
    except Exception as e:
        logging.error(f"Failed to collect CPU metrics: {e}")

    try:
        if collectors_config.get('memory', True):
            metrics['memory'] = memory.collect_memory_metrics()
            metrics['top_memory_processes'] = memory.get_memory_by_process(
                limit=config.get('top_processes_limit', 5)
            )
    except Exception as e:
        logging.error(f"Failed to collect memory metrics: {e}")

    try:
        if collectors_config.get('disk', True):
            metrics['disk'] = disk.collect_disk_metrics()
    except Exception as e:
        logging.error(f"Failed to collect disk metrics: {e}")

    try:
        if collectors_config.get('network', True):
            metrics['network'] = network.collect_network_metrics()
    except Exception as e:
        logging.error(f"Failed to collect network metrics: {e}")

    return metrics


def main():
    """Main entry point for the agent."""
    parser = argparse.ArgumentParser(description='System Resource Metrics Agent')
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    parser.add_argument(
        '--interval',
        type=int,
        help='Collection interval in seconds'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Collect metrics once and exit'
    )
    parser.add_argument(
        '--format',
        type=str,
        choices=['cli', 'json'],
        default='cli',
        help='Output format (cli or json)'
    )

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Override config with command-line arguments
    if args.interval:
        config['interval'] = args.interval

    # Validate configuration
    try:
        validate_config(config)
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    # Setup logging
    logger = setup_logging(config)

    logger.info("Starting System Resource Metrics Agent")
    logger.info(f"Configuration: interval={config['interval']}s")

    try:
        if args.once:
            # Collect metrics once and exit
            metrics = collect_all_metrics(config)

            if args.format == 'json':
                print(format_metrics_json(metrics))
            else:
                print(format_metrics_cli(metrics))

        else:
            # Continuous collection
            logger.info("Entering continuous collection mode. Press Ctrl+C to stop.")

            while True:
                metrics = collect_all_metrics(config)

                if args.format == 'json':
                    print(format_metrics_json(metrics))
                else:
                    print(format_metrics_cli(metrics))

                time.sleep(config['interval'])

    except KeyboardInterrupt:
        logger.info("Shutting down agent")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
