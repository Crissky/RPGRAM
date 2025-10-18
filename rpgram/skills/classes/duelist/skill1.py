from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.target_skill_buff import AgileFeetCondition, EagleEyeCondition
from rpgram.constants.text import (
    DEXTERITY_EMOJI_TEXT,
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    DuelistSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.classes.multiclasse.precision_attack import QuickAttackSkill
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class WindBladeSkill(BaseSkill):
    NAME = DuelistSkillEnum.WIND_BLADE.value
    DESCRIPTION = (
        'Brande a arma com um único movimento rápido e imprevisível, '
        'cortando o ar violentamente e '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.WIND)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível). '
        f'Essa habilidade possui *{HIT_EMOJI_TEXT}* acima do normal.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.DUELIST.value,
        'skill_list': [QuickAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.00
        }
        damage_types = [DamageEnum.WIND]

        super().__init__(
            name=WindBladeSkill.NAME,
            description=WindBladeSkill.DESCRIPTION,
            rank=WindBladeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=WindBladeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 1.50


class SplashFountSkill(BaseSkill):
    NAME = DuelistSkillEnum.SPLASH_FOUNT.value
    DESCRIPTION = (
        'Saca a arma com celeridade e desfere múltiplos ataques rápidos, '
        'causando dano com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível). '
        'Pode acertar o alvo diversas até 5 vezes '
        '(cada acerto subsequente causa metade do dano).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.DUELIST.value,
        'skill_list': [QuickAttackSkill.NAME, WindBladeSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.25
        }
        damage_types = None

        super().__init__(
            name=SplashFountSkill.NAME,
            description=SplashFountSkill.DESCRIPTION,
            rank=SplashFountSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=SplashFountSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        total_attacks = int(self.dice.value / 5)
        report_text_list = []
        for i in range(total_attacks):
            if target.is_dead:
                break

            total_damage = int(total_damage / 2)
            damage_report = target.cs.damage_hit_points(value=total_damage)
            report_text_list.append(
                f'Ataque {i+2:02}: ' + damage_report['text']
            )
        report['text'] = '\n'.join(report_text_list)

        return report


class AgileFeetSkill(BaseSkill):
    NAME = DuelistSkillEnum.AGILE_FEET.value
    DESCRIPTION = (
        'Com graça e agilidade, se torna um borrão de movimento, '
        'capaz de desviar de ataques com uma destreza impressionante, '
        'aumentando a '
        f'*{EVASION_EMOJI_TEXT}* com base na '
        f'*{DEXTERITY_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.DUELIST.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=AgileFeetSkill.NAME,
            description=AgileFeetSkill.DESCRIPTION,
            rank=AgileFeetSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=AgileFeetSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        char = self.char
        player_name = char.player_name
        power = char.cs.dexterity
        level = self.level_rank
        condition = AgileFeetCondition(power=power, level=level)
        report_list = char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* se torna um borrão de movimento, '
                'aumentando a '
                f'*{EVASION_EMOJI_TEXT}* '
                f'em {condition.bonus_evasion} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class EagleEyeSkill(BaseSkill):
    NAME = DuelistSkillEnum.EAGLE_EYE.value
    DESCRIPTION = (
        'Usa sua percepção aguçada para analisar a situação do combate '
        'com uma clareza excepcional, permitindo antecipar os movimentos '
        'do oponente para antecipar a sua reação, '
        'aumentando o '
        f'*{HIT_EMOJI_TEXT}* com base na '
        f'*{DEXTERITY_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.DUELIST.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=EagleEyeSkill.NAME,
            description=EagleEyeSkill.DESCRIPTION,
            rank=EagleEyeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=EagleEyeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        char = self.char
        player_name = char.player_name
        power = char.cs.dexterity
        level = self.level_rank
        condition = EagleEyeCondition(power=power, level=level)
        report_list = char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* amplifica a sua capacidade de analisar '
                'o combate, '
                'aumentando o '
                f'*{HIT_EMOJI_TEXT}* '
                f'em {condition.bonus_hit} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class LungeSkill(BaseSkill):
    NAME = DuelistSkillEnum.LUNGE.value
    DESCRIPTION = (
        'Concentra toda a sua força e '
        'executa um único ataque direto e conciso, '
        'visando um ponto vital do oponente, '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.DUELIST.value,
        'skill_list': [AgileFeetSkill.NAME, EagleEyeSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.50
        }
        damage_types = [DamageEnum.PIERCING]

        super().__init__(
            name=LungeSkill.NAME,
            description=LungeSkill.DESCRIPTION,
            rank=LungeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=LungeSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class TranspassSkill(BaseSkill):
    NAME = DuelistSkillEnum.TRANSPASS.value
    DESCRIPTION = (
        'Avança contra o oponente, superando as suas defesas e '
        'atingindo-o em seus pontos mais vulneráveis com um '
        'golpe preciso e poderoso, '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (75% + 5% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.DUELIST.value,
        'skill_list': [
            AgileFeetSkill.NAME,
            EagleEyeSkill.NAME,
            LungeSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 0.75
        }
        damage_types = [DamageEnum.PIERCING]

        super().__init__(
            name=TranspassSkill.NAME,
            description=TranspassSkill.DESCRIPTION,
            rank=TranspassSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.TRUE,
            char=char,
            use_equips_damage_types=True,
            requirements=TranspassSkill.REQUIREMENTS,
            damage_types=damage_types
        )


SKILL_WAY_DESCRIPTION = {
    'name': 'Dança da Morte',
    'description': (
        'O Dança da Morte é um duelista que transformou a arte da luta '
        'em uma dança macabra. '
        'Sua habilidade reside em prever os movimentos de seus '
        'inimigos e contra-atacar com precisão mortal. '
        'Ele é um mestre da esgrima, capaz de executar manobras acrobáticas e '
        'golpes fulminantes que deixam seus oponentes perplexos.'
    ),
    'skill_list': [
        QuickAttackSkill,
        WindBladeSkill,
        SplashFountSkill,
        AgileFeetSkill,
        EagleEyeSkill,
        LungeSkill,
        TranspassSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import DUELIST_CHARACTER

    skill = QuickAttackSkill(DUELIST_CHARACTER)
    print(skill)
    print(DUELIST_CHARACTER.cs.precision_attack)
    print(DUELIST_CHARACTER.to_attack(
        defender_char=DUELIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    DUELIST_CHARACTER.skill_tree.learn_skill(QuickAttackSkill)

    skill = WindBladeSkill(DUELIST_CHARACTER)
    print(skill)
    print(DUELIST_CHARACTER.cs.precision_attack)
    print(DUELIST_CHARACTER.to_attack(
        defender_char=DUELIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    DUELIST_CHARACTER.skill_tree.learn_skill(WindBladeSkill)

    skill = SplashFountSkill(DUELIST_CHARACTER)
    print(skill)
    print(DUELIST_CHARACTER.cs.precision_attack)
    print(DUELIST_CHARACTER.to_attack(
        defender_char=DUELIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    DUELIST_CHARACTER.skill_tree.learn_skill(SplashFountSkill)

    skill = AgileFeetSkill(DUELIST_CHARACTER)
    print(skill)
    print(DUELIST_CHARACTER.cs.dexterity, DUELIST_CHARACTER.cs.evasion)
    print(skill.function())
    print(DUELIST_CHARACTER.cs.dexterity, DUELIST_CHARACTER.cs.evasion)
    DUELIST_CHARACTER.skill_tree.learn_skill(AgileFeetSkill)

    skill = EagleEyeSkill(DUELIST_CHARACTER)
    print(skill)
    print(DUELIST_CHARACTER.cs.dexterity, DUELIST_CHARACTER.cs.hit)
    print(skill.function())
    print(DUELIST_CHARACTER.cs.dexterity, DUELIST_CHARACTER.cs.hit)
    DUELIST_CHARACTER.skill_tree.learn_skill(EagleEyeSkill)

    skill = LungeSkill(DUELIST_CHARACTER)
    print(skill)
    print(DUELIST_CHARACTER.cs.precision_attack)
    print(DUELIST_CHARACTER.to_attack(
        defender_char=DUELIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    DUELIST_CHARACTER.skill_tree.learn_skill(LungeSkill)

    skill = TranspassSkill(DUELIST_CHARACTER)
    print(skill)
    print(DUELIST_CHARACTER.cs.precision_attack)
    print(DUELIST_CHARACTER.to_attack(
        defender_char=DUELIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    DUELIST_CHARACTER.skill_tree.learn_skill(TranspassSkill)
