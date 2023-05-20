from typing import List

from constants.text import SECTION_HEAD, TEXT_DELIMITER
from rpgram.stats import BaseStats
from rpgram.boosters import StatsBooster


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
        damage: int = 0,
        stats_boosters: List[StatsBooster] = []
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
                stats_boosters=stats_boosters
            )
        self.__base_stats = base_stats
        self.__damage = int(damage)

        self.__stats_boosters = set(base_stats.stats_boosters)
        self.update()

    def set_damage(self, value: int) -> None:
        value = int(value * -1)
        if value > 0:
            print(f'Recebeu {value} de Dano!!!')
        elif value < 0:
            print(f'Recebeu {-value} de Cura.')
        self.__damage += value
        if self.__damage > self.hit_points:
            self.__damage = self.hit_points
        elif self.__damage < 0:
            self.__damage = 0

    def update(self) -> None:
        self.__boost_stats()

    def __boost_stats(self) -> None:
        self.__bonus_hit_points = 0
        self.__bonus_initiative = 0
        self.__bonus_physical_attack = 0
        self.__bonus_precision_attack = 0
        self.__bonus_magical_attack = 0
        self.__bonus_physical_defense = 0
        self.__bonus_magical_defense = 0
        self.__bonus_hit = 0
        self.__bonus_evasion = 0

        for sb in self.__stats_boosters:
            self.__bonus_hit_points += int(sb.bonus_hit_points)
            self.__bonus_initiative += int(sb.bonus_initiative)
            self.__bonus_physical_attack += int(sb.bonus_physical_attack)
            self.__bonus_precision_attack += int(sb.bonus_precision_attack)
            self.__bonus_magical_attack += int(sb.bonus_magical_attack)
            self.__bonus_physical_defense += int(sb.bonus_physical_defense)
            self.__bonus_magical_defense += int(sb.bonus_magical_defense)
            self.__bonus_hit += int(sb.bonus_hit)
            self.__bonus_evasion += int(sb.bonus_evasion)

    # Getters
    # Combat Attributes
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
            (self.dexterity * 1.5) +
            (self.wisdom * 1.5) +
            (self.charisma * 1.5) +
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
    def precision_attack(self) -> int:
        return int(
            (self.dexterity * 2.5) +
            self.bonus_precision_attack
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
    def hit(self) -> int:
        return int(
            (self.dexterity * 2) +
            self.wisdom +
            self.bonus_hit
        )

    @property
    def evasion(self) -> int:
        return int(
            (self.dexterity * 2) +
            self.wisdom +
            self.bonus_evasion
        )

    # Setters
    # Combat Attributes
    @hit_points.setter
    def hit_points(self, value) -> int:
        return self.set_damage(value)

    hp = hit_points

    @current_hit_points.setter
    def current_hit_points(self, value) -> int:
        return self.set_damage(value)

    # Getters
    # Base Attributes
    strength = property(fget=lambda self: self.__base_stats.strength)
    dexterity = property(fget=lambda self: self.__base_stats.dexterity)
    constitution = property(fget=lambda self: self.__base_stats.constitution)
    intelligence = property(fget=lambda self: self.__base_stats.intelligence)
    wisdom = property(fget=lambda self: self.__base_stats.wisdom)
    charisma = property(fget=lambda self: self.__base_stats.charisma)

    # Getters
    # Bonus Combat Attributes
    @property
    def bonus_initiative(self) -> int:
        return self.__bonus_initiative

    @property
    def bonus_physical_attack(self) -> int:
        return self.__bonus_physical_attack

    @property
    def bonus_precision_attack(self) -> int:
        return self.__bonus_precision_attack

    @property
    def bonus_magical_attack(self) -> int:
        return self.__bonus_magical_attack

    @property
    def bonus_physical_defense(self) -> int:
        return self.__bonus_physical_defense

    @property
    def bonus_magical_defense(self) -> int:
        return self.__bonus_magical_defense

    @property
    def bonus_hit_points(self) -> int:
        return self.__bonus_hit_points

    @property
    def bonus_hit(self) -> int:
        return self.__bonus_hit

    @property
    def bonus_evasion(self) -> int:
        return self.__bonus_evasion

    # Getters
    # Stats Boosters
    @property
    def stats_boosters(self) -> set:
        return set(self.__stats_boosters)

    def get_sheet(self) -> str:
        base_init = self.initiative - self.bonus_initiative
        base_hp = self.hit_points - self.bonus_hit_points
        base_phy_atk = self.physical_attack - self.bonus_physical_attack
        base_pre_atk = self.precision_attack - self.bonus_precision_attack
        base_mag_atk = self.magical_attack - self.bonus_magical_attack
        base_phy_def = self.physical_defense - self.bonus_physical_defense
        base_mag_def = self.magical_defense - self.bonus_magical_defense
        base_hit = self.hit - self.bonus_hit
        base_evasion = self.evasion - self.bonus_evasion
        return (
            '\n' + SECTION_HEAD.format('ATRIBUTOS DE COMBATE') +

            f'HP: {self.current_hit_points}/{self.hit_points} '
            f'[{base_hp}{self.bonus_hit_points:+}]\n'

            f'INICIATIVA: {self.initiative:02} '
            f'[{base_init}{self.bonus_initiative:+}]\n'

            f'ATAQUE FÍSICO: {self.physical_attack:02} '
            f'[{base_phy_atk}{self.bonus_physical_attack:+}]\n'

            f'ATAQUE DE PRECISÃO: {self.precision_attack:02} '
            f'[{base_pre_atk}{self.bonus_precision_attack:+}]\n'

            f'ATAQUE MÁGICO: {self.magical_attack:02} '
            f'[{base_mag_atk}{self.bonus_magical_attack:+}]\n'

            f'DEFESA FÍSICA: {self.physical_defense:02} '
            f'[{base_phy_def}{self.bonus_physical_defense:+}]\n'

            f'DEFESA MÁGICA: {self.magical_defense:02} '
            f'[{base_mag_def}{self.bonus_magical_defense:+}]\n'

            f'ACERTO: {self.hit:02} '
            f'[{base_hit}{self.bonus_hit:+}]\n'

            f'EVASÃO: {self.evasion:02} '
            f'[{base_evasion}{self.bonus_evasion:+}]\n'
        )

    def __repr__(self) -> str:
        return (
            TEXT_DELIMITER +
            f'{self.__base_stats.get_sheet()}'
            f'{self.get_sheet()}'
            + TEXT_DELIMITER
        )


if __name__ == '__main__':
    base_stats = BaseStats(10)
    combat_stats = CombatStats(
        level=10,
        base_strength=6,
        base_dexterity=6,
        base_constitution=6,
        base_intelligence=3,
        base_wisdom=3,
        base_charisma=4,
        damage=0,
    )

    print(combat_stats)
    # Danos e Cura
    combat_stats.hit_points = -10
    combat_stats.current_hit_points = -20
    combat_stats.hp = -30
    combat_stats.hp = 10  # Cura
    print(combat_stats)
