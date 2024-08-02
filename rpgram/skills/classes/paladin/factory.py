from typing import TYPE_CHECKING, List, Type

from rpgram.skills.classes.paladin.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    BlueDjinnBalmSkill,
    CourtesanAnointingSkill,
    GreenDragonBalmSkill,
    KnightAnointingSkill,
    LordAnointingSkill,
    MaidenAnointingSkill,
    RedPhoenixBalmSkill,
    SquireAnointingSkill,
    SacredBalmSkill,
    WarriorAnointingSkill
)
from rpgram.skills.classes.paladin.skill2 import (
    SKILL_WAY_DESCRIPTION as skill_way2,
    ExcaliburSkill,
    GungnirSkill,
    KusanagiNoTsurugiSkill,
    OsheSkill,
    SudarshanaChakraSkill,
    TyrfingSkill
)
from rpgram.skills.classes.paladin.skill3 import (
    SKILL_WAY_DESCRIPTION as skill_way3,
    ConfessionSkill,
    ConfiscationSkill,
    CutThroatSkill,
    ExcommunicateSkill,
    ExileSkill,
    FloggingsSkill,
    PenitenceSkill,
    VladsPunishmentSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def paladin_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == SacredBalmSkill.__name__:
        skill_class = SacredBalmSkill
    elif skill_class_name == GreenDragonBalmSkill.__name__:
        skill_class = GreenDragonBalmSkill
    elif skill_class_name == RedPhoenixBalmSkill.__name__:
        skill_class = RedPhoenixBalmSkill
    elif skill_class_name == BlueDjinnBalmSkill.__name__:
        skill_class = BlueDjinnBalmSkill
    elif skill_class_name == SquireAnointingSkill.__name__:
        skill_class = SquireAnointingSkill
    elif skill_class_name == WarriorAnointingSkill.__name__:
        skill_class = WarriorAnointingSkill
    elif skill_class_name == MaidenAnointingSkill.__name__:
        skill_class = MaidenAnointingSkill
    elif skill_class_name == KnightAnointingSkill.__name__:
        skill_class = KnightAnointingSkill
    elif skill_class_name == CourtesanAnointingSkill.__name__:
        skill_class = CourtesanAnointingSkill
    elif skill_class_name == LordAnointingSkill.__name__:
        skill_class = LordAnointingSkill
    # SKILL2
    elif skill_class_name == ExcaliburSkill.__name__:
        skill_class = ExcaliburSkill
    elif skill_class_name == KusanagiNoTsurugiSkill.__name__:
        skill_class = KusanagiNoTsurugiSkill
    elif skill_class_name == TyrfingSkill.__name__:
        skill_class = TyrfingSkill
    elif skill_class_name == OsheSkill.__name__:
        skill_class = OsheSkill
    elif skill_class_name == SudarshanaChakraSkill.__name__:
        skill_class = SudarshanaChakraSkill
    elif skill_class_name == GungnirSkill.__name__:
        skill_class = GungnirSkill
    # SKILL3
    elif skill_class_name == FloggingsSkill.__name__:
        skill_class = FloggingsSkill
    elif skill_class_name == CutThroatSkill.__name__:
        skill_class = CutThroatSkill
    elif skill_class_name == VladsPunishmentSkill.__name__:
        skill_class = VladsPunishmentSkill
    elif skill_class_name == ConfessionSkill.__name__:
        skill_class = ConfessionSkill
    elif skill_class_name == PenitenceSkill.__name__:
        skill_class = PenitenceSkill
    elif skill_class_name == ConfiscationSkill.__name__:
        skill_class = ConfiscationSkill
    elif skill_class_name == ExcommunicateSkill.__name__:
        skill_class = ExcommunicateSkill
    elif skill_class_name == ExileSkill.__name__:
        skill_class = ExileSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


PALADIN_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    SacredBalmSkill,
    GreenDragonBalmSkill,
    RedPhoenixBalmSkill,
    BlueDjinnBalmSkill,
    SquireAnointingSkill,
    WarriorAnointingSkill,
    MaidenAnointingSkill,
    KnightAnointingSkill,
    CourtesanAnointingSkill,
    LordAnointingSkill,

    # SKILL2
    ExcaliburSkill,
    KusanagiNoTsurugiSkill,
    TyrfingSkill,
    OsheSkill,
    SudarshanaChakraSkill,
    GungnirSkill,

    # SKILL3
    FloggingsSkill,
    CutThroatSkill,
    VladsPunishmentSkill,
    ConfessionSkill,
    PenitenceSkill,
    ConfiscationSkill,
    ExcommunicateSkill,
    ExileSkill,
]
PALADIN_SKILL_WAYS: List[dict] = [
    skill_way1,
    skill_way2,
    skill_way3,
]
