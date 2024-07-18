from itertools import chain
from rpgram.conditions.condition import Condition
from rpgram.conditions.barrier import BarrierCondition
from rpgram.conditions.barrier import GuardianShieldCondition
from rpgram.conditions.barrier import AegisShadowCondition
from rpgram.conditions.barrier import PrismaticShieldCondition
from rpgram.conditions.barrier import ChaosWeaverCondition
from rpgram.conditions.buff import BuffCondition
from rpgram.conditions.debuff import DEBUFFS
from rpgram.conditions.debuff import DebuffCondition
from rpgram.conditions.debuff import BerserkerCondition
from rpgram.conditions.debuff import BleedingCondition
from rpgram.conditions.debuff import BlindnessCondition
from rpgram.conditions.debuff import BurnCondition
from rpgram.conditions.debuff import ConfusionCondition
from rpgram.conditions.debuff import CrystallizedCondition
from rpgram.conditions.debuff import CurseCondition
from rpgram.conditions.debuff import ExhaustionCondition
from rpgram.conditions.debuff import FearingCondition
from rpgram.conditions.debuff import FrozenCondition
from rpgram.conditions.debuff import ParalysisCondition
from rpgram.conditions.debuff import PetrifiedCondition
from rpgram.conditions.debuff import PoisoningCondition
from rpgram.conditions.debuff import SilenceCondition
from rpgram.conditions.debuff import StunnedCondition
from rpgram.conditions.heal import HealingCondition
from rpgram.conditions.heal import Heal1Condition
from rpgram.conditions.heal import Heal2Condition
from rpgram.conditions.heal import Heal3Condition
from rpgram.conditions.heal import Heal4Condition
from rpgram.conditions.heal import Heal5Condition
from rpgram.conditions.heal import Heal6Condition
from rpgram.conditions.heal import Heal7Condition
from rpgram.conditions.heal import Heal8Condition
from rpgram.conditions.target_skill_debuff import TARGET_DEBUFFS


class AllDebuffs:
    __list = [
        DEBUFFS,
        TARGET_DEBUFFS,
    ]

    def __iter__(self):
        for condition in chain(*self.__list):
            yield condition


ALL_DEBUFFS = AllDebuffs()
