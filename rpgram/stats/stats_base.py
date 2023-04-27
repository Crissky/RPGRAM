from rpgram.boosters import StatsBooster


class BaseStats:
    '''Classe que representa as estatísticas básicas de um personagem.

    Fonte: https://i.pinimg.com/originals/ee/9b/0c/ee9b0cd5fc0c94dcfb215ad94c6a6871.jpg'''

    def __init__(
        self,
        level: int = 1,
        base_strength: int = 0,
        base_dexterity: int = 0,
        base_constitution: int = 0,
        base_intelligence: int = 0,
        base_wisdom: int = 0,
        base_charisma: int = 0,
        *stats_boosters: StatsBooster
    ) -> None:
        if level < 1 and isinstance(level, int):
            raise ValueError('Nível deve ser um inteiro maior que zero.')
        self.__level = int(level)
        self.__current_xp = 0

        self.__base_strength = 0
        self.__base_dexterity = 0
        self.__base_constitution = 0
        self.__base_intelligence = 0
        self.__base_wisdom = 0
        self.__base_charisma = 0

        self.base_strength = base_strength
        self.base_dexterity = base_dexterity
        self.base_constitution = base_constitution
        self.base_intelligence = base_intelligence
        self.base_wisdom = base_wisdom
        self.base_charisma = base_charisma

        self.__stats_boosters = set(stats_boosters)

    def __get_points(self) -> int:
        max_level_points = self.__level * 3
        points = max_level_points - self.total_base_stats
        if points < 0:
            raise ValueError(
                f'Foi gasto mais Pontos nos atributos que o Nível permite.\n'
                f'Total de Pontos do Nível {self.__level}: '
                f'{max_level_points}.\n'
                f'Total de Pontos gastos: {self.total_base_stats}.'
            )
        return points

    def __get_modifier_stats(self, attribute_points: int) -> int:
        return (attribute_points - 10) // 2

    def __add_stats(self, points: int, attribute: str) -> None:
        points = int(points)
        clean_attribute = attribute.split('_')[-1].title()
        print(f'Adicionando {points} Ponto(s) de {clean_attribute}.')
        if points > self.points:
            raise ValueError(
                f'Não há Pontos({points}) suficientes para adicionar.\n'
                f'Atualmente você tem {self.points} Ponto(s).'
            )
        if points < 0:  # Permite 0 por causa do init.
            raise ValueError(
                f'Não é possível adicionar menos que '
                f'1 Ponto de {clean_attribute}.'
            )
        new_value = getattr(self, attribute) + points
        setattr(self, attribute, new_value)

    def __boost_stats(self) -> None:
        self.__bonus_strength = 0
        self.__bonus_dexterity = 0
        self.__bonus_constitution = 0
        self.__bonus_intelligence = 0
        self.__bonus_wisdom = 0
        self.__bonus_charisma = 0

        self.__multiplier_strength = 1
        self.__multiplier_dexterity = 1
        self.__multiplier_constitution = 1
        self.__multiplier_intelligence = 1
        self.__multiplier_wisdom = 1
        self.__multiplier_charisma = 1

        for sb in self.__stats_boosters:
            self.__bonus_strength += int(sb.bonus_strength)
            self.__bonus_dexterity += int(sb.bonus_dexterity)
            self.__bonus_constitution += int(sb.bonus_constitution)
            self.__bonus_intelligence += int(sb.bonus_intelligence)
            self.__bonus_wisdom += int(sb.bonus_wisdom)
            self.__bonus_charisma += int(sb.bonus_charisma)

            self.__multiplier_strength += sb.multiplier_strength - 1.0
            self.__multiplier_dexterity += sb.multiplier_dexterity - 1.0
            self.__multiplier_constitution += sb.multiplier_constitution - 1.0
            self.__multiplier_intelligence += sb.multiplier_intelligence - 1.0
            self.__multiplier_wisdom += sb.multiplier_wisdom - 1.0
            self.__multiplier_charisma += sb.multiplier_charisma - 1.0

    # Getters
    @property
    def total_base_stats(self) -> int:
        return int(sum([
            self.base_strength,
            self.base_dexterity,
            self.base_constitution,
            self.base_intelligence,
            self.base_wisdom,
            self.base_charisma
        ]))

    @property
    def level(self) -> int:
        return self.__level

    @property
    def next_level_xp(self) -> int:
        return self.__level * 100

    @property
    def points(self) -> int:
        return self.__get_points()

    @property
    def xp(self) -> int:
        return self.__current_xp

    # Base Attributes
    @property
    def base_strength(self) -> int:
        return self.__base_strength

    @property
    def base_dexterity(self) -> int:
        return self.__base_dexterity

    @property
    def base_constitution(self) -> int:
        return self.__base_constitution

    @property
    def base_intelligence(self) -> int:
        return self.__base_intelligence

    @property
    def base_wisdom(self) -> int:
        return self.__base_wisdom

    @property
    def base_charisma(self) -> int:
        return self.__base_charisma

    # Attributes
    @property
    def strength(self) -> int:
        self.__boost_stats()
        return int(
            (self.base_strength + self.bonus_strength) *
            self.multiplier_strength
        )

    @property
    def dexterity(self) -> int:
        self.__boost_stats()
        return int(
            (self.base_dexterity + self.bonus_dexterity) *
            self.multiplier_dexterity
        )

    @property
    def constitution(self) -> int:
        self.__boost_stats()
        return int(
            (self.base_constitution + self.bonus_constitution) *
            self.multiplier_constitution
        )

    @property
    def intelligence(self) -> int:
        self.__boost_stats()
        return int(
            (self.base_intelligence + self.bonus_intelligence) *
            self.multiplier_intelligence
        )

    @property
    def wisdom(self) -> int:
        self.__boost_stats()
        return int(
            (self.base_wisdom + self.bonus_wisdom) *
            self.multiplier_wisdom
        )

    @property
    def charisma(self) -> int:
        self.__boost_stats()
        return int(
            (self.base_charisma + self.bonus_charisma) *
            self.multiplier_charisma
        )

    # Setters
    @xp.setter
    def xp(self, value: int) -> None:
        value = int(value)
        if value <= 0:
            raise ValueError(
                f'Não é possível adicionar Pontos de Experiência menor que 1.'
            )
        print(f'Ganhou {value} Pontos de Experiência.')
        while value > 0:
            self.__current_xp += value
            if self.__current_xp >= self.next_level_xp:
                value = self.__current_xp - self.next_level_xp
                self.__current_xp = 0
                self.__level += 1
                print(
                    f'Subiu para o Nível {self.__level}. '
                    f'Agora possui {self.points} Pontos.'
                )
            else:
                break

    @base_strength.setter
    def base_strength(self, value: int) -> None:
        self.__add_stats(value, '_BaseStats__base_strength')

    @base_dexterity.setter
    def base_dexterity(self, value: int) -> None:
        return self.__add_stats(value, '_BaseStats__base_dexterity')

    @base_constitution.setter
    def base_constitution(self, value: int) -> None:
        return self.__add_stats(value, '_BaseStats__base_constitution')

    @base_intelligence.setter
    def base_intelligence(self, value: int) -> None:
        return self.__add_stats(value, '_BaseStats__base_intelligence')

    @base_wisdom.setter
    def base_wisdom(self, value: int) -> None:
        return self.__add_stats(value, '_BaseStats__base_wisdom')

    @base_charisma.setter
    def base_charisma(self, value: int) -> None:
        return self.__add_stats(value, '_BaseStats__base_charisma')

    @strength.setter
    def strength(self, value: int) -> None:
        self.base_strength = value

    @dexterity.setter
    def dexterity(self, value: int) -> None:
        self.base_dexterity = value

    @constitution.setter
    def constitution(self, value: int) -> None:
        self.base_constitution = value

    @intelligence.setter
    def intelligence(self, value: int) -> None:
        self.base_intelligence = value

    @wisdom.setter
    def wisdom(self, value: int) -> None:
        self.base_wisdom = value

    @charisma.setter
    def charisma(self, value: int) -> None:
        self.base_charisma = value

    xp_points = xp

    # Getters and Setters
    # Attribute Bonus
    @property
    def bonus_strength(self) -> int:
        return self.__bonus_strength

    @property
    def bonus_dexterity(self) -> int:
        return self.__bonus_dexterity

    @property
    def bonus_constitution(self) -> int:
        return self.__bonus_constitution

    @property
    def bonus_intelligence(self) -> int:
        return self.__bonus_intelligence

    @property
    def bonus_wisdom(self) -> int:
        return self.__bonus_wisdom

    @property
    def bonus_charisma(self) -> int:
        return self.__bonus_charisma

    # Getters and Setters
    # Attribute Bonus
    @property
    def multiplier_strength(self) -> float:
        return self.__multiplier_strength

    @property
    def multiplier_dexterity(self) -> float:
        return self.__multiplier_dexterity

    @property
    def multiplier_constitution(self) -> float:
        return self.__multiplier_constitution

    @property
    def multiplier_intelligence(self) -> float:
        return self.__multiplier_intelligence

    @property
    def multiplier_wisdom(self) -> float:
        return self.__multiplier_wisdom

    @property
    def multiplier_charisma(self) -> float:
        return self.__multiplier_charisma

    # Getters and Setters
    # Attribute Modifiers
    @property
    def mod_strength(self) -> int:
        return self.__get_modifier_stats(self.strength)

    @property
    def mod_dexterity(self) -> int:
        return self.__get_modifier_stats(self.dexterity)

    @property
    def mod_constitution(self) -> int:
        return self.__get_modifier_stats(self.constitution)

    @property
    def mod_intelligence(self) -> int:
        return self.__get_modifier_stats(self.intelligence)

    @property
    def mod_wisdom(self) -> int:
        return self.__get_modifier_stats(self.wisdom)

    @property
    def mod_charisma(self) -> int:
        return self.__get_modifier_stats(self.charisma)

    def get_sheet(self) -> str:
        return (
            f'Level: {self.level}\n'
            f'Experiência: {self.xp}/{self.next_level_xp}\n'
            f'Pontos: {self.points}\n'

            f'\n◇── ATRIBUTOS BASE ──◇\n'

            f'FOR: {self.strength} '
            f'[{self.base_strength}{self.bonus_strength:+}]'
            f'x{self.multiplier_strength} '
            f'({self.mod_strength})\n'

            f'DES: {self.dexterity} '
            f'[{self.base_dexterity}{self.bonus_dexterity:+}]'
            f'x{self.multiplier_dexterity} '
            f'({self.mod_dexterity})\n'

            f'CON: {self.constitution} '
            f'[{self.base_constitution}{self.bonus_constitution:+}]'
            f'x{self.multiplier_constitution} '
            f'({self.mod_constitution})\n'

            f'INT: {self.intelligence} '
            f'[{self.base_intelligence}{self.bonus_intelligence:+}]'
            f'x{self.multiplier_intelligence} '
            f'({self.mod_intelligence})\n'

            f'SAB: {self.wisdom} '
            f'[{self.base_wisdom}{self.bonus_wisdom:+}]'
            f'x{self.multiplier_wisdom} '
            f'({self.mod_wisdom})\n'

            f'CAR: {self.charisma} '
            f'[{self.base_charisma}{self.bonus_charisma:+}]'
            f'x{self.multiplier_charisma} '
            f'({self.mod_charisma})\n'
        )

    def __repr__(self) -> str:
        return (
            f'########################################\n'
            f'{self.get_sheet()}'
            f'########################################\n'
        )


if __name__ == '__main__':
    stats = BaseStats(1.50, 3, 0, 0, 0, 0, 0)
    print(stats)
    stats.xp = 310
    print(stats)
    stats.strength = 1
    print(stats)
    stats.dexterity = 1
    print(stats)
    stats.constitution = 1
    print(stats)
    stats.intelligence = 1
    print(stats)
    stats.wisdom = 1
    print(stats)
    stats.charisma = 1
    print(stats)
