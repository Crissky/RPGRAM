from stats_base import BaseStats


class CombatStats:
    def __init__(self, base_stats) -> None:
        self.__base_stats = base_stats
        self.__damage = 0

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

    # Getters
    @property
    def physical_attack(self) -> int:
        return int(
            (self.strength * 2) + self.dexterity
        )

    @property
    def magical_attack(self) -> int:
        return int(
            (self.intelligence * 2) + self.wisdom
        )

    @property
    def physical_defense(self) -> int:
        return int(
            (self.constitution * 2) + self.dexterity
        )

    @property
    def magical_defense(self) -> int:
        return int(
            (self.wisdom * 2) + self.constitution
        )

    @property
    def hit_points(self) -> int:
        return int(
            10 +
            (self.constitution * 10) +
            (self.strength * 5)
        )

    @property
    def initiative(self) -> int:
        return int(
            (self.dexterity * 2) +
            self.wisdom +
            self.charisma
        )

    @property
    def current_hit_points(self) -> int:
        return int(
            self.hit_points - self.__damage
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

    def __repr__(self) -> str:
        str_sign = '+' if self.__base_stats.bonus_strength >= 0 else ''
        dex_sign = '+' if self.__base_stats.bonus_dexterity >= 0 else ''
        con_sign = '+' if self.__base_stats.bonus_constitution >= 0 else ''
        int_sign = '+' if self.__base_stats.bonus_intelligence >= 0 else ''
        wis_sign = '+' if self.__base_stats.bonus_wisdom >= 0 else ''
        cha_sign = '+' if self.__base_stats.bonus_charisma >= 0 else ''
        return (
            f'########################################\n'

            f'Level: {self.__base_stats.level}\n'
            f'Experiência: {self.__base_stats.xp}/'
            f'{self.__base_stats.next_level_xp}\n'
            f'Pontos: {self.__base_stats.points}\n'

            f'\n-ATRIBUTOS BASE-\n'

            f'FOR: {self.strength} '
            f'[{self.__base_stats.base_strength}{str_sign}'
            f'{self.__base_stats.bonus_strength}] '
            f'({self.__base_stats.mod_strength})\n'

            f'DES: {self.dexterity} '
            f'[{self.__base_stats.base_dexterity}{dex_sign}'
            f'{self.__base_stats.bonus_dexterity}] '
            f'({self.__base_stats.mod_dexterity})\n'

            f'CON: {self.constitution} '
            f'[{self.__base_stats.base_constitution}{con_sign}'
            f'{self.__base_stats.bonus_constitution}] '
            f'({self.__base_stats.mod_constitution})\n'

            f'INT: {self.intelligence} '
            f'[{self.__base_stats.base_intelligence}{int_sign}'
            f'{self.__base_stats.bonus_intelligence}] '
            f'({self.__base_stats.mod_intelligence})\n'

            f'SAB: {self.wisdom} '
            f'[{self.__base_stats.base_wisdom}{wis_sign}'
            f'{self.__base_stats.bonus_wisdom}] '
            f'({self.__base_stats.mod_wisdom})\n'

            f'CAR: {self.charisma} '
            f'[{self.__base_stats.base_charisma}{cha_sign}'
            f'{self.__base_stats.bonus_charisma}] '
            f'({self.__base_stats.mod_charisma})\n'

            f'\n-ATRIBUTOS DE COMBATE-\n'

            f'HP: {self.current_hit_points}/{self.hit_points}\n'
            f'INICIATIVA: {self.initiative}\n'
            f'ATAQUE FÍSICO: {self.physical_attack}\n'
            f'ATAQUE MÁGICO: {self.magical_attack}\n'
            f'DEFESA FÍSICO: {self.physical_defense}\n'
            f'DEFESA MÁGICO: {self.magical_defense}\n'

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

    print(combat_stats)
    combat_stats.hit_points = -10
    combat_stats.current_hit_points = -20
    combat_stats.hp = -30
    combat_stats.hp = 10
    print(combat_stats)
