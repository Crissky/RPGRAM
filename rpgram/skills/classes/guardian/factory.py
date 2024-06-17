from rpgram.skills.classes.guardian.skill1 import RobustBlockSkill
from rpgram.skills.skill_base import BaseSkill


def guardian_skill_factory(skill_class_name: str) -> BaseSkill:
    if skill_class_name == RobustBlockSkill.__name__:
        return RobustBlockSkill
