from rpgram.boosters import StatsBooster


class Race(StatsBooster):
    def __init__(
        self,
        name: str,
        description: str = '',
        bonus_strength: int = 0,
        bonus_dexterity: int = 0,
        bonus_constitution: int = 0,
        bonus_intelligence: int = 0,
        bonus_wisdom: int = 0,
        bonus_charisma: int = 0,
        multiplier_strength: float = 1.0,
        multiplier_dexterity: float = 1.0,
        multiplier_constitution: float = 1.0,
        multiplier_intelligence: float = 1.0,
        multiplier_wisdom: float = 1.0,
        multiplier_charisma: float = 1.0,
    ) -> None:
        super().__init__(
            bonus_strength=bonus_strength,
            bonus_dexterity=bonus_dexterity,
            bonus_constitution=bonus_constitution,
            bonus_intelligence=bonus_intelligence,
            bonus_wisdom=bonus_wisdom,
            bonus_charisma=bonus_charisma,
            multiplier_strength=multiplier_strength,
            multiplier_dexterity=multiplier_dexterity,
            multiplier_constitution=multiplier_constitution,
            multiplier_intelligence=multiplier_intelligence,
            multiplier_wisdom=multiplier_wisdom,
            multiplier_charisma=multiplier_charisma,
        )
        self.__name = name
        self.__description = description

    def get_sheet(self) -> str:
        return (
            f'Raça: {self.name}\n'
            f'Descrição da Raça: {self.description}\n'
        )

    def __repr__(self) -> str:
        return (
            f'########################################\n'
            f'{self.get_sheet()}'
            f'{super().get_sheet()}'
            f'########################################\n'
        )

    name = property(lambda self: self.__name)
    description = property(lambda self: self.__description)


if __name__ == '__main__':
    race = Race(
        name='Humano',
        description='Humano Teste',
        bonus_strength=10,
        bonus_dexterity=10,
        bonus_constitution=10,
        bonus_intelligence=10,
        bonus_wisdom=10,
        bonus_charisma=10,
        multiplier_strength=1,
        multiplier_dexterity=1.2,
        multiplier_constitution=1.3,
        multiplier_intelligence=1.4,
        multiplier_wisdom=1.5,
        multiplier_charisma=1.6,
    )
    print(race)
