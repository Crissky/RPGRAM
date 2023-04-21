from stats_base import BaseStats
from stats_combat import CombatStats


class BaseCharacter:
    def __init__(
        self, base_stats: BaseStats, combat_stats: CombatStats
    ) -> None:
        self.__base_stats = base_stats
        self.__combat_stats = combat_stats
