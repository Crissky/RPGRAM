from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.self_skill import (
    FlamingFuryCondition
)
from rpgram.conditions.special_damage_skill import (
    SDFlamingFuryCondition
)
from rpgram.conditions.target_skill_buff import (
    MartialBannerCondition,
    WarCornuCondition
)
from rpgram.constants.text import (
    PHYSICAL_ATTACK_EMOJI_TEXT,
    STRENGTH_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    GladiatorSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class MartialBannerSkill(BaseSkill):
    NAME = GladiatorSkillEnum.MARTIAL_BANNER.value
    DESCRIPTION = (
        'Usa a própria força e ira para evocar o '
        '*Sinal do Senhor da Guerra* e conceder à equipe '
        'uma inspiração de combate que aumenta o '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* com base na '
        f'*{STRENGTH_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.GLADIATOR.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=MartialBannerSkill.NAME,
            description=MartialBannerSkill.DESCRIPTION,
            rank=MartialBannerSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=MartialBannerSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            power = self.char.bs.strength
            level = self.level_rank
            condition = MartialBannerCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* recebe o *Sinal do Senhor da Guerra*, '
                    'aumentando o '
                    f'{PHYSICAL_ATTACK_EMOJI_TEXT} em '
                    f'*{condition.power}* pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class FlamingFurySkill(BaseSkill):
    NAME = GladiatorSkillEnum.FLAMING_FURY.value
    DESCRIPTION = (
        'Por meio de uma conexão baseada no mais puro desejo de guerrear, '
        'é banhado pela *Fúria do Senhor da Guerra*, '
        'aumentando o '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* com base na '
        f'*{STRENGTH_EMOJI_TEXT}* (300% + 10% x Rank x Nível) e '
        'adicionando dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.CHAOS)}* '
        'baseado no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.GLADIATOR.value,
        'skill_list': [MartialBannerSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=FlamingFurySkill.NAME,
            description=FlamingFurySkill.DESCRIPTION,
            rank=FlamingFurySkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=FlamingFurySkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        char = self.char
        player_name = self.char.player_name
        if char.is_alive:
            level = self.level_rank
            condition = FlamingFuryCondition(character=char, level=level)
            sd_power = self.char.cs.physical_attack
            sd_condition = SDFlamingFuryCondition(power=sd_power, level=level)
            report_list = char.status.set_conditions(condition, sd_condition)


            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{player_name}* é banhado pela '
                    '*Fúria do Senhor da Guerra*, '
                    'aumentando o '
                    f'{PHYSICAL_ATTACK_EMOJI_TEXT} em '
                    f'*{condition.bonus_physical_attack}* pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{player_name}* está morto.'}

        return report


class WarCornuSkill(BaseSkill):
    NAME = GladiatorSkillEnum.WAR_CORNU.value
    DESCRIPTION = (
        'Ergue seu imponente *Cornu de Guerra* '
        'e o toca com uma força que ressoa nos corações dos aliados, '
        'invocando a antiga *Bravura do Senhor da Guerra*, '
        'que concede uma aura de coragem e ferocidade '
        'àqueles que lutam ao seu lado, '
        'aumentando o '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* com base na '
        f'*{STRENGTH_EMOJI_TEXT}* (300% + 10% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.GLADIATOR.value,
        'skill_list': [MartialBannerSkill.NAME, FlamingFurySkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=WarCornuSkill.NAME,
            description=WarCornuSkill.DESCRIPTION,
            rank=WarCornuSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=WarCornuSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            power = self.char.bs.strength
            level = self.level_rank
            condition = WarCornuCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* recebe a *Bravura do Senhor da Guerra*, '
                    'aumentando o '
                    f'{PHYSICAL_ATTACK_EMOJI_TEXT} em '
                    f'*{condition.power}* pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Filho da Guerra',
    'description': (
        'Nascido e criado no calor da batalha, '
        'o Filho da Guerra é um guerreiro moldado pela violência. '
        'Seu destino é a batalha, onde ele encontra seu verdadeiro lar. '
        'Com cada combate, ele se fortalece, '
        'tanto física quanto espiritualmente, '
        'tornando-se uma força imparável.'
    ),
    'skill_list': [
        MartialBannerSkill,
        FlamingFurySkill,
        WarCornuSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import GLADIATOR_CHARACTER

    skill = MartialBannerSkill(GLADIATOR_CHARACTER)
    print(skill)
    print(GLADIATOR_CHARACTER.cs.strength,
          GLADIATOR_CHARACTER.cs.physical_attack)
    print(skill.function(GLADIATOR_CHARACTER))
    print(GLADIATOR_CHARACTER.cs.physical_attack)
    GLADIATOR_CHARACTER.skill_tree.learn_skill(MartialBannerSkill)

    skill = FlamingFurySkill(GLADIATOR_CHARACTER)
    print(skill)
    print(GLADIATOR_CHARACTER.cs.strength,
          GLADIATOR_CHARACTER.cs.physical_attack)
    print(skill.function(GLADIATOR_CHARACTER))
    print(GLADIATOR_CHARACTER.cs.physical_attack)
    GLADIATOR_CHARACTER.skill_tree.learn_skill(FlamingFurySkill)

    skill = WarCornuSkill(GLADIATOR_CHARACTER)
    print(skill)
    print(GLADIATOR_CHARACTER.cs.strength,
          GLADIATOR_CHARACTER.cs.physical_attack)
    print(skill.function(GLADIATOR_CHARACTER))
    print(GLADIATOR_CHARACTER.cs.physical_attack)
    GLADIATOR_CHARACTER.skill_tree.learn_skill(WarCornuSkill)
