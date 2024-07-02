from datetime import datetime
from typing import TYPE_CHECKING, Union

from bson import ObjectId

from rpgram.conditions.condition import Condition
from rpgram.constants.text import (
    DEXTERITY_EMOJI_TEXT,
    HIT_POINT_FULL_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT
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


class SelfSkillCondition(Condition):

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
        turn: int = 5,
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
            f'(100%{EmojiEnum.CONSTITUTION.value} + 5% x Nível) '
            f'por 5 turnos.'
        )

    @property
    def bonus_physical_defense(self) -> int:
        power = 1 + (self.level / 20)
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

    def battle_function(self, target: 'BaseCharacter') -> dict:
        return self.function(target)


class FuriousFuryCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 5,
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
            f'(100%{EmojiEnum.STRENGTH.value} + 5% x Nível) '
            f'por 5 turnos.'
        )

    @property
    def bonus_physical_attack(self) -> int:
        power = 1 + (self.level / 20)
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

    def battle_function(self, target: 'BaseCharacter') -> dict:
        return self.function(target)


class FuriousInstinctCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 5,
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
            f' (20% + 5% x Nível por 5 turnos).'
        )

    @property
    def multiplier_dexterity(self) -> int:
        power = 1.20 + (self.level / 20)

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

    def battle_function(self, target: 'BaseCharacter') -> dict:
        return self.function(target)


class MysticalProtectionCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 5,
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
            f'(100%{EmojiEnum.WISDOM.value} + 5% x Nível) '
            f'por 5 turnos.'
        )

    @property
    def bonus_magical_defense(self) -> int:
        power = 1 + (self.level / 20)
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

    def battle_function(self, target: 'BaseCharacter') -> dict:
        return self.function(target)


class MysticalConfluenceCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 5,
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
            f'(100%{EmojiEnum.INTELLIGENCE.value} + 5% x Nível) '
            f'por 5 turnos.'
        )

    @property
    def bonus_magical_attack(self) -> int:
        power = 1 + (self.level / 20)
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

    def battle_function(self, target: 'BaseCharacter') -> dict:
        return self.function(target)


class MysticalVigorCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
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
            f'(200%{EmojiEnum.INTELLIGENCE.value} + 10% x Nível) e'
            f'(200%{EmojiEnum.WISDOM.value} + 10% x Nível) '
            f'por 10 turnos.'
        )

    @property
    def bonus_hit_points(self) -> int:
        power = 2 + (self.level / 10)
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

    def battle_function(self, target: 'BaseCharacter') -> dict:
        return self.function(target)


if __name__ == '__main__':
    from rpgram.constants.test import BASE_CHARACTER
    condition = RobustBlockCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())

    condition = FuriousFuryCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())
    
    condition = FuriousInstinctCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())

    condition = MysticalProtectionCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())

    condition = MysticalConfluenceCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())

    condition = MysticalVigorCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())
