import logging
from typing import List, Optional

from pydantic import BaseModel, Field

import edoverseer.functions as edfuncs

config = edfuncs.load_config()
logging.basicConfig(level=logging.DEBUG)
logging.debug(f"Log Path: {config['log_path']}")


class BasicModel(BaseModel):
    class Config:
        alias_generator = edfuncs.to_camel
        allow_population_by_field_name = True

    @property
    def display_name(self):
        raise NotImplementedError


class Item(BasicModel):
    name: str
    name_localised: str = Field(None, alias="Name_Localised")
    count: int

    @property
    def display_name(self):
        return self.name_localised or self.name.capitalize()


class Cargo(Item):
    stolen: bool
    mission_id: Optional[int]


class RawMaterial(Item):
    def __repr__(self):
        return f'RawMaterial: {self.display_name}'

    def __str__(self):
        return self.__repr__()


class EncodedMaterial(Item):
    def __repr__(self):
        return f'EncodedMaterial: {self.display_name}'

    def __str__(self):
        return self.__repr__()


class ManufacturedMaterial(Item):
    def __repr__(self):
        return f'ManufacturedMaterial: {self.display_name}'

    def __str__(self):
        return self.__repr__()


class MaterialHold(BasicModel):
    raw: List[RawMaterial] = Field(default_generator=list)
    encoded: List[EncodedMaterial] = Field(default_generator=list)
    manufactured: List[ManufacturedMaterial] = Field(default_generator=list)

    @property
    def display_name(self):
        return f'MaterialHold(Raw: {len(self.raw)},Encoded: {len(self.encoded)}, Manufactured: {len(self.manufactured)}'


class Module(BasicModel):
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
        fields = {"class_": "class"}

    @property
    def display_name(self):
        raise self.name.capitalize()


class Ship(BasicModel):
    ship: Optional[str]
    ship_localised: Optional[str]
    ship_name: Optional[str]
    ship_ident: Optional[str]
    fuel_capacity: Optional[dict]
    fuel_level: Optional[float]
    inventory: Optional[List[Cargo]] = []
    status: Optional[dict]
    modules: Optional[List[Module]] = []
    materials: Optional[List[Material]] = []
    pips: Optional[List[int]]

    @property
    def display_name(self):
        return f'{self.ship_name} [{self.ship_ident}]'

    @property
    def display_materials_by_type(self) -> dict:
        ret = {}
        for t in self.get_material_types():
            ret[t] = []
            for m in self.get_materials_of_type(t):
                ret[t].append(m)
        return ret

    def get_material_types(self) -> list:
        types = set()
        for m in self.materials:
            types.add(m.type)
        return list(types)

    def get_materials_of_type(self, t: str) -> list:
        return [x for x in self.materials if x.type == t.lower()]

    def update_modules(self, modules: dict):
        new_modules = list()
        ignore_slots = [
            "ShipCockpit",
            "CargoHatch",
            "PaintJob",
            "Decal1",
            "Decal2",
            "Decal3",
            "VesselVoice",
        ]
        for m in modules:
            if m["Slot"] not in ignore_slots:
                lookup = edfuncs.lookup_module(m["Item"])
                mod = {**m, **lookup, "name": lookup["group"]["name"]}
                new_modules.append(Module.parse_obj(mod))
        self.modules = new_modules

    def update_materials(self, materials: dict):
        new_materials = list()
        material_types = ["Raw", "Manufactured", "Encoded"]
        for mt in material_types:
            for m in materials[mt]:
                m["type"] = mt.lower()
                new_materials.append(Material.parse_obj(m))
        self.materials = new_materials


class Overseer(BasicModel):
    commander: Optional[str]
    credits: Optional[int]
    ship: Ship = Ship()

    def display_name(self):
        return self.commander


Overseer.update_forward_refs()
