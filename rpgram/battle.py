'''
Classe responsável por gerenciar a Batalha
'''
from copy import deepcopy
from datetime import datetime
from operator import attrgetter
from typing import List, Union

from bson import ObjectId

from rpgram.characters import BaseCharacter
from rpgram.errors import CurrentPlayerTurnError


class Battle:
    def __init__(
        self,
        blue_team: List[BaseCharacter],
        red_team: List[BaseCharacter],
        turn_count: int = 1,
        current_player: BaseCharacter = None,
        started: bool = False,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ) -> None:
        if isinstance(blue_team, BaseCharacter):
            blue_team = [blue_team]
        if isinstance(red_team, BaseCharacter):
            red_team = [red_team]
        if isinstance(_id, str):
            _id = ObjectId(_id)

        self.__blue_team = blue_team
        self.__red_team = red_team
        self.__turn_count = int(turn_count)
        self.__turn_order = []
        self.started = started
        self.__id = _id
        self.__created_at = created_at
        self.__updated_at = updated_at
        self.__populate_turn_order(current_player)

    def __populate_turn_order(
        self,
        current_player: BaseCharacter = None
    ) -> None:
        ''' Função que irá montar a order dos jogadores somente quando a 
        classe for instanciada.
        '''
        self.__turn_order = self.__blue_team + self.__red_team

        self.reorder_turn()

        # Se foi passado um current_player ao instanciar a batalha,
        # ele será colocado como o primeiro elemento da lista
        if current_player:
            for _ in range(len(self.__turn_order)):
                if self.current_player == current_player:
                    break
                self.skip_player()

        # Caso o jogador que está na primerira posição da lista (jogador atual)
        # não esteja vivo, a vez será passada para o próximo jogador
        if self.current_player.is_dead():
            self.pass_turn()

    def reorder_turn(self):
        '''Ordena os jogadores pela iniciativa'''
        self.__turn_order.sort(
            key=attrgetter('combat_stats.initiative'),
            reverse=True
        )

    def enter_battle(
        self, player: BaseCharacter, team: str, reorder: bool = False
    ) -> None:
        if player in self.turn_order:
            raise ValueError(
                f'O jogador "{player.name}" já está na batalha.'
            )
        if team in ['blue', 'azul']:
            self.__blue_team.append(player)
        elif team in ['red', 'vermelho']:
            self.__red_team.append(player)
        else:
            raise ValueError(f'"{team}" não é um time inválido.')

        if reorder or not self.started:
            self.reorder_turn()

    def skip_player(self):
        self.__turn_order.append(self.__turn_order.pop(0))

    def pass_turn(self):
        for _ in range(len(self.__turn_order)):
            self.skip_player()
            if self.current_player.is_alive():
                break

    def next_turn(self) -> None:
        self.__turn_count += 1
        self.pass_turn()

    def action(
        self, character: BaseCharacter = None,
        action: str = 'attack', target: str = 'self',
        char_dice: int = 1, target_dice: int = 1,
    ) -> None:
        if not self.started:
            self.started = True

        if not character:
            character = self.current_player

        if character != self.current_player:
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
        damage = int(total_deff - total_atk)
        damage = min(damage, 0)
        target.combat_stats.hp = damage
        report = (
            f'Ação: {action} = atk: {atk} ({total_atk}) - '
            f'def: {deff} ({total_deff}) = {abs(damage)}\n'

            f'{attacker.name} causou {abs(damage)} de dano em {target.name}.'
        )

        return report

    def get_winner(self) -> str:
        blue_team_alive = any([char.is_alive() for char in self.__blue_team])
        red_team_alive = any([char.is_alive() for char in self.__red_team])
        winner = None

        if not blue_team_alive and not red_team_alive:
            winner = 'EMPATE'
        elif blue_team_alive and not red_team_alive:
            winner = 'BLUE'
        elif red_team_alive and not blue_team_alive:
            winner = 'RED'
        return winner

    # Getters
    @property
    def blue_team(self) -> List[BaseCharacter]:
        return deepcopy(self.__blue_team)

    @property
    def red_team(self) -> List[BaseCharacter]:
        return deepcopy(self.__red_team)

    @property
    def turn_count(self) -> int:
        return self.__turn_count

    @property
    def turn_order(self) -> List[BaseCharacter]:
        return deepcopy(self.__turn_order)

    @property
    def current_player(self) -> BaseCharacter:
        return self.__turn_order[0]

    _id: ObjectId = property(lambda self: self.__id)

    def to_dict(self) -> dict:
        return dict(
            blue_team=[char._id for char in self.__blue_team],
            red_team=[char._id for char in self.__red_team],
            turn_count=self.turn_count,
            current_player=self.current_player._id,
            started=self.started,
            _id=self.__id,
            created_at=self.__created_at,
            updated_at=self.__updated_at,
        )

    def get_teams_sheet(self) -> str:
        blue_team = "\n".join([
            (f"    {i+1}: {char.name} "
            f'HP: {char.cs.current_hit_points}/{char.cs.hit_points}')
            for i, char in enumerate(self.__blue_team)
        ])
        red_team = "\n".join([
            (f"    {i+1}: {char.name} "
            f'HP: {char.cs.current_hit_points}/{char.cs.hit_points}')
            for i, char in enumerate(self.__red_team)
        ])
        return (
            f'TIME AZUL:\n'
            f'{blue_team}\n\n'
            f'TIME VERMELHO:\n'
            f'{red_team}'
        )

    def get_sheet(self) -> str:
        turn_order = "\n".join([
            f"    {i+1}: {char.name}"
            for i, char in enumerate(self.turn_order)
        ])
        return (
            f'Turno: {self.turn_count}\n'
            f'Ordem de Jogadores:\n'
            f'{turn_order}'
        )

    def get_sheets(self) -> str:
        return self.get_sheet()

    def __repr__(self) -> str:
        return self.get_sheet()


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
        red_team=[gandalf],
        current_player=gandalf
    )
    print(f'Turno: {battle.turn_count}')
    print(battle.turn_order)
    report = battle.action(action='magical_attack', target='enemy 1')
    print(report)
    print(f'O vencedor é o time "{battle.get_winner()}"\n')

    print(f'Turno: {battle.turn_count}')
    print(battle.turn_order)
    report = battle.action(action='precision_attack', target='enemy 0')
    print(report)
    print(f'O vencedor é o time "{battle.get_winner()}"\n')

    print(f'Turno: {battle.turn_count}')
    print(battle.turn_order)
    report = battle.action(action='physical_attack', target='enemy 0')
    print(report)
    print(f'O vencedor é o time "{battle.get_winner()}"\n')

    print(f'Turno: {battle.turn_count}')
    print(battle.turn_order)
    print(f'O vencedor é o time "{battle.get_winner()}"\n')
