from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.arcanist.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    FireRaySkill,
    FireWaveSkill,
    MagmaGeyserSkill,
    MudTrapSkill,
    SandGustSkill,
    SwirlSkill,
    TetragramShotSkill,
)
from rpgram.skills.classes.arcanist.skill2 import (
    PrismaticAbrumationSkill,
    DarkShotSkill
)
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


def arcanist_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == FireBallSkill.__name__:
        skill_class = FireBallSkill
    elif skill_class_name == WaterBubbleSkill.__name__:
        skill_class = WaterBubbleSkill
    elif skill_class_name == WindGustSkill.__name__:
        skill_class = WindGustSkill
    elif skill_class_name == EarthBreakSkill.__name__:
        skill_class = EarthBreakSkill
    elif skill_class_name == FireRaySkill.__name__:
        skill_class = FireRaySkill
    elif skill_class_name == FireWaveSkill.__name__:
        skill_class = FireWaveSkill
    elif skill_class_name == MagmaGeyserSkill.__name__:
        skill_class = MagmaGeyserSkill
    elif skill_class_name == SwirlSkill.__name__:
        skill_class = SwirlSkill
    elif skill_class_name == SandGustSkill.__name__:
        skill_class = SandGustSkill
    elif skill_class_name == MudTrapSkill.__name__:
        skill_class = MudTrapSkill
    elif skill_class_name == TetragramShotSkill.__name__:
        skill_class = TetragramShotSkill
    # SKILL2
    elif skill_class_name == PrismaticShotSkill.__name__:
        skill_class = PrismaticShotSkill
    elif skill_class_name == DarkShotSkill.__name__:
        skill_class = DarkShotSkill
    elif skill_class_name == PrismaticAbrumationSkill.__name__:
        skill_class = PrismaticAbrumationSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


ARCANIST_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    FireBallSkill,
    WaterBubbleSkill,
    WindGustSkill,
    EarthBreakSkill,
    FireRaySkill,
    FireWaveSkill,
    MagmaGeyserSkill,
    SwirlSkill,
    SandGustSkill,
    MudTrapSkill,
    TetragramShotSkill,

    # SKILL2
    PrismaticShotSkill,
    DarkShotSkill,
    PrismaticAbrumationSkill,
]
ARCANIST_SKILL_WAYS: List[dict] = [
    skill_way1
]
