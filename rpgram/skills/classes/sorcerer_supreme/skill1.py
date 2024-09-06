from typing import TYPE_CHECKING
from rpgram.constants.text import (
    HIT_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    SkillDefenseEnum,
    SkillTypeEnum,
    SorcererSupremeSkillEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class MagicOrbSkill(BaseSkill):
    NAME = SorcererSupremeSkillEnum.MAGIC_ORB.value
    DESCRIPTION = (
        f'Conjura uma *Esfera de Energia* pura e destrutiva que flutua '
        f'diante do conjurador e irrompe contra o inimigo, '
        f'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.MAGIC)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (155% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.SORCERER_SUPREME.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.55,
        }
        damage_types = [DamageEnum.MAGIC]

        super().__init__(
            name=MagicOrbSkill.NAME,
            description=MagicOrbSkill.DESCRIPTION,
            rank=MagicOrbSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=MagicOrbSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.90


SKILL_WAY_DESCRIPTION = {
    'name': '',
    'description': (
        ''
    ),
    'skill_list': []
}


if __name__ == '__main__':
    from rpgram.constants.test import SORCERER_SUPREME_CHARACTER
    skill = MagicOrbSkill(SORCERER_SUPREME_CHARACTER)
    print(skill)
    print(SORCERER_SUPREME_CHARACTER.cs.magical_attack)
    SORCERER_SUPREME_CHARACTER.skill_tree.learn_skill(MagicOrbSkill)
