from typing import TYPE_CHECKING
from rpgram.constants.text import MAGICAL_ATTACK_EMOJI_TEXT
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    MultiClasseSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    SorcererSkillEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class FireBallSkill(BaseSkill):
    NAME = MultiClasseSkillEnum.FIRE_BALL.value
    DESCRIPTION = (
        f'Com movimentos incisivos, conjura uma *Bola de Fogo* e a lança '
        f'contra um alvo, causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name_list': [
            ClasseEnum.MAGE.value,
            ClasseEnum.ARCANIST.value
        ],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.FIRE]

        super().__init__(
            name=FireBallSkill.NAME,
            description=FireBallSkill.DESCRIPTION,
            rank=FireBallSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=FireBallSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class WaterBubbleSkill(BaseSkill):
    NAME = MultiClasseSkillEnum.WATER_BUBBLE.value
    DESCRIPTION = (
        f'Com movimentos suaves, conjura uma *Bolha de Água* e a lança '
        f'contra um alvo, causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.WATER)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name_list': [
            ClasseEnum.MAGE.value,
            ClasseEnum.ARCANIST.value
        ],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.WATER]

        super().__init__(
            name=WaterBubbleSkill.NAME,
            description=WaterBubbleSkill.DESCRIPTION,
            rank=WaterBubbleSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=WaterBubbleSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class WindGustSkill(BaseSkill):
    NAME = MultiClasseSkillEnum.WIND_GUST.value
    DESCRIPTION = (
        f'Com movimentos undosos, conjura uma *Rajada de Vento* que vai de '
        f'encontro ao alvo, causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.WIND)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name_list': [
            ClasseEnum.MAGE.value,
            ClasseEnum.ARCANIST.value
        ],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.WIND]

        super().__init__(
            name=WindGustSkill.NAME,
            description=WindGustSkill.DESCRIPTION,
            rank=WindGustSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=WindGustSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class EarthBreakSkill(BaseSkill):
    NAME = MultiClasseSkillEnum.EARTH_BREAK.value
    DESCRIPTION = (
        f'Com um movimento brusco, *Quebra-Terra* '
        f'debaixo de um alvo, causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.GROUND)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name_list': [
            ClasseEnum.MAGE.value,
            ClasseEnum.ARCANIST.value
        ],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.GROUND]

        super().__init__(
            name=EarthBreakSkill.NAME,
            description=EarthBreakSkill.DESCRIPTION,
            rank=EarthBreakSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=EarthBreakSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class PrismaticShotSkill(BaseSkill):
    NAME = MultiClasseSkillEnum.PRISMATIC_SHOT.value
    DESCRIPTION = (
        f'Canaliza a *Energia Mágica* e dispara um *Feixe Prismático*, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.LIGHT)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name_list': [
            ClasseEnum.ARCANIST.value,
            ClasseEnum.SORCERER.value
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.LIGHT]

        super().__init__(
            name=PrismaticShotSkill.NAME,
            description=PrismaticShotSkill.DESCRIPTION,
            rank=PrismaticShotSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=PrismaticShotSkill.REQUIREMENTS,
            damage_types=damage_types
        )
