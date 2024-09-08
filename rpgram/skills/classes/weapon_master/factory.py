from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.weapon_master.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    BruisingAttackSkill,
    CrystallineClashSkill,
    GeocrusherAttackSkill,
    SlashingAttackSkill,
    SonicBladeSkill,
    StormDanceSkill,
    TerrebrantAttackSkill,
    ThunderpassSkill,
    VorpalBladeAttackSkill,
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def weapon_master_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == SlashingAttackSkill.__name__:
        skill_class = SlashingAttackSkill
    elif skill_class_name == SonicBladeSkill.__name__:
        skill_class = SonicBladeSkill
    elif skill_class_name == VorpalBladeAttackSkill.__name__:
        skill_class = VorpalBladeAttackSkill
    elif skill_class_name == BruisingAttackSkill.__name__:
        skill_class = BruisingAttackSkill
    elif skill_class_name == CrystallineClashSkill.__name__:
        skill_class = CrystallineClashSkill
    elif skill_class_name == GeocrusherAttackSkill.__name__:
        skill_class = GeocrusherAttackSkill
    elif skill_class_name == TerrebrantAttackSkill.__name__:
        skill_class = TerrebrantAttackSkill
    elif skill_class_name == ThunderpassSkill.__name__:
        skill_class = ThunderpassSkill
    elif skill_class_name == StormDanceSkill.__name__:
        skill_class = StormDanceSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


WEAPON_MASTER_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    SlashingAttackSkill,
    SonicBladeSkill,
    VorpalBladeAttackSkill,
    BruisingAttackSkill,
    CrystallineClashSkill,
    GeocrusherAttackSkill,
    TerrebrantAttackSkill,
    ThunderpassSkill,
    StormDanceSkill,
]
WEAPON_MASTER_SKILL_WAYS: List[dict] = [
    skill_way1,
]
