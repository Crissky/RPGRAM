if __name__ in ['__main__', 'char_player']:
    from char_base import BaseCharacter
    from stats_base import BaseStats
    from stats_combat import CombatStats
else:
    from rpgram.char_base import BaseCharacter
    from rpgram.stats_base import BaseStats
    from rpgram.stats_combat import CombatStats


class PlayerCharacter(BaseCharacter):
    def __init__(
        self,
        player_id: str,
        char_name: str,
        base_stats: BaseStats = None,
        combat_stats: CombatStats = None,
        level: int = 1,
        base_strength: int = 0,
        base_dexterity: int = 0,
        base_constitution: int = 0,
        base_intelligence: int = 0,
        base_wisdom: int = 0,
        base_charisma: int = 0,
        bonus_strength: int = 0,
        bonus_dexterity: int = 0,
        bonus_constitution: int = 0,
        bonus_intelligence: int = 0,
        bonus_wisdom: int = 0,
        bonus_charisma: int = 0,
        bonus_physical_attack: int = 0,
        bonus_magical_attack: int = 0,
        bonus_physical_defense: int = 0,
        bonus_magical_defense: int = 0,
        bonus_hit_points: int = 0,
        bonus_initiative: int = 0
    ) -> None:
        super().__init__(
            char_name,
            base_stats,
            combat_stats,
            level,
            base_strength,
            base_dexterity,
            base_constitution,
            base_intelligence,
            base_wisdom,
            base_charisma,
            bonus_strength,
            bonus_dexterity,
            bonus_constitution,
            bonus_intelligence,
            bonus_wisdom,
            bonus_charisma,
            bonus_physical_attack,
            bonus_magical_attack,
            bonus_physical_defense,
            bonus_magical_defense,
            bonus_hit_points,
            bonus_initiative
        )
        self.__player_id = player_id

    player_id = property(lambda self: self.__player_id)
