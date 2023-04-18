class BaseStats:
    '''Classe que representa as estatísticas básicas de um personagem.'''

    def __init__(self, level: int) -> None:
        self.__strength = 0
        self.__dexterity = 0
        self.__constitution = 0
        self.__intelligence = 0
        self.__wisdom = 0
        self.__charisma = 0
        self.__level = level
        self.__current_xp = 0

    def __get_points(self) -> int:
        max_level_points = self.__level * 3
        points = max_level_points - self.total_stats
        if points < 0:
            raise ValueError(
                f'Foi gasto mais pontos nos atributos que o nível permite.\n'
                f'Total de pontos do level {self.__level}: {max_level_points}.\n'
                f'Total de pontos gastos: {self.total_stats}.'
            )
        return points

    def add_stats(self, points: int, attribute: str) -> None:
        if points > self.points:
            raise ValueError(
                f'Não há pontos suficientes para adicionar.\n'
                f'Atualmente você tem {self.points} pontos.'
            )
        if points < 0:
            raise ValueError('Não é possível adicionar pontos negativos.')
        new_value = getattr(self, attribute) + points
        setattr(self, attribute, new_value)

    @property
    def total_stats(self) -> int:
        return sum([
            self.strength,
            self.dexterity,
            self.constitution,
            self.intelligence,
            self.wisdom,
            self.charisma
        ])

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

    @property
    def strength(self) -> int:
        return self.__strength

    @property
    def dexterity(self) -> int:
        return self.__dexterity

    @property
    def constitution(self) -> int:
        return self.__constitution

    @property
    def intelligence(self) -> int:
        return self.__intelligence

    @property
    def wisdom(self) -> int:
        return self.__wisdom

    @property
    def charisma(self) -> int:
        return self.__charisma

    # Setters
    @xp.setter
    def xp(self, value: int) -> None:
        if value < 0:
            raise ValueError(
                'Não é possível adicionar pontos de experiéncia com valores '
                'negativos.'
            )
        while value > 0:
            self.__current_xp += value
            if self.__current_xp >= self.next_level_xp:
                value = self.__current_xp - self.next_level_xp
                self.__current_xp = 0
                self.__level += 1
            else:
                break

    @strength.setter
    def strength(self, value: int) -> None:
        self.add_stats(value, '_BaseStats__strength')

    @dexterity.setter
    def dexterity(self, value: int) -> None:
        return self.add_stats(value, '_BaseStats__dexterity')

    @constitution.setter
    def constitution(self, value: int) -> None:
        return self.add_stats(value, '_BaseStats__constitution')

    @intelligence.setter
    def intelligence(self, value: int) -> None:
        return self.add_stats(value, '_BaseStats__intelligence')

    @wisdom.setter
    def wisdom(self, value: int) -> None:
        return self.add_stats(value, '_BaseStats__wisdom')

    @charisma.setter
    def charisma(self, value: int) -> None:
        return self.add_stats(value, '_BaseStats__charisma')

    def __repr__(self) -> str:
        return (
            f'Level: {self.level}\n'
            f'Experiência: {self.xp}/{self.next_level_xp}\n'
            f'Pontos: {self.points}\n'
            f'Forca: {self.strength}\n'
            f'Destreza: {self.dexterity}\n'
            f'Constituição: {self.constitution}\n'
            f'Inteligência: {self.intelligence}\n'
            f'Sabedoria: {self.wisdom}\n'
            f'Carisma: {self.charisma}'
        )
    
    xp_points = xp
