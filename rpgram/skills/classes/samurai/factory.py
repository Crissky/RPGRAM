from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.samurai.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    DoUchiSkill,
    KoteUchiSkill,
    MenUchiSkill,
)
from rpgram.skills.classes.samurai.skill2 import (
    SKILL_WAY_DESCRIPTION as skill_way2,
    HonoKogekiSkill,
    IwaKogekiSkill,
    KazeKogekiSkill,
    KosenKogekiSkill,
    MizuKogekiSkill,
    ZantetsusenSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def samurai_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == KoteUchiSkill.__name__:
        skill_class = KoteUchiSkill
    elif skill_class_name == DoUchiSkill.__name__:
        skill_class = DoUchiSkill
    elif skill_class_name == MenUchiSkill.__name__:
        skill_class = MenUchiSkill
    elif skill_class_name == ZantetsusenSkill.__name__:
        skill_class = ZantetsusenSkill
    elif skill_class_name == MizuKogekiSkill.__name__:
        skill_class = MizuKogekiSkill
    elif skill_class_name == HonoKogekiSkill.__name__:
        skill_class = HonoKogekiSkill
    elif skill_class_name == KosenKogekiSkill.__name__:
        skill_class = KosenKogekiSkill
    elif skill_class_name == KazeKogekiSkill.__name__:
        skill_class = KazeKogekiSkill
    elif skill_class_name == IwaKogekiSkill.__name__:
        skill_class = IwaKogekiSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


SAMURAI_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    KoteUchiSkill,
    DoUchiSkill,
    MenUchiSkill,

    # SKILL2
    ZantetsusenSkill,
    MizuKogekiSkill,
    HonoKogekiSkill,
    KosenKogekiSkill,
    KazeKogekiSkill,
    IwaKogekiSkill,
]
SAMURAI_SKILL_WAYS: List[dict] = [
    skill_way1,
    skill_way2,
]
