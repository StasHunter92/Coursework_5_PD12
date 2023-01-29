from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import Optional

from application.models.classes import UnitClass
from application.models.equipment import Weapon, Armor


# ----------------------------------------------------------------------------------------------------------------------
# Create abstract unit class
class BaseUnit(ABC):
    """
    Base unit class
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        Initialize Unit class using UnitClass properties
        """
        self.name: str = name
        self.unit_class: UnitClass = unit_class
        self._hp: float = unit_class.max_health
        self._stamina: float = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used: bool = False

    @property
    def hp(self) -> float:
        """
        Getter for HP of the unit

        :return: Unit HP
        """
        return round(self._hp, 1)

    @hp.setter
    def hp(self, value: float) -> None:
        """
        Setter for HP of the unit

        :param value: HP value
        :return: None
        """
        self._hp: float = value

    @property
    def stamina(self) -> float:
        """
        Getter for Stamina of the unit

        :return: Unit Stamina
        """
        return round(self._stamina, 1)

    @stamina.setter
    def stamina(self, value: float) -> None:
        """
        Setter for Stamina of the unit

        :param value: Stamina value
        :return: None
        """
        self._stamina: float = value

    def equip_weapon(self, weapon: Weapon) -> str:
        """
        Equip weapon for Unit

        :param weapon: Unit weapon
        :return: Weapon equipped successfully
        """
        self.weapon: Weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor) -> str:
        """
        Equip armor for Unit

        :param armor: Unit armor
        :return: Armor equipped successfully
        """
        self.armor: Armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        """
        Calculates the damage dealt by the attacking unit to the target unit

        :param target: The unit that is being attacked
        :return: The damage dealt by the attacking unit to the target unit
        """
        attack_damage: float = random.uniform(self.weapon.min_damage, self.weapon.max_damage) * self.unit_class.attack
        target_defense: float = target.armor.defence * target.unit_class.armor

        if target_defense < attack_damage:
            if target.stamina > target.armor.stamina_per_turn:
                damage: float = attack_damage - target_defense
                target.stamina -= self.armor.stamina_per_turn
            else:
                damage: float = attack_damage
            damage: float = round(damage, 1)
            self.stamina -= self.weapon.stamina_per_hit
            target.get_damage(damage)
        else:
            damage: float = 0.0

        return damage

    def get_damage(self, damage: float) -> Optional[float]:
        """
        Update HP after the damage

        :param damage: Input damage
        :return: New HP or None
        """
        if damage > 0:
            self.hp: float = self.hp - damage
            return self.hp
        return None

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        This method will be overriden below
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        Use the skill of the unit

        :param target: The target of the skill
        :return: A message indicating if the skill was used or not
        """
        if self._is_skill_used:
            return f"Навык использован"
        else:
            self._is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)


# ----------------------------------------------------------------------------------------------------------------------
# Create unit classes
class PlayerUnit(BaseUnit):
    """
    A player unit class
    """

    def hit(self, target: BaseUnit) -> str:
        """
        Hits the target unit with weapon and calculates damage based on target's armor

        :param target: Target unit to hit
        :return: Message indicating result of the hit
        """
        if self.stamina > self.weapon.stamina_per_hit:
            damage: float = self._count_damage(target)

            if damage == 0.0:
                return f"{self.name} используя {self.weapon.name} наносит удар, " \
                       f"но {target.armor.name} противника его останавливает."
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} противника и " \
                   f"наносит {damage} урона."
        return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."


class EnemyUnit(BaseUnit):
    """
    An enemy unit class
    """

    def hit(self, target: BaseUnit) -> str:
        """
        Hits the target unit with weapon and/or skill and calculates damage based on target's armor

        :param target: Target unit to hit
        :return: Message indicating result of the hit
        """
        if not self._is_skill_used and self.stamina >= self.unit_class.skill.stamina and random.randint(0, 100) < 10:
            return self.use_skill(target)

        if self.stamina > self.weapon.stamina_per_hit:
            damage: float = self._count_damage(target)

            if damage == 0.0:
                return f"{self.name} используя {self.weapon.name} наносит удар, " \
                       f"но {target.armor.name} противника его останавливает."
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} противника и " \
                   f"наносит {damage} урона."
        return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
