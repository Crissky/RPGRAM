from datetime import datetime
from typing import Union

from bson import ObjectId
from constant.text import TEXT_DELIMITER

from function.text import escape_basic_markdown_v2, remove_bold, remove_code
from rpgram.conditions.condition import Condition

from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.rarity import RarityEnum


class Consumable:
    def __init__(
        self,
        name: str,
        description: str,
        weight: float,
        function: str,
        battle_function: str = None,
        condition: Condition = None,
        rarity: Union[str, RarityEnum] = RarityEnum.COMMON,
        usable: bool = True,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ) -> None:
        if isinstance(_id, str):
            _id = ObjectId(_id)
        if isinstance(rarity, str):
            rarity = RarityEnum[rarity]
        elif not isinstance(rarity, RarityEnum):
            raise TypeError(f'rarity precisa ser uma string ou RarityEnum')

        self.__name = name
        self.__description = description
        self.__weight = weight
        self.__condition = condition
        self.__function = function
        self.__battle_function = battle_function
        self.__rarity = rarity
        self.__usable = usable
        self.__id = _id
        self.__created_at = created_at
        self.__updated_at = updated_at

    def use(self, target):
        local = {'target': target, 'self': self}
        exec(self.__function, None, local)
        report = local['report']
        return report

    def battle_use(self, target):  # If é provisório até a criação das conditions no banco
        if self.__battle_function:
            local = {'target': target, 'self': self}
            exec(self.__battle_function, None, local)
            report = local['report']
        else:
            report = self.use(target)
        return report

    def to_dict(self):
        return dict(
            name=self.__name,
            description=self.__description,
            weight=self.__weight,
            function=self.__function,
            battle_function=self.__battle_function,
            condition_name=self.__condition.name if self.__condition else None,
            rarity=self.__rarity.name,
            usable=self.__usable,
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
                f'*Peso*: {self.__weight}{EmojiEnum.WEIGHT.value}\n'
                f'*Descrição*: {self.__description}\n'
                f'*Função*: {self.__function}\n'
                f'*Raridade*: {self.__rarity.value}\n'
            )

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return text

    def get_all_sheets(
        self, verbose: bool = False, markdown: bool = False
    ) -> str:
        return self.get_sheet(verbose=verbose, markdown=markdown)

    def __repr__(self) -> str:
        return (
            f'{TEXT_DELIMITER}\n'
            f'{self.get_sheet(True)}'
            f'{TEXT_DELIMITER}\n'
        )

    def __eq__(self, other):
        if isinstance(other, Consumable):
            if self._id is not None and other._id is not None:
                return self._id == other._id
        return False

    # Getters
    @property
    def emoji_type(self) -> str:
        return EmojiEnum.CONSUMABLE.value

    _id = property(lambda self: self.__id)
    name = property(lambda self: self.__name)
    description = property(lambda self: self.__description)
    weight = property(lambda self: self.__weight)
    condition = property(lambda self: self.__condition)
    function = property(lambda self: self.__function)
    rarity = property(lambda self: self.__rarity)
    usable = property(lambda self: self.__usable)


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
        condition=None,
        function='report = target.combat_stats.cure_hit_points(100)'
    )
    print(potion)
    print(potion.to_dict())
    print('HP:', base_character.cs.show_hit_points)
    base_character.cs.hp = -300
    potion(base_character)
    base_character.cs.hp = -300
    potion(base_character)
