from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.self_skill import CrystalArmorCondition
from rpgram.conditions.target_skill_debuff import ShatterCondition
from rpgram.constants.text import (
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    GuardianSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Guardião dos Cristais',
    'description': (
        'Caminho que transforma o Guardião em um protetor místico imbuído '
        'do poder dos cristais, capaz de erguer um escudo poderosos '
        'contra as forças arcanas e retaliar seus inimigos com ataques '
        'mágicos devastadores. '
        'Através de habilidades que canalizam a energia dos cristais, '
        'o Guardião se torna um bastião contra a magia, absorvendo feitiços '
        'e conjurando rajadas de energia cintilante para '
        'dizimar seus oponentes.'
    )
}


class CrystalArmorSkill(BaseSkill):
    NAME = GuardianSkillEnum.CRYSTAL_ARMOR.value
    DESCRIPTION = (
        f'Forja uma armadura de *Cristais Místicos* que aumenta a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* com base na redução de 25% da '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT} BASE* '
        f'mais um bônus de (10% x Rank x Nível) do valor reduzido.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.GUARDIAN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=CrystalArmorSkill.NAME,
            description=CrystalArmorSkill.DESCRIPTION,
            rank=CrystalArmorSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=CrystalArmorSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = CrystalArmorCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* forja uma armadura de *Cristais Místicos*, '
                f'reduzindo a sua '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                f'em favor de aumentar a sua {MAGICAL_DEFENSE_EMOJI_TEXT}.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class ShatterSkill(BaseSkill):
    NAME = GuardianSkillEnum.SHATTER.value
    DESCRIPTION = (
        f'Se envolve com um balandrau de *Cristais Místicos* e avança '
        f'contra o oponente, causando dano com base em '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (75% + 5% x Rank x Nível) e '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* (50% + 5% x Rank x Nível), '
        f'além de reduzir a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* e a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
        f' com base no dano causado (5% + 1% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.GUARDIAN.value,
        'skill_list': [CrystalArmorSkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_DEFENSE: 0.75,
            CombatStatsEnum.PHYSICAL_DEFENSE: 0.50,
        }
        damage_types = None

        super().__init__(
            name=ShatterSkill.NAME,
            description=ShatterSkill.DESCRIPTION,
            rank=ShatterSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=ShatterSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        target_name = target.player_name
        power = int(total_damage)
        level = self.level_rank
        condition = ShatterCondition(power=power, level=level)
        new_turn = condition.turn + 1
        condition.set_turn(new_turn)
        status_report_list = target.status.set_powerful_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in status_report_list]
        )
        report['text'] = f'*{target_name}* - {status_report_text}'

        return report


if __name__ == '__main__':
    from rpgram.constants.test import GUARDIAN_CHARACTER
    skill = CrystalArmorSkill(GUARDIAN_CHARACTER)
    print(skill)
    print(GUARDIAN_CHARACTER.cs.physical_defense)
    print(GUARDIAN_CHARACTER.cs.magical_defense)
    print(skill.function())
    print(GUARDIAN_CHARACTER.cs.physical_defense)
    print(GUARDIAN_CHARACTER.cs.magical_defense)
    GUARDIAN_CHARACTER.skill_tree.learn_skill(CrystalArmorSkill)

    skill = ShatterSkill(GUARDIAN_CHARACTER)
    print(skill)
    print(GUARDIAN_CHARACTER.cs.physical_defense)
    print(GUARDIAN_CHARACTER.cs.magical_defense)
    # print(skill.hit_function(GUARDIAN_CHARACTER, 1000, 1500))
    print(GUARDIAN_CHARACTER.to_attack(
        defender_char=GUARDIAN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    print(GUARDIAN_CHARACTER.cs.physical_defense)
    print(GUARDIAN_CHARACTER.cs.magical_defense)
    GUARDIAN_CHARACTER.skill_tree.learn_skill(ShatterSkill)
