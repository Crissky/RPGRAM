from typing import TYPE_CHECKING
from rpgram.constants.text import (
    HIT_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum,
    WeaponMasterSkillEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class SlashingAttackSkill(BaseSkill):
    NAME = WeaponMasterSkillEnum.SLASHING_ATTACK.value
    DESCRIPTION = (
        f'Com um movimento preciso, inflige múltiplos golpes rápidos, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível). '
        f'Essa habilidade possui *{HIT_EMOJI_TEXT}* acima do normal.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.WEAPON_MASTER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.00,
        }
        damage_types = [DamageEnum.SLASHING]

        super().__init__(
            name=SlashingAttackSkill.NAME,
            description=SlashingAttackSkill.DESCRIPTION,
            rank=SlashingAttackSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=SlashingAttackSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 1.25


class SonicBladeSkill(BaseSkill):
    NAME = WeaponMasterSkillEnum.SONIC_BLADE.value
    DESCRIPTION = (
        f'Canaliza energia através de sua arma, criando uma *Onda de Choque* '
        f'poderosas que corta o ar e dilacera a carne do oponente, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* e '
        f'*{get_damage_emoji_text(DamageEnum.SONIC)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível). '
        f'Essa habilidade possui *{HIT_EMOJI_TEXT}* acima do normal.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.WEAPON_MASTER.value,
        'skill_list': [SlashingAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.00,
        }
        damage_types = [DamageEnum.SLASHING, DamageEnum.SONIC]

        super().__init__(
            name=SonicBladeSkill.NAME,
            description=SonicBladeSkill.DESCRIPTION,
            rank=SonicBladeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=SonicBladeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 1.50


class VorpalBladeAttackSkill(BaseSkill):
    NAME = WeaponMasterSkillEnum.VORPAL_BLADE_ATTACK.value
    DESCRIPTION = (
        f'Desfere um golpe único e poderoso, direcionado à cabeça do inimigo, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}*, '
        f'*{get_damage_emoji_text(DamageEnum.SONIC)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.WIND)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível), '
        f'matando o oponente se for *Acerto Crítico*{EmojiEnum.DICE.value}. '
        f'Essa habilidade possui *{HIT_EMOJI_TEXT}* acima do normal.'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.WEAPON_MASTER.value,
        'skill_list': [SlashingAttackSkill.NAME, SonicBladeSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.25,
        }
        damage_types = [
            DamageEnum.SLASHING,
            DamageEnum.SONIC,
            DamageEnum.WIND
        ]

        super().__init__(
            name=VorpalBladeAttackSkill.NAME,
            description=VorpalBladeAttackSkill.DESCRIPTION,
            rank=VorpalBladeAttackSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=VorpalBladeAttackSkill.REQUIREMENTS,
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
            extra_damage = target.cs.hit_points
            damage_report = target.cs.damage_hit_points(
                value=extra_damage,
                ignore_barrier=True
            )
            report['text'] = damage_report['text']

        return report

    @property
    def hit_multiplier(self) -> float:
        return 1.50


class BruisingAttackSkill(BaseSkill):
    NAME = WeaponMasterSkillEnum.BRUISING_ATTACK.value
    DESCRIPTION = (
        f'Concentra toda a sua força em um único golpe devastador, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (200% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.WEAPON_MASTER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 2.00,
        }
        damage_types = [DamageEnum.BLUDGEONING]

        super().__init__(
            name=BruisingAttackSkill.NAME,
            description=BruisingAttackSkill.DESCRIPTION,
            rank=BruisingAttackSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=BruisingAttackSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.75


class CrystallineClashSkill(BaseSkill):
    NAME = WeaponMasterSkillEnum.CRYSTALLINE_CLASH.value
    DESCRIPTION = (
        f'Canaliza *Energia Cristalina* e desfere um golpe que, '
        f'ao impactar o inimigo, libera uma explosão de cristais, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.CRYSTAL)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (300% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.WEAPON_MASTER.value,
        'skill_list': [BruisingAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 3.00,
        }
        damage_types = [DamageEnum.BLUDGEONING, DamageEnum.CRYSTAL]

        super().__init__(
            name=CrystallineClashSkill.NAME,
            description=CrystallineClashSkill.DESCRIPTION,
            rank=CrystallineClashSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=CrystallineClashSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.75


class GeocrusherAttackSkill(BaseSkill):
    NAME = WeaponMasterSkillEnum.GEOCRUSHER_ATTACK.value
    DESCRIPTION = (
        f'Concentra sua força ao canalizar a energia do solo, '
        f'imbuindo sua(s) arma(s) com o poder dos minerais, '
        f'atingindo seu alvo com força esmagadora, '
        f'destruindo qualquer barreira antes de '
        f'causar dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}*, de '
        f'*{get_damage_emoji_text(DamageEnum.CRYSTAL)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.ROCK)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (350% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.WEAPON_MASTER.value,
        'skill_list': [BruisingAttackSkill.NAME, CrystallineClashSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 3.50,
        }
        damage_types = [
            DamageEnum.BLUDGEONING,
            DamageEnum.CRYSTAL,
            DamageEnum.ROCK,
        ]

        super().__init__(
            name=GeocrusherAttackSkill.NAME,
            description=GeocrusherAttackSkill.DESCRIPTION,
            rank=GeocrusherAttackSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=GeocrusherAttackSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def pre_hit_function(self, target: 'BaseCharacter') -> dict:
        report = {'text': ''}
        status_report = target.status.broken_all_barriers()
        if status_report['text']:
            report['text'] = status_report["text"]

        return report

    @property
    def hit_multiplier(self) -> float:
        return 0.75


class TerrebrantAttackSkill(BaseSkill):
    NAME = WeaponMasterSkillEnum.TERREBRANT_ATTACK.value
    DESCRIPTION = (
        f'Desfere uma série de golpes direcionados aos '
        f'pontos vitais do inimigo, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.WEAPON_MASTER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.PIERCING]

        super().__init__(
            name=TerrebrantAttackSkill.NAME,
            description=TerrebrantAttackSkill.DESCRIPTION,
            rank=TerrebrantAttackSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=TerrebrantAttackSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class ThunderpassSkill(BaseSkill):
    NAME = WeaponMasterSkillEnum.THUNDERPASS.value
    DESCRIPTION = (
        f'Canaliza *Energia do Trovão* através de sua arma e '
        f'desfecha um golpe que libera uma descarga elétrica, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.LIGHTNING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.WEAPON_MASTER.value,
        'skill_list': [TerrebrantAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.PIERCING, DamageEnum.LIGHTNING]

        super().__init__(
            name=ThunderpassSkill.NAME,
            description=ThunderpassSkill.DESCRIPTION,
            rank=ThunderpassSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=ThunderpassSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class StormDanceSkill(BaseSkill):
    NAME = WeaponMasterSkillEnum.STORM_DANCE.value
    DESCRIPTION = (
        f'Percorrer rapidamente todos os inimigos como um ricochete, '
        f'transfixando-os '
        f'com o *Poder da Tempestade*, eletroerosando as suas armaduras - '
        f'ignorando as defesas dos oponentes e '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}*, de '
        f'*{get_damage_emoji_text(DamageEnum.LIGHTNING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.WATER)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (50% + 2.5% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.WEAPON_MASTER.value,
        'skill_list': [TerrebrantAttackSkill.NAME, ThunderpassSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 0.50,
        }
        damage_types = [
            DamageEnum.PIERCING,
            DamageEnum.LIGHTNING,
            DamageEnum.WATER,
        ]

        super().__init__(
            name=StormDanceSkill.NAME,
            description=StormDanceSkill.DESCRIPTION,
            rank=StormDanceSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.TRUE,
            char=char,
            use_equips_damage_types=True,
            requirements=StormDanceSkill.REQUIREMENTS,
            damage_types=damage_types
        )


SKILL_WAY_DESCRIPTION = {
    'name': 'Maestria',
    'description': (
        'Domina o combate com uma variedade de armas, '
        'estendendo-as como parte de si mesmo, '
        'a ponto de conseguir causar Tipos de Dano incompatíveis '
        'com o tipo de arma que está portando. '
        'Cada golpe, cada movimento, '
        'é uma expressão de sua arte e de sua alma.'
    ),
    'skill_list': [
        SlashingAttackSkill,
        SonicBladeSkill,
        VorpalBladeAttackSkill,
        BruisingAttackSkill,
        CrystallineClashSkill,
        GeocrusherAttackSkill,
        TerrebrantAttackSkill,
        ThunderpassSkill,
        StormDanceSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import WEAPON_MASTER_CHARACTER
    from rpgram.conditions.barrier import GuardianShieldCondition

    skill = SlashingAttackSkill(WEAPON_MASTER_CHARACTER)
    print(skill)
    print(WEAPON_MASTER_CHARACTER.cs.physical_attack)
    print(WEAPON_MASTER_CHARACTER.to_attack(
        defender_char=WEAPON_MASTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    WEAPON_MASTER_CHARACTER.skill_tree.learn_skill(SlashingAttackSkill)

    WEAPON_MASTER_CHARACTER.cs.cure_hit_points(20_000)
    skill = BruisingAttackSkill(WEAPON_MASTER_CHARACTER)
    print(skill)
    print(WEAPON_MASTER_CHARACTER.cs.physical_attack)
    print(WEAPON_MASTER_CHARACTER.to_attack(
        defender_char=WEAPON_MASTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    WEAPON_MASTER_CHARACTER.skill_tree.learn_skill(BruisingAttackSkill)

    WEAPON_MASTER_CHARACTER.cs.cure_hit_points(20_000)
    skill = TerrebrantAttackSkill(WEAPON_MASTER_CHARACTER)
    print(skill)
    print(WEAPON_MASTER_CHARACTER.cs.physical_attack)
    print(WEAPON_MASTER_CHARACTER.to_attack(
        defender_char=WEAPON_MASTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    WEAPON_MASTER_CHARACTER.skill_tree.learn_skill(TerrebrantAttackSkill)

    WEAPON_MASTER_CHARACTER.cs.cure_hit_points(20_000)
    skill = SonicBladeSkill(WEAPON_MASTER_CHARACTER)
    print(skill)
    print(WEAPON_MASTER_CHARACTER.cs.physical_attack)
    print(WEAPON_MASTER_CHARACTER.to_attack(
        defender_char=WEAPON_MASTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    WEAPON_MASTER_CHARACTER.skill_tree.learn_skill(SonicBladeSkill)

    WEAPON_MASTER_CHARACTER.cs.cure_hit_points(20_000)
    skill = CrystallineClashSkill(WEAPON_MASTER_CHARACTER)
    print(skill)
    print(WEAPON_MASTER_CHARACTER.cs.physical_attack)
    print(WEAPON_MASTER_CHARACTER.to_attack(
        defender_char=WEAPON_MASTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    WEAPON_MASTER_CHARACTER.skill_tree.learn_skill(CrystallineClashSkill)

    WEAPON_MASTER_CHARACTER.cs.cure_hit_points(20_000)
    skill = ThunderpassSkill(WEAPON_MASTER_CHARACTER)
    print(skill)
    print(WEAPON_MASTER_CHARACTER.cs.physical_attack)
    print(WEAPON_MASTER_CHARACTER.to_attack(
        defender_char=WEAPON_MASTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    WEAPON_MASTER_CHARACTER.skill_tree.learn_skill(ThunderpassSkill)

    WEAPON_MASTER_CHARACTER.cs.cure_hit_points(20_000)
    skill = VorpalBladeAttackSkill(WEAPON_MASTER_CHARACTER)
    print(skill)
    print(WEAPON_MASTER_CHARACTER.cs.physical_attack)
    print(WEAPON_MASTER_CHARACTER.to_attack(
        defender_char=WEAPON_MASTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    WEAPON_MASTER_CHARACTER.skill_tree.learn_skill(VorpalBladeAttackSkill)

    barrier_condition = GuardianShieldCondition(power=50_000)
    WEAPON_MASTER_CHARACTER.status.add_condition(barrier_condition)
    WEAPON_MASTER_CHARACTER.cs.cure_hit_points(20_000)
    skill = GeocrusherAttackSkill(WEAPON_MASTER_CHARACTER)
    print(skill)
    print(WEAPON_MASTER_CHARACTER.cs.physical_attack)
    print(WEAPON_MASTER_CHARACTER.to_attack(
        defender_char=WEAPON_MASTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    WEAPON_MASTER_CHARACTER.skill_tree.learn_skill(GeocrusherAttackSkill)

    WEAPON_MASTER_CHARACTER.cs.cure_hit_points(20_000)
    skill = StormDanceSkill(WEAPON_MASTER_CHARACTER)
    print(skill)
    print(WEAPON_MASTER_CHARACTER.cs.physical_attack)
    print(WEAPON_MASTER_CHARACTER.to_attack(
        defender_char=WEAPON_MASTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    WEAPON_MASTER_CHARACTER.skill_tree.learn_skill(StormDanceSkill)
