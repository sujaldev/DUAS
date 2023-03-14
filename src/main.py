import sys
import logging
import subprocess
from time import sleep
from typing import Callable

from cli import *
from config import Config
from check_methods import *

# import colorlog  # TODO: add color logs

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, "a"),
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
    return False


def push_loop(config: dict, shutdown_callback: Callable) -> None:
    running = True
    while running:
        running = False
        for host, params in config.items():
            logging.info(f"Checking '{host}'")
            if host_is_alive(params):
                sleep(INTERVAL)
                running = True
                break
    shutdown_callback()


def shutdown():
    logging.info("-" * 20 + " Shutting Down " + "-" * 20)
    if DRY_RUN:
        sys.exit(0)


def main():
    logging.info("-" * 20 + " Session start " + "-" * 20)
    config = Config(CONFIG_FILE).config
    push_loop(config, shutdown)


if __name__ == "__main__":
    main()
