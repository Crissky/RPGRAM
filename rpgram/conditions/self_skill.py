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
    PRECISION_ATTACK_EMOJI_TEXT,
    STRENGTH_EMOJI_TEXT
)
from rpgram.enums.damage import DamageEmojiEnum
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    BarbarianSkillEnum,
    BerserkirSkillEnum,
    BountyHunterSkillEnum,
    GladiatorSkillEnum,
    GuardianSkillEnum,
    HeraldSkillEnum,
    KnightSkillEnum,
    MageSkillEnum,
    MercenarySkillEnum,
    MultiClasseSkillEnum,
    PaladinSkillEnum,
    RangerSkillEnum,
    RogueSkillEnum,
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

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{self.character.name}* {self.function_text}'
            )
            report['text'] = text

        return report

    @property
    def function_text(self) -> str:
        raise NotImplementedError()


class RobustBlockCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=MultiClasseSkillEnum.ROBUST_BLOCK,
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

    @property
    def function_text(self) -> str:
        return f'permanece na *Postura Defensiva*.'


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

    @property
    def function_text(self) -> str:
        return f'permanece envolto pelos *Cristais Místicos*.'


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

    @property
    def function_text(self) -> str:
        return f'permanece protegido pela *Armadura de Rocha*.'


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

    @property
    def function_text(self) -> str:
        return f'permanece encoberto pela *Lava Endurecida*.'


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

    @property
    def function_text(self) -> str:
        return f'permanece na *Forma Etérea*.'


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

    @property
    def function_text(self) -> str:
        return f'permanece em estado de *{self.trans_name}*.'


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

    @property
    def function_text(self) -> str:
        return f'permanece em estado de *{self.trans_name}*.'


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

    @property
    def function_text(self) -> str:
        return f'permanece em estado de *{self.trans_name}*.'


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

    @property
    def function_text(self) -> str:
        return f'permanece em *Transe Sobrenatural*.'


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

    @property
    def function_text(self) -> str:
        return f'permanece com *Pele e Músculos Petrificados*.'


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
            f'*Trama de Energia Mística* que aumenta a '
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

    @property
    def function_text(self) -> str:
        return f'permanece coberto pela *{self.trans_name}*.'


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
            f'*Concetração de Energias Místicas* que aumenta o '
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

    @property
    def function_text(self) -> str:
        return f'permanece imbuído pela *{self.trans_name}*.'


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
            f'*Conjunto de Energias Místicas* que aumenta o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
            f'em {self.bonus_hit_points} pontos '
            f'(200%{EmojiEnum.INTELLIGENCE.value} + 20% x Nível) e '
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

    @property
    def function_text(self) -> str:
        return f'está fortificado pelo *{self.trans_name}*.'


class ShadowStepsCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=RogueSkillEnum.SHADOW_STEPS,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Move-se pelas *Sombras*, como um *Fastasma*, aumentando o '
            f'*{HIT_EMOJI_TEXT}* '
            f'em {self.bonus_hit} pontos '
            f'(100%{EmojiEnum.DEXTERITY.value} + 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_hit(self) -> int:
        power = 1 + (self.level / 10)
        power = round(power, 2)
        bonus_hit = self.character.bs.dexterity * power

        return int(bonus_hit)

    @property
    def emoji(self) -> str:
        return DamageEmojiEnum.DARK.value + '👣'

    @property
    def function_text(self) -> str:
        return f'permanece andando pela *Sombras*.'


class ChaoticStepsCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=RogueSkillEnum.CHAOTIC_STEPS,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Move-se de maneira errática e imprevisível, aumentando a '
            f'*{EVASION_EMOJI_TEXT}* '
            f'em {self.bonus_evasion} pontos '
            f'(100%{EmojiEnum.DEXTERITY.value} + 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_evasion(self) -> int:
        power = 1 + (self.level / 10)
        power = round(power, 2)
        bonus_evasion = self.character.bs.dexterity * power

        return int(bonus_evasion)

    @property
    def emoji(self) -> str:
        return DamageEmojiEnum.CHAOS.value + '👣'

    @property
    def function_text(self) -> str:
        return f'permanece com o *Andar Errático*.'


class PenitenceCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=PaladinSkillEnum.PENITENCE,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Cilício Constringido* que fortalecer a fé, '
            f'reduzindo o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}* em '
            f'{self.bonus_hit_points} pontos '
            f'e aumentando o '
            f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* em '
            f'{self.bonus_physical_attack} pontos e a '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* em '
            f'*{self.bonus_magical_defense}* pontos '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_hit_points(self) -> int:
        bonus_hit_points = -(self.character.cs.base_hit_points * 0.25)

        return int(bonus_hit_points)

    @property
    def bonus_physical_attack(self) -> int:
        power = (0.25 + (self.level / 100))
        bonus_physical_attack = power * self.character.cs.base_physical_attack

        return int(bonus_physical_attack)

    @property
    def bonus_magical_defense(self) -> int:
        power = (0.25 + (self.level / 100))
        bonus_magical_defense = power * self.character.cs.base_magical_defense

        return int(bonus_magical_defense)

    @property
    def emoji(self) -> str:
        return '⛓️'

    @property
    def function_text(self) -> str:
        return f'permanece com o *Cilício Constringido*.'


class MysticBlockCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=HeraldSkillEnum.MYSTIC_BLOCK,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Aura Protetora* que aumenta a *{MAGICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.bonus_magical_defense} pontos '
            f'(200%{EmojiEnum.CONSTITUTION.value} + 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_magical_defense(self) -> int:
        power = 2 + (self.level / 10)
        power = round(power, 2)
        bonus_magical_defense = self.character.bs.constitution * power

        return int(bonus_magical_defense)

    @property
    def emoji(self) -> str:
        return '🧖🏽‍♀️'

    @property
    def function_text(self) -> str:
        return f'permanece envolto em uma *Aura Protetora*.'


class SharpFaroCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=BountyHunterSkillEnum.SHARP_FARO,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Olfato Apurado* que '
            f'aumenta o '
            f'*{HIT_EMOJI_TEXT}* '
            f'em {self.bonus_hit} pontos '
            f'(100%{EmojiEnum.DEXTERITY.value} + 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_hit(self) -> int:
        power = 1 + (self.level / 10)
        power = round(power, 2)
        bonus_hit = self.character.bs.dexterity * power

        return int(bonus_hit)

    @property
    def emoji(self) -> str:
        return '👃🏽'

    @property
    def function_text(self) -> str:
        return f'permanece com o *Olfato Apurado*.'


class InvestigationCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=BountyHunterSkillEnum.INVESTIGATION,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Analisa os oponentes para '
            f'aumentar o '
            f'*{HIT_EMOJI_TEXT}* '
            f'em {self.bonus_hit} pontos '
            f'e a '
            f'*{EVASION_EMOJI_TEXT}* '
            f'em {self.bonus_evasion} pontos '
            f'(100%{EmojiEnum.DEXTERITY.value} + 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_hit(self) -> int:
        power = 2 + (self.level / 10)
        power = round(power, 2)
        bonus_hit = self.character.bs.dexterity * power

        return int(bonus_hit)

    @property
    def bonus_evasion(self) -> int:
        power = 2 + (self.level / 10)
        power = round(power, 2)
        bonus_evasion = self.character.bs.dexterity * power

        return int(bonus_evasion)

    @property
    def emoji(self) -> str:
        return '🕵'

    @property
    def function_text(self) -> str:
        return f'permanece *Analisando* os oponentes.'


class ChampionInspirationCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=KnightSkillEnum.CHAMPION_INSPIRATION,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.trans_name}* que '
            f'aumenta o '
            f'*{PRECISION_ATTACK_EMOJI_TEXT}* '
            f'em {self.bonus_precision_attack} pontos e o '
            f'*{HIT_EMOJI_TEXT}* '
            f'em {self.bonus_hit} pontos '
            f'(100%{EmojiEnum.DEXTERITY.value} + 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_precision_attack(self) -> int:
        power = 1 + (self.level / 10)
        power = round(power, 2)
        bonus_precision_attack = self.character.bs.dexterity * power

        return int(bonus_precision_attack)

    @property
    def bonus_hit(self) -> int:
        power = 1 + (self.level / 10)
        power = round(power, 2)
        bonus_hit = self.character.bs.dexterity * power

        return int(bonus_hit)

    @property
    def emoji(self) -> str:
        return '🏆'

    @property
    def function_text(self) -> str:
        return f'permanece com a *{self.trans_name}*.'


class TurtleStanceCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=GladiatorSkillEnum.TURTLE_STANCE,
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
        return '🐢'

    @property
    def function_text(self) -> str:
        return f'permanece na *{self.trans_name}*.'


class UnicornStanceCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=GladiatorSkillEnum.UNICORN_STANCE,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Postura ofensiva que aumenta a *{PHYSICAL_ATTACK_EMOJI_TEXT}* '
            f'em {self.bonus_physical_attack} pontos '
            f'(200%{EmojiEnum.STRENGTH.value} + 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_physical_attack(self) -> int:
        power = 2 + (self.level / 10)
        power = round(power, 2)
        bonus_physical_attack = self.character.bs.strength * power

        return int(bonus_physical_attack)

    @property
    def emoji(self) -> str:
        return '🦄'

    @property
    def function_text(self) -> str:
        return f'permanece na *{self.trans_name}*.'


class ArenaDomainCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=GladiatorSkillEnum.ARENA_DOMAIN,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Estado de Fluxo* '
            f'que aumenta o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}*, '
            f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*, '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}*, '
            f'*{HIT_EMOJI_TEXT}* e '
            f'*{EVASION_EMOJI_TEXT}* '
            f'em {self.__power} pontos '
            f'(100%{EmojiEnum.STRENGTH.value} + '
            f'100%{EmojiEnum.CONSTITUTION.value} + '
            f'100%{EmojiEnum.WISDOM.value} + '
            f'100%{EmojiEnum.CHARACTER.value} '
            f'+ 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def __power(self) -> int:
        power = 1 + (self.level / 10)
        power = power * sum([
            self.character.bs.strength,
            self.character.bs.constitution,
            self.character.bs.wisdom,
            self.character.bs.charisma,
        ])
        power = round(power, 2)

        return int(power)

    @property
    def bonus_hit_points(self) -> int:
        return self.__power

    @property
    def bonus_physical_attack(self) -> int:
        return self.__power

    @property
    def bonus_physical_defense(self) -> int:
        return self.__power

    @property
    def bonus_hit(self) -> int:
        return self.__power

    @property
    def bonus_evasion(self) -> int:
        return self.__power

    @property
    def emoji(self) -> str:
        return '🏟'

    @property
    def function_text(self) -> str:
        return f'permanece com o *{self.trans_name}*.'


class ImproviseCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=MercenarySkillEnum.IMPROVISE,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Aprimoramento Improvisado* '
            f'que aumenta o '
            f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
            f'em {self.bonus_physical_attack} pontos '
            f'(100%{EmojiEnum.DEXTERITY.value} + 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_physical_attack(self) -> int:
        power = 1 + (self.level / 10)
        power = round(power, 2)
        bonus_physical_attack = self.character.bs.dexterity * power

        return int(bonus_physical_attack)

    @property
    def emoji(self) -> str:
        return '♻️🗡️'

    @property
    def function_text(self) -> str:
        return f'permanece com o *Aprimoramento Improvisado*.'


class SniffCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=RangerSkillEnum.SNIFF,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Fareja*, '
            f'aumentando o '
            f'*{HIT_EMOJI_TEXT}* '
            f'em {self.bonus_hit} pontos '
            f'(100%{EmojiEnum.DEXTERITY.value} + 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_hit(self) -> int:
        power = 1 + (self.level / 10)
        power = round(power, 2)
        bonus_hit = self.character.bs.dexterity * power

        return int(bonus_hit)

    @property
    def emoji(self) -> str:
        return '🐕‍🦺💨'

    @property
    def function_text(self) -> str:
        return f'permanece *Farejando*.'


class AlertCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=RangerSkillEnum.ALERT,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Estado de Alerta* que '
            f'aumenta o '
            f'*{PRECISION_ATTACK_EMOJI_TEXT}* '
            f'em {self.bonus_precision_attack} pontos e o '
            f'*{HIT_EMOJI_TEXT}* '
            f'em {self.bonus_hit} pontos '
            f'(200%{EmojiEnum.DEXTERITY.value} + 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_precision_attack(self) -> int:
        power = 2 + (self.level / 10)
        power = round(power, 2)
        bonus_precision_attack = self.character.bs.dexterity * power

        return int(bonus_precision_attack)

    @property
    def bonus_hit(self) -> int:
        power = 2 + (self.level / 10)
        power = round(power, 2)
        bonus_hit = self.character.bs.dexterity * power

        return int(bonus_hit)

    @property
    def emoji(self) -> str:
        return '🐕‍🦺🚨'

    @property
    def function_text(self) -> str:
        return f'permanece em *Estado de Alerta*.'


class HrungnirsSovereigntyCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 10,
        level: int = 1
    ):
        super().__init__(
            name=BerserkirSkillEnum.HRUNGNIRÇÇÇS_SOVEREIGNTY,
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Estado de *Fúria Desenfreada* que aumenta o '
            f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
            f'em {self.bonus_physical_attack} pontos '
            f'(200%{EmojiEnum.STRENGTH.value} + 10% x Nível) '
            f'por {self.turn} turno(s).'
        )

    @property
    def bonus_physical_attack(self) -> int:
        power = 2 + (self.level / 10)
        power = round(power, 2)
        bonus_physical_attack = self.character.bs.strength * power

        return int(bonus_physical_attack)

    @property
    def emoji(self) -> str:
        return '👺🔨'

    @property
    def function_text(self) -> str:
        return f'permanece envolto por *{self.trans_name}*.'


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

    name = 'Fake Char'
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
        ShadowStepsCondition,
        ChaoticStepsCondition,
        PenitenceCondition,
        MysticBlockCondition,
        SharpFaroCondition,
        InvestigationCondition,
        ChampionInspirationCondition,
        TurtleStanceCondition,
        UnicornStanceCondition,
        ArenaDomainCondition,
        ImproviseCondition,
        SniffCondition,
        AlertCondition,
        HrungnirsSovereigntyCondition,
    ]

    def __iter__(self) -> Iterable[SelfSkillCondition]:
        for condition_class in self.__list:
            yield condition_class(character=FakeCharacter())


SELF_BUFFS: Iterable[SelfSkillCondition] = SelfBuffs()


if __name__ == '__main__':
    from rpgram.constants.test import BASE_CHARACTER
    from rpgram.conditions.factory import condition_factory

    for condition in SelfBuffs():
        print(condition)
        print(condition.to_dict())
        _dict = {'character': BASE_CHARACTER, **condition.to_dict()}
        _dict.pop('need_character')
        assert condition_factory(**_dict) == condition

    # for condition in SelfBuffs():
    #     print(condition.function(BASE_CHARACTER)['text'])
