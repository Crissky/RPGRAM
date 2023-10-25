from datetime import datetime
from typing import List, Union

from bson import ObjectId
from constant.text import TEXT_DELIMITER, TEXT_SEPARATOR_2
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram.boosters.condition import Condition
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

    def add_condition(self, condition: Condition) -> dict:
        if not isinstance(condition, Condition):
            raise TypeError(
                f'O parâmetro deve ser do tipo Condition. '
                f'Tipo: {type(condition)}.'
            )

        report = {}
        name = condition.name
        if condition in self.__conditions:
            index = self.__conditions.index(condition)
            condition = self.__conditions[index]
            condition.add_level()
            level = condition.level
            report['text'] = (
                f'O nível da Condição "{name}" foi aumentado para {level}.'
            )
        else:
            self.__conditions.append(condition)
            report['text'] = f'A Condição "{name}" foi adicionada.'
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
            name = condition.name
        elif isinstance(condition, str):
            name = condition

        report = {}
        if condition in self.__conditions:
            index = self.__conditions.index(condition)
            new_condition = self.__conditions[index]
            new_condition = new_condition.remove_level()
            if not new_condition:
                report['text'] = f'A Condição "{name}" foi removida.'
                self.__conditions.pop(index)
            else:
                level = new_condition.level
                report['text'] = (
                    f'O nível da Condição "{name}" foi reduzido para {level}.'
                )
        else:
            raise ValueError(f'O status não possui a condição "{name}".')
        self.__update_stats()

        return report

    remove = remove_condition

    def activate(self, char) -> List[dict]:
        reports = []
        for condition in self.__conditions:
            if condition.frequency != TurnEnum.CONTINUOUS:
                report = condition.activate(char)
                reports.append(report)

        # exclui todos as condition con turn igual a zero
        self.__conditions = [
            condition
            for condition in self.__conditions
            if condition.turn != 0
        ]

        return reports

    def battle_activate(self, char) -> List[dict]:
        reports = []
        for condition in self.__conditions:
            if condition.frequency != TurnEnum.CONTINUOUS:
                report = condition.battle_activate(char)
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
                f'*Nome*: {condition.name}\n'
                f'*Descrição*: {condition.description}\n'
                for condition in self.__conditions
            )
        else:
            text += '/'.join(
                condition.name
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
            condition_ids=[
                dict(
                    _id=condition._id,
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
                function='print("function:Poison")',
                battle_function='print("battle_function:Poison")',
                frequency='CONTINUOUS',
            ),
            Condition(
                name='Burn',
                description='Tá pegando fogo',
                function='print("function:Burn")',
                battle_function='print("battle_function:Burn")',
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
