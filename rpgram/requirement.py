from itertools import chain
from typing import TYPE_CHECKING, Iterator, Tuple

from rpgram.enums.stats_base import BASE_STATS_ATTRIBUTE_LIST, BaseStatsEnum
from rpgram.enums.stats_combat import COMBAT_STATS_ATTRIBUTE_LIST
from rpgram.errors import RequirementError

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class Requirement:
    def __init__(self, **kwargs) -> None:
        self.base_stats = {BaseStatsEnum.LEVEL.value.lower(): 1}
        self.combat_stats = {}
        self.classe_name: str = kwargs.pop('classe_name', None)
        self.skill_list = kwargs.pop('skill_list', [])
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

    def check_requirements(
        self,
        character: 'BaseCharacter',
        level: int = 1,
        rank: int = 1,
        to_raise_error: bool = True,
    ) -> dict:
        '''Analisa se o personagem possui os requisitos.
        '''
        errors = []
        level = max(1, int(level))
        rank = max(1, int(rank))
        level_rank = int(level * rank)
        level_rank = max(0, (level_rank - 2))
        for attribute, value in self.base_stats.items():
            value += (level_rank * 10)
            if value > character.base_stats[attribute]:
                errors.append(
                    f'    {attribute}: '
                    f'"{value}" ({character.base_stats[attribute]}).'
                )
        for attribute, value in self.combat_stats.items():
            value += (level_rank * 20)
            if value > character.combat_stats[attribute]:
                errors.append(
                    f'    {attribute}: '
                    f'"{value}" ({character.combat_stats[attribute]}).'
                )

        if self.classe_name and self.classe_name != character.classe_name:
            errors.append(
                f'    Classe: '
                f'"{self.classe_name.title()}" '
                f'({character.classe_name.title()}).'
            )

        for skill in self.skill_list:
            if skill not in character.skill_tree.skill_list:
                errors.append(
                    f'    Habilidade: "{skill}".'
                )

        if errors and to_raise_error is True:
            errors = '\n'.join(errors)
            raise RequirementError(
                f'O personagem não possui os requisitos:\n'
                f'{errors}'
            )

        return {
            'text': '\n'.join(errors),
            'errors': errors,
            'pass': not bool(errors)
        }

    @property
    def level(self) -> int:
        return self.base_stats.get(BaseStatsEnum.LEVEL.value.lower(), 1)

    @property
    def iter(self) -> Iterator[Tuple[str, int]]:
        return chain(
            self.base_stats.items(),
            self.combat_stats.items(),
            {'classe': self.classe_name}.items() if self.classe_name else [],
            {'skills': self.skill_list}.items() if self.skill_list else [],
        )

    @property
    def text(self) -> str:
        text = ''
        for attribute, value in self.iter:
            attribute = attribute.replace('_', ' ').upper()
            text += f'  {attribute}: {value}\n'

        return text

    def to_dict(self) -> dict:
        return {
            key: value
            for key, value in self.iter
        }

    def __str__(self) -> str:
        return self.text


if __name__ == '__main__':
    req = Requirement(
        FOR=10,
        DES=10,
        INT=10,
        LEVEL=10,
        EVASION=300,
        HP=1000,
        classe_name='Warrior',
    )
    print(req.to_dict())
    print(req.level)
    print(req.text)
