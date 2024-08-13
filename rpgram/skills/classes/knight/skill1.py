from typing import TYPE_CHECKING

from rpgram.constants.text import (
    HIT_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    KnightSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class ChargeSkill(BaseSkill):
    NAME = KnightSkillEnum.CHARGE.value
    DESCRIPTION = (
        f'Impulsiona-se sobre o inimigo com *Grande Velocidade*, '
        f'tornando-se uma força imparável no campo de batalha e '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* e '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (200% + 5% x Rank x Nível). '
        f'Essa habilidade possui baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.KNIGHT.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 2.00,
        }
        damage_types = None

        super().__init__(
            name=ChargeSkill.NAME,
            description=ChargeSkill.DESCRIPTION,
            rank=ChargeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=ChargeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.75


SKILL_WAY_DESCRIPTION = {
    'name': 'Campeão',
    'description': (
        'O Campeão é um símbolo de esperança, '
        'um defensor dos fracos e da justiça. '
        'Sua força e habilidade com armas são lendárias, '
        'mas o seu espírito indomável e a sua devoção à causa '
        'são o que o definem. '
        'O Campeão é um líder nato, '
        'capaz de inspirar seus aliados e derrotar seus inimigos.'
    ),
    'skill_list': [
        ChargeSkill
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import KNIGHT_CHARACTER

    skill = ChargeSkill(KNIGHT_CHARACTER)
    print(skill)
    print(KNIGHT_CHARACTER.cs.precision_attack)
    print(KNIGHT_CHARACTER.to_attack(
        defender_char=KNIGHT_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    KNIGHT_CHARACTER.skill_tree.learn_skill(ChargeSkill)
