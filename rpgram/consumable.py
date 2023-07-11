from datetime import datetime
from typing import Union

from bson import ObjectId

from function.text import escape_basic_markdown_v2, remove_bold, remove_code


class Consumable:
    def __init__(
        self,
        name: str,
        description: str,
        weight: float,
        function: str,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ) -> None:
        if isinstance(_id, str):
            _id = ObjectId(_id)

        self.__name = name
        self.__description = description
        self.__weight = weight
        self.__function = function
        self.__id = _id
        self.__created_at = created_at
        self.__updated_at = updated_at

    def use(self, target):
        result = exec(self.__function)
        return result

    def to_dict(self):
        return dict(
            name=self.__name,
            description=self.__description,
            weight=self.__weight,
            function=self.__function,
            _id=self.__id,
            created_at=self.__created_at,
            updated_at=self.__updated_at,
        )

    def __call__(self, target):
        return self.use(target)

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = f'*Item*: {self.__name}\n'

        if verbose:
            text += (
            f'*Peso*: {self.__weight}w\n'
            f'*Descrição*: {self.__description}\n'
            f'*Função*: {self.__function}\n'
        )
        
        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return text

    def __repr__(self) -> str:
        return self.get_sheet(True)

    def __eq__(self, other):
        if isinstance(other, Consumable):
            return self._id == other._id
        return False

    # Getters
    _id = property(lambda self: self.__id)
    name = property(lambda self: self.__name)
    description = property(lambda self: self.__description)
    weight = property(lambda self: self.__weight)
    function = property(lambda self: self.__function)


if __name__ == '__main__':
    from rpgram.boosters import Classe, Race
    from rpgram.characters import BaseCharacter
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
    potion = Consumable(
        name='Potion',
        description='Cura 100 de HP.',
        weight=0.1,
        function='target.combat_stats.hp = 100'
    )
    print(potion)
    print('HP:', base_character.cs.show_hit_points)
    base_character.cs.hp = -300
    potion(base_character)
    base_character.cs.hp = -300
    potion(base_character)
