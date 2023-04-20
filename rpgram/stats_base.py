class BaseStats:
    '''Classe que representa as estatísticas básicas de um personagem.

    Fonte: https://i.pinimg.com/originals/ee/9b/0c/ee9b0cd5fc0c94dcfb215ad94c6a6871.jpg'''

    def __init__(self, level: int = 1) -> None:
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

        self.__bonus_strength = 0
        self.__bonus_dexterity = 0
        self.__bonus_constitution = 0
        self.__bonus_intelligence = 0
        self.__bonus_wisdom = 0
        self.__bonus_charisma = 0

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
        print(f'Adicionando {points} Ponto(s) ao atributo {clean_attribute}.')
        if points > self.points:
            raise ValueError(
                f'Não há Pontos suficientes para adicionar.\n'
                f'Atualmente você tem {self.points} Ponto(s).'
            )
        if points <= 0:
            raise ValueError('Não é possível adicionar menos que 1 Ponto.')
        new_value = getattr(self, attribute) + points
        setattr(self, attribute, new_value)

    def __add_bonus_stats(self, value: int, attribute: str) -> None:
        value = int(value)
        clean_attribute = attribute.split('_')[-1].title()
        print(
            f'Adicionando {value} Ponto(s) '
            f'ao bônus do atributo {clean_attribute}.'
        )
        setattr(self, attribute, value)

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
        return self.base_strength + self.bonus_strength

    @property
    def dexterity(self) -> int:
        return self.base_dexterity + self.bonus_dexterity

    @property
    def constitution(self) -> int:
        return self.base_constitution + self.bonus_constitution

    @property
    def intelligence(self) -> int:
        return self.base_intelligence + self.bonus_intelligence

    @property
    def wisdom(self) -> int:
        return self.base_wisdom + self.bonus_wisdom

    @property
    def charisma(self) -> int:
        return self.base_charisma + self.bonus_charisma

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

    xp_points = xp

    # Getters and Setters
    # Attribute Bonus
    bonus_strength = property(
        fget=lambda self: self.__bonus_strength,
        fset=lambda self, value: self.__add_bonus_stats(
            value, '_BaseStats__bonus_strength'
        )
    )
    bonus_dexterity = property(
        fget=lambda self: self.__bonus_dexterity,
        fset=lambda self, value: self.__add_bonus_stats(
            value, '_BaseStats__bonus_dexterity'
        )
    )
    bonus_constitution = property(
        fget=lambda self: self.__bonus_constitution,
        fset=lambda self, value: self.__add_bonus_stats(
            value, '_BaseStats__bonus_constitution'
        )
    )
    bonus_intelligence = property(
        fget=lambda self: self.__bonus_intelligence,
        fset=lambda self, value: self.__add_bonus_stats(
            value, '_BaseStats__bonus_intelligence'
        )
    )
    bonus_wisdom = property(
        fget=lambda self: self.__bonus_wisdom,
        fset=lambda self, value: self.__add_bonus_stats(
            value, '_BaseStats__bonus_wisdom'
        )
    )
    bonus_charisma = property(
        fget=lambda self: self.__bonus_charisma,
        fset=lambda self, value: self.__add_bonus_stats(
            value, '_BaseStats__bonus_charisma'
        )
    )

    # Getters and Setters
    # Attribute Modifiers
    mod_strength = property(
        fget=lambda self: self.__get_modifier_stats(self.strength)
    )
    mod_dexterity = property(
        fget=lambda self: self.__get_modifier_stats(self.dexterity)
    )
    mod_constitution = property(
        fget=lambda self: self.__get_modifier_stats(self.constitution)
    )
    mod_intelligence = property(
        fget=lambda self: self.__get_modifier_stats(self.intelligence)
    )
    mod_wisdom = property(
        fget=lambda self: self.__get_modifier_stats(self.wisdom)
    )
    mod_charisma = property(
        fget=lambda self: self.__get_modifier_stats(self.charisma)
    )

    def __repr__(self) -> str:
        str_sign = '+' if self.bonus_strength >= 0 else ''
        dex_sign = '+' if self.bonus_dexterity >= 0 else ''
        con_sign = '+' if self.bonus_constitution >= 0 else ''
        int_sign = '+' if self.bonus_intelligence >= 0 else ''
        wis_sign = '+' if self.bonus_wisdom >= 0 else ''
        cha_sign = '+' if self.bonus_charisma >= 0 else ''
        return (
            f'########################################\n'

            f'Level: {self.level}\n'
            f'Experiência: {self.xp}/{self.next_level_xp}\n'
            f'Pontos: {self.points}\n'

            f'Força: {self.strength} '
            f'[{self.base_strength}{str_sign}{self.bonus_strength}] '
            f'({self.mod_strength})\n'

            f'Destreza: {self.dexterity} '
            f'[{self.base_dexterity}{dex_sign}{self.bonus_dexterity}] '
            f'({self.mod_dexterity})\n'

            f'Constituição: {self.constitution} '
            f'[{self.base_constitution}{con_sign}{self.bonus_constitution}] '
            f'({self.mod_constitution})\n'

            f'Inteligência: {self.intelligence} '
            f'[{self.base_intelligence}{int_sign}{self.bonus_intelligence}] '
            f'({self.mod_intelligence})\n'

            f'Sabedoria: {self.base_wisdom} '
            f'[{self.base_wisdom}{wis_sign}{self.bonus_wisdom}] '
            f'({self.mod_wisdom})\n'

            f'Carisma: {self.base_charisma} '
            f'[{self.base_charisma}{cha_sign}{self.bonus_charisma}] '
            f'({self.mod_charisma})\n'

            f'########################################\n'
        )


if __name__ == '__main__':
    stats = BaseStats(1.50)
    print(stats)
    stats.xp = 310
    print(stats)
    stats.base_strength = 2
    stats.bonus_strength = 5
    print(stats)
    stats.base_dexterity = 1
    stats.bonus_dexterity = 2
    print(stats)
    stats.base_constitution = 1
    stats.bonus_constitution = 3
    print(stats)
    stats.base_intelligence = 1
    stats.bonus_intelligence = 10
    print(stats)
    stats.base_wisdom = 1
    print(stats)
    stats.base_charisma = 1
    stats.bonus_charisma = -5
    print(stats)
