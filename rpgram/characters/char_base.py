from bson import ObjectId
from datetime import datetime

from constants.text import TEXT_DELIMITER
from functions.text import escape_basic_markdown_v2, remove_bold, remove_code
from rpgram.boosters import Race, Classe
from rpgram.stats import BaseStats, CombatStats


class BaseCharacter:
    def __init__(
        self,
        char_name: str,
        classe: Classe,
        race: Race,
        level: int = 1,
        xp: int = 0,
        base_strength: int = 0,
        base_dexterity: int = 0,
        base_constitution: int = 0,
        base_intelligence: int = 0,
        base_wisdom: int = 0,
        base_charisma: int = 0,
        combat_damage: int = 0,
        _id: ObjectId = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        if isinstance(_id, str):
            _id = ObjectId(_id)
        self.__name = char_name
        self.__id = _id
        self.__classe = classe
        self.__race = race
        self.__base_stats = BaseStats(
            level=level,
            xp=xp,
            base_strength=base_strength,
            base_dexterity=base_dexterity,
            base_constitution=base_constitution,
            base_intelligence=base_intelligence,
            base_wisdom=base_wisdom,
            base_charisma=base_charisma,
            stats_boosters=[self.__race, self.__classe]
        )
        self.__combat_stats = CombatStats(
            base_stats=self.__base_stats,
            damage=combat_damage
        )
        self.__created_at = created_at
        self.__updated_at = updated_at

    # Getters
    name: str = property(lambda self: self.__name)
    _id: ObjectId = property(lambda self: self.__id)
    base_stats: BaseStats = property(fget=lambda self: self.__base_stats)
    combat_stats: CombatStats = property(fget=lambda self: self.__combat_stats)
    classe: Classe = property(fget=lambda self: self.__classe)
    race: Race = property(fget=lambda self: self.__race)
    created_at: datetime = property(lambda self: self.__created_at)
    updated_at: datetime = property(lambda self: self.__updated_at)
    bs = base_stats
    cs = combat_stats

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = f'*Personagem*: {self.name}\n'
        if verbose:
            text += f'*ID Personagem*: {self._id}\n'

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return text

    def get_all_sheets(
        self, verbose: bool = False, markdown: bool = False
    ) -> str:
        if verbose:
            text = (
                f'{self.get_sheet(verbose, markdown)}'
                f'{self.base_stats.get_sheet(verbose, markdown)}\n'
                f'{self.combat_stats.get_sheet(verbose, markdown)}\n'
                f'{self.race.get_sheet(verbose, markdown)}\n'
                f'{self.classe.get_sheet(verbose, markdown)}'
            )
        else:
            # Trecho feito dessa forma para o escape_basic_markdown_v2 não ser 
            # usado duas vezes nos textos que vez dos outros get_sheet, pois
            # o esperado seria somente uma \ e não duas.
            race_classe_text = (
                f'*Raça*: {self.race.name}\n'
                f'*Classe*: {self.classe.name}\n'
            )
            if not markdown:
                race_classe_text = remove_bold(race_classe_text)
                race_classe_text = remove_code(race_classe_text)
            else:
                race_classe_text = escape_basic_markdown_v2(race_classe_text)
            text = (
                f'{self.get_sheet(verbose, markdown)}'
                f'{race_classe_text}'
                f'{self.base_stats.get_sheet(verbose, markdown)}\n'
                f'{self.combat_stats.get_sheet(verbose, markdown)}\n'
            )

        return text

    def __str__(self) -> str:
        return (
            f'{TEXT_DELIMITER}\n'
            f'{self.get_all_sheets(True)}'
            f'{TEXT_DELIMITER}\n'
        )

    def __repr__(self) -> str:
        return (
            f'<Personagem: "{self.name}", '
            f'HP: {self.cs.current_hit_points}/{self.cs.hit_points}, '
            f'Classe: "{self.classe.name}", '
            f'Raça: "{self.race.name}">'
        )

    def to_dict(self):
        return dict(
            char_name=self.name,
            _id=self._id,
            level=self.base_stats.level,
            xp=self.base_stats.xp,
            base_strength=self.base_stats.base_strength,
            base_dexterity=self.base_stats.base_dexterity,
            base_constitution=self.base_stats.base_constitution,
            base_intelligence=self.base_stats.base_intelligence,
            base_wisdom=self.base_stats.base_wisdom,
            base_charisma=self.base_stats.base_charisma,
            combat_damage=(self.cs.hit_points - self.cs.current_hit_points),
            race_name=self.race.name,
            classe_name=self.classe.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, BaseCharacter):
            return all((
                self._id == __value._id,
                self.name == __value.name,
            ))


if __name__ == '__main__':
    classe = Classe(
        name='Arqueiro',
        description='Arqueiro Teste',
        bonus_strength=5,
        bonus_dexterity=15,
        bonus_constitution=10,
        bonus_intelligence=10,
        bonus_wisdom=10,
        bonus_charisma=10,
        multiplier_strength=1,
        multiplier_dexterity=1.5,
        multiplier_constitution=1,
        multiplier_intelligence=1,
        multiplier_wisdom=1,
        multiplier_charisma=1,
    )
    race = Race(
        name='Elfo',
        description='Elfo Teste',
        bonus_strength=8,
        bonus_dexterity=12,
        bonus_constitution=8,
        bonus_intelligence=10,
        bonus_wisdom=12,
        bonus_charisma=10,
        multiplier_strength=1.0,
        multiplier_dexterity=1.0,
        multiplier_constitution=1.0,
        multiplier_intelligence=1.2,
        multiplier_wisdom=1.2,
        multiplier_charisma=1.0,
    )
    base_character = BaseCharacter(
        char_name='Personagem Teste',
        classe=classe,
        race=race,
        _id='ffffffffffffffffffffffff',
        level=21,
        xp=0,
        base_strength=10,
        base_dexterity=10,
        base_constitution=10,
        base_intelligence=10,
        base_wisdom=10,
        base_charisma=10,
        combat_damage=0,
    )
    print(base_character)
    base_character.base_stats.xp = 100
    base_character.base_stats.dexterity = 1
    base_character.combat_stats.hp = -100
    base_character.combat_stats.hit_points = 50
    print(base_character)
    print(base_character.to_dict())
