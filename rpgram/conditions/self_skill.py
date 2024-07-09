''' Módulo com as Condições do tipo SELF
    Essas Condições usam dos stats do personagem atualizados, por isso 
    recebem um personagem como argumento.
'''


from datetime import datetime
from typing import TYPE_CHECKING, Union

from bson import ObjectId

from rpgram.conditions.buff import BuffCondition
from rpgram.constants.text import (
    DEXTERITY_EMOJI_TEXT,
    HIT_POINT_FULL_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    STRENGTH_EMOJI_TEXT
)
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    BarbarianSkillEnum,
    GuardianSkillEnum,
    SorcererSkillEnum
)
from rpgram.enums.turn import TurnEnum


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class SelfSkillCondition(BuffCondition):

    def __init__(
        self,
        name: str,
        character: 'BaseCharacter',
        frequency: Union[str, TurnEnum],
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
        self.character = character

    def to_dict(self) -> dict:
        _dict = {'need_character': True}
        _dict.update(super().to_dict())

        return _dict


class RobustBlockCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=GuardianSkillEnum.ROBUST_BLOCK.value,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Postura defensiva que aumenta a *{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.bonus_physical_defense} pontos '
            f'(100%{EmojiEnum.CONSTITUTION.value} + 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_physical_defense(self) -> int:
        power = 1 + (self.level / 10)
        power = round(power, 2)
        bonus_physical_defense = self.character.bs.constitution * power

        return int(bonus_physical_defense)

    @property
    def emoji(self) -> str:
        return '🙅🏿'

    def function(self, target: 'BaseCharacter') -> dict:
        text = (
            f'*{self.full_name}*: '
            f'*{self.character.name}* permanece na *Postura Defensiva*.'
        )
        report = {'text': text}
        report['action'] = self.name

        return report


class FuriousFuryCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=BarbarianSkillEnum.FURIOUS_FURY.value,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Estado de *Fúria* que aumenta o *{PHYSICAL_ATTACK_EMOJI_TEXT}* '
            f'em {self.bonus_physical_attack} pontos '
            f'(100%{EmojiEnum.STRENGTH.value} + 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_physical_attack(self) -> int:
        power = 1 + (self.level / 10)
        power = round(power, 2)
        bonus_physical_attack = self.character.bs.strength * power

        return int(bonus_physical_attack)

    @property
    def emoji(self) -> str:
        return '😤'

    def function(self, target: 'BaseCharacter') -> dict:
        text = (
            f'*{self.full_name}*: '
            f'*{self.character.name}* permanece em estado de '
            f'*{self.name}*.'
        )
        report = {'text': text}
        report['action'] = self.name

        return report


class FuriousInstinctCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=BarbarianSkillEnum.FURIOUS_INSTINCT.value,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Instinto de *Fúria* que aumenta a *{DEXTERITY_EMOJI_TEXT}* '
            f'base em {int((self.multiplier_dexterity-1)*100)}% '
            f'(20% + 5% x Nível) por {self.turn} turno(s).'
        )

    @property
    def multiplier_dexterity(self) -> int:
        power = 1.20 + (self.level / 20)
        power = round(power, 2)

        return power

    @property
    def emoji(self) -> str:
        return '‼️'

    def function(self, target: 'BaseCharacter') -> dict:
        text = (
            f'*{self.full_name}*: '
            f'*{self.character.name}* permanece em estado de '
            f'*{self.name}*.'
        )
        report = {'text': text}
        report['action'] = self.name

        return report


class FrenzyCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=BarbarianSkillEnum.FRENZY.value,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'O personagem fica em estado de *Frenesi*, aumentando a '
            f'*{STRENGTH_EMOJI_TEXT}* e a *{DEXTERITY_EMOJI_TEXT}* '
            f'base em {int((self.multiplier_dexterity-1)*100)}% '
            f'(50% + 5% x Nível) por {self.turn} turno(s), '
            f'mas pode atacar aliados ou a si.'
        )

    @property
    def multiplier_dexterity(self) -> int:
        power = 1.50 + (self.level / 20)
        power = round(power, 2)

        return power

    @property
    def multiplier_strength(self) -> int:
        power = 1.50 + (self.level / 20)
        power = round(power, 2)

        return power

    @property
    def emoji(self) -> str:
        return '🤬'

    def function(self, target: 'BaseCharacter') -> dict:
        text = (
            f'*{self.full_name}*: '
            f'*{self.character.name}* permanece em estado de '
            f'*{self.name}*.'
        )
        report = {'text': text}
        report['action'] = self.name

        return report


class MysticalProtectionCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=SorcererSkillEnum.MYSTICAL_PROTECTION.value,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Trama de energia *Mística* que aumenta a '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.bonus_magical_defense} pontos '
            f'(100%{EmojiEnum.WISDOM.value} + 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_magical_defense(self) -> int:
        power = 1 + (self.level / 10)
        power = round(power, 2)
        bonus_magical_defense = self.character.bs.wisdom * power

        return int(bonus_magical_defense)

    @property
    def emoji(self) -> str:
        return '🧘🏾'

    def function(self, target: 'BaseCharacter') -> dict:
        text = (
            f'*{self.full_name}*: '
            f'*{self.character.name}* permanece coberto pela '
            f'*{self.name}*.'
        )
        report = {'text': text}
        report['action'] = self.name

        return report


class MysticalConfluenceCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=SorcererSkillEnum.MYSTICAL_CONFLUENCE.value,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Concetração de energias *Místicas* que aumenta o '
            f'*{MAGICAL_ATTACK_EMOJI_TEXT}* '
            f'em {self.bonus_magical_attack} pontos '
            f'(100%{EmojiEnum.INTELLIGENCE.value} + 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_magical_attack(self) -> int:
        power = 1 + (self.level / 10)
        power = round(power, 2)
        bonus_magical_attack = self.character.bs.intelligence * power

        return int(bonus_magical_attack)

    @property
    def emoji(self) -> str:
        return '🧘🏾'

    def function(self, target: 'BaseCharacter') -> dict:
        text = (
            f'*{self.full_name}*: '
            f'*{self.character.name}* permanece imbuído pela '
            f'*{self.name}*.'
        )
        report = {'text': text}
        report['action'] = self.name

        return report


class MysticalVigorCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 15,
        level: int = 1
    ):
        super().__init__(
            name=SorcererSkillEnum.MYSTICAL_VIGOR.value,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Conjunto de energias *Místicas* que aumenta o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
            f'em {self.bonus_hit_points} pontos '
            f'(200%{EmojiEnum.INTELLIGENCE.value} + 20% x Nível) e'
            f'(200%{EmojiEnum.WISDOM.value} + 20% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_hit_points(self) -> int:
        power = 2 + (self.level / 5)
        power = round(power, 2)
        bonus_magical_attack = sum([
            self.character.bs.intelligence * power,
            self.character.bs.wisdom * power
        ])

        return int(bonus_magical_attack)

    @property
    def emoji(self) -> str:
        return '🧘🏾'

    def function(self, target: 'BaseCharacter') -> dict:
        text = (
            f'*{self.full_name}*: '
            f'*{self.character.name}* está revigorado pelo '
            f'*{self.name}*.'
        )
        report = {'text': text}
        report['action'] = self.name

        return report


if __name__ == '__main__':
    from rpgram.constants.test import BASE_CHARACTER
    from rpgram.conditions.factory import condition_factory

    condition = RobustBlockCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())
    _dict = {'character': BASE_CHARACTER, **condition.to_dict()}
    _dict.pop('need_character')
    assert condition_factory(**_dict) == condition

    condition = FuriousFuryCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())
    _dict = {'character': BASE_CHARACTER, **condition.to_dict()}
    _dict.pop('need_character')
    assert condition_factory(**_dict) == condition

    condition = FuriousInstinctCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())
    _dict = {'character': BASE_CHARACTER, **condition.to_dict()}
    _dict.pop('need_character')
    assert condition_factory(**_dict) == condition

    condition = FrenzyCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())
    _dict = {'character': BASE_CHARACTER, **condition.to_dict()}
    _dict.pop('need_character')
    assert condition_factory(**_dict) == condition

    condition = MysticalProtectionCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())
    _dict = {'character': BASE_CHARACTER, **condition.to_dict()}
    _dict.pop('need_character')
    assert condition_factory(**_dict) == condition

    condition = MysticalConfluenceCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())
    _dict = {'character': BASE_CHARACTER, **condition.to_dict()}
    _dict.pop('need_character')
    assert condition_factory(**_dict) == condition

    condition = MysticalVigorCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())
    _dict = {'character': BASE_CHARACTER, **condition.to_dict()}
    _dict.pop('need_character')
    assert condition_factory(**_dict) == condition
