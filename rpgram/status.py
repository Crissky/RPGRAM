'''
Este módulo gerencia as Condições do Personagem.
'''

from enum import Enum
from random import choice, random
from typing import Iterable, Iterator, List, Tuple, Type, Union

from constant.text import TEXT_DELIMITER, TEXT_SEPARATOR_2
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram.conditions.barrier import BarrierCondition
from rpgram.conditions.condition import Condition
from rpgram.conditions.debuff import DebuffCondition
from rpgram.conditions.factory import condition_factory
from rpgram.conditions.heal import HealingCondition
from rpgram.conditions.self_skill import SelfSkillCondition
from rpgram.conditions.special_damage_skill import SpecialDamageSkillCondition
from rpgram.conditions.target_skill_buff import TargetSkillBuffCondition
from rpgram.enums.debuff import (
    BREAKABLE_IMMOBILIZED_DEBUFFS_NAMES,
    CURSED_DEBUFFS_NAMES,
    IMMOBILIZED_DEBUFFS_NAMES,
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

    def add_condition(
        self,
        new_condition: Condition,
        notify: bool = True
    ) -> dict:
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

        if notify is True:
            self.notify_observers()

        return report

    add = add_condition

    def add_conditions_by_ratio(
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
                report_text = self.add_condition(
                    condition_class(),
                    notify=False
                )['text']
                report['text'] += f'{report_text}\n'
                report['effective'] = True

        report['text'] = report['text'].rstrip()
        self.notify_observers()

        return report

    add_by_ratio = add_conditions_by_ratio

    def remove_condition(
        self,
        condition: Union[Condition, str],
        ignore_not_find: bool = False,
        notify: bool = True
    ) -> dict:
        if not isinstance(condition, (Condition, str, Enum)):
            raise TypeError(
                f'O parâmetro deve ser do tipo Condition, String ou Enum. '
                f'Tipo: {type(condition)}.'
            )

        if isinstance(condition, Condition):
            condition_name = condition.emoji_name
            condition_level = condition.level
        elif isinstance(condition, str):
            condition_name = condition
            condition_level = 1
        elif isinstance(condition, Enum):
            condition_name = condition.name
            condition_level = 1

        report = {
            'text': '',
            'condition_name': condition_name,
            'is_fail': True
        }
        if condition in self.__conditions:
            index = self.__conditions.index(condition)
            new_condition = self.__conditions[index]
            condition_emoji_name = new_condition.emoji_name
            old_condition_level = new_condition.level
            new_condition = new_condition.remove_level(condition_level)
            report['is_fail'] = False
            if not new_condition:
                report['text'] = f'{condition_emoji_name} foi removido.'
                self.__conditions.pop(index)
            else:
                new_condition_level = new_condition.level
                report['text'] = (
                    f'{condition_emoji_name} reduziu Nível: '
                    f'{old_condition_level} ››› {new_condition_level} '
                    f'(-{condition_level})'
                )
        elif ignore_not_find is False:
            report['text'] = (
                f'O status não possui a condição "{condition_name}".'
            )

        if notify is True:
            self.notify_observers()

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
                ignore_not_find=ignore_not_find,
                notify=False
            )
            if report['text']:
                report_list.append(report)

        if not report_list:
            report_list.append({'text': 'Nenhuma condição foi removida!'})

        self.notify_observers()

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
        '''Adiciona ou substitui condições
        '''

        report_list = []
        for condition in conditions:
            if condition in self.__conditions:
                self.__conditions.remove(condition)
            report = self.add_condition(condition, notify=False)
            report_list.append(report)

        self.notify_observers()

        return report_list

    def set_powerful_conditions(
        self,
        *conditions: Union[Condition]
    ) -> List[dict]:
        '''Adiciona ou substitui as condições se forem mais poderosas
        '''

        report_list = []
        for condition in conditions:
            if condition in self.__conditions:
                new_turn = condition.turn
                index = self.__conditions.index(condition)
                current_condition = self.__conditions[index]
                self.__conditions.remove(condition)
                condition = (
                    condition
                    if condition.power >= current_condition.power
                    else current_condition
                )
                condition.set_turn(new_turn)
            report = self.add_condition(condition, notify=False)
            report_list.append(report)

        self.notify_observers()

        return report_list

    def get_filtered_condition(
        self,
        *filters: Tuple[Type[Condition]]
    ) -> Iterable[Condition]:
        for condition in self.__conditions:
            if any(isinstance(condition, filter) for filter in filters):
                yield condition

    def get_debuffs(self) -> Iterable[DebuffCondition]:
        yield from self.get_filtered_condition(DebuffCondition)

    def get_barriers(self) -> Iterable[BarrierCondition]:
        yield from self.get_filtered_condition(BarrierCondition)

    def get_condition(self, condition_name: str) -> Condition:
        for condition in self.__conditions:
            if condition == condition_name:
                return condition

    def cure_condition(self, condition: Union[str, Condition, Enum]) -> dict:
        if isinstance(condition, Condition):
            condition_name = condition.name
        elif isinstance(condition, str):
            condition_name = condition
        elif isinstance(condition, Enum):
            condition_name = condition.name

        condition = self.get_condition(condition)
        if condition:
            report = self.remove_condition(condition)
        else:
            report = {
                'text': f'O status não possui a condição "{condition_name}".',
                'condition_name': condition_name,
                'is_fail': True
            }

        return report

    def clean_status(self) -> dict:
        condition_names = ', '.join(
            [condition.emoji_name for condition in self.__conditions]
        )
        self.__conditions = []
        self.notify_observers()

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
                        f'Condição "{condition.emoji_name}" '
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

    @property
    def cursed(self) -> bool:
        return any(
            condition in CURSED_DEBUFFS_NAMES
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

    def cursed_names(self) -> str:
        '''Retorna os nomes das condições de maldição que o personagem 
        possui. Caso não haja condições desse tipo, retorna uma exceção.'''

        names = []
        for condition in self.__conditions:
            if condition in CURSED_DEBUFFS_NAMES:
                names.append(condition.full_name)

        if not names:
            raise ValueError('Status não tem condições imobilizadoras.')

        return ', '.join(names)

    def condition_type_order(self, condition: Condition) -> int:
        if isinstance(condition, BarrierCondition):
            return 1
        elif isinstance(condition, HealingCondition):
            return 2
        elif isinstance(condition, DebuffCondition):
            return 3
        elif isinstance(condition, SpecialDamageSkillCondition):
            return 4
        elif isinstance(condition, TargetSkillBuffCondition):
            return 5
        elif isinstance(condition, SelfSkillCondition):
            return 6

    def attach_observer(self, observer):
        self.__observers.append(observer)

    def detach_observer(self, observer):
        self.__observers.remove(observer)

    def notify_observers(self):
        for observer in self.__observers:
            observer.update()

    def get_attr_sum_from_conditions(self, attribute: str) -> int:
        value = sum([
            getattr(condition, attribute)
            for condition in self.conditions
        ])

        return int(value)

    def get_multiplier_sum_from_conditions(self, attribute: str) -> float:
        value = 1.0 + sum([
            getattr(condition, attribute) - 1.0
            for condition in self.conditions
        ])

        return max(value, 0.1)

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

    @property
    def conditions(self) -> List[Condition]:
        self.__conditions.sort(
            key=lambda c: (
                self.condition_type_order(c),
                c.name,
                -c.level,
            )
        )
        return self.__conditions

    @property
    def bonus_strength(self) -> int:
        return self.get_attr_sum_from_conditions('bonus_strength')

    @property
    def bonus_dexterity(self) -> int:
        return self.get_attr_sum_from_conditions('bonus_dexterity')

    @property
    def bonus_constitution(self) -> int:
        return self.get_attr_sum_from_conditions('bonus_constitution')

    @property
    def bonus_intelligence(self) -> int:
        return self.get_attr_sum_from_conditions('bonus_intelligence')

    @property
    def bonus_wisdom(self) -> int:
        return self.get_attr_sum_from_conditions('bonus_wisdom')

    @property
    def bonus_charisma(self) -> int:
        return self.get_attr_sum_from_conditions('bonus_charisma')

    @property
    def multiplier_strength(self) -> float:
        return self.get_multiplier_sum_from_conditions(
            'multiplier_strength'
        )

    @property
    def multiplier_dexterity(self) -> float:
        return self.get_multiplier_sum_from_conditions(
            'multiplier_dexterity'
        )

    @property
    def multiplier_constitution(self) -> float:
        return self.get_multiplier_sum_from_conditions(
            'multiplier_constitution'
        )

    @property
    def multiplier_intelligence(self) -> float:
        return self.get_multiplier_sum_from_conditions(
            'multiplier_intelligence'
        )

    @property
    def multiplier_wisdom(self) -> float:
        return self.get_multiplier_sum_from_conditions(
            'multiplier_wisdom'
        )

    @property
    def multiplier_charisma(self) -> float:
        return self.get_multiplier_sum_from_conditions(
            'multiplier_charisma'
        )

    @property
    def bonus_hit_points(self) -> int:
        return self.get_attr_sum_from_conditions('bonus_hit_points')

    @property
    def bonus_initiative(self) -> int:
        return self.get_attr_sum_from_conditions('bonus_initiative')

    @property
    def bonus_physical_attack(self) -> int:
        return self.get_attr_sum_from_conditions('bonus_physical_attack')

    @property
    def bonus_precision_attack(self) -> int:
        return self.get_attr_sum_from_conditions('bonus_precision_attack')

    @property
    def bonus_magical_attack(self) -> int:
        return self.get_attr_sum_from_conditions('bonus_magical_attack')

    @property
    def bonus_physical_defense(self) -> int:
        return self.get_attr_sum_from_conditions('bonus_physical_defense')

    @property
    def bonus_magical_defense(self) -> int:
        return self.get_attr_sum_from_conditions('bonus_magical_defense')

    @property
    def bonus_hit(self) -> int:
        return self.get_attr_sum_from_conditions('bonus_hit')

    @property
    def bonus_evasion(self) -> int:
        return self.get_attr_sum_from_conditions('bonus_evasion')


if __name__ == '__main__':
    from rpgram.enums.debuff import DebuffEnum

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
                name=DebuffEnum.POISONING,
                frequency='CONTINUOUS',
            ),
            Condition(
                name=DebuffEnum.BURN,
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
