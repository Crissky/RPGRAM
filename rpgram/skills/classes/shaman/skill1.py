from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.target_skill_buff import (
    CrystalSapRingCondition,
    VineCrosierCondition,
    WildCarnationCloakCondition
)
from rpgram.constants.text import (
    MAGICAL_ATTACK_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    WISDOM_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    ShamanSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class VineCrosierSkill(BaseSkill):
    NAME = ShamanSkillEnum.VINE_CROSIER.value
    DESCRIPTION = (
        f'Reveste as próprias armas em um emaranhado de *Vinhas*, '
        f'transmutando-as em um *{ShamanSkillEnum.VINE_CROSIER.value}* que '
        f'aumenta o '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.SHAMAN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=VineCrosierSkill.NAME,
            description=VineCrosierSkill.DESCRIPTION,
            rank=VineCrosierSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=VineCrosierSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = char.cs.wisdom
        condition = VineCrosierCondition(power=power, level=level)
        report_list = char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* cria e equipa um *{self.name}*, '
                f'aumentando o '
                f'*{MAGICAL_ATTACK_EMOJI_TEXT}* em '
                f'{condition.bonus_magical_attack} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class WildCarnationCloakSkill(BaseSkill):
    NAME = ShamanSkillEnum.WILD_CARNATION_CLOAK.value
    DESCRIPTION = (
        f'Tece um *Manto* imbuido por *Pétalas de Cravo Selvagem* que '
        f'aumenta a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.SHAMAN.value,
        'skill_list': [VineCrosierSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=WildCarnationCloakSkill.NAME,
            description=WildCarnationCloakSkill.DESCRIPTION,
            rank=WildCarnationCloakSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=WildCarnationCloakSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = char.cs.wisdom
        condition = WildCarnationCloakCondition(power=power, level=level)
        report_list = char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* cria e equipa um *{self.name}*, '
                f'aumentando a '
                f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* em '
                f'{condition.bonus_magical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class CrystalSapRingSkill(BaseSkill):
    NAME = ShamanSkillEnum.CRYSTAL_SAP_RING.value
    DESCRIPTION = (
        f'Esculpe um *Anel* reluzente feito de *Seiva Cristalina* que '
        f'aumenta o '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* e a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (300% + 10% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.SHAMAN.value,
        'skill_list': [VineCrosierSkill.NAME, WildCarnationCloakSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=CrystalSapRingSkill.NAME,
            description=CrystalSapRingSkill.DESCRIPTION,
            rank=CrystalSapRingSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=CrystalSapRingSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = char.cs.wisdom
        condition = CrystalSapRingCondition(power=power, level=level)
        report_list = char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* cria e equipa um *{self.name}*, '
                f'aumentando o '
                f'*{MAGICAL_ATTACK_EMOJI_TEXT}* em '
                f'{condition.bonus_magical_attack} pontos e a '
                f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* em '
                f'{condition.bonus_magical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Artesão Verde',
    'description': (
        'O Artesão Verde representa o domínio do Xamã sobre a '
        'a vida e a matéria Verde da natureza, moldando-a para esculpir '
        'diversos artefatos mágicos imbuídos de vida. '
        'O Xamã transforma a matéria prima da floresta em '
        'acessórios poderosos, dando-lhe a capacidade de defender '
        'a natureza e seus aliados.'
    ),
    'skill_list': [
        VineCrosierSkill,
        WildCarnationCloakSkill,
        CrystalSapRingSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import SHAMAN_CHARACTER

    skill = VineCrosierSkill(SHAMAN_CHARACTER)
    print(skill)
    print(SHAMAN_CHARACTER.cs.wisdom)
    print(SHAMAN_CHARACTER.cs.magical_attack)
    print(skill.function())
    print(SHAMAN_CHARACTER.cs.magical_attack)
    SHAMAN_CHARACTER.skill_tree.learn_skill(VineCrosierSkill)

    skill = WildCarnationCloakSkill(SHAMAN_CHARACTER)
    print(skill)
    print(SHAMAN_CHARACTER.cs.wisdom)
    print(SHAMAN_CHARACTER.cs.magical_defense)
    print(skill.function())
    print(SHAMAN_CHARACTER.cs.magical_defense)
    SHAMAN_CHARACTER.skill_tree.learn_skill(WildCarnationCloakSkill)

    skill = CrystalSapRingSkill(SHAMAN_CHARACTER)
    print(skill)
    print(SHAMAN_CHARACTER.cs.wisdom)
    print(SHAMAN_CHARACTER.cs.magical_attack,
          SHAMAN_CHARACTER.cs.magical_defense)
    print(skill.function())
    print(SHAMAN_CHARACTER.cs.magical_attack,
          SHAMAN_CHARACTER.cs.magical_defense)
    SHAMAN_CHARACTER.skill_tree.learn_skill(CrystalSapRingSkill)

    print('\n'.join([
        report['text']
        for report in SHAMAN_CHARACTER.activate_status()
    ]))
