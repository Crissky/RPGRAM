
from typing import TYPE_CHECKING
from rpgram.conditions.debuff import PoisoningCondition
from rpgram.constants.text import (
    HIT_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    RogueSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.classes.multiclasse.precision_attack import (
    QuickAttackSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Mestre dos Assassinos',
    'description': (
        'Mestre na morte, um predador que opera nas sombras. '
        'Sua vida é dedicada à perfeição da arte do assassinato, '
        'e ele possui uma habilidade inigualável para eliminar seus alvos '
        'de forma silenciosa e eficiente.'
        'O Mestre dos Assassinos é um artífice da morte, '
        'capaz de eliminar seus inimigos, utilizando o fio da lâmina e '
        'venenos letais para infligir feridas fatais.'
    ),
    'skill_list': [
        QuickAttackSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import LORD_OF_THE_ROGUES_CHARACTER

    skill = QuickAttackSkill(LORD_OF_THE_ROGUES_CHARACTER)
    print(skill)
    print(LORD_OF_THE_ROGUES_CHARACTER.cs.precision_attack)
    print(LORD_OF_THE_ROGUES_CHARACTER.to_attack(
        defender_char=LORD_OF_THE_ROGUES_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    LORD_OF_THE_ROGUES_CHARACTER.skill_tree.learn_skill(QuickAttackSkill)
