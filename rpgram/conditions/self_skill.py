''' Módulo com as Condições do tipo SELF
    Essas Condições usam dos stats do personagem atualizados, por isso 
    recebem um personagem como argumento.
'''


from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Iterable, Union

from bson import ObjectId

from rpgram.conditions.buff import BuffCondition
from rpgram.constants.text import (
    DEXTERITY_EMOJI_TEXT,
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
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
    MageSkillEnum,
    SorcererSkillEnum
)
from rpgram.enums.turn import TurnEnum


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class SelfSkillCondition(BuffCondition):

    def __init__(
        self,
        name: Enum,
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
            name=GuardianSkillEnum.ROBUST_BLOCK,
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
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{self.character.name}* permanece na *Postura Defensiva*.'
            )
            report['text'] = text

        return report


class CrystalArmorCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=GuardianSkillEnum.CRYSTAL_ARMOR,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Armadura forjada com *Cristais Místicos* que reduz a '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
            f'em *{self.bonus_physical_defense}* pontos para aumentar a '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* em '
            f'*{self.bonus_magical_defense}* pontos '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_physical_defense(self) -> int:
        bonus_physical_defense = -(self.character.cs.base_physical_defense / 4)

        return int(bonus_physical_defense)

    @property
    def bonus_magical_defense(self) -> int:
        power = (1 + (self.level / 10))
        bonus_magical_defense = power * abs(self.bonus_physical_defense)

        return int(bonus_magical_defense)

    @property
    def emoji(self) -> str:
        return '🟪'

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{self.character.name}* permanece envolto pelos '
                f'*Cristais Místicos*.'
            )
            report['text'] = text

        return report


class RockArmorCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=MageSkillEnum.ROCK_ARMOR,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Uma pesada *Armadura de Rocha* conjurada com magia que reduz a '
            f'*{EVASION_EMOJI_TEXT}* '
            f'em *{self.bonus_evasion}* pontos para aumentar a '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* em '
            f'*{self.bonus_physical_defense}* pontos '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_evasion(self) -> int:
        bonus_evasion = -(self.character.cs.base_evasion / 4)

        return int(bonus_evasion)

    @property
    def bonus_physical_defense(self) -> int:
        power = (1 + (self.level / 6.666))
        bonus_physical_defense = power * abs(self.bonus_evasion)

        return int(bonus_physical_defense)

    @property
    def emoji(self) -> str:
        return '🪨🛡'

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{self.character.name}* permanece protegido pela '
                f'*Armadura de Rocha*.'
            )
            report['text'] = text

        return report


class LavaSkinCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=MageSkillEnum.LAVA_SKIN,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Camada de *Lava Endurecida* que aumenta a '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* em '
            f'*{self.bonus_magical_defense}* pontos e a '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* em '
            f'*{self.bonus_physical_defense}* pontos '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_magical_defense(self) -> int:
        power = 2 + (self.level / 10)
        power = round(power, 2)
        bonus_magical_defense = self.character.bs.wisdom * power

        return int(bonus_magical_defense)

    @property
    def bonus_physical_defense(self) -> int:
        power = 1 + (self.level / 10)
        power = round(power, 2)
        bonus_physical_defense = self.character.bs.wisdom * power

        return int(bonus_physical_defense)

    @property
    def emoji(self) -> str:
        return '🌋🛡'

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{self.character.name}* permanece encoberto pela '
                f'*Lava Endurecida*.'
            )
            report['text'] = text

        return report


class MistFormCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=MageSkillEnum.MIST_FORM,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Forma Etérea* que aumenta a '
            f'*{EVASION_EMOJI_TEXT}* em '
            f'*{self.bonus_evasion}* pontos '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_evasion(self) -> int:
        power = 3 + (self.level / 10)
        power = round(power, 2)
        bonus_evasion = self.character.bs.intelligence * power

        return int(bonus_evasion)

    @property
    def emoji(self) -> str:
        return '🧖'

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{self.character.name}* permanece na *Forma Etérea*.'
            )
            report['text'] = text

        return report


class FuriousFuryCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=BarbarianSkillEnum.FURIOUS_FURY,
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
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{self.character.name}* permanece em estado de '
                f'*{self.name}*.'
            )
            report['text'] = text

        return report


class FuriousInstinctCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=BarbarianSkillEnum.FURIOUS_INSTINCT,
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
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{self.character.name}* permanece em estado de '
                f'*{self.name}*.'
            )
            report['text'] = text

        return report


class FrenzyCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=BarbarianSkillEnum.FRENZY,
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
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{self.character.name}* permanece em estado de '
                f'*{self.name}*.'
            )
            report['text'] = text

        return report


class RaijusFootstepsCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=BarbarianSkillEnum.RAIJŪÇÇÇS_FOOTSTEPS,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Estado de *Transe Sobrenatural* que aumenta o '
            f'*{HIT_EMOJI_TEXT}* '
            f'em {self.bonus_hit} pontos e a '
            f'*{EVASION_EMOJI_TEXT}* '
            f'em {self.bonus_evasion} pontos '
            f'(200%{EmojiEnum.STRENGTH.value} + 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_hit(self) -> int:
        power = 2 + (self.level / 10)
        power = round(power, 2)
        bonus_hit = self.character.bs.strength * power

        return int(bonus_hit)

    @property
    def bonus_evasion(self) -> int:
        power = 2 + (self.level / 10)
        power = round(power, 2)
        bonus_hit = self.character.bs.strength * power

        return int(bonus_hit)

    @property
    def emoji(self) -> str:
        return '⚡🐺'

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{self.character.name}* permanece em *Transe Sobrenatural*.'
            )
            report['text'] = text

        return report


class FafnirsScalesCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=BarbarianSkillEnum.FAFNIRÇÇÇS_SCALES,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Pele e Músculos Petrificados* que aumenta a '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.bonus_physical_defense} '
            f'(200%{EmojiEnum.STRENGTH.value} + 10% x Nível), '
            f'aumenta com base na vida perdida, '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_physical_defense(self) -> int:
        power = 2 + (self.level / 10) + (self.character.cs.irate_hp * 2)
        power = round(power, 2)
        bonus_physical_defense = self.character.bs.strength * power

        return int(bonus_physical_defense)

    @property
    def emoji(self) -> str:
        return '🏔️🐲'

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{self.character.name}* permanece com '
                f'*Pele e Músculos Petrificados*.'
            )
            report['text'] = text

        return report


class MysticalProtectionCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=SorcererSkillEnum.MYSTICAL_PROTECTION,
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
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{self.character.name}* permanece coberto pela '
                f'*{self.name}*.'
            )
            report['text'] = text

        return report


class MysticalConfluenceCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=SorcererSkillEnum.MYSTICAL_CONFLUENCE,
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
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{self.character.name}* permanece imbuído pela '
                f'*{self.name}*.'
            )
            report['text'] = text

        return report


class MysticalVigorCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 15,
        level: int = 1
    ):
        super().__init__(
            name=SorcererSkillEnum.MYSTICAL_VIGOR,
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
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{self.character.name}* está revigorado pelo '
                f'*{self.name}*.'
            )
            report['text'] = text

        return report


class FakeCharacter:
    # BASE STATS
    class FakeBaseStats:
        strength = 100
        dexterity = 100
        constitution = 100
        intelligence = 100
        wisdom = 100
        charisma = 100
        base_strength = 100
        base_dexterity = 100
        base_constitution = 100
        base_intelligence = 100
        base_wisdom = 100
        base_charisma = 100
        bonus_strength = 100
        bonus_dexterity = 100
        bonus_constitution = 100
        bonus_intelligence = 100
        bonus_wisdom = 100
        bonus_charisma = 100
        multiplier_strength = 1.0
        multiplier_dexterity = 1.0
        multiplier_constitution = 1.0
        multiplier_intelligence = 1.0
        multiplier_wisdom = 1.0
        multiplier_charisma = 1.0

    # COMBAT STATS
    class FakeCombatStats:
        hit_points = 100
        initiative = 100
        physical_attack = 100
        precision_attack = 100
        magical_attack = 100
        physical_defense = 100
        magical_defense = 100
        hit = 100
        evasion = 100
        base_hit_points = 100
        base_initiative = 100
        base_physical_attack = 100
        base_precision_attack = 100
        base_magical_attack = 100
        base_physical_defense = 100
        base_magical_defense = 100
        base_hit = 100
        base_evasion = 100
        hit_points = 100
        bonus_initiative = 100
        bonus_physical_attack = 100
        bonus_precision_attack = 100
        bonus_magical_attack = 100
        bonus_physical_defense = 100
        bonus_magical_defense = 100
        bonus_hit = 100
        bonus_evasion = 100
        irate_hp = 0.66

    base_stats = bs = FakeBaseStats()
    combat_stats = cs = FakeCombatStats()


class SelfBuffs:
    __list = [
        RobustBlockCondition,
        CrystalArmorCondition,
        RockArmorCondition,
        LavaSkinCondition,
        MistFormCondition,
        FuriousFuryCondition,
        FuriousInstinctCondition,
        FrenzyCondition,
        RaijusFootstepsCondition,
        FafnirsScalesCondition,
        MysticalProtectionCondition,
        MysticalConfluenceCondition,
        MysticalVigorCondition,
    ]

    def __iter__(self) -> Iterable[SelfSkillCondition]:
        for condition_class in self.__list:
            yield condition_class(character=FakeCharacter())


SELF_BUFFS: Iterable[SelfSkillCondition] = SelfBuffs()


if __name__ == '__main__':
    from rpgram.constants.test import BASE_CHARACTER
    from rpgram.conditions.factory import condition_factory

    condition = RobustBlockCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())
    _dict = {'character': BASE_CHARACTER, **condition.to_dict()}
    _dict.pop('need_character')
    assert condition_factory(**_dict) == condition

    condition = CrystalArmorCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())
    _dict = {'character': BASE_CHARACTER, **condition.to_dict()}
    _dict.pop('need_character')
    assert condition_factory(**_dict) == condition

    condition = RockArmorCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())
    _dict = {'character': BASE_CHARACTER, **condition.to_dict()}
    _dict.pop('need_character')
    assert condition_factory(**_dict) == condition

    condition = LavaSkinCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())
    _dict = {'character': BASE_CHARACTER, **condition.to_dict()}
    _dict.pop('need_character')
    assert condition_factory(**_dict) == condition

    condition = MistFormCondition(BASE_CHARACTER)
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

    condition = RaijusFootstepsCondition(BASE_CHARACTER)
    print(condition)
    print(condition.to_dict())
    _dict = {'character': BASE_CHARACTER, **condition.to_dict()}
    _dict.pop('need_character')
    assert condition_factory(**_dict) == condition

    condition = FafnirsScalesCondition(BASE_CHARACTER)
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
