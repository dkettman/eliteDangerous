import inspect
import json
import logging
from pathlib import Path
from typing import List, Optional

import requests
from pydantic import BaseModel, Field


def to_camel(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


def load_config():
    logging.debug(f"Entered: {inspect.stack()[0][3]}")
    with open("config.json") as fp:
        cfg = json.load(fp)
    for entry in cfg["eddb_data"].values():
        update_remote_data(entry)

    if cfg["log_path"] == "":
        cfg['log_path'] = Path(
            "~\\Saved Games\\Frontier Developments\\Elite Dangerous"
        ).expanduser()

    return cfg


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


def lookup_module(module: str):
    module_lookup = {
        x.get("ed_symbol").lower(): x for x in config["eddb_data"]["modules"]["data"]
    }
    return module_lookup[module.lower()]


def lookup_commodities(commodity: str):
    module_lookup = {
        x.get("name"): x for x in config["eddb_data"]["commodities"]["data"]
    }
    return module_lookup[commodity]


logging.basicConfig(level=logging.DEBUG)

config = load_config()
logging.debug(f"Log Path: {config['log_path']}")


class BaseEvent(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

    @property
    def display_name(self):
        raise NotImplementedError


class Cargo(BaseEvent):
    name: str
    name_localised: str = Field(None, alias="Name_Localised")
    count: int
    stolen: bool
    mission_id: Optional[int]

    @property
    def display_name(self):
        return self.name_localised or self.name.capitalize()


class Module(BaseEvent):
    item: str
    on: bool
    priority: Optional[int]
    slot: str
    ammo_in_clip: Optional[int]
    ammo_in_hopper: Optional[int]
    health: int
    engineering: Optional[dict]

    @property
    def display_name(self):
        raise NotImplementedError


class Ship(BaseEvent):
    ship: Optional[str]
    ship_localised: Optional[str]
    ship_name: Optional[str]
    ship_ident: Optional[str]
    fuel_capacity: Optional[dict]
    fuel_level: Optional[float]
    inventory: Optional[List[Cargo]] = []
    status: Optional[dict]
    modules: Optional[List[Module]] = []
    pips: Optional[List[int]]

    @property
    def display_name(self):
        raise NotImplementedError


class Overseer(BaseEvent):
    commander: Optional[str]
    credits: Optional[int]
    ship: Ship = Ship()

    def display_name(self):
        return self.commander


Overseer.update_forward_refs()
