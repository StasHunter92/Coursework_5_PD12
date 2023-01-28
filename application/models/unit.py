from __future__ import annotations

import random
from abc import ABC, abstractmethod

from application.models.classes import UnitClass
from application.models.equipment import Weapon, Armor

from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self._hp = unit_class.max_health
        self._stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

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
        Setter for Stamina of the unit
        :param value: HP value
        :return: None
        """
        self._hp = value

    @property
    def stamina(self) -> float:
        """Getter for Stamina of the unit"""
        return round(self._stamina, 1)

    @stamina.setter
    def stamina(self, value: float) -> None:
        """Setter for Stamina of the unit"""
        self._stamina = value

    def equip_weapon(self, weapon: Weapon) -> str:
        """Equip weapon for Unit"""
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor) -> str:
        """Equip armor for Unit"""
        self.armor = armor
        return f"{self.name} экипирован броней {self.weapon.name}"

    def _count_damage(self, target: BaseUnit) -> int:

        attack_damage = random.uniform(self.weapon.min_damage, self.weapon.max_damage) * self.unit_class.attack
        target_defense = target.armor.defence * target.unit_class.armor
        if target_defense < attack_damage:
            if target.stamina > target.armor.stamina_per_turn:
                damage = attack_damage - target_defense
                target.stamina -= self.armor.stamina_per_turn
            else:
                damage = attack_damage
            damage = round(damage, 1)
            self.stamina -= self.weapon.stamina_per_hit
            target.get_damage(damage)
        else:
            damage = 0

        return damage

    def get_damage(self, damage: int) -> Optional[float]:
        """
        Update HP after the damage
        :param damage: Input damage
        :return: New HP or None
        """
        if damage > 0:
            self.hp = self.hp - damage
            return self.hp
        return None

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if self._is_skill_used:
            return f"Навык использован"
        else:
            self._is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        if self.stamina > self.weapon.stamina_per_hit:
            damage = self._count_damage(target)
            if damage == 0:
                return f"{self.name} используя {self.weapon.name} наносит удар, " \
                       f"но {target.armor.name} cоперника его останавливает."
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и " \
                   f"наносит {damage} урона."
        return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """
        if not self._is_skill_used and self.stamina >= self.unit_class.skill.stamina and random.randint(0, 100) < 10:
            return self.use_skill(target)

        if self.stamina > self.weapon.stamina_per_hit:
            damage = self._count_damage(target)
            if damage == 0:
                return f"{self.name} используя {self.weapon.name} наносит удар, " \
                       f"но {target.armor.name} cоперника его останавливает."
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и " \
                   f"наносит {damage} урона."
        return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
