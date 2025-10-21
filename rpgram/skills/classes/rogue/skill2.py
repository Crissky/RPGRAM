from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.self_skill import (
    ChaoticStepsCondition,
    ShadowStepsCondition
)
from rpgram.constants.text import (
    DEXTERITY_EMOJI_TEXT,
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    RogueSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class ShadowStepsSkill(BaseSkill):
    NAME = RogueSkillEnum.SHADOW_STEPS.value
    DESCRIPTION = (
        'Torna-se um "Fantasma", movendo-se pelas *Sombras* e '
        'aumentando o '
        f'*{HIT_EMOJI_TEXT}* com base na '
        f'*{DEXTERITY_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.ROGUE.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=ShadowStepsSkill.NAME,
            description=ShadowStepsSkill.DESCRIPTION,
            rank=ShadowStepsSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=ShadowStepsSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = ShadowStepsCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* move-se pelas *Sombras*, '
                ' aumentando o '
                f'*{HIT_EMOJI_TEXT}* '
                f'em {condition.bonus_hit} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class ChaoticStepsSkill(BaseSkill):
    NAME = RogueSkillEnum.CHAOTIC_STEPS.value
    DESCRIPTION = (
        'Assume um padrão errático e imprevisível de movimentos, '
        'tornado sua locomoção ainda mais difícil de prever, '
        'aumentando a '
        f'*{EVASION_EMOJI_TEXT}* com base na '
        f'*{DEXTERITY_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.ROGUE.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=ChaoticStepsSkill.NAME,
            description=ChaoticStepsSkill.DESCRIPTION,
            rank=ChaoticStepsSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=ChaoticStepsSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = ChaoticStepsCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* começa a mover-se de maneira '
                'errática e imprevisível, '
                'aumentando a '
                f'*{EVASION_EMOJI_TEXT}* '
                f'em {condition.bonus_evasion} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class ShadowStrikeSkill(BaseSkill):
    NAME = RogueSkillEnum.SHADOW_STRIKE.value
    DESCRIPTION = (
        'Se mescla as *Sombras* e as usa para lançar um ataque poderoso, '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.DARK)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.ROGUE.value,
        'skill_list': [ShadowStepsSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.DARK, DamageEnum.DARK]

        super().__init__(
            name=ShadowStrikeSkill.NAME,
            description=ShadowStrikeSkill.DESCRIPTION,
            rank=ShadowStrikeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=ShadowStrikeSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class ChaoticStrikeSkill(BaseSkill):
    NAME = RogueSkillEnum.CHAOTIC_STRIKE.value
    DESCRIPTION = (
        'Usa a imprevisibilidade e a desorientação para realizar uma '
        'série de golpes rápidos e *Caóticos*, '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.CHAOS)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.ROGUE.value,
        'skill_list': [ChaoticStepsSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.CHAOS, DamageEnum.CHAOS]

        super().__init__(
            name=ChaoticStrikeSkill.NAME,
            description=ChaoticStrikeSkill.DESCRIPTION,
            rank=ChaoticStrikeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=ChaoticStrikeSkill.REQUIREMENTS,
            damage_types=damage_types
        )


SKILL_WAY_DESCRIPTION = {
    'name': 'Mestre das Sombras',
    'description': (
        'O Mestre das Sombras é um especialista em manipular a escuridão '
        'para seu proveito. '
        'Ele se move silenciosamente, explorando as profundezas da trevas '
        'como se fosse parte dela. '
        'Suas habilidades se concentram em enganar e confundir seus '
        'inimigos, utilizando as sombras como sua aliada.'
    ),
    'skill_list': [
        ShadowStepsSkill,
        ChaoticStepsSkill,
        ShadowStrikeSkill,
        ChaoticStrikeSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import ROGUE_CHARACTER

    skill = ShadowStepsSkill(ROGUE_CHARACTER)
    print(skill)
    print(ROGUE_CHARACTER.cs.dexterity)
    print(ROGUE_CHARACTER.cs.hit)
    print(skill.function())
    print(ROGUE_CHARACTER.cs.hit)
    ROGUE_CHARACTER.skill_tree.learn_skill(ShadowStepsSkill)

    skill = ChaoticStepsSkill(ROGUE_CHARACTER)
    print(skill)
    print(ROGUE_CHARACTER.cs.dexterity)
    print(ROGUE_CHARACTER.cs.evasion)
    print(skill.function())
    print(ROGUE_CHARACTER.cs.evasion)
    ROGUE_CHARACTER.skill_tree.learn_skill(ChaoticStepsSkill)

    print('\n'.join([
        report['text']
        for report in ROGUE_CHARACTER.activate_status()
    ]))

    skill = ShadowStrikeSkill(ROGUE_CHARACTER)
    print(skill)
    print(ROGUE_CHARACTER.cs.precision_attack)
    print(ROGUE_CHARACTER.to_attack(
        defender_char=ROGUE_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ROGUE_CHARACTER.skill_tree.learn_skill(ShadowStrikeSkill)

    skill = ChaoticStrikeSkill(ROGUE_CHARACTER)
    print(skill)
    print(ROGUE_CHARACTER.cs.precision_attack)
    print(ROGUE_CHARACTER.to_attack(
        defender_char=ROGUE_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ROGUE_CHARACTER.skill_tree.learn_skill(ChaoticStrikeSkill)
