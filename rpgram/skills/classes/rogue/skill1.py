
from typing import TYPE_CHECKING
from rpgram.constants.text import (
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    RogueSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Assassino Letal',
    'description': (
        ''
    )
}


class VipersFangSkill(BaseSkill):
    NAME = RogueSkillEnum.VIPERÇÇÇS_FANGS.value
    DESCRIPTION = (
        f'Com um movimento rápido, golpeia o inimigo usando uma arma '
        f'imbuída de *Veneno*, causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.POISON)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.ROGUE.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.POISON]

        super().__init__(
            name=VipersFangSkill.NAME,
            description=VipersFangSkill.DESCRIPTION,
            rank=VipersFangSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=VipersFangSkill.REQUIREMENTS,
            damage_types=damage_types
        )


if __name__ == '__main__':
    from rpgram.constants.test import ROGUE_CHARACTER

    skill = VipersFangSkill(ROGUE_CHARACTER)
    print(skill)
    print(ROGUE_CHARACTER.cs.physical_attack)
    print(ROGUE_CHARACTER.to_attack(
        defender_char=ROGUE_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ROGUE_CHARACTER.skill_tree.learn_skill(VipersFangSkill)
