from dataclasses import dataclass

from application.models.skills import Skill, FuryPunch, HardShot, FireballShot


# ----------------------------------------------------------------------------------------------------------------------
# Create dataclass for units
@dataclass
class UnitClass:
    """
    Class representing the properties of a game unit \n
    name: The name of the unit \n
    max_health: The maximum health value for the unit \n
    max_stamina: The maximum stamina value for the unit \n
    attack: The attack modifier value for the unit \n
    stamina: The stamina modifier value for the unit \n
    armor: The armor modifier value for the unit \n
    skill: The skill object associated with the unit
    """
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill
    image: str


# ----------------------------------------------------------------------------------------------------------------------
# Create unit classes for game
WarriorClass: UnitClass = UnitClass(name="Воин",
                                    max_health=60,
                                    max_stamina=30,
                                    attack=0.8,
                                    stamina=0.9,
                                    armor=1.2,
                                    skill=FuryPunch(),
                                    image="../static/warrior.png")

ThiefClass: UnitClass = UnitClass(name="Вор",
                                  max_health=50,
                                  max_stamina=25,
                                  attack=1.5,
                                  stamina=1.2,
                                  armor=1,
                                  skill=HardShot(),
                                  image="../static/assassin.png")

MageClass: UnitClass = UnitClass(name="Маг",
                                 max_health=30,
                                 max_stamina=50,
                                 attack=2,
                                 stamina=1.5,
                                 armor=0.8,
                                 skill=FireballShot(),
                                 image="../static/mage.png")
# ----------------------------------------------------------------------------------------------------------------------
# Create dict with classes names for HTML page
unit_classes: dict = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass,
    MageClass.name: MageClass
}
