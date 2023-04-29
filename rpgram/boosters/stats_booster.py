class StatsBooster:
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
        multiplier_strength: float = 1.0,
        multiplier_dexterity: float = 1.0,
        multiplier_constitution: float = 1.0,
        multiplier_intelligence: float = 1.0,
        multiplier_wisdom: float = 1.0,
        multiplier_charisma: float = 1.0,
        bonus_hit_points: int = 0,
        bonus_initiative: int = 0,
        bonus_physical_attack: int = 0,
        bonus_ranged_attack: int = 0,
        bonus_magical_attack: int = 0,
        bonus_physical_defense: int = 0,
        bonus_magical_defense: int = 0,
        bonus_hit: int = 0,
        bonus_evasion: int = 0,
    ) -> None:
        self.__bonus_strength = int(bonus_strength)
        self.__bonus_dexterity = int(bonus_dexterity)
        self.__bonus_constitution = int(bonus_constitution)
        self.__bonus_intelligence = int(bonus_intelligence)
        self.__bonus_wisdom = int(bonus_wisdom)
        self.__bonus_charisma = int(bonus_charisma)

        self.__multiplier_strength = float(multiplier_strength)
        self.__multiplier_dexterity = float(multiplier_dexterity)
        self.__multiplier_constitution = float(multiplier_constitution)
        self.__multiplier_intelligence = float(multiplier_intelligence)
        self.__multiplier_wisdom = float(multiplier_wisdom)
        self.__multiplier_charisma = float(multiplier_charisma)

        self.__bonus_hit_points = int(bonus_hit_points)
        self.__bonus_initiative = int(bonus_initiative)
        self.__bonus_physical_attack = int(bonus_physical_attack)
        self.__bonus_ranged_attack = int(bonus_ranged_attack)
        self.__bonus_magical_attack = int(bonus_magical_attack)
        self.__bonus_physical_defense = int(bonus_physical_defense)
        self.__bonus_magical_defense = int(bonus_magical_defense)
        self.__bonus_hit = int(bonus_hit)
        self.__bonus_evasion = int(bonus_evasion)

    def get_sheet(self) -> str:
        return (
            f'◇── BÔNUS E MULTIPLICADORES ──◇\n'
            f'FOR: {self.strength:+} '
            f'x({self.__multiplier_strength:+.2f})\n'
            f'DES: {self.dexterity:+} '
            f'x({self.__multiplier_dexterity:+.2f})\n'
            f'CON: {self.constitution:+} '
            f'x({self.__multiplier_constitution:+.2f})\n'
            f'INT: {self.intelligence:+} '
            f'x({self.__multiplier_intelligence:+.2f})\n'
            f'SAB: {self.wisdom:+} '
            f'x({self.__multiplier_wisdom:+.2f})\n'
            f'CAR: {self.charisma:+} '
            f'x({self.__multiplier_charisma:+.2f})\n\n'

            f'HP: {self.hp:+}\n'
            f'INICIATIVA: {self.initiative:+}\n'
            f'ATAQUE FÍSICO: {self.physical_attack:+}\n'
            f'ATAQUE À DISTÂNCIA: {self.ranged_attack:+}\n'
            f'ATAQUE MÁGICO: {self.magical_attack:+}\n'
            f'DEFESA FÍSICA: {self.physical_defense:+}\n'
            f'DEFESA MÁGICA: {self.magical_defense:+}\n'
            f'ACERTO: {self.hit:+}\n'
            f'EVASÃO: {self.evasion:+}\n'
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
    wisdom = bonus_wisdom = property(
        fget=lambda self: self.__bonus_wisdom)
    charisma = bonus_charisma = property(
        fget=lambda self: self.__bonus_charisma)
    multiplier_strength = property(
        fget=lambda self: self.__multiplier_strength)
    multiplier_dexterity = property(
        fget=lambda self: self.__multiplier_dexterity)
    multiplier_constitution = property(
        fget=lambda self: self.__multiplier_constitution)
    multiplier_intelligence = property(
        fget=lambda self: self.__multiplier_intelligence)
    multiplier_wisdom = property(
        fget=lambda self: self.__multiplier_wisdom)
    multiplier_charisma = property(
        fget=lambda self: self.__multiplier_charisma)
    hp = hit_points = bonus_hit_points = property(
        fget=lambda self: self.__bonus_hit_points)
    initiative = bonus_initiative = property(
        fget=lambda self: self.__bonus_initiative)
    physical_attack = bonus_physical_attack = property(
        fget=lambda self: self.__bonus_physical_attack)
    ranged_attack = bonus_ranged_attack = property(
        fget=lambda self: self.__bonus_ranged_attack)
    magical_attack = bonus_magical_attack = property(
        fget=lambda self: self.__bonus_magical_attack)
    physical_defense = bonus_physical_defense = property(
        fget=lambda self: self.__bonus_physical_defense)
    magical_defense = bonus_magical_defense = property(
        fget=lambda self: self.__bonus_magical_defense)
    hit = bonus_hit = property(
        fget=lambda self: self.__bonus_hit)
    evasion = bonus_evasion = property(
        fget=lambda self: self.__bonus_evasion)


if __name__ == '__main__':
    bonus_stats = StatsBooster(
        bonus_strength=10,
        bonus_dexterity=11,
        bonus_constitution=12,
        bonus_intelligence=13,
        bonus_wisdom=14,
        bonus_charisma=15,
        multiplier_strength=1.6,
        multiplier_dexterity=1.7,
        multiplier_constitution=1.8,
        multiplier_intelligence=-1.9,
        multiplier_wisdom=2.0,
        multiplier_charisma=-2.1,
        bonus_hit_points=220,
        bonus_initiative=23,
        bonus_physical_attack=24,
        bonus_ranged_attack=25,
        bonus_magical_attack=-26,
        bonus_physical_defense=27,
        bonus_magical_defense=-28,
        bonus_hit=29,
        bonus_evasion=30,
    )
    print(bonus_stats)
