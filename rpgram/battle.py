from copy import deepcopy
from operator import attrgetter
from typing import List

from rpgram.characters import BaseCharacter
from rpgram.errors import CurrentPlayerTurnError


class Battle:
    def __init__(
        self,
        blue_team: List[BaseCharacter],
        red_team: List[BaseCharacter]
    ) -> None:
        self.__blue_team = blue_team
        self.__red_team = red_team
        self.__turn_count = 0
        self.__turn_order = []
        self.populate_turn_order()

    def populate_turn_order(self) -> None:
        self.__turn_order = self.__blue_team + self.__red_team
        self.__turn_order.sort(
            key=attrgetter('combat_stats.initiative'),
            reverse=True
        )

    def next_turn(self) -> None:
        self.__turn_count += 1
        self.__turn_order.append(self.__turn_order.pop(0))

    def action(
        self,
        character: BaseCharacter,
        action: str = 'attack',
        target: str = 'self',
        char_dice: int = 1,
        target_dice: int = 1,
    ) -> None:
        current_player_turn = self.current_player_turn
        if character != current_player_turn:
            raise CurrentPlayerTurnError(
                f'Não é o turno de "{character.name}".'
            )

        target_char = self.get_target(character, target)

        # Executando Ação
        if action in ['physical_attack', 'precision_attack', 'magical_attack']:
            report = self.basic_attack(
                character, target_char, action, char_dice, target_dice
            )

        self.next_turn()

        return report

    def get_target(self, character: BaseCharacter, target: str) -> BaseCharacter:
        if target == 'self':
            target = character
        else:
            team_name, team_index = target.split()
            team_index = int(team_index)
            if team_name == 'blue':
                target = self.__blue_team[team_index]
            elif team_name == 'red':
                target = self.__red_team[team_index]
            elif team_name == 'ally':
                if character in self.__blue_team:
                    target = self.__blue_team[team_index]
                else:
                    target = self.__red_team[team_index]
            elif team_name == 'enemy':
                if character in self.__blue_team:
                    target = self.__red_team[team_index]
                else:
                    target = self.__blue_team[team_index]

        return target

    def basic_attack(
        self,
        attacker: BaseCharacter,
        target: BaseCharacter,
        action: str,
        char_dice: int,
        target_dice: int,
    ) -> str:
        if action == 'physical_attack':
            atk = attacker.combat_stats.physical_attack
            deff = target.combat_stats.physical_defense
        elif action == 'precision_attack':
            atk = attacker.combat_stats.precision_attack
            deff = target.combat_stats.physical_defense
        elif action == 'magical_attack':
            atk = attacker.combat_stats.magical_attack
            deff = target.combat_stats.magical_defense

        total_atk = atk * (1 + (char_dice * 0.05))
        total_deff = deff * (1 + (target_dice * 0.05))
        damage = int((total_deff * 0.5) - total_atk)
        damage = min(damage, 0)
        target.combat_stats.hp = damage
        report = (
            f'Ação: {action} = atk: {atk} ({total_atk}) - def: {deff} ({total_deff}) = {abs(damage)}\n'
            f'{attacker.name} causou {abs(damage)} de dano em '
            f'{target.name}.\n'
        )

        print(report)
        return report

    # Getters
    @property
    def ally_team(self) -> List[BaseCharacter]:
        return deepcopy(self.__blue_team)

    @property
    def enemy_team(self) -> List[BaseCharacter]:
        return deepcopy(self.__red_team)

    @property
    def turn_count(self) -> int:
        return self.__turn_count

    @property
    def turn_order(self) -> List[BaseCharacter]:
        return deepcopy(self.__turn_order)

    @property
    def current_player_turn(self) -> BaseCharacter:
        return self.__turn_order[0]


if __name__ == '__main__':
    from rpgram.boosters import Classe, Race
    frodo = BaseCharacter(
        char_name='Frodo',
        classe=Classe('Ladino'),
        race=Race('Hobbit'),
        base_dexterity=2,
        base_constitution=1
    )
    gandalf = BaseCharacter(
        char_name='Gandalf',
        classe=Classe('Mago'),
        race=Race('Humano'),
        base_intelligence=3,
    )
    aragorn = BaseCharacter(
        char_name='Aragorn',
        classe=Classe('Guerreiro'),
        race=Race('Humano'),
        base_strength=3,
    )
    battle = Battle(
        blue_team=[aragorn, frodo],
        red_team=[gandalf]
    )
    print(battle.turn_order)
    current_player_turn = battle.current_player_turn
    battle.action(current_player_turn, 'precision_attack', 'enemy 0')

    print(battle.turn_order)
    current_player_turn = battle.current_player_turn
    battle.action(current_player_turn, 'physical_attack', 'enemy 0')

    print(battle.turn_order)
    current_player_turn = battle.current_player_turn
    battle.action(current_player_turn, 'magical_attack', 'enemy 1')

    print(battle.turn_order)
