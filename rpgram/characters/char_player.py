from rpgram.boosters import Race
from rpgram.characters import BaseCharacter
from rpgram.stats import BaseStats, CombatStats


class PlayerCharacter(BaseCharacter):
    def __init__(
        self,
        player_id: str,
        player_name: str,
        char_name: str,
        base_stats: BaseStats = None,
        combat_stats: CombatStats = None,
        race: Race = None,
        level: int = 1,
        base_strength: int = 0,
        base_dexterity: int = 0,
        base_constitution: int = 0,
        base_intelligence: int = 0,
        base_wisdom: int = 0,
        base_charisma: int = 0,
        race_name: str = '',
        race_description: str = '',
        race_strength: int = 0,
        race_dexterity: int = 0,
        race_constitution: int = 0,
        race_intelligence: int = 0,
        race_wisdom: int = 0,
        race_charisma: int = 0,
        race_hit_points: int = 0,
        race_initiative: int = 0,
        race_physical_attack: int = 0,
        race_magical_attack: int = 0,
        race_physical_defense: int = 0,
        race_magical_defense: int = 0,
    ) -> None:
        super().__init__(
            char_name=char_name,
            base_stats=base_stats,
            combat_stats=combat_stats,
            race=race,
            level=level,
            base_strength=base_strength,
            base_dexterity=base_dexterity,
            base_constitution=base_constitution,
            base_intelligence=base_intelligence,
            base_wisdom=base_wisdom,
            base_charisma=base_charisma,
            race_name=race_name,
            race_description=race_description,
            race_strength=race_strength,
            race_dexterity=race_dexterity,
            race_constitution=race_constitution,
            race_intelligence=race_intelligence,
            race_wisdom=race_wisdom,
            race_charisma=race_charisma,
            race_hit_points=race_hit_points,
            race_initiative=race_initiative,
            race_physical_attack=race_physical_attack,
            race_magical_attack=race_magical_attack,
            race_physical_defense=race_physical_defense,
            race_magical_defense=race_magical_defense,
        )
        self.__player_id = player_id
        self.__player_name = player_name

    player_id = property(lambda self: self.__player_id)
    player_name = property(lambda self: self.__player_name)
