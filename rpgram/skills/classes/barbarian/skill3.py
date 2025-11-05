from random import sample
from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.debuff import BurnCondition, PoisoningCondition
from rpgram.conditions.self_skill import (
    FafnirsScalesCondition,
    RaijusFootstepsCondition
)
from rpgram.conditions.special_damage_skill import (
    SDWildAcidCondition,
    SDWildFireCondition,
    SDWildGroundCondition,
    SDWildLightningCondition,
    SDWildPoisonCondition,
    SDWildRockCondition,
    SDWildWindCondition
)
from rpgram.constants.text import (
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    STRENGTH_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.skill import (
    BarbarianSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class WildForgeSkill(BaseSkill):
    NAME = BarbarianSkillEnum.WILD_FORGE.value
    DESCRIPTION = (
        'Imbui a própria arma com algum *Elemento Selvagem* aleatório '
        'com dano baseado no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BARBARIAN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=WildForgeSkill.NAME,
            description=WildForgeSkill.DESCRIPTION,
            rank=WildForgeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=WildForgeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        power = char.cs.physical_attack
        level = self.level_rank

        total_conditions = 2
        if self.dice.is_critical:
            total_conditions = 5
        elif self.dice.is_critical_fail:
            total_conditions = 1

        condition_class_list = [
            SDWildFireCondition,
            SDWildLightningCondition,
            SDWildWindCondition,
            SDWildRockCondition,
            SDWildGroundCondition,
            SDWildAcidCondition,
            SDWildPoisonCondition,
        ]
        sample_condition_list = sample(condition_class_list, total_conditions)
        report_list = []
        name_list = []
        damage_emoji_name_list = []
        for condition_cls in sample_condition_list:
            condition = condition_cls(power=power, level=level)
            name_list.append(condition.name)
            damage_emoji_name_list.append(condition.damage_emoji_name)
            report_list.extend(self.char.status.set_conditions(condition))
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )

        if len(name_list) > 1:
            element_names = ', '.join([
                f'o *Elemento {name}*' for name in name_list[:-1]
            ]) + f' e o *Elemento {name_list[-1]}*'
        else:
            element_names = ', '.join([
                f'o *Elemento {name}*' for name in name_list
            ])

        if len(damage_emoji_name_list) > 1:
            damage_emoji_names = ', '.join([
                f'*{emoji_name}*' for emoji_name in damage_emoji_name_list[:-1]
            ]) + f' e *{damage_emoji_name_list[-1]}*'
        else:
            damage_emoji_names = ', '.join([
                f'*{emoji_name}*' for emoji_name in damage_emoji_name_list
            ])

        report = {
            'text': (
                f'*{player_name}*{self.dice.text} forja {element_names} '
                'e embebeda sua(s) arma(s), recebendo '
                f'o tipo de dano {damage_emoji_names}.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class SalamandersBreathSkill(BaseSkill):
    NAME = BarbarianSkillEnum.SALAMANDERÇÇÇS_BREATH.value
    DESCRIPTION = (
        '*Espírito da Salamandra*: Respira fundo, '
        'concentrando seu calor interno, e '
        'com um rugido feroz expele uma nuvem densa de vapor '
        'incandescente de sua boca, liberando chamas abrasadoras que '
        'incinera seu alvo, causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BARBARIAN.value,
        'skill_list': [WildForgeSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.FIRE]

        super().__init__(
            name=SalamandersBreathSkill.NAME,
            description=SalamandersBreathSkill.DESCRIPTION,
            rank=SalamandersBreathSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=SalamandersBreathSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class SweepingRocSkill(BaseSkill):
    NAME = BarbarianSkillEnum.SWEEPING_ROC.value
    DESCRIPTION = (
        '*Espírito de Roc*: Com um grito feroz, '
        'realiza um salto veloz em direção ao alvo e '
        'executa um golpe devastador '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.WIND)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível). '
        f'Essa habilidade possui *{HIT_EMOJI_TEXT}* acima do normal.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BARBARIAN.value,
        'skill_list': [WildForgeSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.00,
        }
        damage_types = [DamageEnum.WIND, DamageEnum.SLASHING]

        super().__init__(
            name=SweepingRocSkill.NAME,
            description=SweepingRocSkill.DESCRIPTION,
            rank=SweepingRocSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=SweepingRocSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 1.50


class HydraFangsSkill(BaseSkill):
    NAME = BarbarianSkillEnum.HYDRAÇÇÇS_FANGS.value
    DESCRIPTION = (
        '*Espírito da Hidra*: Com movimentos de um predador implacável, '
        'ataca com as armas envolvidas em '
        'uma névoa ácida, '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.ACID)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.POISON)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível) e '
        'adicionando as condições '
        f'*{get_debuff_emoji_text(DebuffEnum.BURN)}* e '
        f'*{get_debuff_emoji_text(DebuffEnum.POISONING)}* '
        'com nível igual a (Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BARBARIAN.value,
        'skill_list': [WildForgeSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.ACID, DamageEnum.POISON]

        super().__init__(
            name=HydraFangsSkill.NAME,
            description=HydraFangsSkill.DESCRIPTION,
            rank=HydraFangsSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=HydraFangsSkill.REQUIREMENTS,
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
        if target.is_alive:
            level = self.level_rank

            burn_condition = BurnCondition(level=level)
            status_report = target.status.add_condition(burn_condition)
            report['status_text'] = status_report['text']

            poisoning_condition = PoisoningCondition(level=level)
            status_report = target.status.add_condition(poisoning_condition)
            report['status_text'] += '\n' + status_report['text']

        return report


class RaijusFootstepsSkill(BaseSkill):
    NAME = BarbarianSkillEnum.RAIJŪÇÇÇS_FOOTSTEPS.value
    DESCRIPTION = (
        '*Espírito da Raijū*: Entra em transe com seus olhos brilhando '
        'como eletricidade, se tornando um raio implacável e movendo-se com '
        'velocidade sobrenatural, '
        'aumentando o '
        f'*{HIT_EMOJI_TEXT}* e a *{EVASION_EMOJI_TEXT}* com base na '
        f'{STRENGTH_EMOJI_TEXT} (200% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BARBARIAN.value,
        'skill_list': [WildForgeSkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=RaijusFootstepsSkill.NAME,
            description=RaijusFootstepsSkill.DESCRIPTION,
            rank=RaijusFootstepsSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=RaijusFootstepsSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        level = self.level_rank
        char = self.char
        condition = RaijusFootstepsCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* desperta um *Transe Sobrenatural* '
                'que aumenta '
                f'*{HIT_EMOJI_TEXT}* '
                f'em {condition.bonus_hit} pontos e '
                f'*{EVASION_EMOJI_TEXT}* '
                f'em {condition.bonus_evasion} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class FafnirsScalesSkill(BaseSkill):
    NAME = BarbarianSkillEnum.FAFNIRÇÇÇS_SCALES.value
    DESCRIPTION = (
        '*Espírito da Fáfnir*: Tenciona os seus músculos, '
        'os contraindo juntamente com a sua pele, transformando-os em pedra, '
        'aumentando a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
        'com base na '
        f'{STRENGTH_EMOJI_TEXT} (200% + 10% x Rank x Nível), '
        'o bônus concedido aumenta quanto mais próximo da morte estiver.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BARBARIAN.value,
        'skill_list': [WildForgeSkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=FafnirsScalesSkill.NAME,
            description=FafnirsScalesSkill.DESCRIPTION,
            rank=FafnirsScalesSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=FafnirsScalesSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        level = self.level_rank
        char = self.char
        condition = FafnirsScalesCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* Tenciona os músculos, '
                'transformando-os em pedra, '
                'aumentando a '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Espírito Selvagem',
    'description': (
        'O caminho do Espírito Selvagem transforma o Bárbaro em um canal vivo '
        'das forças da natureza, utilizando habilidades ancestrais para '
        'manipular os elementos selvagens e liberar a '
        'fúria indomável da fera interior. '
        'Através de rituais primitivos e conexão profunda com os elementos, '
        'o Bárbaro se torna um agente da destruição natural.'
    ),
    'skill_list': [
        WildForgeSkill,
        SalamandersBreathSkill,
        SweepingRocSkill,
        HydraFangsSkill,
        RaijusFootstepsSkill,
        FafnirsScalesSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import BARBARIAN_CHARACTER

    skill = WildForgeSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(skill.function())
    print(BARBARIAN_CHARACTER.status)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(WildForgeSkill)

    skill = SalamandersBreathSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.cs.physical_attack)
    print(BARBARIAN_CHARACTER.to_attack(
        defender_char=BARBARIAN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BARBARIAN_CHARACTER.skill_tree.learn_skill(SalamandersBreathSkill)

    skill = SweepingRocSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.cs.physical_attack)
    print(BARBARIAN_CHARACTER.to_attack(
        defender_char=BARBARIAN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BARBARIAN_CHARACTER.skill_tree.learn_skill(SweepingRocSkill)

    skill = HydraFangsSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.cs.physical_attack)
    print(BARBARIAN_CHARACTER.to_attack(
        defender_char=BARBARIAN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BARBARIAN_CHARACTER.skill_tree.learn_skill(HydraFangsSkill)

    skill = RaijusFootstepsSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.bs.strength)
    print(BARBARIAN_CHARACTER.cs.hit)
    print(BARBARIAN_CHARACTER.cs.evasion)
    print(skill.function())
    print(BARBARIAN_CHARACTER.cs.hit)
    print(BARBARIAN_CHARACTER.cs.evasion)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(RaijusFootstepsSkill)

    skill = FafnirsScalesSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.bs.strength)
    print(BARBARIAN_CHARACTER.cs.irate_hp)
    print(BARBARIAN_CHARACTER.cs.physical_defense)
    print(skill.function())
    print(BARBARIAN_CHARACTER.cs.physical_defense)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(FafnirsScalesSkill)
