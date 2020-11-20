from typing import List, Optional

from pydantic import BaseModel, Field, validator, root_validator


def to_camel(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


class BaseEvent(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

    @root_validator
    def replace_name_with_localised(cls, values):
        name_loc = values.get('name_localised')
        if not name_loc:
            # values['name'] = values['name'].capitalize()
            values['name'].capitalize()
        else:
            values['name'] = name_loc
        return values


class Cargo(BaseEvent):
    name: str
    name_localised: str = Field(None, alias='Name_Localised')
    count: int
    stolen: bool
    mission_id: Optional[int]


data1 = {'name': 'gold', 'count': 3, 'stolen': False}
data2 = {'name': 'iondrive', 'name_localised': 'Ion Drive', 'count': 3, 'stolen': False}


class Module(BaseEvent):
    item: str
    on: bool
    priority: Optional[int]
    slot: str
    ammo_in_clip: Optional[int]
    ammo_in_hopper: Optional[int]
    health: int
    engineering: Optional[dict]


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


class Overseer(BaseEvent):
    commander: Optional[str]
    credits: Optional[int]
    ship: Ship = Ship()


Overseer.update_forward_refs()
