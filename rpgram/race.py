if __name__ in ['__main__', 'race']:
    from stats_bonus import BonusStats
else:
    from rpgram.stats_bonus import BonusStats


class Race(BonusStats):
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
        bonus_hit_points: int = 0,
        bonus_initiative: int = 0,
        bonus_physical_attack: int = 0,
        bonus_magical_attack: int = 0,
        bonus_physical_defense: int = 0,
        bonus_magical_defense: int = 0,
    ) -> None:
        super().__init__(
            bonus_strength,
            bonus_dexterity,
            bonus_constitution,
            bonus_intelligence,
            bonus_wisdom,
            bonus_charisma,
            bonus_hit_points,
            bonus_initiative,
            bonus_physical_attack,
            bonus_magical_attack,
            bonus_physical_defense,
            bonus_magical_defense,
        )
        self.__name = name
        self.__description = description

    def get_sheet(self) -> str:
        return (
            f'Raça: {self.name}\n'
            f'Descrição: {self.description}\n'
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
        bonus_hit_points=0,
        bonus_initiative=0,
        bonus_physical_attack=0,
        bonus_magical_attack=0,
        bonus_physical_defense=0,
        bonus_magical_defense=0,
    )
    print(race)
