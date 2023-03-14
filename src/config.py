import sys
import json
import logging
from typing import Union
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError


class Config:
    PROJECT_ROOT = Path(__file__).parent.resolve()
    SCHEMA_PATH = PROJECT_ROOT / "schema.json"

    def __init__(self, path: Union[str, Path] = None):
        if not isinstance(path, Path):
            path = Path(path or self.PROJECT_ROOT / "duas.conf.json").resolve()

        logging.info(f"Loading config from '{path}'")

        self.config: dict = self.__read_json(path)
        self.schema: dict = self.__read_json(self.SCHEMA_PATH)

        self.__validate_config()

        logging.info("Loaded config, no errors detected.")

    @staticmethod
    def __read_json(path: Path):
        try:
            with open(path) as json_file:
                parsed_json = json.load(json_file)
            return parsed_json
        except FileNotFoundError:
            logging.critical(f"{path.name} not found, quiting...")
            sys.exit(1)
        except OSError:
            logging.critical(f"OS error while reading {path.name}, quiting...", exc_info=True)
            sys.exit(1)
        except json.JSONDecodeError:
            logging.critical(f"Error decoding {path.name}, quiting...", exc_info=True)
            sys.exit(1)

    def __validate_config(self):
        validator = Draft202012Validator(self.schema)
        fixed_config = self.config.copy()
        for err in validator.iter_errors(self.config):
            err: ValidationError
            logging.warning(f"Error in config at '{'.'.join(err.absolute_path)}' >>  {err.message}")

            # Delete erroneous node from config
            if (key := err.absolute_path[0]) in fixed_config:
                logging.warning(f"Deleting '{key}' from config...")
                del fixed_config[key]

        # Check again with deleted nodes, i.e., nodes that had errors have been removed
        if not validator.is_valid(fixed_config):
            logging.critical("Non recoverable errors in config, quiting...")
            sys.exit(1)

        if not fixed_config.keys():
            logging.warning("No hosts to check, empty config file!")
            sys.exit(0)

        self.config = fixed_config
