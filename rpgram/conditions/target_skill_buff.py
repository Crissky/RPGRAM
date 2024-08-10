''' Módulo com as Condições do tipo de Target diferente de SELF
    Essas Condições usam o power fornecido no momendo da instância
'''


from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Iterable, Union

from bson import ObjectId
from rpgram.conditions.buff import BuffCondition
from rpgram.constants.text import (
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    HIT_POINT_FULL_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    BardSkillEnum,
    ClericSkillEnum,
    DruidSkillEnum,
    DuelistSkillEnum,
    PaladinSkillEnum,
    WarriorSkillEnum
)
from rpgram.enums.turn import TurnEnum


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class TargetSkillBuffCondition(BuffCondition):

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


class WarBannerCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=WarriorSkillEnum.WAR_BANNER,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Marca do Senhor da Guerra* que aumenta o '
            f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*, '
            f'*{PRECISION_ATTACK_EMOJI_TEXT}* e '
            f'*{MAGICAL_ATTACK_EMOJI_TEXT}* em {self.power} pontos.'
        )

    @property
    def bonus_physical_attack(self) -> int:
        return self.power

    @property
    def bonus_precision_attack(self) -> int:
        return self.power

    @property
    def bonus_magical_attack(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🚩'

    @property
    def function_text(self) -> str:
        return 'permanece com a *Marca do Senhor da Guerra*.'


class IdunnsAppleCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=ClericSkillEnum.IDUNNÇÇÇS_APPLE,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Beção de Idunn* que aumenta o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}* em {self.power} pontos.'
        )

    @property
    def bonus_hit_points(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🍎'

    @property
    def function_text(self) -> str:
        return 'permanece abençoado por *Idunn*.'

    @property
    def power(self) -> int:
        power_multiplier = 2 + (self.level / 5)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)


class KratossWrathCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=ClericSkillEnum.KRATOSÇÇÇS_WRATH,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Ira do Deus Grego da Guerra* que aumenta o '
            f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* em {self.power} pontos.'
        )

    @property
    def bonus_physical_attack(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '😡'

    @property
    def function_text(self) -> str:
        return 'permanece com a *Ira do Deus Grego da Guerra*.'


class UllrsFocusCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=ClericSkillEnum.ULLRÇÇÇS_FOCUS,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Benção de Ullr* que aumenta o '
            f'*{PRECISION_ATTACK_EMOJI_TEXT}* em {self.power} pontos.'
        )

    @property
    def bonus_precision_attack(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🦌'

    @property
    def function_text(self) -> str:
        return 'permanece com a *Benção de Ullr*.'


class HecatesFlamesCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=ClericSkillEnum.HECATEÇÇÇS_FLAMES,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Fagulhas da Tocha de Hécate* que aumentam o '
            f'*{MAGICAL_ATTACK_EMOJI_TEXT}* em {self.power} pontos.'
        )

    @property
    def bonus_magical_attack(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🗽'

    @property
    def function_text(self) -> str:
        return 'permanece com as *Fagulhas da Tocha de Hécate*.'


class OgunsCloakCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=ClericSkillEnum.OGUNÇÇÇS_CLOAK,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Fragmentos de Metal dos Deuses* que aumentam a '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* em {self.power} pontos.'
        )

    @property
    def bonus_physical_defense(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '⛓️‍💥'

    @property
    def function_text(self) -> str:
        return 'permanece com os *Fragmentos de Metal dos Deuses*.'


class IsissVeilCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=ClericSkillEnum.ISISÇÇÇS_VEIL,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Névoa Resplandecente de Energia Divina* que aumenta a '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* em {self.power} pontos.'
        )

    @property
    def bonus_magical_defense(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🌌'

    @property
    def function_text(self) -> str:
        return 'permanece com a *Névoa Resplandecente de Energia Divina*.'


class AnansisTrickeryCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=ClericSkillEnum.ANANSIÇÇÇS_TRICKERY,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Teia de Ilusões* que aumenta o '
            f'*{HIT_EMOJI_TEXT}* e a *{EVASION_EMOJI_TEXT}* '
            f'em {self.power} pontos.'
        )

    @property
    def bonus_hit(self) -> int:
        return self.power

    @property
    def bonus_evasion(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🕸️'

    @property
    def function_text(self) -> str:
        return 'permanece com a *Teia de Ilusões*.'


class VidarsBraveryCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=ClericSkillEnum.VIDARÇÇÇS_BRAVERY,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Bravura Indomita* de um antigo *Guerreiro Silencioso* '
            f'que aumenta o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}*, '
            f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* e a '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.power} pontos.'
        )

    @property
    def bonus_hit_points(self) -> int:
        return self.power

    @property
    def bonus_physical_attack(self) -> int:
        return self.power

    @property
    def bonus_physical_defense(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🇻'

    @property
    def function_text(self) -> str:
        return 'permanece com a *Bravura Indomita*.'


class ArtemissArrowCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=ClericSkillEnum.ARTEMISÇÇÇS_ARROW,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Flecha Lunar* da *Deusa da Lua* que aumenta o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}*, '
            f'*{PRECISION_ATTACK_EMOJI_TEXT}*, '
            f'*{HIT_EMOJI_TEXT}* e a '
            f'*{EVASION_EMOJI_TEXT}* '
            f'em {self.power} pontos.'
        )

    @property
    def bonus_hit_points(self) -> int:
        return self.power

    @property
    def bonus_precision_attack(self) -> int:
        return self.power

    @property
    def bonus_hit(self) -> int:
        return self.power

    @property
    def bonus_evasion(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🌙'

    @property
    def function_text(self) -> str:
        return 'permanece afetado pela *Flecha Lunar*.'


class CeridwensMagicPotionCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=ClericSkillEnum.CERIDWENÇÇÇS_MAGIC_POTION,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Poção Mágica* da *Deusa Feiticeira* que aumenta o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}*, '
            f'*{MAGICAL_ATTACK_EMOJI_TEXT}* e a '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.power} pontos.'
        )

    @property
    def bonus_hit_points(self) -> int:
        return self.power

    @property
    def bonus_magical_attack(self) -> int:
        return self.power

    @property
    def bonus_magical_defense(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🧉'

    @property
    def function_text(self) -> str:
        return 'permanece sob os efeitos da *Poção Mágica*.'


class GraceOfThePantheonCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=ClericSkillEnum.GRACE_OF_THE_PANTHEON,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Fragmento da *{self.enum_name.value}* '
            f'que aumenta o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}*, '
            f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*, '
            f'*{PRECISION_ATTACK_EMOJI_TEXT}*, '
            f'*{MAGICAL_ATTACK_EMOJI_TEXT}*, '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}*, '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}*, '
            f'*{HIT_EMOJI_TEXT}* e a '
            f'*{EVASION_EMOJI_TEXT}* '
            f'em {self.power} pontos.'
        )

    @property
    def bonus_hit_points(self) -> int:
        return self.power

    @property
    def bonus_physical_attack(self) -> int:
        return self.power

    @property
    def bonus_precision_attack(self) -> int:
        return self.power

    @property
    def bonus_magical_attack(self) -> int:
        return self.power

    @property
    def bonus_physical_defense(self) -> int:
        return self.power

    @property
    def bonus_magical_defense(self) -> int:
        return self.power

    @property
    def bonus_hit(self) -> int:
        return self.power

    @property
    def bonus_evasion(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🏛️'

    @property
    def function_text(self) -> str:
        return f'permanece sob a *{self.enum_name.value}*.'

    @property
    def power(self) -> int:
        power_multiplier = 2 + (self.level / 10)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)


class RangerFalconCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DruidSkillEnum.RANGER_FALCON,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que o vigia, '
            f'aumentando o '
            f'*{HIT_EMOJI_TEXT}* e a '
            f'*{EVASION_EMOJI_TEXT}* '
            f'em {self.power} pontos.'
        )

    @property
    def bonus_hit(self) -> int:
        return self.power

    @property
    def bonus_evasion(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🚨🦅'

    @property
    def function_text(self) -> str:
        return f'permanece vigiado pelo *{self.enum_name.value}*.'


class BodyguardBearCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DruidSkillEnum.GUARDIAN_BEAR,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que o protege, '
            f'aumentando o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}* e a '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.power} pontos.'
        )

    @property
    def bonus_hit_points(self) -> int:
        return self.power

    @property
    def bonus_physical_defense(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🛡️🐻'

    @property
    def function_text(self) -> str:
        return f'permanece protegido pelo *{self.enum_name.value}*.'


class HunterTigerCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DruidSkillEnum.HUNTER_TIGER,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que persegue ao seu lado, '
            f'aumentando o '
            f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* e o '
            f'*{PRECISION_ATTACK_EMOJI_TEXT}* '
            f'em {self.power} pontos.'
        )

    @property
    def bonus_physical_attack(self) -> int:
        return self.power

    @property
    def bonus_precision_attack(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '💪🐯'

    @property
    def function_text(self) -> str:
        return f'permanece caçando com o *{self.enum_name.value}*.'


class WatcherOwlCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DruidSkillEnum.WATCHER_OWL,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que observa o plano místico, '
            f'aumentando o '
            f'*{MAGICAL_ATTACK_EMOJI_TEXT}* e o '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.power} pontos.'
        )

    @property
    def bonus_magical_attack(self) -> int:
        return self.power

    @property
    def bonus_magical_defense(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🔮🦉'

    @property
    def function_text(self) -> str:
        return f'permanece observando com a *{self.enum_name.value}*.'


class VineBucklerCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DruidSkillEnum.VINE_BUCKLER,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que aumenta a '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.bonus_magical_defense} pontos e a '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.bonus_physical_defense} pontos.'
        )

    @property
    def bonus_physical_defense(self) -> int:
        return int(self.power / 2)

    @property
    def bonus_magical_defense(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🛡🍇'

    @property
    def function_text(self) -> str:
        return f'permanece equipado com o *{self.enum_name.value}*.'


class SilkFlossSpaulderCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DruidSkillEnum.SILK_FLOSS_SPAULDER,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que aumenta o '
            f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
            f'em {self.bonus_physical_attack} pontos e a '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.bonus_magical_defense} pontos.'
        )

    @property
    def bonus_physical_attack(self) -> int:
        return self.power

    @property
    def bonus_magical_defense(self) -> int:
        return int(self.power / 2)

    @property
    def emoji(self) -> str:
        return '🌵🍇'

    @property
    def function_text(self) -> str:
        return f'permanece equipado com o *{self.enum_name.value}*.'

    @property
    def power(self) -> int:
        power_multiplier = 2 + (self.level / 10)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)


class OakArmorCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DruidSkillEnum.OAK_ARMOR,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que aumenta a '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.bonus_magical_defense} pontos e a '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.bonus_physical_defense} pontos.'
        )

    @property
    def bonus_physical_defense(self) -> int:
        return int(self.power / 2)

    @property
    def bonus_magical_defense(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return EmojiEnum.ARMOR.value + '🍇'

    @property
    def function_text(self) -> str:
        return f'permanece equipado com o *{self.enum_name.value}*.'

    @property
    def power(self) -> int:
        power_multiplier = 3 + (self.level / 10)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)


class SquireAnointingCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=PaladinSkillEnum.SQUIRE_ANOINTING,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que aumenta a '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.bonus_physical_defense} pontos e o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
            f'em {self.bonus_hit_points} pontos.'
        )

    @property
    def bonus_physical_defense(self) -> int:
        return self.power

    @property
    def bonus_hit_points(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return EmojiEnum.SHIELD.value + '🪔'

    @property
    def function_text(self) -> str:
        return f'permanece com a *{self.enum_name.value}*.'


class WarriorAnointingCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=PaladinSkillEnum.WARRIOR_ANOINTING,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que aumenta o '
            f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
            f'em {self.bonus_physical_attack} pontos, o '
            f'*{PRECISION_ATTACK_EMOJI_TEXT}* '
            f'em {self.bonus_precision_attack} pontos e o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
            f'em {self.bonus_hit_points} pontos.'
        )

    @property
    def bonus_physical_attack(self) -> int:
        return self.power

    @property
    def bonus_precision_attack(self) -> int:
        return self.power

    @property
    def bonus_hit_points(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return EmojiEnum.SWORD.value + '🪔'

    @property
    def function_text(self) -> str:
        return f'permanece com a *{self.enum_name.value}*.'


class MaidenAnointingCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=PaladinSkillEnum.MAIDEN_ANOINTING,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que aumenta a '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.bonus_magical_defense} pontos e o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
            f'em {self.bonus_hit_points} pontos.'
        )

    @property
    def bonus_magical_defense(self) -> int:
        return self.power

    @property
    def bonus_hit_points(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return EmojiEnum.CLOAK.value + '🪔'

    @property
    def function_text(self) -> str:
        return f'permanece com a *{self.enum_name.value}*.'


class KnightAnointingCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=PaladinSkillEnum.KNIGHT_ANOINTING,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que aumenta o '
            f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
            f'em {self.bonus_physical_attack} pontos, o '
            f'*{PRECISION_ATTACK_EMOJI_TEXT}* '
            f'em {self.bonus_precision_attack} pontos, a '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.bonus_physical_defense} pontos e o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
            f'em {self.bonus_hit_points} pontos.'
        )

    @property
    def bonus_physical_attack(self) -> int:
        return self.power

    @property
    def bonus_precision_attack(self) -> int:
        return self.power

    @property
    def bonus_physical_defense(self) -> int:
        return self.power

    @property
    def bonus_hit_points(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return EmojiEnum.KNIGHT.value + '🪔'

    @property
    def function_text(self) -> str:
        return f'permanece com a *{self.enum_name.value}*.'

    @property
    def power(self) -> int:
        power_multiplier = 2 + (self.level / 10)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)


class CourtesanAnointingCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=PaladinSkillEnum.COURTESAN_ANOINTING,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que aumenta a '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.bonus_physical_defense} pontos, a '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.bonus_magical_defense} pontos e o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
            f'em {self.bonus_hit_points} pontos.'
        )

    @property
    def bonus_physical_defense(self) -> int:
        return self.power

    @property
    def bonus_magical_defense(self) -> int:
        return self.power

    @property
    def bonus_hit_points(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return EmojiEnum.COURTESAN.value + '🪔'

    @property
    def function_text(self) -> str:
        return f'permanece com a *{self.enum_name.value}*.'

    @property
    def power(self) -> int:
        power_multiplier = 2 + (self.level / 10)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)


class LordAnointingCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=PaladinSkillEnum.LORD_ANOINTING,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que aumenta o '
            f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
            f'em {self.bonus_physical_attack} pontos, o '
            f'*{PRECISION_ATTACK_EMOJI_TEXT}* '
            f'em {self.bonus_precision_attack} pontos, a '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
            f'em {self.bonus_magical_defense} pontos e o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
            f'em {self.bonus_hit_points} pontos.'
        )

    @property
    def bonus_physical_attack(self) -> int:
        return self.power

    @property
    def bonus_precision_attack(self) -> int:
        return self.power

    @property
    def bonus_magical_defense(self) -> int:
        return self.power

    @property
    def bonus_hit_points(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return EmojiEnum.LORD.value + '🪔'

    @property
    def function_text(self) -> str:
        return f'permanece com a *{self.enum_name.value}*.'

    @property
    def power(self) -> int:
        power_multiplier = 2 + (self.level / 10)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)


class AgileFeetCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DuelistSkillEnum.AGILE_FEET,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* amplifica a capacidade de se esquivar '
            f'dos ataques dos opoenentes, aumentando a '
            f'*{EVASION_EMOJI_TEXT}* '
            f'em {self.bonus_evasion} pontos.'
        )

    @property
    def bonus_evasion(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🩰'

    @property
    def function_text(self) -> str:
        return f'permanece com os *{self.enum_name.value}*.'


class EagleEyeCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DuelistSkillEnum.EAGLE_EYE,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* amplifica a capacidade de analisar '
            f'o combate, aumentando o '
            f'*{HIT_EMOJI_TEXT}* '
            f'em {self.bonus_hit} pontos.'
        )

    @property
    def bonus_hit(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🦅👁️'

    @property
    def function_text(self) -> str:
        return (
            f'permanece analisando o combate com o *{self.enum_name.value}*.'
        )


class WarSongCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=BardSkillEnum.WAR_SONG,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que inspira o alvo, '
            f'aumentando o '
            f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*, '
            f'*{PRECISION_ATTACK_EMOJI_TEXT}*, '
            f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* e o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
            f'em {self.power} pontos.'
        )

    @property
    def bonus_physical_attack(self) -> int:
        return self.power

    @property
    def bonus_precision_attack(self) -> int:
        return self.power

    @property
    def bonus_physical_defense(self) -> int:
        return self.power

    @property
    def bonus_hit_points(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🎶⚔️'

    @property
    def function_text(self) -> str:
        return (
            f'permanece inspirado pela *{self.enum_name.value}*.'
        )


class CrescentMoonSongCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=BardSkillEnum.CRESCENT_MOON_SONG,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que inspira o alvo, '
            f'aumentando o '
            f'*{MAGICAL_ATTACK_EMOJI_TEXT}*, '
            f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* e o '
            f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
            f'em {self.power} pontos.'
        )

    @property
    def bonus_magical_attack(self) -> int:
        return self.power

    @property
    def bonus_magical_defense(self) -> int:
        return self.power

    @property
    def bonus_hit_points(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🎶🌙'

    @property
    def function_text(self) -> str:
        return (
            f'permanece inspirado pela *{self.enum_name.value}*.'
        )


class TargetBuffs:
    __list = [
        WarBannerCondition,
        IdunnsAppleCondition,
        KratossWrathCondition,
        UllrsFocusCondition,
        HecatesFlamesCondition,
        OgunsCloakCondition,
        IsissVeilCondition,
        AnansisTrickeryCondition,
        VidarsBraveryCondition,
        ArtemissArrowCondition,
        CeridwensMagicPotionCondition,
        GraceOfThePantheonCondition,
        RangerFalconCondition,
        BodyguardBearCondition,
        HunterTigerCondition,
        WatcherOwlCondition,
        VineBucklerCondition,
        SilkFlossSpaulderCondition,
        OakArmorCondition,
        SquireAnointingCondition,
        WarriorAnointingCondition,
        MaidenAnointingCondition,
        KnightAnointingCondition,
        CourtesanAnointingCondition,
        LordAnointingCondition,
        AgileFeetCondition,
        EagleEyeCondition,
        WarSongCondition,
        CrescentMoonSongCondition,
    ]

    def __iter__(self) -> Iterable[TargetSkillBuffCondition]:
        for condition_class in self.__list:
            yield condition_class(power=100)


TARGET_BUFFS: Iterable[TargetSkillBuffCondition] = TargetBuffs()


if __name__ == '__main__':
    from rpgram.conditions.factory import condition_factory
    from rpgram.constants.test import BASE_CHARACTER

    for condition in TargetBuffs():
        print(condition)
        print(condition.to_dict())
        assert condition_factory(**condition.to_dict()) == condition

    # for condition in TargetBuffs():
    #     print(condition.function(BASE_CHARACTER)['text'])
