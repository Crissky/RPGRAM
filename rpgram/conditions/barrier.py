from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Iterable, Union

from bson import ObjectId
from function.text import escape_basic_markdown_v2, remove_bold, remove_code
from rpgram.conditions.condition import Condition
from rpgram.constants.text import (
    BARRIER_POINT_FULL_EMOJI_TEXT,
    HIT_POINT_FULL_EMOJI_TEXT
)
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    GladiatorSkillEnum,
    HealerSkillEnum,
    MultiClasseSkillEnum,
    SorcererSkillEnum,
    SorcererSupremeSkillEnum,
    SummonerSkillEnum,
    WarriorSkillEnum
)
from rpgram.enums.turn import TurnEnum


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class BarrierCondition(Condition):

    def __init__(
        self,
        name: Enum,
        frequency: Union[str, TurnEnum],
        power: int,
        damage: int = 0,
        turn: int = 5,
        level: int = 1,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        super().__init__(
            name=name,
            frequency=frequency,
            turn=turn,
            level=level,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )
        self.power = int(power)
        self.__damage = int(damage)

    def add_damage(self, value: int) -> int:
        '''Adiciona dano a barreira e retorna o dano excedente.
        '''

        value = int(abs(value))
        if value > 0:
            print(f'Barreira recebeu {value} de Dano!!!', end=' ')
        remaining_damage = value - self.current_barrier_points
        self.__damage += value
        self.__damage = min(self.__damage, self.barrier_points)
        print(f'{self.show_bp}')

        return max(0, remaining_damage)

    def damage_barrier_points(
        self,
        value: int,
        markdown: bool = False,
    ) -> dict:
        '''Adiciona dano a barreira e retorna o dano excedente.
        '''

        value = int(abs(value))
        old_bp = self.current_barrier_points
        old_show_bp = self.show_barrier_points
        remaining_damage = self.add_damage(value)
        new_bp = self.current_barrier_points
        new_show_bp = self.show_barrier_points
        absolute_damage = (old_bp - new_bp)
        broke_text = ' QUEBROU!' if self.is_broken else ''
        text = (
            f'*{self.name}*: {old_show_bp} ››› {new_show_bp} '
            f'(*{value}*){broke_text}.'
        )

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return {
            'old_bp': old_bp,
            'old_show_bp': old_show_bp,
            'new_bp': new_bp,
            'new_show_bp': new_show_bp,
            'damage': value,
            'absolute_damage': absolute_damage,
            'action': 'DANO',
            'remaining_damage': remaining_damage,
            'text': text,
        }

    @property
    def base_power_multiplier(self) -> float:
        return 1.00

    @property
    def barrier_points(self) -> int:
        power_multiplier = self.base_power_multiplier + (self.level / 10)
        power_multiplier = round(power_multiplier, 2)
        return int(self.power * power_multiplier)

    @property
    def current_barrier_points(self) -> int:
        return int(self.barrier_points - self.__damage)
    current_bp = current_barrier_points

    @property
    def show_barrier_points(self) -> str:
        current_barrier_points = max(self.current_barrier_points, 0)
        alert_text = ''
        if self.current_barrier_points < 0:
            alert_text = EmojiEnum.UNDER_ZERO.value
        return (
            f'*{BARRIER_POINT_FULL_EMOJI_TEXT}*: '
            f'{current_barrier_points}/{self.barrier_points}{alert_text}'
        )
    show_bp = show_barrier_points

    @property
    def barrier_points_text(self) -> str:
        return f'{self.full_name}: {self.show_barrier_points}'

    @property
    def is_broken(self) -> bool:
        return self.current_barrier_points <= 0

    @property
    def emoji(self) -> str:
        return EmojiEnum.BARRIER_POINT.value

    def function(self, target: 'BaseCharacter') -> dict:
        text = f'*{self.full_name}*: {self.show_barrier_points}'
        report = {'text': text}
        report['action'] = self.name

        return report

    def to_dict(self) -> dict:
        _dict = {
            'power': self.power,
            'damage': self.__damage,
        }
        _dict.update(super().to_dict())

        return _dict


class GuardianShieldCondition(BarrierCondition):

    def __init__(
        self,
        power: int,
        damage: int = 0,
        turn: int = 5,
        level: int = 1,
    ):
        super().__init__(
            name=MultiClasseSkillEnum.GUARDIAN_SHIELD,
            frequency=TurnEnum.START,
            power=power,
            damage=damage,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Escudo Familiar Protetivo* que resguarda com uma barreira '
            f'de *{self.barrier_points}* {BARRIER_POINT_FULL_EMOJI_TEXT}.'
        )


class AegisShadowCondition(BarrierCondition):

    def __init__(
        self,
        power: int,
        damage: int = 0,
        turn: int = 5,
        level: int = 1,
    ):
        super().__init__(
            name=WarriorSkillEnum.AEGIS_SHADOW,
            frequency=TurnEnum.START,
            power=power,
            damage=damage,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Sombra do Escudo Lendário* que protege com uma barreira '
            f'de *{self.barrier_points}* {BARRIER_POINT_FULL_EMOJI_TEXT}.'
        )

    @property
    def base_power_multiplier(self) -> float:
        return 2.00


class PrismaticShieldCondition(BarrierCondition):

    def __init__(
        self,
        power: int,
        damage: int = 0,
        turn: int = 5,
        level: int = 1,
    ):
        super().__init__(
            name=SorcererSkillEnum.PRISMATIC_SHIELD,
            frequency=TurnEnum.START,
            power=power,
            damage=damage,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Círculo Cintilante* que protege com uma barreira '
            f'de *{self.barrier_points}* {BARRIER_POINT_FULL_EMOJI_TEXT}.'
        )

    @property
    def base_power_multiplier(self) -> float:
        return 2.00


class ChaosWeaverCondition(BarrierCondition):

    def __init__(
        self,
        power: int,
        damage: int = 0,
        turn: int = 5,
        level: int = 1,
    ):
        super().__init__(
            name=SorcererSkillEnum.CHAOS_WEAVER,
            frequency=TurnEnum.START,
            power=power,
            damage=damage,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Véu Caótico* que protege com uma barreira '
            f'de *{self.barrier_points}* {BARRIER_POINT_FULL_EMOJI_TEXT}.'
        )


class ProtectiveAuraCondition(BarrierCondition):

    def __init__(
        self,
        power: int,
        damage: int = 0,
        turn: int = 5,
        level: int = 1,
    ):
        super().__init__(
            name=HealerSkillEnum.PROTECTIVE_AURA,
            frequency=TurnEnum.START,
            power=power,
            damage=damage,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Aura Protetiva* que salvaguarda com uma barreira '
            f'de *{self.barrier_points}* {BARRIER_POINT_FULL_EMOJI_TEXT}.'
        )


class AjaxShieldCondition(BarrierCondition):

    def __init__(
        self,
        power: int,
        damage: int = 0,
        turn: int = 5,
        level: int = 1,
    ):
        super().__init__(
            name=GladiatorSkillEnum.AJAX_SHIELD,
            frequency=TurnEnum.START,
            power=power,
            damage=damage,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Lendária Proteção* que protege com uma barreira '
            f'de *{self.barrier_points}* {BARRIER_POINT_FULL_EMOJI_TEXT}.'
        )

    @property
    def base_power_multiplier(self) -> float:
        return 2.00


class PiskieWindbagCondition(BarrierCondition):

    def __init__(
        self,
        power: int,
        damage: int = 0,
        turn: int = 5,
        level: int = 1,
    ):
        super().__init__(
            name=SummonerSkillEnum.PISKIE_WINDBAG,
            frequency=TurnEnum.START,
            power=power,
            damage=damage,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Barreira de Ar Turbilhonante* que protege com '
            f'*{self.barrier_points}* {BARRIER_POINT_FULL_EMOJI_TEXT}.'
        )


class MagicShieldCondition(BarrierCondition):

    def __init__(
        self,
        power: int,
        damage: int = 0,
        turn: int = 5,
        level: int = 1,
    ):
        super().__init__(
            name=SorcererSupremeSkillEnum.MAGIC_SHIELD,
            frequency=TurnEnum.START,
            power=power,
            damage=damage,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Manto Mágico* que protege com uma barreira '
            f'de *{self.barrier_points}* {BARRIER_POINT_FULL_EMOJI_TEXT}.'
        )

    @property
    def base_power_multiplier(self) -> float:
        return 2.00


class HealingRefugeCondition(BarrierCondition):

    def __init__(
        self,
        power: int,
        damage: int = 0,
        turn: int = 5,
        level: int = 1,
    ):
        super().__init__(
            name=HealerSkillEnum.HEALING_REFUGE,
            frequency=TurnEnum.START,
            power=power,
            damage=damage,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Refúgio Curativo* que engendrar com uma barreira '
            f'de *{self.barrier_points}* {BARRIER_POINT_FULL_EMOJI_TEXT} '
            f'e cura *{self.healing_points}* {HIT_POINT_FULL_EMOJI_TEXT} '
            f'a cada turno.'
        )

    @property
    def base_power_multiplier(self) -> float:
        return 2.00

    @property
    def healing_points(self) -> str:
        return int(self.barrier_points / 10)

    def function(self, target: 'BaseCharacter') -> dict:
        report = super().function(target)
        healing_report = target.combat_stats.cure_hit_points(
            value=self.healing_points,
            markdown=True,
        )
        healing_text = healing_report['text']
        text = f'\n*{self.full_name}*: {healing_text[:-2]}'
        report['text'] += text

        return report


class ProtectiveInfusionCondition(BarrierCondition):

    def __init__(
        self,
        power: int,
        damage: int = 0,
        turn: int = 5,
        level: int = 1,
    ):
        super().__init__(
            name=HealerSkillEnum.PROTECTIVE_INFUSION,
            frequency=TurnEnum.START,
            power=power,
            damage=damage,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Infusão Protetiva* que protege com uma barreira '
            f'de *{self.barrier_points}* {BARRIER_POINT_FULL_EMOJI_TEXT} '
            f'e cura até (Nível) níveis de condições aleatórias '
            f'a cada turno.'
        )

    @property
    def base_power_multiplier(self) -> float:
        return 2.00

    def function(self, target: 'BaseCharacter') -> dict:
        report = super().function(target)
        quantity = self.level
        status_report = target.status.remove_random_debuff_conditions(
            quantity=quantity
        )
        status_text = status_report["text"]
        if status_text:
            text = f'\n*{self.full_name}*: {status_text}'
            report['text'] += text

        return report


class BeatifyingAegisCondition(BarrierCondition):

    def __init__(
        self,
        power: int,
        damage: int = 0,
        turn: int = 5,
        level: int = 1,
    ):
        super().__init__(
            name=HealerSkillEnum.BEATIFYING_AEGIS,
            frequency=TurnEnum.START,
            power=power,
            damage=damage,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Proteção Sacra* que escuda com uma barreira '
            f'de *{self.barrier_points}* {BARRIER_POINT_FULL_EMOJI_TEXT}, '
            f'recupera *{self.healing_points}* {HIT_POINT_FULL_EMOJI_TEXT} '
            f'a cada turno '
            f'e cura até (5 * Nível) níveis de condições aleatórias '
            f'a cada turno.'
        )

    @property
    def base_power_multiplier(self) -> float:
        return 2.00

    @property
    def healing_points(self) -> str:
        return int(self.barrier_points / 5)

    def function(self, target: 'BaseCharacter') -> dict:
        # MAIN
        report = super().function(target)

        # HEAL
        healing_report = target.combat_stats.cure_hit_points(
            value=self.healing_points,
            markdown=True,
        )
        healing_text = healing_report['text']
        text = f'\n*{self.full_name}*: {healing_text[:-2]}'
        report['text'] += text

        # CURE
        quantity = self.level * 5
        status_report = target.status.remove_random_debuff_conditions(
            quantity=quantity
        )
        status_text = status_report["text"]
        if status_text:
            text = f'\n*{self.full_name}*: {status_text}'
            report['text'] += text

        return report


class BarrierBuffs:
    __list = [
        GuardianShieldCondition,
        AegisShadowCondition,
        PrismaticShieldCondition,
        ChaosWeaverCondition,
        ProtectiveAuraCondition,
        AjaxShieldCondition,
        PiskieWindbagCondition,
        MagicShieldCondition,
        HealingRefugeCondition,
        ProtectiveInfusionCondition,
        BeatifyingAegisCondition,
    ]

    def __iter__(self) -> Iterable[BarrierCondition]:
        for condition_class in self.__list:
            yield condition_class(power=100)


BARRIER_BUFFS: Iterable[BarrierCondition] = BarrierBuffs()


if __name__ == '__main__':
    from rpgram.conditions.factory import condition_factory
    from rpgram.constants.test import BASE_CHARACTER

    for condition in BarrierBuffs():
        print(condition)
        print(condition.to_dict())
        assert condition_factory(**condition.to_dict()) == condition

    # for condition in BarrierBuffs():
    #     print(condition.function(BASE_CHARACTER)['text'])
