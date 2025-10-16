from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.debuff import (
    BleedingCondition,
    ImprisonedCondition
)
from rpgram.conditions.self_skill import (
    InvestigationCondition,
    SharpFaroCondition
)
from rpgram.constants.text import (
    DEXTERITY_EMOJI_TEXT,
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    BountyHunterSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class StabSkill(BaseSkill):
    NAME = BountyHunterSkillEnum.STAB.value
    DESCRIPTION = (
        'Se aproxima do inimigo e com um movimento súbito, '
        'inflige um golpe mortal com sua arma, '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (200% + 5% x Rank x Nível) e '
        'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BLEEDING)}* com nível igual ao '
        '(Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BOUNTY_HUNTER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 2.00,
        }
        damage_types = [DamageEnum.PIERCING]

        super().__init__(
            name=StabSkill.NAME,
            description=StabSkill.DESCRIPTION,
            rank=StabSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=StabSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        if target.is_alive:
            level = self.level_rank
            bleeding_condition = BleedingCondition(level=level)
            status_report = target.status.add_condition(bleeding_condition)
            report['status_text'] = status_report['text']

        return report

    @property
    def hit_multiplier(self) -> float:
        return 0.75


class QuickDrawSkill(BaseSkill):
    NAME = BountyHunterSkillEnum.QUICK_DRAW.value
    DESCRIPTION = (
        'Desenfunda sua arma com uma velocidade incrível, '
        'atacando contra o alvo antes que ele possa reagir, '
        'causando dano com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível). '
        f'Essa habilidade possui *{HIT_EMOJI_TEXT}* acima do normal.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BOUNTY_HUNTER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.00
        }
        damage_types = None

        super().__init__(
            name=QuickDrawSkill.NAME,
            description=QuickDrawSkill.DESCRIPTION,
            rank=QuickDrawSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=QuickDrawSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 1.25


class SurpriseAttackSkill(BaseSkill):
    NAME = BountyHunterSkillEnum.SURPRISE_ATTACK.value
    DESCRIPTION = (
        'Conhecendo o terreno como a palma de sua mão, '
        'embosca o inimigo e o ataca com um movimento rápido e silencioso, '
        'causando dano com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível), '
        f'dobrando o dano se for *Acerto Crítico*{EmojiEnum.DICE.value}. '
        f'Essa habilidade possui *{HIT_EMOJI_TEXT}* acima do normal.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BOUNTY_HUNTER.value,
        'skill_list': [QuickDrawSkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.00
        }
        damage_types = None

        super().__init__(
            name=SurpriseAttackSkill.NAME,
            description=SurpriseAttackSkill.DESCRIPTION,
            rank=SurpriseAttackSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=SurpriseAttackSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        if target.is_alive and self.dice.is_critical:
            damage_report = target.cs.damage_hit_points(value=total_damage)
            report['text'] = damage_report['text']

        return report

    @property
    def hit_multiplier(self) -> float:
        return 1.50


class HuntingNetSkill(BaseSkill):
    NAME = BountyHunterSkillEnum.HUNTING_NET.value
    DESCRIPTION = (
        'Lança sobre o oponente uma *Rede* feita de fios cortantes de metal, '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível) e '
        'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.IMPRISONED)}* com nível igual ao '
        f'(Rank x Nível) se for *Acerto Crítico*{EmojiEnum.DICE.value}.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BOUNTY_HUNTER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.SLASHING]

        super().__init__(
            name=HuntingNetSkill.NAME,
            description=HuntingNetSkill.DESCRIPTION,
            rank=HuntingNetSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=HuntingNetSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        if target.is_alive and self.dice.is_critical:
            level = self.level_rank
            imprisoned_condition = ImprisonedCondition(level=level)
            status_report = target.status.add_condition(imprisoned_condition)
            report['status_text'] = status_report['text']

        return report


class ChompTrapSkill(BaseSkill):
    NAME = BountyHunterSkillEnum.CHOMP_TRAP.value
    DESCRIPTION = (
        'Inspirada nas antigas armadilhas utilizadas para capturar '
        'grandes animais, '
        'lançar um dispositivo articular repleto de espinhos que '
        'causa dano de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível) e '
        'adiciona a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.IMPRISONED)}* e '
        f'*{get_debuff_emoji_text(DebuffEnum.BLEEDING)}* com nível igual ao '
        f'(Rank x Nível) se tirar 15{EmojiEnum.DICE.value} ou mais.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BOUNTY_HUNTER.value,
        'skill_list': [HuntingNetSkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.PIERCING]

        super().__init__(
            name=ChompTrapSkill.NAME,
            description=ChompTrapSkill.DESCRIPTION,
            rank=ChompTrapSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=ChompTrapSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        if target.is_alive and self.dice.value >= 15:
            level = self.level_rank
            imprisoned_condition = ImprisonedCondition(level=level)
            status_report = target.status.add_condition(imprisoned_condition)
            report['status_text'] = status_report['text']

            bleeding_condition = BleedingCondition(level=level)
            status_report = target.status.add_condition(bleeding_condition)
            report['status_text'] += '\n' + status_report['text']

        return report


class SharpFaroSkill(BaseSkill):
    NAME = BountyHunterSkillEnum.SHARP_FARO.value
    DESCRIPTION = (
        'Se conentra em usa o *Olfato Apurado* para rastrear os oponentes, '
        'aumentando o '
        f'*{HIT_EMOJI_TEXT}* com base na '
        f'*{DEXTERITY_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BOUNTY_HUNTER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=SharpFaroSkill.NAME,
            description=SharpFaroSkill.DESCRIPTION,
            rank=SharpFaroSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=SharpFaroSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = SharpFaroCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* se concentra em usa o seu *Olfato Apurado*, '
                'aumentando o '
                f'*{HIT_EMOJI_TEXT}* '
                f'em {condition.bonus_hit} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class InvestigationSkill(BaseSkill):
    NAME = BountyHunterSkillEnum.INVESTIGATION.value
    DESCRIPTION = (
        'Estuda os movimentos dos oponentes no *Campo de Batalha*, '
        'aumentando o '
        f'*{HIT_EMOJI_TEXT}* e a '
        f'*{EVASION_EMOJI_TEXT}* com base na '
        f'*{DEXTERITY_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BOUNTY_HUNTER.value,
        'skill_list': [SharpFaroSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=InvestigationSkill.NAME,
            description=InvestigationSkill.DESCRIPTION,
            rank=InvestigationSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=InvestigationSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = InvestigationCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* analisa o *Campo de Batalha*, '
                'aumentando o '
                f'*{HIT_EMOJI_TEXT}* '
                f'em {condition.bonus_hit} pontos e a '
                f'*{EVASION_EMOJI_TEXT}* '
                f'em {condition.bonus_evasion} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Predador',
    'description': (
        'O Predador personifica a natureza implacável da caçada. '
        'Sua expertise reside em perseguir e capturar (às vezes eliminar) '
        'seus alvos com a eficiência de um predador voraz. '
        'Ele é um mestre do rastreio, da emboscada, da camuflagem e do '
        'combate silencioso, capaz de desaparecer '
        'nas sombras e atacar sem aviso.'
    ),
    'skill_list': [
        StabSkill,
        QuickDrawSkill,
        SurpriseAttackSkill,
        HuntingNetSkill,
        ChompTrapSkill,
        SharpFaroSkill,
        InvestigationSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import BOUNTY_HUNTER_CHARACTER

    skill = StabSkill(BOUNTY_HUNTER_CHARACTER)
    print(skill)
    print(BOUNTY_HUNTER_CHARACTER.cs.physical_attack)
    print(BOUNTY_HUNTER_CHARACTER.to_attack(
        defender_char=BOUNTY_HUNTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BOUNTY_HUNTER_CHARACTER.skill_tree.learn_skill(StabSkill)

    skill = QuickDrawSkill(BOUNTY_HUNTER_CHARACTER)
    print(skill)
    print(BOUNTY_HUNTER_CHARACTER.cs.physical_attack)
    print(BOUNTY_HUNTER_CHARACTER.to_attack(
        defender_char=BOUNTY_HUNTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BOUNTY_HUNTER_CHARACTER.skill_tree.learn_skill(QuickDrawSkill)

    skill = SurpriseAttackSkill(BOUNTY_HUNTER_CHARACTER)
    print(skill)
    print(BOUNTY_HUNTER_CHARACTER.cs.physical_attack)
    print(BOUNTY_HUNTER_CHARACTER.to_attack(
        defender_char=BOUNTY_HUNTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BOUNTY_HUNTER_CHARACTER.skill_tree.learn_skill(SurpriseAttackSkill)

    skill = HuntingNetSkill(BOUNTY_HUNTER_CHARACTER)
    print(skill)
    print(BOUNTY_HUNTER_CHARACTER.cs.physical_attack)
    print(BOUNTY_HUNTER_CHARACTER.to_attack(
        defender_char=BOUNTY_HUNTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BOUNTY_HUNTER_CHARACTER.skill_tree.learn_skill(HuntingNetSkill)

    skill = ChompTrapSkill(BOUNTY_HUNTER_CHARACTER)
    print(skill)
    print(BOUNTY_HUNTER_CHARACTER.cs.physical_attack)
    print(BOUNTY_HUNTER_CHARACTER.to_attack(
        defender_char=BOUNTY_HUNTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BOUNTY_HUNTER_CHARACTER.skill_tree.learn_skill(ChompTrapSkill)

    skill = SharpFaroSkill(BOUNTY_HUNTER_CHARACTER)
    print(skill)
    print(BOUNTY_HUNTER_CHARACTER.cs.dexterity)
    print(BOUNTY_HUNTER_CHARACTER.cs.hit)
    print(skill.function())
    print(BOUNTY_HUNTER_CHARACTER.cs.hit)
    BOUNTY_HUNTER_CHARACTER.skill_tree.learn_skill(SharpFaroSkill)

    skill = InvestigationSkill(BOUNTY_HUNTER_CHARACTER)
    print(skill)
    print(BOUNTY_HUNTER_CHARACTER.cs.dexterity)
    print(BOUNTY_HUNTER_CHARACTER.cs.hit, BOUNTY_HUNTER_CHARACTER.cs.evasion)
    print(skill.function())
    print(BOUNTY_HUNTER_CHARACTER.cs.hit, BOUNTY_HUNTER_CHARACTER.cs.evasion)
    BOUNTY_HUNTER_CHARACTER.skill_tree.learn_skill(InvestigationSkill)
