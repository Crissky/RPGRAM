from typing import TYPE_CHECKING
from rpgram.constants.text import HIT_EMOJI_TEXT, PRECISION_ATTACK_EMOJI_TEXT
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    DuelistSkillEnum,
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
    'name': 'Jogo Sujo',
    'description': (
        ''
    ),
    'skill_list': []
}


if __name__ == '__main__':
    from rpgram.constants.test import DUELIST_CHARACTER
