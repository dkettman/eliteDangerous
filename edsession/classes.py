from typing import List, Optional, Type
from pydantic import BaseModel


def to_camel(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


class BaseEvent(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class Session(BaseEvent):
    commander: str = None
    credits: int = 0
    ship: "Ship" = None


class Cargo(BaseEvent):
    name: str
    name_localised: str = None
    count: int
    stolen: bool
    mission_id: int = None


class Ship(BaseEvent):
    ship: str = None
    ship_localised: str = None
    ship_name: str = None
    ship_ident: str = None
    fuel_capacity: float = None
    fuel_level: float = None
    inventory: Optional[List[Type[Cargo]]] = []


Session.update_forward_refs()


# s = Session(
#     commander="Me",
#     credits=100,
#     ship=Ship.parse_raw(
#         """{ "timestamp":"2020-11-12T14:16:11Z", "event":"LoadGame", "FID":"F4640506", "Commander":"Watch_Me_Be_Meh", "Horizons":true, "Ship":"DiamondBackXL", "Ship_Localised":"Diamondback Explorer", "ShipID":9, "ShipName":"HIPPITY HOP", "ShipIdent":"BOING", "FuelLevel":39.973835, "FuelCapacity":40.000000, "GameMode":"Solo", "Credits":281233277, "Loan":0 }"""
#     ),
# )
