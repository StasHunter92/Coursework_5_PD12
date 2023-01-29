from dataclasses import dataclass
from typing import List
from random import uniform
import json

import marshmallow_dataclass
import marshmallow


# ----------------------------------------------------------------------------------------------------------------------
# Create dataclasses for equipment
@dataclass
class Armor:
    """
    Class representing the properties of an armor \n
    name: The name of the armor \n
    defence: The defense value of the armor \n
    stamina_per_turn: The amount of stamina consumed by the armor per turn
    """
    name: str
    defence: float
    stamina_per_turn: float

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Weapon:
    """
    Class representing the properties of a weapon \n
    name: The name of the weapon \n
    min_damage: The minimum damage value of the weapon \n
    max_damage: The maximum damage value of the weapon \n
    stamina_per_hit: The amount of stamina consumed by the weapon per hit
    """
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    class Meta:
        unknown = marshmallow.EXCLUDE

    @property
    def damage(self) -> float:
        """
        Get damage value for the weapon as a random value between min_damage and max_damage

        :return: Random value"""
        return uniform(self.min_damage, self.max_damage)


@dataclass
class EquipmentData:
    """
    Class representing the data of the unit's equipment \n

    weapons: A list of the weapons in the unit's inventory \n
    armors: A list of the armors in the unit's inventory
    """
    weapons: List[Weapon]
    armors: List[Armor]


# ----------------------------------------------------------------------------------------------------------------------
# Create equipment class
class Equipment:
    """
    Class for handling equipment
    """

    def __init__(self):
        self.equipment: EquipmentData = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Weapon:
        """
        Return weapon object filtered by name

        :param weapon_name: Name of the weapon
        :return: Weapon object
        """
        return next(filter(lambda weapon: weapon.name == weapon_name, self.equipment.weapons))

    def get_armor(self, armor_name: str) -> Armor:
        """
        Return armor object filtered by name

        :param armor_name: Name of the armor
        :return: Armor object
        """
        return next(filter(lambda armor: armor.name == armor_name, self.equipment.armors))

    def get_weapons_names(self) -> list:
        """
        Get list of weapon names

        :return: List of weapon names
        """
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> list:
        """
        Get list of armor names

        :return: List of armor names
        """
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData | ValueError:
        """
        Load equipment data from json file

        :return: EquipmentData object or ValueError
        """
        with open("././application/data/equipment.json", encoding="utf-8") as equipment_file:
            data = json.load(equipment_file)
            equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError("Invalid equipment data")
