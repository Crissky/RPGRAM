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

        self.__mod_strength = 0
        self.__mod_dexterity = 0
        self.__mod_constitution = 0
        self.__mod_intelligence = 0
        self.__mod_wisdom = 0
        self.__mod_charisma = 0

    def __get_points(self) -> int:
        max_level_points = self.__level * 3
        points = max_level_points - self.total_base_stats
        if points < 0:
            raise ValueError(
                f'Foi gasto mais pontos nos atributos que o nível permite.\n'
                f'Total de pontos do level {self.__level}: '
                f'{max_level_points}.\n'
                f'Total de pontos gastos: {self.total_base_stats}.'
            )
        return points

    def __add_stats(self, points: int, attribute: str) -> None:
        points = int(points)
        clean_attribute = attribute.split('_')[-1].title()
        print(f'Adicionando {points} ponto(s) ao atributo {clean_attribute}.')
        if points > self.points:
            raise ValueError(
                f'Não há pontos suficientes para adicionar.\n'
                f'Atualmente você tem {self.points} ponto(s).'
            )
        if points <= 0:
            raise ValueError('Não é possível adicionar menos que 1 ponto.')
        new_value = getattr(self, attribute) + points
        setattr(self, attribute, new_value)

    def __add_mod_stats(self, value: int, attribute: str) -> None:
        value = int(value)
        clean_attribute = attribute.split('_')[-1].title()
        print(
            f'Adicionando {value} ponto(s) '
            f'ao modificador do atributo {clean_attribute}.'
        )
        setattr(self, attribute, value)

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

    # Getters
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

    @property
    def strength(self) -> int:
        return self.base_strength + self.mod_strength

    @property
    def dexterity(self) -> int:
        return self.base_dexterity + self.mod_dexterity

    @property
    def constitution(self) -> int:
        return self.base_constitution + self.mod_constitution

    @property
    def intelligence(self) -> int:
        return self.base_intelligence + self.mod_intelligence

    @property
    def wisdom(self) -> int:
        return self.base_wisdom + self.mod_wisdom

    @property
    def charisma(self) -> int:
        return self.base_charisma + self.mod_charisma

    # Setters
    @xp.setter
    def xp(self, value: int) -> None:
        value = int(value)
        if value < 0:
            raise ValueError(
                f'Não é possível adicionar pontos de experiência com valores '
                f'negativos. Valor {value}.'
            )
        print(f'Ganhou {value} pontos de experiência.')
        while value > 0:
            self.__current_xp += value
            if self.__current_xp >= self.next_level_xp:
                value = self.__current_xp - self.next_level_xp
                self.__current_xp = 0
                self.__level += 1
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
    mod_strength = property(
        fget=lambda self: self.__mod_strength,
        fset=lambda self, value: self.__add_mod_stats(
            value, '_BaseStats__mod_strength'
        )
    )
    mod_dexterity = property(
        fget=lambda self: self.__mod_dexterity,
        fset=lambda self, value: self.__add_mod_stats(
            value, '_BaseStats__mod_dexterity'
        )
    )
    mod_constitution = property(
        fget=lambda self: self.__mod_constitution,
        fset=lambda self, value: self.__add_mod_stats(
            value, '_BaseStats__mod_constitution'
        )
    )
    mod_intelligence = property(
        fget=lambda self: self.__mod_intelligence,
        fset=lambda self, value: self.__add_mod_stats(
            value, '_BaseStats__mod_intelligence'
        )
    )
    mod_wisdom = property(
        fget=lambda self: self.__mod_wisdom,
        fset=lambda self, value: self.__add_mod_stats(
            value, '_BaseStats__mod_wisdom'
        )
    )
    mod_charisma = property(
        fget=lambda self: self.__mod_charisma,
        fset=lambda self, value: self.__add_mod_stats(
            value, '_BaseStats__mod_charisma'
        )
    )

    def __repr__(self) -> str:
        return (
            f'########################################\n'
            f'Level: {self.level}\n'
            f'Experiência: {self.xp}/{self.next_level_xp}\n'
            f'Pontos: {self.points}\n'
            f'Forca: {self.base_strength} + '
            f'({self.mod_strength}) = {self.strength}\n'
            f'Destreza: {self.base_dexterity} + '
            f'({self.mod_dexterity}) = {self.dexterity}\n'
            f'Constituição: {self.base_constitution} + '
            f'({self.mod_constitution}) = {self.constitution}\n'
            f'Inteligência: {self.base_intelligence} + '
            f'({self.mod_intelligence}) = {self.intelligence}\n'
            f'Sabedoria: {self.base_wisdom} + '
            f'({self.mod_wisdom}) = {self.wisdom}\n'
            f'Carisma: {self.base_charisma} + '
            f'({self.mod_charisma}) = {self.charisma}\n'
            f'########################################'
        )


if __name__ == '__main__':
    stats = BaseStats(1.50)
    print(stats)
    stats.xp = 310
    print(stats)
    stats.base_strength = 2
    stats.mod_strength = 5
    print(stats)
    stats.base_dexterity = 1
    stats.mod_dexterity = 2
    print(stats)
    stats.base_constitution = 1
    stats.mod_constitution = 3
    print(stats)
    stats.base_intelligence = 1
    stats.mod_intelligence = 10
    print(stats)
    stats.base_wisdom = 1
    print(stats)
    stats.base_charisma = 1
    stats.mod_charisma = -5
    print(stats)
