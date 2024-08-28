from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.ranger.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    AlertSkill,
    DoubleAmbushSkill,
    K9AttackSkill,
    SniffSkill,
    ThePackSkill,
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def ranger_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == K9AttackSkill.__name__:
        skill_class = K9AttackSkill
    elif skill_class_name == DoubleAmbushSkill.__name__:
        skill_class = DoubleAmbushSkill
    elif skill_class_name == ThePackSkill.__name__:
        skill_class = ThePackSkill
    elif skill_class_name == SniffSkill.__name__:
        skill_class = SniffSkill
    elif skill_class_name == AlertSkill.__name__:
        skill_class = AlertSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


RANGER_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    K9AttackSkill,
    DoubleAmbushSkill,
    ThePackSkill,
    SniffSkill,
    AlertSkill,
]
RANGER_SKILL_WAYS: List[dict] = [
    skill_way1,
]
