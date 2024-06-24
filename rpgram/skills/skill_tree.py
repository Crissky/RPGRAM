from typing import TYPE_CHECKING, Callable, List

from function.text import escape_basic_markdown_v2, remove_bold, remove_code
from rpgram.enums.emojis import EmojiEnum
from rpgram.skills.factory import skill_factory
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class SkillTree:
    def __init__(
        self,
        character: 'BaseCharacter',
        skill_list: List[BaseSkill] = [],
        current_action_points: int = 0,
        max_action_points: int = 5,
    ):
        classe_name = character.classe_name
        for index, skill in enumerate(skill_list):
            if isinstance(skill, Callable):
                skill_list[index] = skill_factory(
                    classe_name=classe_name,
                    skill_class_name=skill['class_name'],
                    char=character,
                    level=skill['level'],
                )

        self.character = character
        self.skill_list: List[BaseSkill] = skill_list
        self.current_action_points = current_action_points
        self.max_action_points = max_action_points

    def get_skill(self, skill_name: str) -> BaseSkill:
        index = self.skill_list.index(skill_name)
        return self.skill_list[index]

    def add_action_points(self, value: int = 1) -> dict:
        value = int(abs(value))
        if value <= 0:
            raise ValueError(
                f'O valor "{value}" não pode ser menor ou igual a zero.'
            )

        current_value = self.max_action_points - self.current_action_points
        current_value = min(current_value, value)
        self.current_action_points += current_value
        self.current_action_points = min(
            self.current_action_points, self.max_action_points
        )
        report = {
            'value': value,
            'current_value': current_value,
            'text': (
                f'Adicionado(s) {current_value} ponto(s) de ação.\n'
                f'{self.current_action_points_text}'
            )
        }

        return report

    def sub_action_points(self, value: int = 1) -> dict:
        value = int(abs(value))
        if value > self.current_action_points:
            raise ValueError(
                f'O valor para subtrair "{value}" é maior que o valor total '
                f'({self.current_action_points}) de pontos de ação que o '
                f'jogador {self.name} possui.'
            )

        current_value = self.current_action_points - value
        current_value = max(current_value, 0)
        self.current_action_points = current_value
        report = {
            'value': value,
            'current_value': current_value,
            'text': (
                f'Removido(s) {value} ponto(s) de ação.\n'
                f'{self.current_action_points_text}'
            )
        }

        return report

    @property
    def current_action_points_text(self) -> str:
        return (
            f'{EmojiEnum.ACTION_POINTS.value}Pontos de Ação: '
            f'{self.current_action_points}/{self.max_action_points}'
        )

    @property
    def is_full_action_points(self) -> bool:
        return self.current_action_points >= self.max_action_points

    @property
    def have_action_points(self) -> bool:
        return self.current_action_points > 0

    @property
    def max_skill_points(self) -> int:
        return self.character.bs.classe_level

    @property
    def current_skill_points(self) -> int:
        return int(
            self.max_skill_points -
            sum(skill.level for skill in self.skill_list)
        )

    @property
    def have_skill_points(self) -> bool:
        return self.current_skill_points > 0

    @property
    def skill_points_text(self) -> str:
        return (
            f'{EmojiEnum.SKILL_POINTS.value}Pontos de Habilidade: '
            f'{self.current_skill_points}/{self.max_skill_points}'
        )

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = f'{self.current_action_points_text}\n'
        text += f'{self.skill_points_text}'

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

    def to_dict(self) -> dict:
        return {
            'skill_list': [skill.to_dict() for skill in self.skill_list],
            'current_action_points': self.current_action_points,
            'max_action_points': self.max_action_points,
        }
