from rpgram.skills.classes.warrior.skill1 import PowerfulAttackSkill
from rpgram.skills.classes.warrior.skill2 import LethalAttackSkill, QuickAttackSkill
from rpgram.skills.skill_base import BaseSkill


def warrior_skill_factory(skill_class_name: str) -> BaseSkill:
    # SKILL1
    if skill_class_name == PowerfulAttackSkill.__name__:
        return PowerfulAttackSkill
    # SKILL2
    elif skill_class_name == QuickAttackSkill.__name__:
        return QuickAttackSkill
    elif skill_class_name == LethalAttackSkill.__name__:
        return LethalAttackSkill


WARRIOR_SKILL_LIST = [
    # SKILL1
    PowerfulAttackSkill,

    # SKILL2
    QuickAttackSkill,
    LethalAttackSkill,
]
