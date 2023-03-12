import sys
import logging
from typing import Tuple, Dict

from schema import schema

from cerberus import Validator
from yaml import load as load_yaml, SafeLoader


class SafeLineLoader(SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super(SafeLineLoader, self).construct_mapping(node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping['__line__'] = node.start_mark.line + 1
        return mapping


def split_config(config: dict) -> Tuple[dict, dict]:
    # The meta key is named like this because "/meta" is not a valid network destination.

    if not isinstance(config, dict):
        logging.critical("Config should be key value pairs at root level, quiting...")
        sys.exit()

    meta_config = {"/meta": config.get("/meta", {})}
    if "/meta" in config:
        del config["/meta"]
    return meta_config, config


def parse_errors(errors, line_numbers: dict, r=0) -> str:
    # for e in errors:
    #     print("\t" * r, ">>>", e.document_path, e.field)
    #     if e.child_errors:
    #         parse_errors(e.child_errors, line_numbers, r=r+1)
    return errors


def validate_config(config: dict, line_numbers: dict) -> Dict[dict, dict]:
    validator = Validator(schema)
    is_valid = validator.validate(config)
    if not is_valid:
        # TODO: print better errors, and possibly continue running if only one host has errors
        logging.exception(
            "Errors in config file:"
            f"\n\n{parse_errors(validator.document_error_tree, line_numbers)}\n\n"
            "quiting..."
        )
        sys.exit()

    logging.debug("Config file validation check passed")
    return validator.document


def load_config(path: str) -> Dict[dict, dict]:
    logging.info(f"Loading config from '{path}'")

    try:
        with open(path) as file:
            yaml = file.read()
    except FileNotFoundError:
        logging.critical("Config file does not exist, quiting...")
        sys.exit()

    meta_config, host_config = split_config(load_yaml(yaml, SafeLoader))
    if not host_config:  # there's really no point having a filled meta_config if there are no hosts declared
        logging.critical("Config file is empty, quiting...")
        sys.exit()
    config = {
        "meta_config": meta_config,
        "host_config": host_config,
    }

    # For error reporting
    line_numbers = load_yaml(yaml, SafeLineLoader)

    return validate_config(config, line_numbers)


if __name__ == "__main__":
    from pathlib import Path
    from pprint import pprint

    testing_config = str((Path(__file__).parent / "../local/config.yml").resolve())
    pprint(load_config(testing_config))
    # load_config(testing_config)
