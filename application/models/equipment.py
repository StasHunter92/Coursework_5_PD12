from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    name: str
    defence: float
    stamina_per_turn: float

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Weapon:
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    class Meta:
        unknown = marshmallow.EXCLUDE

    @property
    def damage(self) -> float:
        return uniform(self.min_damage, self.max_damage)


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Weapon:
        """
        Return weapon object filtered by name
        :param weapon_name: name of the weapon
        :return: weapon object
        """
        return next(filter(lambda weapon: weapon.name == weapon_name, self.equipment.weapons))
        # for weapon in self.equipment.weapons:
        #     if weapon.name == weapon_name:
        #         return weapon

    def get_armor(self, armor_name: str) -> Armor:
        """
        Return armor object filtered by name
        :param armor_name: name of the armor
        :return: armor object
        """
        return next(filter(lambda armor: armor.name == armor_name, self.equipment.armors))

    def get_weapons_names(self) -> list:
        """
        Generate list of weapon names
        :return: List of weapon names
        """
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> list:
        """
        Generate list of armor names
        :return: List of armor names
        """
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        with open("././application/data/equipment.json", encoding="utf-8") as equipment_file:
            data = json.load(equipment_file)
            equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
