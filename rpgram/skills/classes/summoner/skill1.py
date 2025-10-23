from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.barrier import PiskieWindbagCondition
from rpgram.constants.text import (
    HIT_POINT_FULL_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    SkillDefenseEnum,
    SkillTypeEnum,
    SummonerSkillEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class FlamingSpecterSkill(BaseSkill):
    NAME = SummonerSkillEnum.FLAMING_SPECTER.value
    DESCRIPTION = (
        'Conjura uma *Criatura Espectral de Fogo* com olhos ardentes '
        'e corpo feito de chamas, ele avança sobre um inimigo '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.SUMMONER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.FIRE]

        super().__init__(
            name=FlamingSpecterSkill.NAME,
            description=FlamingSpecterSkill.DESCRIPTION,
            rank=FlamingSpecterSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=FlamingSpecterSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class KappaFountainSkill(BaseSkill):
    NAME = SummonerSkillEnum.KAPPA_FOUNTAIN.value
    DESCRIPTION = (
        'Convoca um *Kappa Amigável* que fornece um pouco da '
        '*Água do seu Prato* para um aliado, '
        f'curando o seu *{HIT_POINT_FULL_EMOJI_TEXT}* '
        f'com base na *{MAGICAL_DEFENSE_EMOJI_TEXT}* '
        '(200% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.SUMMONER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=KappaFountainSkill.NAME,
            description=KappaFountainSkill.DESCRIPTION,
            rank=KappaFountainSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.HEALING,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=KappaFountainSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            dice = self.dice
            level = self.level_rank
            power_multiplier = 2 + (level / 10)
            power = dice.boosted_magical_defense * power_multiplier
            power = round(power)

            cure_report = char.cs.cure_hit_points(power)
            report_text = cure_report["text"]
            report = {
                'text': (
                    f'*{target_name}* recebe um pouco de água do '
                    '*Prato do Kappa* que cura suas feridas.\n'
                    f'*{report_text}*({dice.text}).'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class PiskieWindbagSkill(BaseSkill):
    NAME = SummonerSkillEnum.PISKIE_WINDBAG.value
    DESCRIPTION = (
        'Chama um *Pequenino Piskie* que mira a boca do seu '
        'minúsculo *Sacovento* para proteger um aliado com uma '
        '*Barreira de Ar Turbilhonante* '
        'baseada na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.SUMMONER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=PiskieWindbagSkill.NAME,
            description=PiskieWindbagSkill.DESCRIPTION,
            rank=PiskieWindbagSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BARRIER,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=PiskieWindbagSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            dice = self.dice
            power = dice.boosted_magical_defense
            level = self.level_rank
            condition = PiskieWindbagCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    '*Piskie* dispara uma *Barreira de Ar Turbilhonante* '
                    'para proteger '
                    f'*{target_name}* com '
                    f'*{condition.barrier_points_text}*({dice.text}).\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Arcano Dimensional',
    'description': (
        'O Arcano Dimensional é um arquiteto cósmico, '
        'um manipulador das leis da realidade. '
        'Seus poderes transcendem os limites do mundo material, '
        'permitindo-lhe convocar criaturas de outros planos dimensionais. '
        'O Arcano Dimensional é um mago versátil, '
        'capaz de tanto atacar quanto defender. '
        'Ele pode convocar criaturas poderosas para lutar ao seu lado, '
        'criar campos de força para proteger a si mesmo e seus aliados, '
        'ou manipular o ambiente para confundir e incapacitar seus inimigos. '
    ),
    'skill_list': [
        FlamingSpecterSkill,
        KappaFountainSkill,
        PiskieWindbagSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import SUMMONER_CHARACTER

    skill = FlamingSpecterSkill(SUMMONER_CHARACTER)
    print(skill)
    print(SUMMONER_CHARACTER.cs.magical_attack)
    print(SUMMONER_CHARACTER.to_attack(
        defender_char=SUMMONER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    SUMMONER_CHARACTER.skill_tree.learn_skill(FlamingSpecterSkill)

    skill = KappaFountainSkill(SUMMONER_CHARACTER)
    print(skill)
    print(SUMMONER_CHARACTER.cs.magical_defense)
    print(skill.function(SUMMONER_CHARACTER))
    SUMMONER_CHARACTER.skill_tree.learn_skill(KappaFountainSkill)

    skill = PiskieWindbagSkill(SUMMONER_CHARACTER)
    print(skill)
    print(SUMMONER_CHARACTER.cs.magical_defense)
    print(skill.function(SUMMONER_CHARACTER))
    SUMMONER_CHARACTER.skill_tree.learn_skill(PiskieWindbagSkill)
