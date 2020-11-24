import logging
import pprint
from typing import List, Optional

from pydantic import BaseModel, Field

import edoverseer.functions as edfuncs


config = edfuncs.load_config()
logging.basicConfig(level=logging.DEBUG)
logging.debug(f"Log Path: {config['log_path']}")


class BaseEvent(BaseModel):
    class Config:
        alias_generator = edfuncs.to_camel
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
    name: str
    on: bool
    priority: Optional[int]
    slot: str
    class_: int
    rating: str
    ammo_in_clip: Optional[int]
    ammo_in_hopper: Optional[int]
    health: float
    engineering: Optional[dict]

    class Config:
        fields = {
            'class_': 'class'
        }

    @property
    def display_name(self):
        raise self.name.capitalize()


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

    def update_modules(self, modules: dict):
        new_modules = list()
        ignore_slots = ['ShipCockpit', 'CargoHatch', 'PaintJob', 'Decal1', 'Decal2', 'Decal3', 'VesselVoice']
        for m in modules:
            if m['Slot'] not in ignore_slots:
                lookup = edfuncs.lookup_module(m['Item'])
                mod = {**m, **lookup, 'name': lookup['group']['name']}
                new_modules.append(Module.parse_obj(mod))
                pprint.pprint(mod)
        self.modules = new_modules


class Overseer(BaseEvent):
    commander: Optional[str]
    credits: Optional[int]
    ship: Ship = Ship()

    def display_name(self):
        return self.commander


Overseer.update_forward_refs()
