from datetime import datetime
from typing import Union

from bson import ObjectId

from constants.text import SECTION_HEAD, TEXT_DELIMITER
from functions.text import escape_basic_markdown_v2, remove_bold, remove_code
from rpgram.boosters import StatsBooster


class Classe(StatsBooster):
    def __init__(
        self,
        name: str,
        description: str = '',
        _id: Union[str, ObjectId] = None,
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
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        super().__init__(
            _id=_id,
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
            created_at=created_at,
            updated_at=updated_at,
        )
        self.__name = name
        self.__description = description

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = f'*Classe*: {self.name}\n'.upper()

        text += f'*{SECTION_HEAD.format("BÔNUS E MULTIPLICADORES")}*\n'

        text += f'`FOR: {self.strength:+}'
        if verbose:
            text += f'x({self.multiplier_strength:+.2f})'
        text += f'`\n'

        text += f'`DES: {self.dexterity:+}'
        if verbose:
            text += f'x({self.multiplier_dexterity:+.2f})'
        text += f'`\n'

        text += f'`CON: {self.constitution:+}'
        if verbose:
            text += f'x({self.multiplier_constitution:+.2f})'
        text += f'`\n'

        text += f'`INT: {self.intelligence:+}'
        if verbose:
            text += f'x({self.multiplier_intelligence:+.2f})'
        text += f'`\n'

        text += f'`SAB: {self.wisdom:+}'
        if verbose:
            text += f'x({self.multiplier_wisdom:+.2f})'
        text += f'`\n'

        text += f'`CAR: {self.charisma:+}'
        if verbose:
            text += f'x({self.multiplier_charisma:+.2f})'
        text += f'`\n'

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

    def to_dict(self):
        return dict(
            name=self.name,
            description=self.description,
            _id=self._id,
            bonus_strength=self.bonus_strength,
            bonus_dexterity=self.bonus_dexterity,
            bonus_constitution=self.bonus_constitution,
            bonus_intelligence=self.bonus_intelligence,
            bonus_wisdom=self.bonus_wisdom,
            bonus_charisma=self.bonus_charisma,
            multiplier_strength=self.multiplier_strength,
            multiplier_dexterity=self.multiplier_dexterity,
            multiplier_constitution=self.multiplier_constitution,
            multiplier_intelligence=self.multiplier_intelligence,
            multiplier_wisdom=self.multiplier_wisdom,
            multiplier_charisma=self.multiplier_charisma,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    name = property(lambda self: self.__name)
    description = property(lambda self: self.__description)


if __name__ == '__main__':
    classe = Classe(
        name='Clérigo',
        description='Clérigo de teste',
        _id='ffffffffffffffffffffffff',
        bonus_strength=5,
        bonus_dexterity=5,
        bonus_constitution=8,
        bonus_intelligence=10,
        bonus_wisdom=16,
        bonus_charisma=16,
        multiplier_strength=0.5,
        multiplier_dexterity=0.5,
        multiplier_constitution=1.0,
        multiplier_intelligence=1.0,
        multiplier_wisdom=1.8,
        multiplier_charisma=1.7,
    )
    print(classe)
    print(classe.to_dict())
