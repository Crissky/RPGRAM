from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.debuff import StunnedCondition
from rpgram.conditions.self_skill import ChampionInspirationCondition
from rpgram.conditions.target_skill_buff import LeadershipCondition
from rpgram.constants.text import (
    CHARISMA_EMOJI_TEXT,
    DEXTERITY_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.skill import (
    KnightSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class ChargeSkill(BaseSkill):
    NAME = KnightSkillEnum.CHARGE.value
    DESCRIPTION = (
        'Impulsiona-se sobre o inimigo com *Grande Velocidade*, '
        'tornando-se uma força imparável no campo de batalha e '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* e '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (200% + 5% x Rank x Nível). '
        f'Essa habilidade possui baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.KNIGHT.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 2.00,
        }
        damage_types = [
            DamageEnum.BLUDGEONING,
            DamageEnum.PIERCING,
        ]

        super().__init__(
            name=ChargeSkill.NAME,
            description=ChargeSkill.DESCRIPTION,
            rank=ChargeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=ChargeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.75


class HeavyChargeSkill(BaseSkill):
    NAME = KnightSkillEnum.HEAVY_CHARGE.value
    DESCRIPTION = (
        'Impulsiona-se sobre o inimigo com *Força Devastadora*, '
        'tornando-se uma força incontível no campo de batalha e '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* e '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (300% + 5% x Rank x Nível). '
        f'Essa habilidade possui baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.KNIGHT.value,
        'skill_list': [ChargeSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 3.00,
        }
        damage_types = [
            DamageEnum.BLUDGEONING,
            DamageEnum.PIERCING,
        ]

        super().__init__(
            name=HeavyChargeSkill.NAME,
            description=HeavyChargeSkill.DESCRIPTION,
            rank=HeavyChargeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=HeavyChargeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.75


class SuperChargeSkill(BaseSkill):
    NAME = KnightSkillEnum.SUPER_CHARGE.value
    DESCRIPTION = (
        'Impulsiona-se sobre o inimigo com *Ímpeto Inimaginável*, '
        'tornando-se uma força irrefreável no campo de batalha, '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* e '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (400% + 5% x Rank x Nível) e '
        'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.STUNNED)}* com nível igual ao '
        '(Rank x Nível). '
        f'Essa habilidade possui baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.KNIGHT.value,
        'skill_list': [ChargeSkill.NAME, HeavyChargeSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 4.00,
        }
        damage_types = [
            DamageEnum.BLUDGEONING,
            DamageEnum.PIERCING,
        ]

        super().__init__(
            name=SuperChargeSkill.NAME,
            description=SuperChargeSkill.DESCRIPTION,
            rank=SuperChargeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=SuperChargeSkill.REQUIREMENTS,
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
            stunned_condition = StunnedCondition(level=level)
            status_report = target.status.add_condition(stunned_condition)
            report['status_text'] = status_report['text']

        return report

    @property
    def hit_multiplier(self) -> float:
        return 0.75


class ChampionInspirationSkill(BaseSkill):
    NAME = KnightSkillEnum.CHAMPION_INSPIRATION.value
    DESCRIPTION = (
        'Libera uma *Explosão de Energia Inspiradora* que '
        'fortalece o seu espírito, '
        'aumentando o '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* e '
        f'*{HIT_EMOJI_TEXT}* com base no '
        f'*{DEXTERITY_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.KNIGHT.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=ChampionInspirationSkill.NAME,
            description=ChampionInspirationSkill.DESCRIPTION,
            rank=ChampionInspirationSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=ChampionInspirationSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = ChampionInspirationCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* liberou uma '
                '*Explosão de Energia Inspiradora*, '
                'aumentando o seu '
                f'*{PRECISION_ATTACK_EMOJI_TEXT}* '
                f'em {condition.bonus_precision_attack} pontos e '
                f'*{HIT_EMOJI_TEXT}* '
                f'em {condition.bonus_hit} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class LeadershipSkill(BaseSkill):
    NAME = KnightSkillEnum.LEADERSHIP.value
    DESCRIPTION = (
        'Usa a própria *Força* e *Determinação* para despertar o seu '
        '*Espírito de Liderança* e conceder à equipe '
        'uma inspiração de combate que aumenta o '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*, '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}*, '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* e '
        f'*{HIT_EMOJI_TEXT}* com base na '
        f'*{DEXTERITY_EMOJI_TEXT}* (100% + 10% x Rank x Nível) e '
        f'*{CHARISMA_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.KNIGHT.value,
        'skill_list': [ChampionInspirationSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=LeadershipSkill.NAME,
            description=LeadershipSkill.DESCRIPTION,
            rank=LeadershipSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=LeadershipSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            power = int(self.char.bs.dexterity + self.char.bs.charisma)
            level = self.level_rank
            condition = LeadershipCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* recebe a *Inspiração do Líder* '
                    'aumentando o '
                    f'{PHYSICAL_ATTACK_EMOJI_TEXT}, '
                    f'{PRECISION_ATTACK_EMOJI_TEXT}, '
                    f'{MAGICAL_ATTACK_EMOJI_TEXT} e '
                    f'{HIT_EMOJI_TEXT} em '
                    f'*{condition.power}* pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Campeão',
    'description': (
        'O Campeão é um símbolo de esperança, '
        'um defensor dos fracos e da justiça. '
        'Sua força e habilidade com armas são lendárias, '
        'mas o seu espírito indomável e a sua devoção à causa '
        'são o que o definem. '
        'O Campeão é um líder nato, '
        'capaz de inspirar seus aliados e derrotar seus inimigos.'
    ),
    'skill_list': [
        ChargeSkill,
        HeavyChargeSkill,
        SuperChargeSkill,
        ChampionInspirationSkill,
        LeadershipSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import KNIGHT_CHARACTER

    skill = ChargeSkill(KNIGHT_CHARACTER)
    print(skill)
    print(KNIGHT_CHARACTER.cs.precision_attack)
    print(KNIGHT_CHARACTER.to_attack(
        defender_char=KNIGHT_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    KNIGHT_CHARACTER.skill_tree.learn_skill(ChargeSkill)

    skill = HeavyChargeSkill(KNIGHT_CHARACTER)
    print(skill)
    print(KNIGHT_CHARACTER.cs.precision_attack)
    print(KNIGHT_CHARACTER.to_attack(
        defender_char=KNIGHT_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    KNIGHT_CHARACTER.skill_tree.learn_skill(HeavyChargeSkill)

    skill = SuperChargeSkill(KNIGHT_CHARACTER)
    print(skill)
    print(KNIGHT_CHARACTER.cs.precision_attack)
    print(KNIGHT_CHARACTER.to_attack(
        defender_char=KNIGHT_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    KNIGHT_CHARACTER.skill_tree.learn_skill(SuperChargeSkill)

    skill = ChampionInspirationSkill(KNIGHT_CHARACTER)
    print(skill)
    print(KNIGHT_CHARACTER.bs.dexterity)
    print(KNIGHT_CHARACTER.cs.precision_attack, KNIGHT_CHARACTER.cs.hit)
    print(skill.function())
    print(KNIGHT_CHARACTER.cs.precision_attack, KNIGHT_CHARACTER.cs.hit)
    KNIGHT_CHARACTER.skill_tree.learn_skill(ChampionInspirationSkill)

    skill = LeadershipSkill(KNIGHT_CHARACTER)
    print(skill)
    print(KNIGHT_CHARACTER.bs.dexterity, KNIGHT_CHARACTER.bs.charisma)
    print(KNIGHT_CHARACTER.cs.precision_attack, KNIGHT_CHARACTER.cs.hit)
    print(skill.function(KNIGHT_CHARACTER))
    print(KNIGHT_CHARACTER.cs.precision_attack, KNIGHT_CHARACTER.cs.hit)
    KNIGHT_CHARACTER.skill_tree.learn_skill(LeadershipSkill)

    print('\n'.join([
        report['text']
        for report in KNIGHT_CHARACTER.activate_status()
    ]))
