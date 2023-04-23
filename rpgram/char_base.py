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
            )
        self.__base_stats = base_stats
        if not isinstance(combat_stats, CombatStats):
            combat_stats = CombatStats(
                base_stats=self.__base_stats,
            )
        self.__combat_stats = combat_stats
        if not isinstance(race, Race):
            race = Race(
                name=race_name,
                description=race_description,
                bonus_strength=race_strength,
                bonus_dexterity=race_dexterity,
                bonus_constitution=race_constitution,
                bonus_intelligence=race_intelligence,
                bonus_wisdom=race_wisdom,
                bonus_charisma=race_charisma,
                bonus_hit_points=race_hit_points,
                bonus_initiative=race_initiative,
                bonus_physical_attack=race_physical_attack,
                bonus_magical_attack=race_magical_attack,
                bonus_physical_defense=race_physical_defense,
                bonus_magical_defense=race_magical_defense
            )
        self.__race = race
        self.update_bonus_stats()

    def update_bonus_stats(self):
        strength = 0
        dexterity = 0
        constitution = 0
        intelligence = 0
        wisdom = 0
        charisma = 0

        hit_points = 0
        initiative = 0
        physical_attack = 0
        magical_attack = 0
        physical_defense = 0
        magical_defense = 0

        check_list = [self.race]
        for item in check_list:
            strength += item.strength
            dexterity += item.dexterity
            constitution += item.constitution
            intelligence += item.intelligence
            wisdom += item.wisdom
            charisma += item.charisma

            hit_points += item.hit_points
            initiative += item.initiative
            physical_attack += item.physical_attack
            magical_attack += item.magical_attack
            physical_defense += item.physical_defense
            magical_defense += item.magical_defense

        self.base_stats.bonus_strength = strength
        self.base_stats.bonus_dexterity = dexterity
        self.base_stats.bonus_constitution = constitution
        self.base_stats.bonus_intelligence = intelligence
        self.base_stats.bonus_wisdom = wisdom
        self.base_stats.bonus_charisma = charisma

        self.combat_stats.bonus_hit_points = hit_points
        self.combat_stats.bonus_initiative = initiative
        self.combat_stats.bonus_physical_attack = physical_attack
        self.combat_stats.bonus_magical_attack = magical_attack
        self.combat_stats.bonus_physical_defense = physical_defense
        self.combat_stats.bonus_magical_defense = magical_defense

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
        char_name='Test Character',
        level=50,
        base_strength=10,
        base_dexterity=10,
        base_constitution=10,
        base_intelligence=10,
        base_wisdom=10,
        base_charisma=10,
        race_name='Humano',
        race_description='Humano Teste',
        race_strength=10,
        race_dexterity=10,
        race_constitution=10,
        race_intelligence=10,
        race_wisdom=10,
        race_charisma=10,
        race_hit_points=10,
        race_initiative=10,
        race_physical_attack=10,
        race_magical_attack=10,
        race_physical_defense=10,
        race_magical_defense=10,
    )
    print(base_character)
    base_character.base_stats.xp = 100
    base_character.base_stats.base_strength = 1
    base_character.base_stats.bonus_strength += 2
    base_character.combat_stats.bonus_hp += 10
    print(base_character)
