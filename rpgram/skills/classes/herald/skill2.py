from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.self_skill import MysticBlockCondition
from rpgram.constants.text import (
    CONSTITUTION_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    HeraldSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.classes.multiclasse.physical_defense import (
    GuardianShieldSkill,
    HeavyChargeSkill,
    RobustBlockSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Vigia das Chamas',
    'description': (
        'Um bastião ardente que utiliza o fogo como símbolo de proteção, '
        'purificação e justiça. '
        'Neste caminho, o Arauto manipula chamas sagradas para proteger '
        'seus aliados e devastar aqueles que ameaçam o equilíbrio. '
        'Suas habilidades mesclam ofensiva e defensiva, '
        'transformando o fogo em um aliado fiel que incinera o mal e aquece '
        'o coração dos justos.'
    ),
    'skill_list': [
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import HERALD_CHARACTER
