if __name__ in ['__main__', 'char_base']:
    from stats_base import BaseStats
    from stats_combat import CombatStats
else:
    from rpgram.stats_base import BaseStats
    from rpgram.stats_combat import CombatStats


class BaseCharacter:
    def __init__(
        self,
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
        bonus_initiative: int = 0,
    ) -> None:
        self.__name = char_name
        if not isinstance(base_stats, BaseStats):
            base_stats = BaseStats(
                level=level,
                base_strength=base_strength,
                base_dexterity=base_dexterity,
                base_constitution=base_constitution,
                base_intelligence=base_intelligence,
                base_wisdom=base_wisdom,
                base_charisma=base_charisma,
                bonus_strength=bonus_strength,
                bonus_dexterity=bonus_dexterity,
                bonus_constitution=bonus_constitution,
                bonus_intelligence=bonus_intelligence,
                bonus_wisdom=bonus_wisdom,
                bonus_charisma=bonus_charisma,
            )
        self.__base_stats = base_stats
        if not isinstance(combat_stats, CombatStats):
            combat_stats = CombatStats(
                base_stats=self.__base_stats,
                bonus_physical_attack=bonus_physical_attack,
                bonus_magical_attack=bonus_magical_attack,
                bonus_physical_defense=bonus_physical_defense,
                bonus_magical_defense=bonus_magical_defense,
                bonus_hit_points=bonus_hit_points,
                bonus_initiative=bonus_initiative,
            )
        self.__combat_stats = combat_stats

    # Getters
    name = property(lambda self: self.__name)
    strength = property(fget=lambda self: self.__base_stats.strength)
    dexterity = property(fget=lambda self: self.__base_stats.dexterity)
    constitution = property(fget=lambda self: self.__base_stats.constitution)
    intelligence = property(fget=lambda self: self.__base_stats.intelligence)
    wisdom = property(fget=lambda self: self.__base_stats.wisdom)
    charisma = property(fget=lambda self: self.__base_stats.charisma)
    hp = hit_points = property(
        fget=lambda self: self.__combat_stats.hit_points
    )
    physical_attack = property(
        fget=lambda self: self.__combat_stats.physical_attack
    )
    magical_attack = property(
        fget=lambda self: self.__combat_stats.magical_attack
    )
    physical_defense = property(
        fget=lambda self: self.__combat_stats.physical_defense
    )
    magical_defense = property(
        fget=lambda self: self.__combat_stats.magical_defense
    )
    initiative = property(
        fget=lambda self: self.__combat_stats.initiative
    )

    def __repr__(self) -> str:
        return (
            f'########################################\n'
            f'Nome: {self.name}\n'
            f'{self.__base_stats.get_sheet()}'
            f'{self.__combat_stats.get_sheet()}'
            f'########################################\n'
        )


if __name__ == '__main__':
    base_character = BaseCharacter(
        char_name='Test Character',
        level=50,
        base_strength=10,
        base_dexterity=10,
        base_constitution=10,
        base_intelligence=10,
        base_wisdom=10,
        base_charisma=10,
        bonus_strength=10,
        bonus_dexterity=10,
        bonus_constitution=10,
        bonus_intelligence=10,
        bonus_wisdom=10,
        bonus_charisma=10,
        bonus_physical_attack=10,
        bonus_magical_attack=10,
        bonus_physical_defense=10,
        bonus_magical_defense=10,
        bonus_hit_points=10,
        bonus_initiative=10,
    )
    print(base_character)
