from typing import TYPE_CHECKING, List

from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class SkillTree:
    def __init__(
        self,
        character: 'BaseCharacter',
        skills: List[BaseSkill],
        current_action_points: int = 0,
        max_action_points: int = 5,
    ):
        for index, skill in enumerate(skills):
            if isinstance(skill, dict):
                skills[index] = BaseSkill(**skill)

        self.character = character
        self.skills = skills
        self.current_action_points = current_action_points
        self.max_action_points = max_action_points

    def get_skill(self, skill_name: str) -> BaseSkill:
        index = self.skills.index(skill_name)
        return self.skills[index]

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
            f'Pontos de Ação: '
            f'{self.current_action_points}/{self.max_action_points}'
        )
