if __name__ in ['__main__', 'char_base']:
    from stats_base import BaseStats
    from stats_combat import CombatStats
    from race import Race
else:
    from rpgram.stats_base import BaseStats
    from rpgram.stats_combat import CombatStats
    from rpgram.race import Race


class BaseCharacter:
    def __init__(
        self,
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
        race_bonus_strength: int = 0,
        race_bonus_dexterity: int = 0,
        race_bonus_constitution: int = 0,
        race_bonus_intelligence: int = 0,
        race_bonus_wisdom: int = 0,
        race_bonus_charisma: int = 0,
        race_multiplier_strength: float = 1.0,
        race_multiplier_dexterity: float = 1.0,
        race_multiplier_constitution: float = 1.0,
        race_multiplier_intelligence: float = 1.0,
        race_multiplier_wisdom: float = 1.0,
        race_multiplier_charisma: float = 1.0,
    ) -> None:
        self.__name = char_name
        if not isinstance(race, Race):
            race = Race(
                name=race_name,
                description=race_description,
                bonus_strength=race_bonus_strength,
                bonus_dexterity=race_bonus_dexterity,
                bonus_constitution=race_bonus_constitution,
                bonus_intelligence=race_bonus_intelligence,
                bonus_wisdom=race_bonus_wisdom,
                bonus_charisma=race_bonus_charisma,
                multiplier_strength=race_multiplier_strength,
                multiplier_dexterity=race_multiplier_dexterity,
                multiplier_constitution=race_multiplier_constitution,
                multiplier_intelligence=race_multiplier_intelligence,
                multiplier_wisdom=race_multiplier_wisdom,
                multiplier_charisma=race_multiplier_charisma,
            )
        self.__race = race
        if not isinstance(base_stats, BaseStats):
            base_stats = BaseStats(
                level,
                base_strength,
                base_dexterity,
                base_constitution,
                base_intelligence,
                base_wisdom,
                base_charisma,
                self.__race,
            )
        self.__base_stats = base_stats
        if not isinstance(combat_stats, CombatStats):
            combat_stats = CombatStats(
                base_stats=self.__base_stats,
            )
        self.__combat_stats = combat_stats

    # Getters
    name = property(lambda self: self.__name)
    base_stats = bs = property(fget=lambda self: self.__base_stats)
    combat_stats = cs = property(fget=lambda self: self.__combat_stats)
    race = property(fget=lambda self: self.__race)

    def __repr__(self) -> str:
        return (
            f'########################################\n'
            f'Nome: {self.name}\n'
            f'{self.race.get_sheet()}'
            f'{self.base_stats.get_sheet()}'
            f'{self.combat_stats.get_sheet()}'
            f'########################################\n'
        )


if __name__ == '__main__':
    base_character = BaseCharacter(
        char_name='Personagem Teste',
        level=21,
        base_strength=10,
        base_dexterity=10,
        base_constitution=10,
        base_intelligence=10,
        base_wisdom=10,
        base_charisma=10,
        race_name='Elfo',
        race_description='Elfo Teste',
        race_bonus_strength=8,
        race_bonus_dexterity=12,
        race_bonus_constitution=8,
        race_bonus_intelligence=10,
        race_bonus_wisdom=12,
        race_bonus_charisma=10,
        race_multiplier_strength=1.0,
        race_multiplier_dexterity=1.2,
        race_multiplier_constitution=1,
        race_multiplier_intelligence=1.0,
        race_multiplier_wisdom=1.2,
        race_multiplier_charisma=1.0,
    )
    print(base_character)
    base_character.base_stats.xp = 100
    base_character.base_stats.dexterity = 1
    base_character.combat_stats.hp = -100
    base_character.combat_stats.hit_points = 50
    print(base_character)
