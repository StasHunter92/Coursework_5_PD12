from typing import Optional, Tuple

from application.models.unit import BaseUnit


# ----------------------------------------------------------------------------------------------------------------------
# Create singleton class
class BaseSingleton(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


# ----------------------------------------------------------------------------------------------------------------------
# Create Arena class
class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND: int = 1
    player: BaseUnit = None
    enemy: BaseUnit = None
    game_is_running: bool = False
    battle_result: str = ""

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        """
        Set up player and enemy units and change game status

        :param player: Player instance
        :param enemy: Enemy instance
        :return: None
        """
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        """
        Determine the HP status of Player and Enemy and either end the game with the battle result
        or continue to the next turn

        :return: Battle result status or None
        """
        if self.player.hp > 0 and self.enemy.hp > 0:
            return None

        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = "Ничья."

        elif self.player.hp > 0 and self.enemy.hp <= 0:
            self.battle_result = "Игрок выиграл битву."

        elif self.enemy.hp > 0 and self.player.hp <= 0:
            self.battle_result = "Игрок проиграл битву."

        return self._end_game()

    def _end_game(self) -> str:
        """
        Reset the Singleton instance, update the game status, and return the outcome of the battle

        :return: Battle result
        """
        self._instances: dict = {}
        self.game_is_running = False
        return self.battle_result

    def _stamina_regeneration(self) -> None:
        """
        Recharge the stamina of both Player and Enemy every turn

        :return: None
        """
        units: Tuple[BaseUnit, BaseUnit] = (self.player, self.enemy)

        for unit in units:
            if unit.stamina + self.STAMINA_PER_ROUND > unit.unit_class.max_stamina:
                unit.stamina = unit.unit_class.max_stamina
            unit.stamina += self.STAMINA_PER_ROUND

    def next_turn(self) -> Optional[str]:
        """
        If both Player and Enemy are alive, perform the next turn, otherwise end the game

        :return: Battle result or turn result
        """
        result: Optional[str] = self._check_players_hp()

        if result:
            return result
        else:
            self._stamina_regeneration()
            return self.enemy.hit(self.player)

    def player_hit(self) -> str:
        """
        Make the Player hit the Enemy and return the result and next turn status

        :return: The result of the Player's hit and the next turn status as a string
        """
        result: Optional[str] = self._check_players_hp()
        if not result:
            result: str = self.player.hit(self.enemy)
            next_turn: Optional[str] = self.next_turn()
            return f"{result}\n{next_turn}"
        return result

    def player_use_skill(self) -> str:
        """
        Make the Player use skill on Enemy and return the result and next turn status

        :return: The result of the player's hit and the next turn status as a string
        """
        result: Optional[str] = self._check_players_hp()
        if not result:
            result: str = self.player.use_skill(self.enemy)
            next_turn: Optional[str] = self.next_turn()
            return f"{result}\n{next_turn}"
        return result
