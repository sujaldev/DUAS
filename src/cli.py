import sys
import logging
import argparse
from pathlib import Path

__all__ = [
    "CONFIG_FILE", "LOG_FILE", "LOG_LEVEL", "LOG_FORMAT", "LOG_DATE_FORMAT", "INTERVAL"
]

parser = argparse.ArgumentParser(
    prog="duas",
    description="Signals an auto shutdown for a device connected to a dumb UPS by checking other network devices that "
                "shut down in case of a power outage"
)

PROJECT_ROOT = Path(__file__).parent.resolve()

parser.add_argument("-c", "--config", help="Path to the config file", default=PROJECT_ROOT / "duas.conf.json")
parser.add_argument("-l", "--log-file", help="Path to the log file", default=PROJECT_ROOT / "duas.log")
parser.add_argument("--log-level", help="Recommend level is INFO",
                    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="DEBUG")
parser.add_argument("-f", "--log-format", help="See python's logging module docs for help",
                    default="[%(asctime)s] [%(levelname)s] %(message)s")
parser.add_argument("-d", "--date-format", help="The date format in logs, see python's logging module docs for help",
                    default="%a %d-%b-%Y %H:%M:%S")
parser.add_argument("-i", "--interval", help="Amount of time to wait after a successful healthcheck.", default=30,
                    type=int)

args = parser.parse_args(sys.argv[1:])

CONFIG_FILE = args.config
LOG_FILE = args.log_file
LOG_LEVEL = logging.__dict__[args.log_level]
LOG_FORMAT = args.log_format
LOG_DATE_FORMAT = args.date_format
INTERVAL = args.interval
