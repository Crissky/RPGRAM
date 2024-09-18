from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.self_skill import MysticBlockCondition
from rpgram.constants.text import (
    CONSTITUTION_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    HeraldSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.classes.multiclasse.physical_defense import (
    GuardianShieldSkill,
    HeavyChargeSkill,
    RobustBlockSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class MysticBlockSkill(BaseSkill):
    NAME = HeraldSkillEnum.MYSTIC_BLOCK.value
    DESCRIPTION = (
        f'Utiliza a *Fé* e *Devoção* para invocar *Forças Místicas*, '
        f'criando uma *Aura Protetora* que o rodeia, '
        f'aumentando a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{CONSTITUTION_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.HERALD.value,
        'skill_list': [RobustBlockSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=MysticBlockSkill.NAME,
            description=MysticBlockSkill.DESCRIPTION,
            rank=MysticBlockSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=MysticBlockSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        char = self.char
        player_name = char.player_name
        level = self.level_rank
        condition = MysticBlockCondition(character=char, level=level)
        report_list = char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* se concentra para criar uma '
                f'*Aura Protetora*, '
                f'aumentando a sua '
                f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_magical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class ColossalOnslaughtSkill(BaseSkill):
    NAME = HeraldSkillEnum.COLOSSAL_ONSLAUGHT.value
    DESCRIPTION = (
        f'Avança através das linhas inimigas com uma *Força Colossal* '
        f'como um *Gigante Implacável*, envolto em uma aura de fogo e rocha, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}*, de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.ROCK)}* com base em '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* (50% + 5% x Rank x Nível), '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (50% + 5% x Rank x Nível) e '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (50% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.HERALD.value,
        'skill_list': [HeavyChargeSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_DEFENSE: 0.50,
            CombatStatsEnum.MAGICAL_DEFENSE: 0.50,
            CombatStatsEnum.PHYSICAL_ATTACK: 0.50,
        }
        damage_types = [
            DamageEnum.BLUDGEONING,
            DamageEnum.FIRE,
            DamageEnum.ROCK,
        ]

        super().__init__(
            name=ColossalOnslaughtSkill.NAME,
            description=ColossalOnslaughtSkill.DESCRIPTION,
            rank=ColossalOnslaughtSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=ColossalOnslaughtSkill.REQUIREMENTS,
            damage_types=damage_types
        )


SKILL_WAY_DESCRIPTION = {
    'name': 'Protetor Implacável',
    'description': (
        'O Protetor Implacável encarna a força indomável para proteger. '
        'Sua devoção à causa da justiça o torna um defensor inflexível '
        'dos fracos e oprimidos. Ele é um escudo inquebrantável, '
        'capaz de absorver o impacto de qualquer ataque e retaliar '
        'com força brutal.'
    ),
    'skill_list': [
        RobustBlockSkill,
        MysticBlockSkill,
        GuardianShieldSkill,
        HeavyChargeSkill,
        ColossalOnslaughtSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import HERALD_CHARACTER

    skill = RobustBlockSkill(HERALD_CHARACTER)
    print(skill)
    print(HERALD_CHARACTER.bs.constitution)
    print(HERALD_CHARACTER.cs.physical_defense)
    print(skill.function())
    print(HERALD_CHARACTER.cs.physical_defense)
    HERALD_CHARACTER.skill_tree.learn_skill(RobustBlockSkill)

    skill = MysticBlockSkill(HERALD_CHARACTER)
    print(skill)
    print(HERALD_CHARACTER.cs.constitution,
          HERALD_CHARACTER.cs.magical_defense)
    print(skill.function(HERALD_CHARACTER))
    print(HERALD_CHARACTER.cs.magical_defense)
    HERALD_CHARACTER.skill_tree.learn_skill(MysticBlockSkill)

    skill = GuardianShieldSkill(HERALD_CHARACTER)
    print(skill)
    print(skill.function(HERALD_CHARACTER))
    HERALD_CHARACTER.skill_tree.learn_skill(GuardianShieldSkill)

    skill = HeavyChargeSkill(HERALD_CHARACTER)
    print(skill)
    print(HERALD_CHARACTER.to_attack(
        defender_char=HERALD_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    HERALD_CHARACTER.skill_tree.learn_skill(HeavyChargeSkill)

    skill = ColossalOnslaughtSkill(HERALD_CHARACTER)
    print(skill)
    print(HERALD_CHARACTER.to_attack(
        defender_char=HERALD_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    HERALD_CHARACTER.skill_tree.learn_skill(ColossalOnslaughtSkill)
