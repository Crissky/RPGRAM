from typing import TYPE_CHECKING
from rpgram.conditions.debuff import BlindnessCondition
from rpgram.conditions.target_skill_debuff import MuddyCondition
from rpgram.constants.text import EVASION_EMOJI_TEXT, MAGICAL_ATTACK_EMOJI_TEXT
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.skill import (
    ArcanistSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.classes.multiclasse.magical_attack import (
    EarthBreakSkill,
    FireBallSkill,
    PrismaticShotSkill,
    WaterBubbleSkill,
    WindGustSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Arcano Crepúscular',
    'description': (
        'O Arcano Crepúscular possui uma alma intrinsecamente ligada aos '
        'elementos Luz e Trevas. '
        'Ele é um canal, um condutor de forças essenciais que '
        'moldam a realidade. '
        'Sua compreensão dos elementos não se limita a simples '
        'manipulação; ele os sente, os compreende e os respeita.'
    ),
    'skill_list': [
        PrismaticShotSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import ARCANIST_CHARACTER

    skill = PrismaticShotSkill(ARCANIST_CHARACTER)
    print(skill)
    print(ARCANIST_CHARACTER.cs.magical_attack)
    print(ARCANIST_CHARACTER.to_attack(
        defender_char=ARCANIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ARCANIST_CHARACTER.skill_tree.learn_skill(PrismaticShotSkill)
