'''
Este módulo gerencia as Condições do Personagem.
'''

from datetime import datetime
from typing import List, Union

from bson import ObjectId
from constant.text import TEXT_DELIMITER, TEXT_SEPARATOR_2
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram.conditions.condition import Condition
from rpgram.conditions.factory import factory_condition
from rpgram.enums.debuff import IMMOBILIZED_DEBUFFS_NAMES
from rpgram.constants.text import STATUS_EMOJI_TEXT
from rpgram.enums.turn import TurnEnum


class Status:

    def __init__(
        self,
        player_id: int,
        conditions: List[Condition] = [],
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ) -> None:
        if isinstance(_id, str):
            _id = ObjectId(_id)
        if isinstance(conditions, list):
            for index, condition in enumerate(conditions):
                if not isinstance(condition, Condition):
                    raise TypeError(
                        f'Conditions deve ser uma lista de Conditions. '
                        f'Index: {index}, Tipo: {type(condition)}.'
                    )
        else:
            raise TypeError(
                f'Conditions deve ser uma lista de Conditions. '
                f'Tipo: {type(conditions)}.'
            )

        self.__observers = []

        self.__player_id = player_id
        self.__conditions = conditions
        self.__id = _id
        self.__created_at = created_at
        self.__updated_at = updated_at

        self.__update_stats()

    def add_condition(self, new_condition: Condition) -> dict:
        if not isinstance(new_condition, Condition):
            raise TypeError(
                f'O parâmetro deve ser do tipo Condition. '
                f'Tipo: {type(new_condition)}.'
            )

        report = {}
        name = new_condition.name
        if new_condition in self.__conditions:
            new_condition_turn = new_condition.turn
            new_condition_level = new_condition.level
            index = self.__conditions.index(new_condition)
            current_condition = self.__conditions[index]
            current_condition.set_turn(new_condition_turn)
            current_condition.add_level(new_condition_level)
            current_condition_level = current_condition.level
            report['text'] = (
                f'O nível da Condição "{name}" foi aumentado '
                f'para {current_condition_level}.'
            )
        else:
            self.__conditions.append(new_condition)
            report['text'] = (
                f'A Condição "{name} NV: {new_condition.level}" '
                f'foi adicionada.'
            )
        self.__update_stats()

        return report

    add = add_condition

    def remove_condition(self, condition: Union[Condition, str]) -> dict:
        if not isinstance(condition, (Condition, str)):
            raise TypeError(
                f'O parâmetro deve ser do tipo Condition ou String. '
                f'Tipo: {type(condition)}.'
            )

        if isinstance(condition, Condition):
            condition_name = condition.name
            condition_level = condition.level
        elif isinstance(condition, str):
            condition_name = condition
            condition_level = 1

        report = {}
        if condition in self.__conditions:
            index = self.__conditions.index(condition)
            new_condition = self.__conditions[index]
            new_condition = new_condition.remove_level(condition_level)
            if not new_condition:
                report['text'] = f'A Condição "{condition_name}" foi removida.'
                self.__conditions.pop(index)
            else:
                new_condition_level = new_condition.level
                report['text'] = (
                    f'O nível da Condição "{condition_name}" '
                    f'foi reduzido para {new_condition_level}.'
                )
        else:
            report['text'] = (
                f'O status não possui a condição "{condition_name}".'
            )
        self.__update_stats()

        return report

    remove = remove_condition

    def remove_conditions(
        self, *conditions: Union[Condition, str]
    ) -> List[dict]:
        report_list = []
        unique_conditions = sorted(set(conditions))
        for condition_name in unique_conditions:
            condition_level = conditions.count(condition_name)
            condition = factory_condition(
                name=condition_name,
                level=condition_level
            )
            report = self.remove_condition(condition)
            report_list.append(report)

        return report_list

    def activate(self, char) -> List[dict]:
        reports = []
        for condition in self.__conditions:
            if condition.frequency != TurnEnum.CONTINUOUS:
                report = condition.activate(char)
                if condition.turn == 0:
                    report['text'] += (
                        f'\n'
                        f'Condição "{condition.name}" foi removida do Status.'
                    )
                reports.append(report)

        # exclui todos as condition con turn igual a zero
        self.__conditions = [
            condition
            for condition in self.__conditions
            if condition.turn != 0
        ]

        return reports

    @property
    def immobilized(self) -> bool:
        return any(
            condition in IMMOBILIZED_DEBUFFS_NAMES
            for condition in self.__conditions
        )

    def immobilized_names(self) -> str:
        '''Retorna os nomes das condições imobilizantes que o personagem 
        possui. Caso não haja condições desse tipo, retorna uma exceção.'''
        names = []
        for condition in self.__conditions:
            if condition in IMMOBILIZED_DEBUFFS_NAMES:
                names.append(condition.full_name)

        if not names:
            raise ValueError('Status não tem condições imobilizadoras.')

        return ', '.join(names)

    def battle_activate(self, char) -> List[dict]:
        reports = []
        for condition in self.__conditions:
            if condition.frequency != TurnEnum.CONTINUOUS:
                report = condition.battle_activate(char)
                if condition.turn == 0:
                    report['text'] += (
                        f'\n'
                        f'Condição "{condition.name}" foi removida do Status.'
                    )
                reports.append(report)

        # exclui todos as condition con turn igual a zero
        self.__conditions = [
            condition
            for condition in self.__conditions
            if condition.turn != 0
        ]

        return reports

    def attach_observer(self, observer):
        self.__observers.append(observer)

    def detach_observer(self, observer):
        self.__observers.remove(observer)

    def notify_observers(self):
        for observer in self.__observers:
            observer.update()

    def __update_stats(self):
        self.__bonus_strength = 0
        self.__bonus_dexterity = 0
        self.__bonus_constitution = 0
        self.__bonus_intelligence = 0
        self.__bonus_wisdom = 0
        self.__bonus_charisma = 0

        self.__multiplier_strength = 1
        self.__multiplier_dexterity = 1
        self.__multiplier_constitution = 1
        self.__multiplier_intelligence = 1
        self.__multiplier_wisdom = 1
        self.__multiplier_charisma = 1

        self.__bonus_hit_points = 0
        self.__bonus_initiative = 0
        self.__bonus_physical_attack = 0
        self.__bonus_precision_attack = 0
        self.__bonus_magical_attack = 0
        self.__bonus_physical_defense = 0
        self.__bonus_magical_defense = 0
        self.__bonus_hit = 0
        self.__bonus_evasion = 0

        for c in self.conditions:
            self.__bonus_strength += int(c.bonus_strength)
            self.__bonus_dexterity += int(c.bonus_dexterity)
            self.__bonus_constitution += int(c.bonus_constitution)
            self.__bonus_intelligence += int(c.bonus_intelligence)
            self.__bonus_wisdom += int(c.bonus_wisdom)
            self.__bonus_charisma += int(c.bonus_charisma)

            self.__multiplier_strength += c.multiplier_strength - 1.0
            self.__multiplier_dexterity += c.multiplier_dexterity - 1.0
            self.__multiplier_constitution += c.multiplier_constitution - 1.0
            self.__multiplier_intelligence += c.multiplier_intelligence - 1.0
            self.__multiplier_wisdom += c.multiplier_wisdom - 1.0
            self.__multiplier_charisma += c.multiplier_charisma - 1.0

            self.__bonus_hit_points += int(c.bonus_hit_points)
            self.__bonus_initiative += int(c.bonus_initiative)
            self.__bonus_physical_attack += int(c.bonus_physical_attack)
            self.__bonus_precision_attack += int(c.bonus_precision_attack)
            self.__bonus_magical_attack += int(c.bonus_magical_attack)
            self.__bonus_physical_defense += int(c.bonus_physical_defense)
            self.__bonus_magical_defense += int(c.bonus_magical_defense)
            self.__bonus_hit += int(c.bonus_hit)
            self.__bonus_evasion += int(c.bonus_evasion)

        self.notify_observers()

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = ''
        if not self.__conditions:
            text = 'Normal'
        elif verbose:
            text += f'{TEXT_SEPARATOR_2}\n'.join(
                f'*Nome*: {condition.name} (Nv: {condition.level})\n'
                f'*Descrição*: {condition.description}\n'
                f'*Turno*: '
                f'{condition.turn if condition.turn > -1 else "Eterno"}\n'
                f'*Nível*: {condition.level}\n'
                for condition in self.__conditions
            )
        else:
            text += '/'.join(
                condition.full_name
                for condition in self.__conditions
            )

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return text

    def get_all_sheets(
        self, verbose: bool = False, markdown: bool = False
    ) -> str:
        text = f'*{STATUS_EMOJI_TEXT}*:'
        text += '\n' if verbose and self.__conditions else f' '

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)
        text += self.get_sheet(verbose=verbose, markdown=markdown)

        return text

    def __repr__(self) -> str:
        return (
            f'{TEXT_DELIMITER}\n'
            f'{self.get_sheet(True)}'
            f'{TEXT_DELIMITER}\n'
        )

    def to_dict(self):
        return dict(
            player_id=self.__player_id,
            condition_args=[
                dict(
                    name=condition.name,
                    turn=condition.turn,
                    level=condition.level,
                )
                for condition in self.__conditions
            ],
            _id=self.__id,
            created_at=self.__created_at,
            updated_at=self.__updated_at,
        )

    # Getters
    conditions = property(lambda self: self.__conditions)
    _id = property(lambda self: self.__id)
    bonus_strength = property(lambda self: self.__bonus_strength)
    bonus_dexterity = property(lambda self: self.__bonus_dexterity)
    bonus_constitution = property(lambda self: self.__bonus_constitution)
    bonus_intelligence = property(lambda self: self.__bonus_intelligence)
    bonus_wisdom = property(lambda self: self.__bonus_wisdom)
    bonus_charisma = property(lambda self: self.__bonus_charisma)
    multiplier_strength = property(lambda self: self.__multiplier_strength)
    multiplier_dexterity = property(lambda self: self.__multiplier_dexterity)
    multiplier_constitution = property(
        lambda self: self.__multiplier_constitution)
    multiplier_intelligence = property(
        lambda self: self.__multiplier_intelligence)
    multiplier_wisdom = property(lambda self: self.__multiplier_wisdom)
    multiplier_charisma = property(lambda self: self.__multiplier_charisma)
    bonus_hit_points = property(lambda self: self.__bonus_hit_points)
    bonus_initiative = property(lambda self: self.__bonus_initiative)
    bonus_physical_attack = property(lambda self: self.__bonus_physical_attack)
    bonus_precision_attack = property(
        lambda self: self.__bonus_precision_attack)
    bonus_magical_attack = property(lambda self: self.__bonus_magical_attack)
    bonus_physical_defense = property(
        lambda self: self.__bonus_physical_defense)
    bonus_magical_defense = property(lambda self: self.__bonus_magical_defense)
    bonus_hit = property(lambda self: self.__bonus_hit)
    bonus_evasion = property(lambda self: self.__bonus_evasion)


if __name__ == '__main__':
    status = Status(
        player_id='1',
        conditions=[],
    )
    print(status.get_sheet())
    print('#'*30)
    print(status.get_sheet(verbose=True))
    print('#'*30)
    print(status.get_all_sheets())
    print('#'*30)
    print(status.get_all_sheets(verbose=True))
    print('#'*30)
    status = Status(
        player_id='1',
        conditions=[
            Condition(
                name='Poison',
                description='Veneno venenoso',
                function='print("function:Poison");report={};',
                battle_function='print("battle_function:Poison");report={};',
                frequency='CONTINUOUS',
            ),
            Condition(
                name='Burn',
                description='Tá pegando fogo',
                function='print("function:Burn");report={};',
                battle_function='print("battle_function:Burn");report={};',
                frequency='CONTINUOUS',
            ),
        ],
    )
    print(status.get_sheet())
    print('#'*30)
    print(status.get_sheet(verbose=True))
    print('#'*30)
    print(status.get_all_sheets())
    print('#'*30)
    print(status.get_all_sheets(verbose=True))
