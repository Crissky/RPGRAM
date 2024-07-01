from operator import attrgetter
from typing import TYPE_CHECKING, Callable, List, Type, Union

from function.text import escape_basic_markdown_v2, remove_bold, remove_code
from rpgram.enums.emojis import EmojiEnum
from rpgram.skills.factory import skill_factory, skill_list_factory
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter

ACTION_POINTS_EMOJI_TEXT = f'{EmojiEnum.ACTION_POINTS.value}Pontos de Ação'
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
            if isinstance(skill, dict):
                skill_list[index] = skill_factory(
                    classe_name=classe_name,
                    skill_class_name=skill['class_name'],
                    char=character,
                    level=skill['level'],
                )

        self.character = character
        self.__skill_list: List[BaseSkill] = skill_list
        self.current_action_points = int(current_action_points)
        self.max_action_points = int(max_action_points)

    def get_skill(self, skill_name: str) -> BaseSkill:
        index = self.skill_list.index(skill_name)
        return self.skill_list[index]

    def learn_skill(self, skill_class_name: Union[BaseSkill, str]) -> dict:
        if issubclass(skill_class_name, BaseSkill):
            skill_class_name = skill_class_name.__name__

        report = {'text': '', 'skill': None}
        if skill_class_name in self.skill_list:
            skill = self.get_skill(skill_class_name)
            report['text'] = (
                f'O personagem já sabe usar a habilidade "{skill.name}".'
            )
        else:
            new_skill = skill_factory(
                classe_name=self.character.classe_name,
                skill_class_name=skill_class_name,
                char=self.character,
            )
            report['skill'] = new_skill
            report['text'] = (
                f'O personagem aprendeu a habilidade "{new_skill.name}".'
            )
            self.__skill_list.append(new_skill)

        return report

    def upgrade_skill(self, skill_class_name: Union[BaseSkill, str]) -> dict:
        report = {'text': '', 'skill': None}
        if skill_class_name not in self.skill_list:
            report['text'] = (
                f'O personagem não sabe usar a habilidade '
                f'"{skill_class_name}".'
            )
        elif not self.have_skill_points:
            report['text'] = (
                f'O personagem não tem {self.skill_points_name} suficientes.'
            )
        else:
            skill = self.get_skill(skill_class_name)
            old_level = skill.level
            requirements_report = skill.requirements.check_requirements(
                self.character,
                level=old_level + 1,
                rank=skill.rank,
                to_raise_error=False
            )
            if requirements_report['pass']:
                skill.add_level()
                new_level = skill.level
                report['skill'] = skill
                report['text'] = (
                    f'A habilidade "{skill.name}" foi aprimorada do '
                    f'nível {old_level} para {new_level}.'
                )
            else:
                report['text'] = (
                    f'O personagem não atende aos requisitos para aprimorar a '
                    f'habilidade "{skill.name}"\n\n'
                    f'{requirements_report["text"]}'
                )

        return report

    def add_action_points(self, value: int = 1) -> dict:
        value = int(abs(value))

        self.current_action_points += value
        self.current_action_points = min(
            self.current_action_points, self.max_action_points
        )
        report = {
            'value': value,
            'current_value': self.current_action_points,
            'text': (
                f'Adicionado(s) {value} ponto(s) de ação.\n'
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

        self.current_action_points -= value
        self.current_action_points = max(self.current_action_points, 0)
        report = {
            'value': value,
            'current_value': self.current_action_points,
            'text': (
                f'Removido(s) {value} ponto(s) de ação.\n'
                f'{self.current_action_points_text}'
            )
        }

        return report

    @property
    def current_action_points_text(self) -> str:
        return (
            f'{ACTION_POINTS_EMOJI_TEXT}: '
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
    def skill_points_name(self) -> str:
        return f'{EmojiEnum.SKILL_POINTS.value}Pontos de Habilidade'

    @property
    def skill_points_text(self) -> str:
        return (
            f'{self.skill_points_name}: '
            f'{self.current_skill_points}/{self.max_skill_points}'
        )

    @property
    def skill_list(self) -> List[BaseSkill]:
        return sorted(self.__skill_list, key=attrgetter('rank', 'name'))

    @property
    def learnable_skill_list(self) -> List[Type[BaseSkill]]:
        classe_name = self.character.classe_name
        skill_list = skill_list_factory(classe_name)

        return sorted(
            [
                skill for skill in skill_list
                if skill.NAME not in self.skill_list
            ],
            key=attrgetter('RANK', 'NAME')
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
