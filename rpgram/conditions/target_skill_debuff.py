''' Módulo com as Condições do tipo de Target diferente de SELF
    Essas Condições usam o power fornecido no momendo da instância
'''


from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Iterable, Union

from bson import ObjectId
from rpgram.conditions.debuff import DebuffCondition
from rpgram.constants.text import (
    EVASION_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    DuelistSkillEnum,
    GuardianSkillEnum,
    HeraldSkillEnum,
    MageSkillEnum,
    SamuraiSkillEnum
)
from rpgram.enums.turn import TurnEnum


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class TargetSkillDebuffCondition(DebuffCondition):

    def __init__(
        self,
        name: Enum,
        frequency: Union[str, TurnEnum],
        power: int,
        turn: int = 1,
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
        self._power = int(power)

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{target.name}* {self.function_text}'
            )
            report['text'] = text

        return report

    @property
    def power(self) -> int:
        power_multiplier = 1 + (self.level / 10)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)

    @property
    def function_text(self) -> str:
        raise NotImplementedError()

    def to_dict(self) -> dict:
        _dict = {'power': self._power}
        _dict.update(super().to_dict())

        return _dict


class ShatterCondition(TargetSkillDebuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=GuardianSkillEnum.SHATTER,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Fragmentos de *Cristais Místicos* que diminuem a '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* e a '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* em {self.power} pontos.'
        )

    @property
    def power(self) -> int:
        power_multiplier = 0.05 + (self.level / 100)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)

    @property
    def bonus_magical_defense(self) -> int:
        return -(self.power)

    @property
    def bonus_physical_defense(self) -> int:
        return -(self.power)

    @property
    def emoji(self) -> str:
        return '💔'

    @property
    def function_text(self) -> str:
        return f'permanece cravejado de fragmentos de *Cristais Místicos*.'


class MuddyCondition(TargetSkillDebuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=MageSkillEnum.MUDDY,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Lama pegajosa que diminui a '
            f'*{EVASION_EMOJI_TEXT}* em {self.power} pontos.'
        )

    @property
    def power(self) -> int:
        power_multiplier = 0.08 + (self.level / 50)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)

    @property
    def bonus_evasion(self) -> int:
        return -(self.power)

    @property
    def emoji(self) -> str:
        return '🦶🏾'

    @property
    def function_text(self) -> str:
        return f'permanece *Enlameado*.'


class AchillesHeelCondition(TargetSkillDebuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DuelistSkillEnum.ACHILLEÇÇÇS_HEEL,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Ferida* que debilita a mobilidade, diminuindo a '
            f'*{EVASION_EMOJI_TEXT}* em {self.power} pontos.'
        )

    @property
    def power(self) -> int:
        power_multiplier = 0.05 + (self.level / 100)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)

    @property
    def bonus_evasion(self) -> int:
        return -(self.power)

    @property
    def emoji(self) -> str:
        return '🩸🦶🏽'

    @property
    def function_text(self) -> str:
        return f'permanece com uma *Ferida Debilitante*.'


class DisarmorCondition(TargetSkillDebuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DuelistSkillEnum.DISARMOR,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Proteções Fragilizadas* que diminuem a '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* em {self.power} pontos.'
        )

    @property
    def power(self) -> int:
        power_multiplier = 0.05 + (self.level / 100)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)

    @property
    def bonus_physical_defense(self) -> int:
        return -(self.power)

    @property
    def emoji(self) -> str:
        return EmojiEnum.SHIELD.value + '📉'

    @property
    def function_text(self) -> str:
        return f'permanece com as *Proteções Fragilizadas*.'


class KoteUchiCondition(TargetSkillDebuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 1,
        level: int = 1,
    ):
        super().__init__(
            name=SamuraiSkillEnum.KOTE_UCHI,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Braços Desestabilizados* que diminuem o '
            f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* em {self.power} pontos e o '
            f'*{PRECISION_ATTACK_EMOJI_TEXT}* em {self.power} pontos.'
        )

    @property
    def power(self) -> int:
        power_multiplier = 0.10 + (self.level / 100)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)

    @property
    def bonus_physical_attack(self) -> int:
        return -(self.power)

    @property
    def bonus_precision_attack(self) -> int:
        return -(self.power)

    @property
    def emoji(self) -> str:
        return EmojiEnum.ATTACK.value + '📉'

    @property
    def function_text(self) -> str:
        return f'permanece com os *Braços Desestabilizados*.'


class DoUchiCondition(TargetSkillDebuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 1,
        level: int = 1,
    ):
        super().__init__(
            name=SamuraiSkillEnum.DO_UCHI,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Tronco Desestabilizado* que diminue a '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* em {self.power} pontos.'
        )

    @property
    def power(self) -> int:
        power_multiplier = 0.10 + (self.level / 100)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)

    @property
    def bonus_physical_defense(self) -> int:
        return -(self.power)

    @property
    def emoji(self) -> str:
        return '🩻📉'

    @property
    def function_text(self) -> str:
        return f'permanece com o *Tronco Desestabilizado*.'


class RedEquilibriumCondition(TargetSkillDebuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=HeraldSkillEnum.RED_EQUILIBRIUM,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Chamas Vermelhas* que diminuem a '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* em {self.power} pontos.'
        )

    @property
    def power(self) -> int:
        power_multiplier = 0.025 + (self.level / 100)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)

    @property
    def bonus_magical_defense(self) -> int:
        return -(self.power)

    @property
    def emoji(self) -> str:
        return '❤️🔥'

    @property
    def function_text(self) -> str:
        return f'permanece *Afogueado*.'


class TargetDebuffs:
    __list = [
        ShatterCondition,
        MuddyCondition,
        AchillesHeelCondition,
        DisarmorCondition,
        KoteUchiCondition,
        DoUchiCondition,
        RedEquilibriumCondition,
    ]

    def __init__(self, default_power: int = 100):
        self.default_power = default_power

    def __iter__(self) -> Iterable[TargetSkillDebuffCondition]:
        for condition_class in self.__list:
            yield condition_class(power=self.default_power)


TARGET_DEBUFFS: Iterable[TargetSkillDebuffCondition] = TargetDebuffs()


if __name__ == '__main__':
    from rpgram.conditions.factory import condition_factory
    from rpgram.constants.test import BASE_CHARACTER

    for target_debuff in TargetDebuffs():
        condition = target_debuff
        print(condition)
        print(condition.to_dict())
        assert condition_factory(**condition.to_dict()) == condition

    # for condition in TargetDebuffs():
    #     print(condition.function(BASE_CHARACTER)['text'])
