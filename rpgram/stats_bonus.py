class BonusStats:
    '''Classe Base para ser usada em características que dão bônus aos 
    atributos dos personagens como: Raça, Classe, Taletos, Equipamentos, etc.

    A princípio esses atributos não são alterados, permanencendo os mesmos 
    valores do momento de sua criação.

    '''

    def __init__(
        self,
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
        self.__bonus_strength = bonus_strength
        self.__bonus_dexterity = bonus_dexterity
        self.__bonus_constitution = bonus_constitution
        self.__bonus_intelligence = bonus_intelligence
        self.__bonus_wisdom = bonus_wisdom
        self.__bonus_charisma = bonus_charisma
        self.__bonus_hit_points = bonus_hit_points
        self.__bonus_initiative = bonus_initiative
        self.__bonus_physical_attack = bonus_physical_attack
        self.__bonus_magical_attack = bonus_magical_attack
        self.__bonus_physical_defense = bonus_physical_defense
        self.__bonus_magical_defense = bonus_magical_defense

    def get_sheet(self) -> str:
        return (
            f'FOR: {self.strength:+}\n'
            f'DES: {self.dexterity:+}\n'
            f'CON: {self.constitution:+}\n'
            f'INT: {self.intelligence:+}\n'
            f'SAB: {self.wisdom:+}\n'
            f'CAR: {self.charisma:+}\n\n'
            f'HP: {self.hp:+}\n'
            f'ATAQUE FÍSICO: {self.physical_attack:+}\n'
            f'ATAQUE MÁGICO: {self.magical_attack:+}\n'
            f'DEFESA FÍSICA: {self.physical_defense:+}\n'
            f'DEFESA MÁGICA: {self.magical_defense:+}\n'
            f'INICIATIVA: {self.initiative:+}\n'
        )

    def __repr__(self) -> str:
        return (
            f'########################################\n'
            f'{self.get_sheet()}'
            f'########################################\n'
        )

    strength = bonus_strength = property(
        fget=lambda self: self.__bonus_strength)
    dexterity = bonus_dexterity = property(
        fget=lambda self: self.__bonus_dexterity)
    constitution = bonus_constitution = property(
        fget=lambda self: self.__bonus_constitution)
    intelligence = bonus_intelligence = property(
        fget=lambda self: self.__bonus_intelligence)
    wisdom = bonus_wisdom = property(fget=lambda self: self.__bonus_wisdom)
    charisma = bonus_charisma = property(
        fget=lambda self: self.__bonus_charisma)
    physical_attack = bonus_physical_attack = property(
        fget=lambda self: self.__bonus_physical_attack)
    magical_attack = bonus_magical_attack = property(
        fget=lambda self: self.__bonus_magical_attack)
    physical_defense = bonus_physical_defense = property(
        fget=lambda self: self.__bonus_physical_defense)
    magical_defense = bonus_magical_defense = property(
        fget=lambda self: self.__bonus_magical_defense)
    hp = hit_points = bonus_hit_points = property(
        fget=lambda self: self.__bonus_hit_points)
    initiative = bonus_initiative = property(
        fget=lambda self: self.__bonus_initiative)


if __name__ == '__main__':
    bonus_stats = BonusStats(
        bonus_strength=10,
        bonus_dexterity=11,
        bonus_constitution=12,
        bonus_intelligence=13,
        bonus_wisdom=14,
        bonus_charisma=15,
        bonus_hit_points=160,
        bonus_initiative=17,
        bonus_physical_attack=18,
        bonus_magical_attack=-19,
        bonus_physical_defense=20,
        bonus_magical_defense=-21,
    )
    print(bonus_stats)
