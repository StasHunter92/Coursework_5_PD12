from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.models.unit import BaseUnit


# ----------------------------------------------------------------------------------------------------------------------
# Create abstract skill class
class Skill(ABC):
    """
    Abstract base class for skills
    """
    user = None
    target = None

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get the name of the skill

        :return: Name of the skill
        """
        pass

    @property
    @abstractmethod
    def stamina(self) -> float:
        """
        Get the stamina cost of using the skill

        :return: Stamina cost of using the skill
        """
        pass

    @property
    @abstractmethod
    def damage(self) -> float:
        """
        Get the damage caused by the skill

        :return: Damage caused by the skill
        """
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        """
        Get the effect of using the skill

        :return: Effect of using the skill
        """
        pass

    def _is_stamina_enough(self) -> bool:
        """
        Check if user has enough stamina to use the skill

        :return: True if user has enough stamina, False otherwise
        """
        return self.user.stamina >= self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Use the skill

        :param user: The user of the skill
        :param target: The target of the skill
        :return: Result of using the skill
        """
        self.user = user
        self.target = target

        if self._is_stamina_enough:
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name}, но у него не хватило выносливости."


# ----------------------------------------------------------------------------------------------------------------------
# Create skills
class FuryPunch(Skill):
    name: str = "Свирепый пинок"
    stamina: float = 6.0
    damage: float = 12.0

    def skill_effect(self):
        self.user.stamina -= self.stamina
        self.target.hp -= self.damage
        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона."


class HardShot(Skill):
    name: str = "Мощный укол"
    stamina: float = 5.0
    damage: float = 15.0

    def skill_effect(self):
        self.user.stamina -= self.stamina
        self.target.hp -= self.damage
        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона."


class FireballShot(Skill):
    name: str = "Метеоритный удар"
    stamina: float = 15.0
    damage: float = 30.0

    def skill_effect(self):
        self.user.stamina -= self.stamina
        self.target.hp -= self.damage
        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона."
