'''
Este módulo gerencia as Condições do Personagem.
'''

from datetime import datetime
from random import choice, random
from typing import Iterable, Iterator, List, Tuple, Type, Union

from bson import ObjectId
from constant.text import TEXT_DELIMITER, TEXT_SEPARATOR_2
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram.conditions.barrier import BarrierCondition
from rpgram.conditions.condition import Condition
from rpgram.conditions.debuff import DEBUFFS, DebuffCondition
from rpgram.conditions.factory import condition_factory
from rpgram.conditions.special_damage_skill import SpecialDamageSkillCondition
from rpgram.enums.debuff import (
    BREAKABLE_IMMOBILIZED_DEBUFFS_NAMES,
    IMMOBILIZED_DEBUFFS_NAMES
)
from rpgram.constants.text import STATUS_EMOJI_TEXT
from rpgram.enums.turn import TurnEnum
from rpgram.skills.special_damage import SpecialDamage


class Status:

    def __init__(self, conditions: List[Condition] = []):
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

        self.__conditions = conditions

        self.__update_stats()

    def add_condition(self, new_condition: Condition) -> dict:
        if not isinstance(new_condition, Condition):
            raise TypeError(
                f'O parâmetro deve ser do tipo Condition. '
                f'Tipo: {type(new_condition)}.'
            )

        emoji_name = new_condition.emoji_name
        report = {'condition_name': new_condition.name}
        if new_condition in self.__conditions:
            new_condition_turn = new_condition.turn
            new_condition_level = new_condition.level
            index = self.__conditions.index(new_condition)
            current_condition = self.__conditions[index]
            current_condition.set_turn(new_condition_turn)
            current_condition.add_level(new_condition_level)
            current_condition_level = current_condition.level
            report['text'] = (
                f'O nível de {emoji_name} foi aumentado '
                f'para {current_condition_level}.'
            )
        else:
            self.__conditions.append(new_condition)
            barrier_value = ''
            if isinstance(new_condition, BarrierCondition):
                barrier_value = f' ({new_condition.barrier_points})'
            report['text'] = (
                f'{emoji_name} NV: {new_condition.level} foi adicionado'
                f'{barrier_value}.'
            )
        self.__update_stats()

        return report

    add = add_condition

    def add_condition_by_ratio(
        self,
        *condition_ratio_tuple: Tuple[dict]
    ) -> dict:
        '''Testa se o personagem irá receber a condição vinda de 
        SpecialDamage.condition_list
        Tupla de dicionários de condições e respectivos ratios de acerto.
        condition = {
            'condition': functools.partial(Condition, level),
            'ratio': float
        }
        '''

        report = {'text': '', 'effective': False}
        for condition_ratio in condition_ratio_tuple:
            condition_class = condition_ratio['condition']
            ratio = condition_ratio['ratio']
            resist_score = random()
            # test
            if resist_score < ratio:
                report_text = self.add_condition(condition_class())['text']
                report['text'] += f'{report_text}\n'
                report['effective'] = True

        report['text'] = report['text'].rstrip()

        return report

    add_by_ratio = add_condition_by_ratio

    def remove_condition(
        self,
        condition: Union[Condition, str],
        ignore_not_find: bool = False
    ) -> dict:
        if not isinstance(condition, (Condition, str)):
            raise TypeError(
                f'O parâmetro deve ser do tipo Condition ou String. '
                f'Tipo: {type(condition)}.'
            )

        if isinstance(condition, Condition):
            condition_name = condition.emoji_name
            condition_level = condition.level
        elif isinstance(condition, str):
            condition_name = condition
            condition_level = 1

        report = {'text': '', 'condition_name': condition_name}
        if condition in self.__conditions:
            index = self.__conditions.index(condition)
            new_condition = self.__conditions[index]
            condition_emoji_name = new_condition.emoji_name
            new_condition = new_condition.remove_level(condition_level)
            if not new_condition:
                report['text'] = f'{condition_emoji_name} foi removido.'
                self.__conditions.pop(index)
            else:
                new_condition_level = new_condition.level
                report['text'] = (
                    f'{condition_emoji_name} reduziu para NV: '
                    f'{new_condition_level}.'
                )
        elif ignore_not_find is False:
            report['text'] = (
                f'O status não possui a condição "{condition_name}".'
            )
        self.__update_stats()

        return report

    remove = remove_condition

    def remove_conditions(
        self,
        *conditions: Union[Condition, str]
    ) -> List[dict]:
        report_list = []
        unique_conditions = sorted(set(conditions))

        ignore_not_find = False
        if len(unique_conditions) > 1:
            ignore_not_find = True

        for condition_name in unique_conditions:
            condition_level = conditions.count(condition_name)
            condition = condition_factory(
                name=condition_name,
                level=condition_level
            )
            report = self.remove_condition(
                condition=condition,
                ignore_not_find=ignore_not_find
            )
            if report['text']:
                report_list.append(report)

        if not report_list:
            report_list.append({'text': 'Nenhuma condição foi removida!'})

        return report_list

    def remove_random_debuff_conditions(self, quantity: int) -> dict:
        if quantity < 1:
            raise ValueError(
                f'quaintity deve ser igual ou maior que 1. ({quantity})'
            )

        report = {'text': ''}
        status_debuff_condition_list = [
            condition
            for condition in self.__conditions
            if isinstance(condition, DebuffCondition)
        ]
        if status_debuff_condition_list:
            debuff_condition_list = [
                choice(status_debuff_condition_list) for _ in range(quantity)
            ]
            report_list = self.remove_conditions(*debuff_condition_list)
            report_text = '\n'.join([report['text'] for report in report_list])
            report['text'] = report_text

        return report

    def remove_broken_barrier(self):
        self.__conditions = [
            condition
            for condition in self.__conditions
            if not isinstance(condition, BarrierCondition) or
            not condition.is_broken
        ]

    def broken_all_barriers(self) -> dict:
        total_damage = 0
        report = {'text': '', 'total_damage': total_damage}
        for condition in self.__conditions:
            if isinstance(condition, BarrierCondition):
                damage = condition.current_barrier_points
                report['total_damage'] += damage
                barrier_report = condition.damage_barrier_points(damage)
                report['text'] += barrier_report['text'] + '\n'

        report['text'] = report['text'].strip()
        self.remove_broken_barrier()
        return report

    def set_conditions(self, *conditions: Union[Condition, str]) -> List[dict]:
        report_list = []
        for condition in conditions:
            if condition in self.__conditions:
                self.__conditions.remove(condition)
            report = self.add_condition(condition)
            report_list.append(report)

        return report_list

    def get_filtered_condition(
        self,
        *filters: Tuple[Type[Condition]]
    ) -> Iterable:
        for condition in self.__conditions:
            if any(isinstance(condition, filter) for filter in filters):
                yield condition

    def get_debuffs(self) -> Iterable:
        yield from self.get_filtered_condition(DebuffCondition)

    def get_barriers(self) -> Iterable:
        yield from self.get_filtered_condition(BarrierCondition)

    def clean_status(self) -> dict:
        condition_names = ', '.join(
            [condition.emoji_name for condition in self.__conditions]
        )
        self.__conditions = []
        self.__update_stats()

        return {
            'text': (
                f'Todas as condições foram removidas.\n'
                f'Condições: {condition_names}'
            )
        }

    clean = clean_status

    def add_barrier_damage(self, damage: int) -> List[dict]:
        damage = int(abs(damage))
        report = {'text': '', 'remaining_damage': damage, 'damage': damage}
        for condition in self.__conditions:
            if isinstance(condition, BarrierCondition) and damage > 0:
                damage_report = condition.damage_barrier_points(damage)
                damage = damage_report['remaining_damage']
                report['remaining_damage'] = damage_report['remaining_damage']
                report['text'] += damage_report['text'] + '\n'

        self.remove_broken_barrier()

        return report

    def activate(self, char) -> List[dict]:
        reports = []
        for condition in self.__conditions:
            if condition.frequency != TurnEnum.CONTINUOUS:
                report = condition.activate(char)
                report['is_debuff'] = isinstance(condition, DebuffCondition)
                if condition.turn == 0:
                    if report['text']:
                        report['text'] += '\n'
                    report['text'] += (
                        f'Condição "{condition.emoji_name}"'
                        f'foi removida do Status.'
                    )
                reports.append(report)

        # exclui todos as condition com turn igual a zero
        self.__conditions = [
            condition
            for condition in self.__conditions
            if condition.turn != 0
        ]

        return reports

    def break_conditions(self) -> List[dict]:
        reports = []
        for condition in self.__conditions:
            if condition in BREAKABLE_IMMOBILIZED_DEBUFFS_NAMES:
                condition_ratio = 0.50 + (condition.level / 100)
                break_score = random()
                if break_score > condition_ratio:
                    report = self.remove_condition(condition=condition)
                    reports.append(report)

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

    def to_list(self) -> List[str]:
        return [condition.name for condition in self.__conditions]

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = ''
        if not self.__conditions:
            text = 'Normal'
        elif verbose:
            text += f'{TEXT_SEPARATOR_2}\n'.join(
                f'*Nome*: {condition.emoji_name} (Nv: {condition.level})\n'
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
            condition_args=[
                condition.to_dict()
                for condition in self.__conditions
            ],
        )

    @property
    def total_level(self) -> int:
        return sum(condition.level for condition in self.__conditions)

    @property
    def total_level_debuff(self) -> int:
        return sum(
            condition.level
            for condition in self.__conditions
            if isinstance(condition, DebuffCondition)
        )

    # Getters
    @property
    def is_empty(self) -> bool:
        return not bool(self.__conditions)

    @property
    def debuffed(self) -> bool:
        for condition in self.__conditions:
            if isinstance(condition, DebuffCondition):
                return True

        return False

    @property
    def debuffs_text(self) -> str:
        return ', '.join([
            condition.full_name
            for condition in self.__conditions
            if isinstance(condition, DebuffCondition)
        ]) or 'Normal'

    @property
    def show_barrier_points(self) -> str:
        current_bp = 0
        max_bp = 0
        for condition in self.__conditions:
            if isinstance(condition, BarrierCondition):
                current_bp += max(0, condition.current_barrier_points)
                max_bp += condition.barrier_points

        return f'{current_bp}/{max_bp}'

    @property
    def special_damage_iter(self) -> Iterator[SpecialDamage]:
        for condition in self.__conditions:
            if isinstance(condition, SpecialDamageSkillCondition):
                yield from condition.special_damage_iter

    conditions = property(lambda self: self.__conditions)
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
        conditions=[
            Condition(
                name='Poison',
                frequency='CONTINUOUS',
            ),
            Condition(
                name='Burn',
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
