from typing import List, Optional, Type
from pydantic import BaseModel, Field

from edsession import ed_enums


def to_camel(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


class BaseEvent(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class Cargo(BaseEvent):
    name: str
    name_localised: str = Field(None, alias='Name_Localised')
    count: int
    stolen: bool
    mission_id: Optional[int]


class Module(BaseEvent):
    item: str
    on: bool
    priority: Optional[int]
    slot: str
    ammo_in_clip: Optional[int]
    ammo_in_hopper: Optional[int]
    health: int


class Ship(BaseEvent):
    ship: Optional[str]
    ship_localised: str = Field(None, alias='Ship_Localised')
    ship_name: Optional[str]
    ship_ident: Optional[str]
    fuel_capacity: Optional[dict]
    fuel_level: Optional[float]
    inventory: Optional[List[Cargo]] = []
    status: Optional[dict]
    modules: Optional[List[Module]] = Field(default_factory=list)
    pips: Optional[List[int]]

    def update_journal_loadgame(self, entry):
        self.ship = entry["Ship"]
        self.ship_localised = entry["Ship_Localised"]
        self.ship_name = entry["ShipName"]
        self.ship_ident = entry["ShipIdent"]


class Session(BaseEvent):
    commander: Optional[str]
    credits: Optional[int]
    ship: Ship = Field(default_factory=Ship)

    def update_journal_loadgame(self,entry):
        self.commander = entry["Commander"]
        self.credits = entry["Credits"]
        self.ship.update_journal_loadgame(entry)


