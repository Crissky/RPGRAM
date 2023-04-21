from stats_base import BaseStats


class CombatStats:
    def __init__(self, base_stats: BaseStats) -> None:
        self.__base_stats = base_stats
        self.__damage = 0
        self.__bonus_physical_attack = 0
        self.__bonus_magical_attack = 0
        self.__bonus_physical_defense = 0
        self.__bonus_magical_defense = 0
        self.__bonus_hit_points = 0
        self.__bonus_initiative = 0

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
            f'Adicionando {value} Ponto(s) '
            f'de bônus de {clean_attribute}.'
        )
        setattr(self, attribute, value)

    # Getters
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
    bonus_hit_points = property(
        fget=lambda self: self.__bonus_hit_points,
        fset=lambda self, value: self.__add_bonus_stats(
            value, '_CombatStats__bonus_hit_points'
        )
    )
    bonus_initiative = property(
        fget=lambda self: self.__bonus_initiative,
        fset=lambda self, value: self.__add_bonus_stats(
            value, '_CombatStats__bonus_initiative'
        )
    )

    def __repr__(self) -> str:
        init_sign = '+' if self.bonus_initiative >= 0 else ''
        hp_sign = '+' if self.bonus_hit_points >= 0 else ''
        phy_sign = '+' if self.bonus_physical_attack >= 0 else ''
        mag_sign = '+' if self.bonus_magical_attack >= 0 else ''
        phy_def_sign = '+' if self.bonus_physical_defense >= 0 else ''
        mag_def_sign = '+' if self.bonus_magical_defense >= 0 else ''

        base_init = self.initiative - self.bonus_initiative
        base_hp = self.hit_points - self.bonus_hit_points
        base_phy_atk = self.physical_attack - self.bonus_physical_attack
        base_mag_atk = self.magical_attack - self.bonus_magical_attack
        base_phy_def = self.physical_defense - self.bonus_physical_defense
        base_mag_def = self.magical_defense - self.bonus_magical_defense
        return (
            f'{self.__base_stats.__repr__()}'

            f'\n-ATRIBUTOS DE COMBATE-\n'

            f'HP: {self.current_hit_points}/{self.hit_points} '
            f'[{base_hp}{hp_sign}{self.bonus_hit_points}]\n'

            f'INICIATIVA: {self.initiative} '
            f'[{base_init}{init_sign}'
            f'{self.bonus_initiative}]\n'

            f'ATAQUE FÍSICO: {self.physical_attack} '
            f'[{base_phy_atk}{phy_sign}'
            f'{self.bonus_physical_attack}]\n'

            f'ATAQUE MÁGICO: {self.magical_attack} '
            f'[{base_mag_atk}{mag_sign}'
            f'{self.bonus_magical_attack}]\n'

            f'DEFESA FÍSICA: {self.physical_defense} '
            f'[{base_phy_def}{phy_def_sign}'
            f'{self.bonus_physical_defense}]\n'

            f'DEFESA MÁGICA: {self.magical_defense} '
            f'[{base_mag_def}{mag_def_sign}'
            f'{self.bonus_magical_defense}]\n'

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
