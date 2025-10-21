
from typing import TYPE_CHECKING
from rpgram.constants.text import (
    HIT_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import CURSED_DEBUFFS_NAMES, get_debuffs_emoji_text
from rpgram.enums.race import MALEGNE_RACES
from rpgram.enums.skill import (
    PaladinSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class ExcaliburSkill(BaseSkill):
    NAME = PaladinSkillEnum.EXCALIBUR.value
    DESCRIPTION = (
        'Transmuta a própria arma na *Épica '
        f'{PaladinSkillEnum.EXCALIBUR.value}* '
        'e desfere um ataque poderoso, '
        'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}*, de '
        f'*{get_damage_emoji_text(DamageEnum.ROCK)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.PALADIN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.25,
        }
        damage_types = [
            DamageEnum.BLESSING,
            DamageEnum.ROCK,
            DamageEnum.SLASHING,
        ]

        super().__init__(
            name=ExcaliburSkill.NAME,
            description=ExcaliburSkill.DESCRIPTION,
            rank=ExcaliburSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=ExcaliburSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class KusanagiNoTsurugiSkill(BaseSkill):
    NAME = PaladinSkillEnum.KUSANAGI_NO_TSURUGI.value
    DESCRIPTION = (
        'Transmuta a própria arma na *Lendária '
        f'{PaladinSkillEnum.KUSANAGI_NO_TSURUGI.value}* '
        'e desfere um ataque devastador, '
        'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}*, de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}*, de '
        f'*{get_damage_emoji_text(DamageEnum.WIND)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.PALADIN.value,
        'skill_list': [ExcaliburSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.50,
        }
        damage_types = [
            DamageEnum.BLESSING,
            DamageEnum.FIRE,
            DamageEnum.WIND,
            DamageEnum.SLASHING,
        ]

        super().__init__(
            name=KusanagiNoTsurugiSkill.NAME,
            description=KusanagiNoTsurugiSkill.DESCRIPTION,
            rank=KusanagiNoTsurugiSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=KusanagiNoTsurugiSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class TyrfingSkill(BaseSkill):
    NAME = PaladinSkillEnum.TYRFING.value
    DESCRIPTION = (
        'Transmuta a própria arma na *Mítica '
        f'{PaladinSkillEnum.TYRFING.value}* '
        'e desfere um ataque implacável, '
        'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}*, de '
        f'*{get_damage_emoji_text(DamageEnum.LIGHT)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (625% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.PALADIN.value,
        'skill_list': [ExcaliburSkill.NAME, KusanagiNoTsurugiSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 6.25,
        }
        damage_types = [
            DamageEnum.BLESSING,
            DamageEnum.LIGHT,
            DamageEnum.SLASHING,
        ]

        super().__init__(
            name=TyrfingSkill.NAME,
            description=TyrfingSkill.DESCRIPTION,
            rank=TyrfingSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=TyrfingSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.50


class OsheSkill(BaseSkill):
    NAME = PaladinSkillEnum.OSHE.value
    DESCRIPTION = (
        'Transmuta a própria arma no *Épico '
        f'{PaladinSkillEnum.OSHE.value}* '
        'e desfere um ataque energético, '
        'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}*, de '
        f'*{get_damage_emoji_text(DamageEnum.LIGHTNING)}*, de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.PALADIN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.25,
        }
        damage_types = [
            DamageEnum.BLESSING,
            DamageEnum.LIGHTNING,
            DamageEnum.FIRE,
            DamageEnum.SLASHING,
        ]

        super().__init__(
            name=OsheSkill.NAME,
            description=OsheSkill.DESCRIPTION,
            rank=OsheSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=OsheSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class SudarshanaChakraSkill(BaseSkill):
    NAME = PaladinSkillEnum.SUDARSHANA_CHAKRA.value
    DESCRIPTION = (
        'Transmuta a própria arma na *Lendária '
        f'{PaladinSkillEnum.SUDARSHANA_CHAKRA.value}* '
        'e a atira contra o oponente de maneira destroçadora, '
        'ignorando suas defesas e '
        'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (50% + 5% x Rank x Nível). '
        'O dano é decuplicado se o alvo for uma *Criatura Malégna* '
        f'({", ".join(r.title() for r in MALEGNE_RACES)}) ou se estiver '
        'com uma *Condição Amaldiçoante* '
        f'({get_debuffs_emoji_text(*CURSED_DEBUFFS_NAMES)}), '
        'além disso, cura todas as *Condições Amaldiçoantes*.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.PALADIN.value,
        'skill_list': [OsheSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 0.50,
        }
        damage_types = [
            DamageEnum.BLESSING,
            DamageEnum.SLASHING,
        ]

        super().__init__(
            name=SudarshanaChakraSkill.NAME,
            description=SudarshanaChakraSkill.DESCRIPTION,
            rank=SudarshanaChakraSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.TRUE,
            char=char,
            use_equips_damage_types=True,
            requirements=SudarshanaChakraSkill.REQUIREMENTS,
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

        if target.is_alive and target.is_malegne:
            purge_damage = int(total_damage * 9)
            damage_report = target.cs.damage_hit_points(
                value=purge_damage,
                markdown=True,
            )
            report['text'] = damage_report['text']
            for condition_name in CURSED_DEBUFFS_NAMES:
                status_report = target.status.cure_condition(condition_name)
                if not status_report['is_fail']:
                    report['text'] += "\n" + status_report['text']

        return report


class GungnirSkill(BaseSkill):
    NAME = PaladinSkillEnum.GUNGNIR.value
    DESCRIPTION = (
        'Transmuta a própria arma na *Mítica '
        f'{PaladinSkillEnum.GUNGNIR.value}* '
        'e a arremessa de maneira inerrável, '
        'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}*, '
        f'*{get_damage_emoji_text(DamageEnum.MAGIC)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível). '
        'Essa habilidade não pode ser esquivada.'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.PALADIN.value,
        'skill_list': [OsheSkill.NAME, SudarshanaChakraSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.25,
        }
        damage_types = [
            DamageEnum.BLESSING,
            DamageEnum.MAGIC,
            DamageEnum.PIERCING,
        ]

        super().__init__(
            name=GungnirSkill.NAME,
            description=GungnirSkill.DESCRIPTION,
            rank=GungnirSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            is_elusive=True,
            use_equips_damage_types=True,
            requirements=GungnirSkill.REQUIREMENTS,
            damage_types=damage_types
        )


SKILL_WAY_DESCRIPTION = {
    'name': 'Armeiro dos Deuses',
    'description': (
        'Um Paladino que transcende a mera luta física. '
        'Ele é um artesão sagrado, forjando, brevemente, '
        'suas armas em armas divinas. '
        'Sua fé se manifesta em cada golpe, imbuindo suas criações com '
        'poder sagrado. '
        'Ele não apenas luta, mas também cria, '
        'moldando o metal em ferramentas de Punição Sagrada.'
    ),
    'skill_list': [
        ExcaliburSkill,
        KusanagiNoTsurugiSkill,
        TyrfingSkill,
        OsheSkill,
        SudarshanaChakraSkill,
        GungnirSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import PALADIN_CHARACTER

    skill = ExcaliburSkill(PALADIN_CHARACTER)
    print(skill)
    print(PALADIN_CHARACTER.cs.physical_attack)
    print(PALADIN_CHARACTER.to_attack(
        defender_char=PALADIN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    PALADIN_CHARACTER.skill_tree.learn_skill(ExcaliburSkill)

    skill = KusanagiNoTsurugiSkill(PALADIN_CHARACTER)
    print(skill)
    print(PALADIN_CHARACTER.cs.physical_attack)
    print(PALADIN_CHARACTER.to_attack(
        defender_char=PALADIN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    PALADIN_CHARACTER.skill_tree.learn_skill(KusanagiNoTsurugiSkill)

    skill = TyrfingSkill(PALADIN_CHARACTER)
    print(skill)
    print(PALADIN_CHARACTER.cs.physical_attack)
    print(PALADIN_CHARACTER.to_attack(
        defender_char=PALADIN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    PALADIN_CHARACTER.skill_tree.learn_skill(TyrfingSkill)

    skill = OsheSkill(PALADIN_CHARACTER)
    print(skill)
    print(PALADIN_CHARACTER.cs.physical_attack)
    print(PALADIN_CHARACTER.to_attack(
        defender_char=PALADIN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    PALADIN_CHARACTER.skill_tree.learn_skill(OsheSkill)

    skill = SudarshanaChakraSkill(PALADIN_CHARACTER)
    print(skill)
    print(PALADIN_CHARACTER.cs.physical_attack)
    print(PALADIN_CHARACTER.to_attack(
        defender_char=PALADIN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    PALADIN_CHARACTER.skill_tree.learn_skill(SudarshanaChakraSkill)

    skill = GungnirSkill(PALADIN_CHARACTER)
    print(skill)
    print(PALADIN_CHARACTER.cs.physical_attack)
    print(PALADIN_CHARACTER.to_attack(
        defender_char=PALADIN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    PALADIN_CHARACTER.skill_tree.learn_skill(GungnirSkill)

    print('\n'.join([
        report['text']
        for report in PALADIN_CHARACTER.activate_status()
    ]))
