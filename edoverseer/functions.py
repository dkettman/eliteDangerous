import inspect
import json
import logging
from pathlib import Path

import requests

from edoverseer import classes


def to_camel(string: str) -> str:
    """

    :param string:
    :return:
    """
    return "".join(word.capitalize() for word in string.split("_"))


def load_config():
    logging.debug(f"Entered: {inspect.stack()[0][3]}")
    with open("config.json") as fp:
        cfg = json.load(fp)
    for entry in cfg["eddb_data"].values():
        update_remote_data(entry)

    if cfg["log_path"] == "":
        cfg['log_path'] = Path(
            f'{Path.home()}/Saved Games/Frontier Developments/Elite Dangerous'
        ).expanduser()

    cfg['lookups'] = dict()

    cfg['lookups']['module'] = {
        x.get("ed_symbol").lower(): x for x in cfg["eddb_data"]["modules"]["data"]
    }

    cfg['lookups']['commodity'] = {
        x.get("name"): x for x in cfg["eddb_data"]["commodities"]["data"]
    }

    return cfg


def lookup_module(module: str):
    return classes.config['lookups']['module'][module]


def lookup_commodity(commodity: str):
    return classes.config['lookups']['commodity'][commodity]


def update_remote_data(src_dict: dict):
    valid_remote_types = ["online", "local"]
    if src_dict["type"] == "online":
        logging.debug(f'Getting Online Data for: {src_dict}')
        src_dict["data"] = requests.get(src_dict["location"]).json()
    elif src_dict["type"] == "local":
        logging.debug(f'Getting Local Data for: {src_dict}')
        with open(src_dict["location"]) as fp:
            src_dict["data"] = json.load(fp)
    else:
        raise NotImplementedError(f"Remote Data type not implemented! Valid types are: {valid_remote_types}")
