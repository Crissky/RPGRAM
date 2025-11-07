from itertools import chain
from typing import Iterable
from rpgram.conditions.condition import Condition  # noqa
from rpgram.conditions.barrier import BarrierCondition  # noqa
from rpgram.conditions.barrier import GuardianShieldCondition  # noqa
from rpgram.conditions.barrier import AegisShadowCondition  # noqa
from rpgram.conditions.barrier import PrismaticShieldCondition  # noqa
from rpgram.conditions.barrier import ChaosWeaverCondition  # noqa
from rpgram.conditions.buff import BuffCondition
from rpgram.conditions.debuff import DEBUFFS
from rpgram.conditions.debuff import DebuffCondition
from rpgram.conditions.debuff import BerserkerCondition  # noqa
from rpgram.conditions.debuff import BleedingCondition  # noqa
from rpgram.conditions.debuff import BlindnessCondition  # noqa
from rpgram.conditions.debuff import BurnCondition  # noqa
from rpgram.conditions.debuff import ConfusionCondition  # noqa
from rpgram.conditions.debuff import CrystallizedCondition  # noqa
from rpgram.conditions.debuff import CurseCondition  # noqa
from rpgram.conditions.debuff import ExhaustionCondition  # noqa
from rpgram.conditions.debuff import FearingCondition  # noqa
from rpgram.conditions.debuff import FrozenCondition  # noqa
from rpgram.conditions.debuff import ParalysisCondition  # noqa
from rpgram.conditions.debuff import PetrifiedCondition  # noqa
from rpgram.conditions.debuff import PoisoningCondition  # noqa
from rpgram.conditions.debuff import SilenceCondition  # noqa
from rpgram.conditions.debuff import StunnedCondition  # noqa
from rpgram.conditions.heal import HealingCondition  # noqa
from rpgram.conditions.heal import Heal1Condition  # noqa
from rpgram.conditions.heal import Heal2Condition  # noqa
from rpgram.conditions.heal import Heal3Condition  # noqa
from rpgram.conditions.heal import Heal4Condition  # noqa
from rpgram.conditions.heal import Heal5Condition  # noqa
from rpgram.conditions.heal import Heal6Condition  # noqa
from rpgram.conditions.heal import Heal7Condition  # noqa
from rpgram.conditions.heal import Heal8Condition  # noqa
from rpgram.conditions.self_skill import SELF_BUFFS
from rpgram.conditions.special_damage_skill import SPECIAL_DAMAGE_BUFFS
from rpgram.conditions.target_skill_buff import TARGET_BUFFS
from rpgram.conditions.target_skill_debuff import TARGET_DEBUFFS


class AllDebuffs:
    __list = [
        DEBUFFS,
        TARGET_DEBUFFS,
    ]

    def __iter__(self) -> Iterable[DebuffCondition]:
        for condition in chain(*self.__list):
            yield condition


class AllBuffs:
    __list = [
        SELF_BUFFS,
        SPECIAL_DAMAGE_BUFFS,
        TARGET_BUFFS,
    ]

    def __iter__(self) -> Iterable[BuffCondition]:
        for condition in chain(*self.__list):
            yield condition


ALL_DEBUFFS: Iterable[DebuffCondition] = AllDebuffs()
ALL_BUFFS: Iterable[BuffCondition] = AllBuffs()
