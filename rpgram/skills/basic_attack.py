
from rpgram.characters.char_base import BaseCharacter
from rpgram.enums.skill import SkillTypeEnum, TargetEnum
from rpgram.skills.skill_base import BaseSkill


class PhysicalAttack(BaseSkill):
    def __init__(self, char: BaseCharacter):
        name = 'Physical Attack'
        description = 'Ataque Físico baseado em "FOR" e "DES".'
        power = 0
        level = 1
        cost = 0

        super().__init__(
            name=name,
            description=description,
            power=power,
            level=level,
            cost=cost,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            char=char,
            requirements={},
            damage_types=None
        )

    @property
    def power(self) -> int:
        return self.combat_stats.physical_attack


class PrecisionAttack(BaseSkill):
    def __init__(self, char: BaseCharacter):
        name = 'Precision Attack'
        description = 'Ataque rápido baseado em "DES".'
        power = 0
        level = 1
        cost = 0

        super().__init__(
            name=name,
            description=description,
            power=power,
            level=level,
            cost=cost,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            char=char,
            requirements={},
            damage_types=None
        )

    @property
    def power(self) -> int:
        return self.combat_stats.precision_attack


class MagicalAttack(BaseSkill):
    def __init__(self, char: BaseCharacter):
        name = 'Magical Attack'
        description = 'Ataque Mágico baseado em "INT" e "WIS".'
        power = 0
        level = 1
        cost = 0

        super().__init__(
            name=name,
            description=description,
            power=power,
            level=level,
            cost=cost,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            char=char,
            requirements={},
            damage_types=None
        )

    @property
    def power(self) -> int:
        return self.combat_stats.magical_attack
