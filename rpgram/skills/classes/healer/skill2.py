from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.barrier import (
    BeatifyingAegisCondition,
    HealingRefugeCondition,
    ProtectiveAuraCondition,
    ProtectiveInfusionCondition
)
from rpgram.constants.text import (
    HIT_POINT_FULL_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    HealerSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class ProtectiveAuraSkill(BaseSkill):
    NAME = HealerSkillEnum.PROTECTIVE_AURA.value
    DESCRIPTION = (
        'Converge *Energia Vital* para tecer um campo de energia benéfica '
        'ao redor de um aliado, salvaguardando-o '
        'com uma barreira baseada na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.HEALER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=ProtectiveAuraSkill.NAME,
            description=ProtectiveAuraSkill.DESCRIPTION,
            rank=ProtectiveAuraSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BARRIER,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=ProtectiveAuraSkill.REQUIREMENTS,
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
            power = dice.boosted_magical_defense
            level = self.level_rank
            condition = ProtectiveAuraCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{player_name}* converge *Energia Vital* e tece '
                    'um campo de energia benéfica, salvaguardando '
                    f'*{target_name}* com uma barreira '
                    f'*{condition.barrier_points_text}*({dice.text}).\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class HealingRefugeSkill(BaseSkill):
    NAME = HealerSkillEnum.HEALING_REFUGE.value
    DESCRIPTION = (
        'Converge *Energia Vital* para engendrar '
        'um campo de energia benéfica '
        'ao redor de um aliado, resguardando-o '
        'com uma barreira baseada na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (200% + 10% x Rank x Nível) que, '
        f'também, cura {HIT_POINT_FULL_EMOJI_TEXT} a cada turno '
        'com uma fração desse valor.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.HEALER.value,
        'skill_list': [
            ProtectiveAuraSkill.NAME
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=HealingRefugeSkill.NAME,
            description=HealingRefugeSkill.DESCRIPTION,
            rank=HealingRefugeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BARRIER,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=HealingRefugeSkill.REQUIREMENTS,
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
            power = dice.boosted_magical_defense
            level = self.level_rank
            condition = HealingRefugeCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{player_name}* converge *Energia Vital* e engendra '
                    'um campo de energia benéfica, resguardando '
                    f'*{target_name}* com uma barreira '
                    f'*{condition.barrier_points_text}*({dice.text}).\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class ProtectiveInfusionSkill(BaseSkill):
    NAME = HealerSkillEnum.PROTECTIVE_INFUSION.value
    DESCRIPTION = (
        'Usando ervas, cria uma *Infusão Protetiva* que protege um aliado '
        'com uma nevoa de incenso purificativo, '
        'gerando uma barreira baseada na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (200% + 10% x Rank x Nível) e '
        'cura até (Nível) níveis de condições aleatórias a cada turno.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.HEALER.value,
        'skill_list': [
            ProtectiveAuraSkill.NAME
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=ProtectiveInfusionSkill.NAME,
            description=ProtectiveInfusionSkill.DESCRIPTION,
            rank=ProtectiveInfusionSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BARRIER,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=ProtectiveInfusionSkill.REQUIREMENTS,
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
            power = dice.boosted_magical_defense
            level = self.level_rank
            condition = ProtectiveInfusionCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{player_name}* cria uma *Infusão Protetiva* e protege '
                    f'*{target_name}* com uma barreira '
                    f'*{condition.barrier_points_text}*({dice.text}).\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class BeatifyingAegisSkill(BaseSkill):
    NAME = HealerSkillEnum.BEATIFYING_AEGIS.value
    DESCRIPTION = (
        f'Convoca a *{HealerSkillEnum.BEATIFYING_AEGIS.value}* para '
        'criar uma *Proteção Sacra* que escuda um aliado '
        'com esse *Artefato Lendário*, '
        'concedendo-lhe uma barreira baseada na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (200% + 10% x Rank x Nível) que, '
        f'também, recupera {HIT_POINT_FULL_EMOJI_TEXT} a cada turno '
        'com uma fração desse valor e '
        'cura até (Nível) níveis de condições aleatórias a cada turno.'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.HEALER.value,
        'skill_list': [
            ProtectiveAuraSkill.NAME,
            HealingRefugeSkill.NAME,
            ProtectiveInfusionSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=BeatifyingAegisSkill.NAME,
            description=BeatifyingAegisSkill.DESCRIPTION,
            rank=BeatifyingAegisSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BARRIER,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=BeatifyingAegisSkill.REQUIREMENTS,
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
            power = dice.boosted_magical_defense
            level = self.level_rank
            condition = BeatifyingAegisCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{player_name}* cria uma *Proteção Sacra* e escuda '
                    f'*{target_name}* com uma barreira '
                    f'*{condition.barrier_points_text}*({dice.text}).\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Guardião da Vida',
    'description': (
        'São mestres na arte de proteger e preservar a existência. '
        'Eles concentram-se na união entre cura e defesa, '
        'permitindo que sejam uma fortaleza para seus aliados. '
        'Eles canalizam energias sagradas para criar barreiras protetoras, '
        'purificar a corrupção, e regenerar feridas críticas mesmo nas '
        'situações mais desesperadoras. '
        'Seus poderes vão além da simples recuperação, '
        'oferecendo proteção ativa contra o dano. '
        'Os Guardiões da Vida são o pilar em qualquer batalha, '
        'garantindo que seus companheiros permaneçam em pé, '
        'não importa o quão intenso seja o embate.'
    ),
    'skill_list': [
        ProtectiveAuraSkill,
        HealingRefugeSkill,
        ProtectiveInfusionSkill,
        BeatifyingAegisSkill
    ]
}


if __name__ == '__main__':
    from rpgram.conditions.debuff import CurseCondition
    from rpgram.constants.test import HEALER_CHARACTER

    skill = ProtectiveAuraSkill(HEALER_CHARACTER)
    print(skill)
    print(HEALER_CHARACTER.cs.show_barrier_points)
    print(skill.function(HEALER_CHARACTER))
    print(HEALER_CHARACTER.cs.show_barrier_points)
    HEALER_CHARACTER.skill_tree.learn_skill(ProtectiveAuraSkill)

    skill = HealingRefugeSkill(HEALER_CHARACTER)
    print(skill)
    print(HEALER_CHARACTER.cs.show_barrier_points)
    print(skill.function(HEALER_CHARACTER))
    print(HEALER_CHARACTER.cs.show_barrier_points)
    HEALER_CHARACTER.skill_tree.learn_skill(HealingRefugeSkill)

    skill = ProtectiveInfusionSkill(HEALER_CHARACTER)
    print(skill)
    print(HEALER_CHARACTER.cs.show_barrier_points)
    print(skill.function(HEALER_CHARACTER))
    print(HEALER_CHARACTER.cs.show_barrier_points)
    HEALER_CHARACTER.skill_tree.learn_skill(ProtectiveInfusionSkill)

    skill = BeatifyingAegisSkill(HEALER_CHARACTER)
    print(skill)
    print(HEALER_CHARACTER.cs.show_barrier_points)
    print(skill.function(HEALER_CHARACTER))
    print(HEALER_CHARACTER.cs.show_barrier_points)
    HEALER_CHARACTER.skill_tree.learn_skill(BeatifyingAegisSkill)

    HEALER_CHARACTER.status.add_condition(CurseCondition(level=20))
    HEALER_CHARACTER.cs.damage_hit_points(5000, ignore_barrier=True)
    print(
        '\n'.join(
            report['text']
            for report in HEALER_CHARACTER.activate_status()
        )
    )
