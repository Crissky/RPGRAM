from rpgram.skills.classes.guardian.skill1 import RobustBlockSkill
from rpgram.skills.classes.guardian.skill2 import HeavyChargeSkill
from rpgram.skills.skill_base import BaseSkill


def guardian_skill_factory(skill_class_name: str) -> BaseSkill:
    # SKILL1
    if skill_class_name == RobustBlockSkill.__name__:
        return RobustBlockSkill
    # SKILL2
    elif skill_class_name == HeavyChargeSkill.__name__:
        return HeavyChargeSkill


GUARDIAN_SKILL_LIST = [
    # SKILL1
    RobustBlockSkill,

    # SKILL2
    HeavyChargeSkill,
]
