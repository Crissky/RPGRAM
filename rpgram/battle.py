from copy import deepcopy
from operator import attrgetter
from typing import List

from rpgram.characters import BaseCharacter


class Battle:
    def __init__(
        self,
        ally_team: List[BaseCharacter],
        enemy_team: List[BaseCharacter]
    ) -> None:
        self.__ally_team = ally_team
        self.__enemy_team = enemy_team
        self.__turn_count = 0
        self.__turn_order = []
        self.populate_turn_order()

    def populate_turn_order(self) -> None:
        self.__turn_order = self.__ally_team + self.__enemy_team
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
        target: str = 'self'
    ) -> None:
        current_turn = self.current_turn
        if character != current_turn:
            raise ValueError(f'Não é o turno de "{character.name}".')

        target = self.get_target(character, target)
        if action == 'attack':
            self.attack(character, target)

        self.next_turn()

    def get_target(self, character: BaseCharacter, target: str) -> BaseCharacter:
        if target == 'self':
            target = character
        else:
            team, index_team = target.split()
            index_team = int(index_team)

        if team == 'ally':
            if character in self.__ally_team:
                target = self.__ally_team[index_team]
            else:
                target = self.__enemy_team[index_team]
        elif team == 'enemy':
            if character in self.__ally_team:
                target = self.__enemy_team[index_team]
            else:
                target = self.__ally_team[index_team]

        return target

    def attack(self, attacker: BaseCharacter, target: BaseCharacter) -> None:
        atk = max((
            attacker.combat_stats.physical_attack,
            attacker.combat_stats.precision_attack
        ))
        deff = target.combat_stats.physical_defense
        damage = int((deff * 0.75) - atk)
        damage = min(damage, 0)
        target.combat_stats.hp = damage

    @property
    def ally_team(self) -> List[BaseCharacter]:
        return deepcopy(self.__ally_team)

    @property
    def enemy_team(self) -> List[BaseCharacter]:
        return deepcopy(self.__enemy_team)

    @property
    def turn_count(self) -> int:
        return self.__turn_count

    @property
    def turn_order(self) -> List[BaseCharacter]:
        return deepcopy(self.__turn_order)

    @property
    def current_turn(self) -> BaseCharacter:
        return deepcopy(self.__turn_order[0])


if __name__ == '__main__':
    from rpgram.boosters import Classe, Race
    char1 = BaseCharacter(
        char_name='Frodo',
        classe=Classe('Ladino'),
        race=Race('Hobbit'),
        base_strength=2,
        base_constitution=1
    )
    char2 = BaseCharacter(
        char_name='Gandalf',
        classe=Classe('Mago'),
        race=Race('Humano'),
        base_strength=2,
        base_constitution=1
    )
    battle = Battle(
        ally_team=[char1],
        enemy_team=[char2]
    )
    print(battle.turn_order)
    current_turn = battle.current_turn
    battle.action(current_turn, 'attack', 'enemy 0')
    print(battle.turn_order)
    # print(battle.current_turn)
