from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.barrier import (
    RobysticShieldCondition
)
from rpgram.conditions.self_skill import (
    MysticBlockCondition,
    RobysticBlockCondition
)
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
        'Utiliza a *Fé* e *Devoção* para invocar *Forças Místicas*, '
        'criando uma *Aura Protetora* que o rodeia, '
        'aumentando a '
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
                '*Aura Protetora*, '
                'aumentando a sua '
                f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_magical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class RobysticShieldSkill(BaseSkill):
    NAME = HeraldSkillEnum.ROBYSTIC_SHIELD.value
    DESCRIPTION = (
        'Erguendo o escudo com *Fé* e *Devoção*, '
        'evoca um *Robusto Escudo Familiar Protetivo* '
        'carregado de *Forças Místicas* '
        'que resguarda com uma barreira baseada na '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* (200% + 10% x Rank x Nível) e '
        'aumentando a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* e a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{CONSTITUTION_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.HERALD.value,
        'skill_list': [
            GuardianShieldSkill.NAME,
            RobustBlockSkill.NAME,
            MysticBlockSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=RobysticShieldSkill.NAME,
            description=RobysticShieldSkill.DESCRIPTION,
            rank=RobysticShieldSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BARRIER,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=RobysticShieldSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
        if char.is_alive:
            target_name = (
                'a si mesmo'
                if target_name == player_name
                else target_name
            )
            dice = self.dice
            power = dice.boosted_physical_defense
            level = self.level_rank
            condition = RobysticBlockCondition(character=char, level=level)
            condition_shield = RobysticShieldCondition(
                power=power,
                level=level
            )
            report_list = char.status.set_conditions(
                condition, condition_shield
            )
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{player_name}* se impõe contra o perigo, evocando um '
                    '*Robusto Escudo Familiar Protetivo* para resguardar '
                    f'*{target_name}* com uma barreira '
                    f'*{condition_shield.barrier_points_text}*({dice.text}).'
                    ' e aumentando a sua '
                    f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                    f'em {condition.bonus_physical_defense} pontos e a '
                    f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
                    f'em {condition.bonus_magical_defense} pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class ColossalOnslaughtSkill(BaseSkill):
    NAME = HeraldSkillEnum.COLOSSAL_ONSLAUGHT.value
    DESCRIPTION = (
        'Avança através das linhas inimigas com uma *Força Colossal* '
        'como um *Gigante Implacável*, envolto em uma aura de fogo e rocha, '
        'causando dano de '
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
        GuardianShieldSkill,
        RobustBlockSkill,
        MysticBlockSkill,
        RobysticShieldSkill,
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

    skill = RobysticShieldSkill(HERALD_CHARACTER)
    print(skill)
    print(HERALD_CHARACTER.bs.constitution)
    print(skill.function(HERALD_CHARACTER))
    HERALD_CHARACTER.skill_tree.learn_skill(RobysticShieldSkill)

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
