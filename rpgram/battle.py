'''
Classe responsável por gerenciar a Batalha
'''
from copy import deepcopy
from datetime import datetime
from operator import attrgetter
from typing import List, Union

from bson import ObjectId

from rpgram import Dice
from rpgram.characters import BaseCharacter
from rpgram.errors import (
    BattleIsNotOverError,
    CurrentPlayerTurnError,
    EmptyTeamError
)
import random

ACTION_LIST = ['physical_attack', 'precision_attack', 'magical_attack']
REACTION_LIST = ['defend', 'dodge']


class Battle:
    def __init__(
        self,
        blue_team: Union[BaseCharacter, List[BaseCharacter]],
        red_team: Union[BaseCharacter, List[BaseCharacter]],
        chat_id: int,
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
        self.__chat_id = chat_id
        self.__id = _id
        self.__created_at = created_at
        self.__updated_at = updated_at
        self.report = {}
        self.__populate_turn_order(current_player)

    def __populate_turn_order(
        self,
        current_player: BaseCharacter = None
    ) -> None:
        ''' Função que irá montar a order dos jogadores somente quando a 
        classe for instanciada.
        '''
        for char in (self.__blue_team + self.__red_team):
            if char not in self.__turn_order:
                self.__turn_order.append(char)

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
        if player in self.__turn_order:
            raise ValueError(
                f'O jogador "{player.name}" já está na batalha.'
            )
        if team in ['blue', 'azul']:
            self.__blue_team.append(player)
        elif team in ['red', 'vermelho']:
            self.__red_team.append(player)
        else:
            raise ValueError(f'"{team}" não é um time inválido.')

        self.__turn_order.append(player)

        if reorder or not self.started:
            self.reorder_turn()

    def start_battle(self):
        if self.blue_team_empty():
            raise EmptyTeamError(
                'A batalha não pode começar porque a '
                'equipe azul está vazia.'
            )
        elif self.red_team_empty():
            raise EmptyTeamError(
                'A batalha não pode começar porque a '
                'equipe vermelha está vazia.'
            )
        self.started = True

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
        self, attacker_char: BaseCharacter = None,
        target: Union[str, BaseCharacter] = 'self',
        action: str = 'attack', reaction: str = 'defend',
        attacker_dice: Dice = None, target_dice: Dice = None,
    ) -> None:
        if not self.started:
            self.start_battle()

        # Definindo o atacante
        if not attacker_char or attacker_char == self.current_player:
            attacker_char = self.current_player
        if attacker_char != self.current_player:
            raise CurrentPlayerTurnError(
                f'Não é o turno de "{attacker_char.name}".'
            )

        # Definindo o alvo
        if isinstance(target, str):
            target_char = self.get_target(attacker_char, target)
        elif isinstance(target, BaseCharacter):
            index = self.__turn_order.index(target)
            target_char = self.__turn_order[index]
        else:
            raise TypeError(
                f'target não é um tipo válido.'
                f'Deve ser uma string ou um objeto do tipo BaseCharacter.'
                f'target fornecido: {target}.'
            )

        if attacker_dice is None:
            attacker_dice = Dice(1)
        if target_dice is None:
            target_dice = Dice(1)

        # Executando Ação
        if action in ACTION_LIST:
            report = self.basic_attack(
                attacker_char=attacker_char,
                target_char=target_char,
                action=action,
                reaction=reaction,
                attacker_dice=attacker_dice,
                target_dice=target_dice
            )
        else:
            raise ValueError(
                f'Ataque básico "{action}" não existe.'
                f'Use um dos seguintes valores: {ACTION_LIST}.'
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
        attacker_char: BaseCharacter,
        target_char: BaseCharacter,
        action: str,
        reaction: str,
        attacker_dice: Dice,
        target_dice: Dice,
    ) -> str:
        if action == 'physical_attack':
            atk = attacker_char.combat_stats.physical_attack
            _def = target_char.combat_stats.physical_defense
        elif action == 'precision_attack':
            atk = attacker_char.combat_stats.precision_attack
            _def = target_char.combat_stats.physical_defense
        elif action == 'magical_attack':
            atk = attacker_char.combat_stats.magical_attack
            _def = target_char.combat_stats.magical_defense
        else:
            raise ValueError(
                f'"{action}" não é uma ação válida. '
                f'Use uma das seguintes ações: "{ACTION_LIST}".'
            )

        hit = attacker_char.combat_stats.hit
        evasion = target_char.combat_stats.evasion

        attacker_dice.throw()
        target_dice.throw()

        total_atk = self.get_total_value(atk, attacker_dice)
        total_hit = self.get_total_value(hit, attacker_dice)
        total_def = self.get_total_value(_def, target_dice)
        total_evasion = self.get_total_value(evasion, target_dice)

        is_miss = False
        dodge_score = random.random()
        accuracy = self.get_accuracy(
            hit=total_hit,
            evasion=total_evasion,
            attacker_dice=attacker_dice,
            target_dice=target_dice
        )
        if reaction == 'dodge':
            if dodge_score >= accuracy:
                is_miss = True
                damage = 0
            else:
                damage = (_def // 2) - total_atk
        elif reaction == 'defend':
            damage = total_def - total_atk
        else:
            raise ValueError(
                f'"{reaction}" não é uma reação válida. '
                f'Use uma das seguintes reações: "{REACTION_LIST}".'
            )

        damage = min(damage, 0)
        damage = damage
        target_char.combat_stats.hp = damage

        self.report[self.turn_count] = {
            'attacker': attacker_char,
            'attacker_char': attacker_char,
            'attack': {
                'action': action,
                'accuracy': (accuracy * 100),
                'dice': attacker_dice.value,
                'is_critical': attacker_dice.is_critical,
                'atk': atk,
                'hit': hit,
                'total_atk': total_atk,
                'total_hit': total_hit,
            },
            'target': target_char,
            'target_char': target_char,
            'defense': {
                'reaction': reaction,
                'dodge_score': (dodge_score * 100),
                'dice': target_dice.value,
                'is_critical': target_dice.is_critical,
                'def': _def,
                'evasion': evasion,
                'total_def': total_def,
                'total_evasion': total_evasion,
                'damage': (damage * -1),
                'is_miss': is_miss
            },
        }

        return self.report[self.turn_count]

    def get_total_value(self, base_value: int, dice: Dice) -> int:
        multiplier = (1 + (dice.value * 0.025))
        boosted_value = int(base_value * multiplier)
        if (boosted_value - base_value) >= dice.value:
            result = boosted_value
        else:
            result = base_value + dice.value

        if dice.is_critical:
            result = result * 2

        return result

    def get_accuracy(
        self,
        hit: int,
        evasion: int,
        attacker_dice: Dice,
        target_dice: Dice
    ) -> float:
        accuracy = hit / evasion
        accuracy = min(accuracy, 1.0)
        dice_bonus = (attacker_dice.value - target_dice.value) / 100
        accuracy = accuracy + dice_bonus
        accuracy = min(accuracy, 1.0)
        accuracy = max(accuracy, 0.0)

        return accuracy

    def get_winner(self) -> str:
        blue_team_alive = any([char.is_alive() for char in self.__blue_team])
        red_team_alive = any([char.is_alive() for char in self.__red_team])
        winner = None

        if not blue_team_alive and not red_team_alive:
            winner = 'draw'
        elif blue_team_alive and not red_team_alive:
            winner = 'blue'
        elif red_team_alive and not blue_team_alive:
            winner = 'red'
        return winner

    def share_xp(self, multiplier: float = 1.0) -> dict:
        winner = self.get_winner()
        if not winner:
            raise BattleIsNotOverError(
                'Não é possível dividir XP em um combate não finalizado.'
            )

        blue_xp = int(sum([
            char.base_stats.level for char in self.__red_team
        ]) * 5 * multiplier // len(self.__blue_team)) + 10 + self.turn_count
        red_xp = int(sum([
            char.base_stats.level for char in self.__blue_team
        ]) * 5 * multiplier // len(self.__red_team)) + 10 + self.turn_count

        if winner == 'draw':
            blue_xp = blue_xp // 2
            red_xp = red_xp // 2
        elif winner == 'blue':
            red_xp = red_xp // 2
        elif winner == 'red':
            blue_xp = blue_xp // 2

        for char in self.__blue_team:
            char.base_stats.xp = blue_xp
        for char in self.__red_team:
            char.base_stats.xp = red_xp

        return {
            'blue': blue_xp,
            'red': red_xp
        }

    def in_battle(self, character: BaseCharacter) -> bool:
        return character in self.__turn_order

    def in_blue_team(self, character: BaseCharacter) -> bool:
        return character in self.__blue_team

    def in_red_team(self, character: BaseCharacter) -> bool:
        return character in self.__red_team

    def blue_team_empty(self) -> bool:
        return len(self.__blue_team) == 0

    def red_team_empty(self) -> bool:
        return len(self.__red_team) == 0

    in_blue = in_blue_team
    in_red = in_red_team
    blue_empty = blue_team_empty
    red_empty = red_team_empty

    def get_char_emojis(self, character: BaseCharacter) -> str:
        text = ''
        if self.in_blue_team(character):
            text = '🔵'
        elif self.in_red_team(character):
            text = '🔴'
        else:
            text = '🔘'

        if character.is_dead():
            text += '☠️'

        return text

    # Getters
    @property
    def blue_team(self) -> List[BaseCharacter]:
        return deepcopy(self.__blue_team)

    @property
    def red_team(self) -> List[BaseCharacter]:
        return deepcopy(self.__red_team)

    @property
    def chat_id(self) -> int:
        return self.__chat_id

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
            chat_id=self.chat_id,
            turn_count=self.turn_count,
            current_player=self.current_player._id,
            started=self.started,
            _id=self.__id,
            created_at=self.__created_at,
            updated_at=self.__updated_at,
        )

    def get_teams_sheet(self) -> str:
        blue_team = "\n".join([
            (
                f"    {self.get_char_emojis(char)}{i+1}: {char.name} "
                f'HP: {char.cs.show_hp}'
            )
            for i, char in enumerate(self.__blue_team)
        ])
        red_team = "\n".join([
            (
                f"    {self.get_char_emojis(char)}{i+1}: {char.name} "
                f'HP: {char.cs.show_hp}'
            )
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
            f"    {self.get_char_emojis(char)}{i+1}: {char.name} HP: {char.cs.show_hp}"
            for i, char in enumerate(self.__turn_order)
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

    def __eq__(self, other: 'Battle') -> bool:
        return self.__id == other.__id


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
        chat_id=-123456789,
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
