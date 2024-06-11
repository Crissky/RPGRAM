

from itertools import chain
from typing import TYPE_CHECKING
from rpgram.enums.stats_base import BASE_STATS_ATTRIBUTE_LIST, BaseStatsEnum
from rpgram.enums.stats_combat import COMBAT_STATS_ATTRIBUTE_LIST
from rpgram.errors import RequirementError

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class Requirement:
    def __init__(self, **kwargs) -> None:
        self.base_stats = {BaseStatsEnum.LEVEL.value.lower(): 1}
        self.combat_stats = {}
        kwargs = {k.lower(): v for k, v in kwargs.items()}
        for attr in BASE_STATS_ATTRIBUTE_LIST:
            attr = attr.lower()
            if attr in kwargs:
                self.base_stats[attr] = kwargs.pop(attr)

        for attr in COMBAT_STATS_ATTRIBUTE_LIST:
            attr = attr.lower()
            if attr in kwargs:
                self.combat_stats[attr] = kwargs.pop(attr)

        if kwargs:
            raise TypeError(
                f'Argumentos inválidos: {", ".join(kwargs.keys())}'
            )

    def check_requirements(self, character: 'BaseCharacter'):
        errors = []
        for attribute, value in self.base_stats.items():
            if value > character.base_stats[attribute]:
                errors.append(
                    f'    {attribute}: '
                    f'"{value}" ({character.base_stats[attribute]}).'
                )
        for attribute, value in self.combat_stats.items():
            if value > character.combat_stats[attribute]:
                errors.append(
                    f'    {attribute}: '
                    f'"{value}" ({character.combat_stats[attribute]}).'
                )

        if errors:
            errors = "\n".join(errors)
            raise RequirementError(
                f'O personagem não possui os requisitos:\n'
                f'{errors}'
            )

    @property
    def level(self) -> int:
        return self.base_stats.get(BaseStatsEnum.LEVEL.value.lower(), 1)

    @property
    def text(self) -> str:
        text = ''
        _iter = chain(self.base_stats.items(), self.combat_stats.items())
        for attribute, value in _iter:
            attribute = attribute.replace('_', ' ').upper()
            text += f'  {attribute}: {value}\n'

        return text

    def to_dict(self) -> dict:
        return {
            key: value
            for key, value in chain(
                self.base_stats.items(),
                self.combat_stats.items(),
            )
        }


if __name__ == '__main__':
    req = Requirement(
        FOR=10,
        DES=10,
        INT=10,
        LEVEL=10,
        EVASION=300,
        HP=1000,
    )
    print(req.to_dict())
    print(req.level)
    print(req.text)
