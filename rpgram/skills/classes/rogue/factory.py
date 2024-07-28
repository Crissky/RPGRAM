from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.multiclasse.precision_attack import QuickAttackSkill
from rpgram.skills.classes.rogue.skill1 import (
    DoubleFangsSkill,
    ElusiveAssaultSkill,
    PhantomStrikeSkill,
    TaipanInoculateSkill,
    VipersFangSkill
)
from rpgram.skills.classes.rogue.skill2 import ChaoticStepsSkill, ShadowStepsSkill
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def rogue_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == VipersFangSkill.__name__:
        skill_class = VipersFangSkill
    elif skill_class_name == DoubleFangsSkill.__name__:
        skill_class = DoubleFangsSkill
    elif skill_class_name == TaipanInoculateSkill.__name__:
        skill_class = TaipanInoculateSkill
    elif skill_class_name == QuickAttackSkill.__name__:
        skill_class = QuickAttackSkill
    elif skill_class_name == PhantomStrikeSkill.__name__:
        skill_class = PhantomStrikeSkill
    elif skill_class_name == ElusiveAssaultSkill.__name__:
        skill_class = ElusiveAssaultSkill
    # SKILL2
    elif skill_class_name == ShadowStepsSkill.__name__:
        skill_class = ShadowStepsSkill
    elif skill_class_name == ChaoticStepsSkill.__name__:
        skill_class = ChaoticStepsSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


ROGUE_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    VipersFangSkill,
    DoubleFangsSkill,
    TaipanInoculateSkill,
    QuickAttackSkill,
    PhantomStrikeSkill,
    ElusiveAssaultSkill,

    # SKILL2
    ShadowStepsSkill,
    ChaoticStepsSkill,
]
