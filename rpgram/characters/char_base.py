from datetime import datetime
from bson import ObjectId
from rpgram.boosters import Race, Classe
from rpgram.stats import BaseStats, CombatStats


class BaseCharacter:
    def __init__(
        self,
        char_name: str,
        _id: ObjectId = None,
        base_stats: BaseStats = None,
        combat_stats: CombatStats = None,
        classe: Classe = None,
        race: Race = None,
        level: int = 1,
        base_strength: int = 0,
        base_dexterity: int = 0,
        base_constitution: int = 0,
        base_intelligence: int = 0,
        base_wisdom: int = 0,
        base_charisma: int = 0,
        race_name: str = '',
        race_description: str = '',
        race_bonus_strength: int = 0,
        race_bonus_dexterity: int = 0,
        race_bonus_constitution: int = 0,
        race_bonus_intelligence: int = 0,
        race_bonus_wisdom: int = 0,
        race_bonus_charisma: int = 0,
        race_multiplier_strength: float = 1.0,
        race_multiplier_dexterity: float = 1.0,
        race_multiplier_constitution: float = 1.0,
        race_multiplier_intelligence: float = 1.0,
        race_multiplier_wisdom: float = 1.0,
        race_multiplier_charisma: float = 1.0,
        classe_name: str = '',
        classe_description: str = '',
        classe_bonus_strength: int = 0,
        classe_bonus_dexterity: int = 0,
        classe_bonus_constitution: int = 0,
        classe_bonus_intelligence: int = 0,
        classe_bonus_wisdom: int = 0,
        classe_bonus_charisma: int = 0,
        classe_multiplier_strength: float = 1.0,
        classe_multiplier_dexterity: float = 1.0,
        classe_multiplier_constitution: float = 1.0,
        classe_multiplier_intelligence: float = 1.0,
        classe_multiplier_wisdom: float = 1.0,
        classe_multiplier_charisma: float = 1.0,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        if isinstance(_id, str):
            _id = ObjectId(_id)
        self.__name = char_name
        self.__id = _id
        self.__created_at = created_at
        self.__updated_at = updated_at
        if not isinstance(race, Race):
            race = Race(
                name=race_name,
                description=race_description,
                bonus_strength=race_bonus_strength,
                bonus_dexterity=race_bonus_dexterity,
                bonus_constitution=race_bonus_constitution,
                bonus_intelligence=race_bonus_intelligence,
                bonus_wisdom=race_bonus_wisdom,
                bonus_charisma=race_bonus_charisma,
                multiplier_strength=race_multiplier_strength,
                multiplier_dexterity=race_multiplier_dexterity,
                multiplier_constitution=race_multiplier_constitution,
                multiplier_intelligence=race_multiplier_intelligence,
                multiplier_wisdom=race_multiplier_wisdom,
                multiplier_charisma=race_multiplier_charisma,
            )
        self.__race = race
        if not isinstance(classe, Classe):
            classe = Classe(
                name=classe_name,
                description=classe_description,
                bonus_strength=classe_bonus_strength,
                bonus_dexterity=classe_bonus_dexterity,
                bonus_constitution=classe_bonus_constitution,
                bonus_intelligence=classe_bonus_intelligence,
                bonus_wisdom=classe_bonus_wisdom,
                bonus_charisma=classe_bonus_charisma,
                multiplier_strength=classe_multiplier_strength,
                multiplier_dexterity=classe_multiplier_dexterity,
                multiplier_constitution=classe_multiplier_constitution,
                multiplier_intelligence=classe_multiplier_intelligence,
                multiplier_wisdom=classe_multiplier_wisdom,
                multiplier_charisma=classe_multiplier_charisma,
            )
        self.__classe = classe
        if not isinstance(base_stats, BaseStats):
            base_stats = BaseStats(
                level,
                base_strength,
                base_dexterity,
                base_constitution,
                base_intelligence,
                base_wisdom,
                base_charisma,
                self.__race,
                self.__classe,
            )
        self.__base_stats = base_stats
        if not isinstance(combat_stats, CombatStats):
            combat_stats = CombatStats(
                base_stats=self.__base_stats,
            )
        self.__combat_stats = combat_stats

    # Getters
    name = property(lambda self: self.__name)
    _id = property(lambda self: self.__id)
    base_stats = bs = property(fget=lambda self: self.__base_stats)
    combat_stats = cs = property(fget=lambda self: self.__combat_stats)
    race = property(fget=lambda self: self.__race)
    classe = property(fget=lambda self: self.__classe)
    created_at = property(lambda self: self.__created_at)
    updated_at = property(lambda self: self.__updated_at)

    def get_sheet(self):
        return (
            f'Personagem: {self.name}\n'
            f'ID: {self._id}\n'
            f'{self.race.get_sheet()}'
            f'{self.classe.get_sheet()}'
            f'{self.base_stats.get_sheet()}'
            f'{self.combat_stats.get_sheet()}'
        )

    def __repr__(self) -> str:
        return (
            f'########################################\n'
            f'{self.get_sheet()}'
            f'########################################\n'
        )

    def to_dict(self):
        return dict(
            char_name=self.name,
            _id=self._id,
            level=self.base_stats.level,
            base_strength=self.base_stats.base_strength,
            base_dexterity=self.base_stats.base_dexterity,
            base_constitution=self.base_stats.base_constitution,
            base_intelligence=self.base_stats.base_intelligence,
            base_wisdom=self.base_stats.base_wisdom,
            base_charisma=self.base_stats.base_charisma,
            race_name=self.race.name,
            race_description=self.race.description,
            race_bonus_strength=self.race.bonus_strength,
            race_bonus_dexterity=self.race.bonus_dexterity,
            race_bonus_constitution=self.race.bonus_constitution,
            race_bonus_intelligence=self.race.bonus_intelligence,
            race_bonus_wisdom=self.race.bonus_wisdom,
            race_bonus_charisma=self.race.bonus_charisma,
            race_multiplier_strength=self.race.multiplier_strength,
            race_multiplier_dexterity=self.race.multiplier_dexterity,
            race_multiplier_constitution=self.race.multiplier_constitution,
            race_multiplier_intelligence=self.race.multiplier_intelligence,
            race_multiplier_wisdom=self.race.multiplier_wisdom,
            race_multiplier_charisma=self.race.multiplier_charisma,
            classe_name=self.classe.name,
            classe_description=self.classe.description,
            classe_bonus_strength=self.classe.bonus_strength,
            classe_bonus_dexterity=self.classe.bonus_dexterity,
            classe_bonus_constitution=self.classe.bonus_constitution,
            classe_bonus_intelligence=self.classe.bonus_intelligence,
            classe_bonus_wisdom=self.classe.bonus_wisdom,
            classe_bonus_charisma=self.classe.bonus_charisma,
            classe_multiplier_strength=self.classe.multiplier_strength,
            classe_multiplier_dexterity=self.classe.multiplier_dexterity,
            classe_multiplier_constitution=self.classe.multiplier_constitution,
            classe_multiplier_intelligence=self.classe.multiplier_intelligence,
            classe_multiplier_wisdom=self.classe.multiplier_wisdom,
            classe_multiplier_charisma=self.classe.multiplier_charisma,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


if __name__ == '__main__':
    base_character = BaseCharacter(
        char_name='Personagem Teste',
        _id='ffffffffffffffffffffffff',
        level=21,
        base_strength=10,
        base_dexterity=10,
        base_constitution=10,
        base_intelligence=10,
        base_wisdom=10,
        base_charisma=10,
        race_name='Elfo',
        race_description='Elfo Teste',
        race_bonus_strength=8,
        race_bonus_dexterity=12,
        race_bonus_constitution=8,
        race_bonus_intelligence=10,
        race_bonus_wisdom=12,
        race_bonus_charisma=10,
        race_multiplier_strength=1.0,
        race_multiplier_dexterity=1.0,
        race_multiplier_constitution=1.0,
        race_multiplier_intelligence=1.2,
        race_multiplier_wisdom=1.2,
        race_multiplier_charisma=1.0,
        classe_name='Arqueiro',
        classe_description='Arqueiro Teste',
        classe_bonus_strength=5,
        classe_bonus_dexterity=15,
        classe_bonus_constitution=10,
        classe_bonus_intelligence=10,
        classe_bonus_wisdom=10,
        classe_bonus_charisma=10,
        classe_multiplier_strength=1,
        classe_multiplier_dexterity=1.5,
        classe_multiplier_constitution=1,
        classe_multiplier_intelligence=1,
        classe_multiplier_wisdom=1,
        classe_multiplier_charisma=1,
    )
    print(base_character)
    base_character.base_stats.xp = 100
    base_character.base_stats.dexterity = 1
    base_character.combat_stats.hp = -100
    base_character.combat_stats.hit_points = 50
    print(base_character)
    print(base_character.to_dict())
