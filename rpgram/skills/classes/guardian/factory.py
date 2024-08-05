from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.guardian.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    ShieldWallSkill
)
from rpgram.skills.classes.guardian.skill2 import (
    SKILL_WAY_DESCRIPTION as skill_way2,
    IronChargeSkill,
    SteelStormSkill
)
from rpgram.skills.classes.guardian.skill3 import (
    SKILL_WAY_DESCRIPTION as skill_way3,
    CrystalArmorSkill,
    CrystalChrysalisSkill,
    CrystallineInfusionSkill,
    ShatterSkill
)
from rpgram.skills.classes.multiclasse.physical_defense import (
    GuardianShieldSkill,
    HeavyChargeSkill,
    RobustBlockSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def guardian_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == RobustBlockSkill.__name__:
        skill_class = RobustBlockSkill
    elif skill_class_name == GuardianShieldSkill.__name__:
        skill_class = GuardianShieldSkill
    elif skill_class_name == ShieldWallSkill.__name__:
        skill_class = ShieldWallSkill
    # SKILL2
    elif skill_class_name == HeavyChargeSkill.__name__:
        skill_class = HeavyChargeSkill
    elif skill_class_name == IronChargeSkill.__name__:
        skill_class = IronChargeSkill
    elif skill_class_name == SteelStormSkill.__name__:
        skill_class = SteelStormSkill
    # SKILL3
    elif skill_class_name == CrystalArmorSkill.__name__:
        skill_class = CrystalArmorSkill
    elif skill_class_name == CrystallineInfusionSkill.__name__:
        skill_class = CrystallineInfusionSkill
    elif skill_class_name == ShatterSkill.__name__:
        skill_class = ShatterSkill
    elif skill_class_name == CrystalChrysalisSkill.__name__:
        skill_class = CrystalChrysalisSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


GUARDIAN_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    RobustBlockSkill,
    GuardianShieldSkill,
    ShieldWallSkill,

    # SKILL2
    HeavyChargeSkill,
    IronChargeSkill,
    SteelStormSkill,

    # SKILL3
    CrystalArmorSkill,
    CrystallineInfusionSkill,
    ShatterSkill,
    CrystalChrysalisSkill,
]
GUARDIAN_SKILL_WAYS: List[dict] = [
    skill_way1,
    skill_way2,
    skill_way3,
]
