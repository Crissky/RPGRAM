from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.debuff import (
    BleedingCondition,
    ImprisonedCondition
)
from rpgram.conditions.self_skill import (
    InvestigationCondition,
    SharpFaroCondition
)
from rpgram.constants.text import (
    DEXTERITY_EMOJI_TEXT,
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    BountyHunterSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class GlowBurstSkill(BaseSkill):
    NAME = BountyHunterSkillEnum.GLOW_BURST.value
    DESCRIPTION = (
        f'Lança no alvo um *Estouro Brilhante* que irrompe em uma '
        f'*Explosão Fúlgida*, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLAST)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.LIGHT)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BOUNTY_HUNTER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.BLAST, DamageEnum.LIGHT]

        super().__init__(
            name=GlowBurstSkill.NAME,
            description=GlowBurstSkill.DESCRIPTION,
            rank=GlowBurstSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=GlowBurstSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class GlowBurstVolleySkill(BaseSkill):
    NAME = BountyHunterSkillEnum.GLOW_BURST_VOLLEY.value
    DESCRIPTION = (
        f'Lança uma enxurrada de *Estouros Brilhantes* '
        f'que irrompem em várias *Explosões Fúlgidas*, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLAST)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.LIGHT)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (75% + 2.5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BOUNTY_HUNTER.value,
        'skill_list': [GlowBurstSkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 0.75,
        }
        damage_types = [DamageEnum.BLAST, DamageEnum.LIGHT]

        super().__init__(
            name=GlowBurstVolleySkill.NAME,
            description=GlowBurstVolleySkill.DESCRIPTION,
            rank=GlowBurstVolleySkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=GlowBurstVolleySkill.REQUIREMENTS,
            damage_types=damage_types
        )


class GigaGlowBurstSkill(BaseSkill):
    NAME = BountyHunterSkillEnum.GIGA_GLOW_BURST.value
    DESCRIPTION = (
        f'Lança um *Estouro Brilhante Gigante* '
        f'que irrompe em uma imensa *Explosão Fúlgida*, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLAST)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.LIGHT)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (400% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.BOUNTY_HUNTER.value,
        'skill_list': [GlowBurstSkill.NAME, GlowBurstVolleySkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 4.00,
        }
        damage_types = [DamageEnum.BLAST, DamageEnum.LIGHT]

        super().__init__(
            name=GigaGlowBurstSkill.NAME,
            description=GigaGlowBurstSkill.DESCRIPTION,
            rank=GigaGlowBurstSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=GigaGlowBurstSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.75


SKILL_WAY_DESCRIPTION = {
    'name': 'Senhor Bélico',
    'description': (
        'Senhor Bélico é a personificação da força marcial pura, '
        'uma figura indomável nas artes de combate e na '
        'liderança em batalhas. '
        'Através de técnicas de guerra ancestrais, '
        'ele domina o campo de batalha com uma presença avassaladora, '
        'guiado por instintos aguçados e uma habilidade '
        'incomparável de controle. '
        'Seu arsenal inclui armadilhas brutais, '
        'emboscadas precisas e táticas que exploram fraquezas, '
        'transformando qualquer ambiente em uma arena sob seu comando.'
    ),
    'skill_list': [
        GlowBurstSkill,
        GlowBurstVolleySkill,
        GigaGlowBurstSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import BOUNTY_HUNTER_CHARACTER

    skill = GlowBurstSkill(BOUNTY_HUNTER_CHARACTER)
    print(skill)
    print(BOUNTY_HUNTER_CHARACTER.cs.physical_attack)
    print(BOUNTY_HUNTER_CHARACTER.to_attack(
        defender_char=BOUNTY_HUNTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BOUNTY_HUNTER_CHARACTER.skill_tree.learn_skill(GlowBurstSkill)

    skill = GlowBurstVolleySkill(BOUNTY_HUNTER_CHARACTER)
    print(skill)
    print(BOUNTY_HUNTER_CHARACTER.cs.physical_attack)
    print(BOUNTY_HUNTER_CHARACTER.to_attack(
        defender_char=BOUNTY_HUNTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BOUNTY_HUNTER_CHARACTER.skill_tree.learn_skill(GlowBurstVolleySkill)

    skill = GigaGlowBurstSkill(BOUNTY_HUNTER_CHARACTER)
    print(skill)
    print(BOUNTY_HUNTER_CHARACTER.cs.physical_attack)
    print(BOUNTY_HUNTER_CHARACTER.to_attack(
        defender_char=BOUNTY_HUNTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BOUNTY_HUNTER_CHARACTER.skill_tree.learn_skill(GigaGlowBurstSkill)
