import sys
import logging
from time import sleep
from pathlib import Path
from typing import Callable

from config import Config
from check_methods import *

import colorlog  # TODO: add color logs
from jsonschema import Draft202012Validator, ValidationError

PROJECT_ROOT = Path(__file__).parent.resolve()
# TODO: implement cli to remove hard coded variables
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
LOG_DATE_FORMAT = "%a %d-%b-%Y %H:%M:%S"
CONFIG_FILE_PATH = PROJECT_ROOT / "duas.conf.json"
PUSH_LOOP_INTERVAL = 30

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("duas.log", "a"),
    ]
)


def host_is_alive(params: dict) -> bool:
    dispatch_map = {
        "ping": ping,
        "http": http,
        "https": https,
        # TODO: implement heartbeat
    }
    location = params.get("location")
    for check_method, method_params in params.items():
        if check_method == "location":  # location is not a check method, rather a parameter to check methods
            continue

        method_is_alive = dispatch_map[check_method]
        if method_is_alive(location, method_params):
            logging.info(f"method '{check_method}' is up!")
            return True
        logging.info(f"method '{check_method}' is down, checking via next method...")
    return False


def push_loop(config: dict, shutdown_callback: Callable) -> None:
    while True:
        for host, params in config.items():
            logging.info(f"Checking '{host}'")
            if host_is_alive(params):
                sleep(PUSH_LOOP_INTERVAL)
                break
        shutdown_callback()


def shutdown():
    logging.info("Shutting down...")
    sys.exit(0)  # TODO: temporary, replace with actual shutdown command later


def main():
    logging.info("-" * 20, " Session start ", "-" * 20)
    config = Config(CONFIG_FILE_PATH).config
    push_loop(config, shutdown)


if __name__ == "__main__":
    main()
