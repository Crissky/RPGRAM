if __name__ in ['__main__', 'stats_combat']:
    from stats_base import BaseStats
else:
    from rpgram.stats_base import BaseStats


class CombatStats:
    def __init__(
        self,
        base_stats: BaseStats = None,
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
        bonus_hit_points: int = 0,
        bonus_initiative: int = 0,
        bonus_physical_attack: int = 0,
        bonus_magical_attack: int = 0,
        bonus_physical_defense: int = 0,
        bonus_magical_defense: int = 0,
    ) -> None:
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
        self.__damage = 0

        self.__bonus_hit_points = 0
        self.__bonus_initiative = 0
        self.__bonus_physical_attack = 0
        self.__bonus_magical_attack = 0
        self.__bonus_physical_defense = 0
        self.__bonus_magical_defense = 0

        self.bonus_hit_points = bonus_hit_points
        self.bonus_initiative = bonus_initiative
        self.bonus_physical_attack = bonus_physical_attack
        self.bonus_magical_attack = bonus_magical_attack
        self.bonus_physical_defense = bonus_physical_defense
        self.bonus_magical_defense = bonus_magical_defense

    def set_damage(self, value: int) -> None:
        value = int(value * -1)
        if value > 0:
            print(f'{value} de Dano!!!')
        elif value < 0:
            print(f'{-value} de Cura.')
        self.__damage += value
        if self.__damage > self.hit_points:
            self.__damage = self.hit_points
        elif self.__damage < 0:
            self.__damage = 0

    def __add_bonus_stats(self, value: int, attribute: str) -> None:
        value = int(value)
        clean_attribute = attribute.split('_CombatStats__bonus_')[-1].title()
        clean_attribute = clean_attribute.replace('_', ' ')
        print(
            f'Bônus de {clean_attribute} definidos para {value}.'
        )
        setattr(self, attribute, value)

    # Getters
    @property
    def hit_points(self) -> int:
        return int(
            10 +
            (self.constitution * 10) +
            (self.strength * 5) +
            self.bonus_hit_points
        )

    @property
    def current_hit_points(self) -> int:
        return int(
            self.hit_points - self.__damage
        )

    @property
    def initiative(self) -> int:
        return int(
            (self.dexterity * 2) +
            self.wisdom +
            self.charisma +
            self.bonus_initiative
        )

    @property
    def physical_attack(self) -> int:
        return int(
            (self.strength * 2) +
            self.dexterity +
            self.bonus_physical_attack
        )

    @property
    def magical_attack(self) -> int:
        return int(
            (self.intelligence * 2) +
            self.wisdom +
            self.bonus_magical_attack
        )

    @property
    def physical_defense(self) -> int:
        return int(
            (self.constitution * 2) +
            self.dexterity +
            self.bonus_physical_defense
        )

    @property
    def magical_defense(self) -> int:
        return int(
            (self.wisdom * 2) +
            self.constitution +
            self.bonus_magical_defense
        )

    # Setters
    @hit_points.setter
    def hit_points(self, value) -> int:
        return self.set_damage(value)

    @current_hit_points.setter
    def current_hit_points(self, value) -> int:
        return self.set_damage(value)

    strength = property(fget=lambda self: self.__base_stats.strength)
    dexterity = property(fget=lambda self: self.__base_stats.dexterity)
    constitution = property(fget=lambda self: self.__base_stats.constitution)
    intelligence = property(fget=lambda self: self.__base_stats.intelligence)
    wisdom = property(fget=lambda self: self.__base_stats.wisdom)
    charisma = property(fget=lambda self: self.__base_stats.charisma)

    hp = hit_points
    bonus_initiative = property(
        fget=lambda self: self.__bonus_initiative,
        fset=lambda self, value: self.__add_bonus_stats(
            value, '_CombatStats__bonus_initiative'
        )
    )
    bonus_physical_attack = property(
        fget=lambda self: self.__bonus_physical_attack,
        fset=lambda self, value: self.__add_bonus_stats(
            value, '_CombatStats__bonus_physical_attack'
        )
    )
    bonus_magical_attack = property(
        fget=lambda self: self.__bonus_magical_attack,
        fset=lambda self, value: self.__add_bonus_stats(
            value, '_CombatStats__bonus_magical_attack'
        )
    )
    bonus_physical_defense = property(
        fget=lambda self: self.__bonus_physical_defense,
        fset=lambda self, value: self.__add_bonus_stats(
            value, '_CombatStats__bonus_physical_defense'
        )
    )
    bonus_magical_defense = property(
        fget=lambda self: self.__bonus_magical_defense,
        fset=lambda self, value: self.__add_bonus_stats(
            value, '_CombatStats__bonus_magical_defense'
        )
    )
    bonus_hit_points = bonus_hp = property(
        fget=lambda self: self.__bonus_hit_points,
        fset=lambda self, value: self.__add_bonus_stats(
            value, '_CombatStats__bonus_hit_points'
        )
    )

    def get_sheet(self) -> str:
        base_init = self.initiative - self.bonus_initiative
        base_hp = self.hit_points - self.bonus_hit_points
        base_phy_atk = self.physical_attack - self.bonus_physical_attack
        base_mag_atk = self.magical_attack - self.bonus_magical_attack
        base_phy_def = self.physical_defense - self.bonus_physical_defense
        base_mag_def = self.magical_defense - self.bonus_magical_defense
        return (
            f'\n-ATRIBUTOS DE COMBATE-\n'

            f'HP: {self.current_hit_points}/{self.hit_points} '
            f'[{base_hp}{self.bonus_hit_points:+}]\n'

            f'INICIATIVA: {self.initiative} '
            f'[{base_init}{self.bonus_initiative:+}]\n'

            f'ATAQUE FÍSICO: {self.physical_attack} '
            f'[{base_phy_atk}{self.bonus_physical_attack:+}]\n'

            f'ATAQUE MÁGICO: {self.magical_attack} '
            f'[{base_mag_atk}{self.bonus_magical_attack:+}]\n'

            f'DEFESA FÍSICA: {self.physical_defense} '
            f'[{base_phy_def}{self.bonus_physical_defense:+}]\n'

            f'DEFESA MÁGICA: {self.magical_defense} '
            f'[{base_mag_def}{self.bonus_magical_defense:+}]\n'
        )

    def __repr__(self) -> str:
        return (
            f'########################################\n'
            f'{self.__base_stats.get_sheet()}'
            f'{self.get_sheet()}'
            f'########################################\n'
        )


if __name__ == '__main__':
    base_stats = BaseStats(10)
    combat_stats = CombatStats(base_stats)

    base_stats.base_strength = 6
    base_stats.base_dexterity = 6
    base_stats.base_constitution = 6
    base_stats.base_intelligence = 3
    base_stats.base_wisdom = 3
    base_stats.base_charisma = 4

    base_stats.bonus_strength = 10
    base_stats.bonus_dexterity = 10
    base_stats.bonus_constitution = 10
    base_stats.bonus_intelligence = 10
    base_stats.bonus_wisdom = 10
    base_stats.bonus_charisma = 10

    combat_stats.bonus_hit_points = 100
    combat_stats.bonus_initiative = 10
    combat_stats.bonus_physical_attack = 11
    combat_stats.bonus_magical_attack = 12
    combat_stats.bonus_physical_defense = -13
    combat_stats.bonus_magical_defense = -14

    print(combat_stats)
    combat_stats.hit_points = -10
    combat_stats.current_hit_points = -20
    combat_stats.hp = -30
    combat_stats.hp = 10
    print(combat_stats)
