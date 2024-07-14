from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.self_skill import RockArmorCondition
from rpgram.constants.text import (
    EVASION_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum
from rpgram.enums.skill import (
    MageSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class FireBallSkill(BaseSkill):
    NAME = MageSkillEnum.FIRE_BALL.value
    DESCRIPTION = (
        f'Com movimentos incisivos, conjura uma *Bola de Fogo* e a lança '
        f'contra um alvo, causando dano com base em '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.MAGE.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.FIRE]

        super().__init__(
            name=FireBallSkill.NAME,
            description=FireBallSkill.DESCRIPTION,
            rank=FireBallSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=FireBallSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class WaterBubbleSkill(BaseSkill):
    NAME = MageSkillEnum.WATER_BUBBLE.value
    DESCRIPTION = (
        f'Com movimentos suaves, conjura uma *Bolha de Água* e a lança '
        f'contra um alvo, causando dano com base em '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.MAGE.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.WATER]

        super().__init__(
            name=WaterBubbleSkill.NAME,
            description=WaterBubbleSkill.DESCRIPTION,
            rank=WaterBubbleSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=WaterBubbleSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class WindGustSkill(BaseSkill):
    NAME = MageSkillEnum.WIND_GUST.value
    DESCRIPTION = (
        f'Com movimentos undosos, conjura uma *Rajada de Vento* que vai de '
        f'encontro ao alvo, causando dano com base em '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.MAGE.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.WIND]

        super().__init__(
            name=WindGustSkill.NAME,
            description=WindGustSkill.DESCRIPTION,
            rank=WindGustSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=WindGustSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class EarthBreakSkill(BaseSkill):
    NAME = MageSkillEnum.EARTH_BREAK.value
    DESCRIPTION = (
        f'Com um movimento brusco, *Quebra-Terra* '
        f'debaixo de um alvo, causando dano com base em '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.MAGE.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.GROUND]

        super().__init__(
            name=EarthBreakSkill.NAME,
            description=EarthBreakSkill.DESCRIPTION,
            rank=EarthBreakSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=EarthBreakSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class MagicBlastSkill(BaseSkill):
    NAME = MageSkillEnum.MAGIC_BLAST.value
    DESCRIPTION = (
        f'Concentra energia em um ponto específico, resultando em uma '
        f'*Explosão Mágica* devastadora '
        f'que causa dano com base em '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.MAGE.value,
        'skill_list': [FireBallSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.BLAST, DamageEnum.MAGIC]

        super().__init__(
            name=MagicBlastSkill.NAME,
            description=MagicBlastSkill.DESCRIPTION,
            rank=MagicBlastSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=MagicBlastSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class IceShardSkill(BaseSkill):
    NAME = MageSkillEnum.ICE_SHARD.value
    DESCRIPTION = (
        f'Com um gesto rápido e preciso, conjura uma *Estaca Afiada '
        f'de Gelo Puro*, lançando-a em alta velocidade '
        f'em direção ao seu alvo, causando dano com base em '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.MAGE.value,
        'skill_list': [WaterBubbleSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.COLD, DamageEnum.PIERCING]

        super().__init__(
            name=IceShardSkill.NAME,
            description=IceShardSkill.DESCRIPTION,
            rank=IceShardSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=IceShardSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class FulminantLightningSkill(BaseSkill):
    NAME = MageSkillEnum.FULMINANT_LIGHTNING.value
    DESCRIPTION = (
        f'Canalisa na ponta dos dedos uma energia infrene '
        f'e dispara no alvo um *Raio Fulminante* '
        f'que causa dano com base em '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.MAGE.value,
        'skill_list': [WindGustSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.LIGHTNING, DamageEnum.LIGHTNING]

        super().__init__(
            name=FulminantLightningSkill.NAME,
            description=FulminantLightningSkill.DESCRIPTION,
            rank=FulminantLightningSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=FulminantLightningSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class RockArmorSkill(BaseSkill):
    NAME = MageSkillEnum.ROCK_ARMOR.value
    DESCRIPTION = (
        f'Assume uma posição defensiva e conjura uma pesada '
        f'*Armadura de Rocha* que aumenta a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* com base na redução de 25% da '
        f'*{EVASION_EMOJI_TEXT} BASE* '
        f'mais um bônus de (15% x Rank x Nível) do valor reduzido.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.MAGE.value,
        'skill_list': [EarthBreakSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=RockArmorSkill.NAME,
            description=RockArmorSkill.DESCRIPTION,
            rank=RockArmorSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=RockArmorSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = RockArmorCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* conjura uma *Armadura de Rocha*, '
                f'reduzindo a sua '
                f'*{EVASION_EMOJI_TEXT}* em favor de aumentar a sua '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}*.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


if __name__ == '__main__':
    from rpgram.constants.test import MAGE_CHARACTER

    skill = FireBallSkill(MAGE_CHARACTER)
    print(skill)
    print(MAGE_CHARACTER.cs.magical_attack)
    print(MAGE_CHARACTER.to_attack(
        defender_char=MAGE_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    MAGE_CHARACTER.skill_tree.learn_skill(FireBallSkill)

    skill = WaterBubbleSkill(MAGE_CHARACTER)
    print(skill)
    print(MAGE_CHARACTER.cs.magical_attack)
    print(MAGE_CHARACTER.to_attack(
        defender_char=MAGE_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    MAGE_CHARACTER.skill_tree.learn_skill(WaterBubbleSkill)

    skill = WindGustSkill(MAGE_CHARACTER)
    print(skill)
    print(MAGE_CHARACTER.cs.magical_attack)
    print(MAGE_CHARACTER.to_attack(
        defender_char=MAGE_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    MAGE_CHARACTER.skill_tree.learn_skill(WindGustSkill)

    skill = EarthBreakSkill(MAGE_CHARACTER)
    print(skill)
    print(MAGE_CHARACTER.cs.magical_attack)
    print(MAGE_CHARACTER.to_attack(
        defender_char=MAGE_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    MAGE_CHARACTER.skill_tree.learn_skill(EarthBreakSkill)

    skill = MagicBlastSkill(MAGE_CHARACTER)
    print(skill)
    print(MAGE_CHARACTER.cs.magical_attack)
    print(MAGE_CHARACTER.to_attack(
        defender_char=MAGE_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    MAGE_CHARACTER.skill_tree.learn_skill(MagicBlastSkill)

    skill = IceShardSkill(MAGE_CHARACTER)
    print(skill)
    print(MAGE_CHARACTER.cs.magical_attack)
    print(MAGE_CHARACTER.to_attack(
        defender_char=MAGE_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    MAGE_CHARACTER.skill_tree.learn_skill(IceShardSkill)

    skill = FulminantLightningSkill(MAGE_CHARACTER)
    print(skill)
    print(MAGE_CHARACTER.cs.magical_attack)
    print(MAGE_CHARACTER.to_attack(
        defender_char=MAGE_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    MAGE_CHARACTER.skill_tree.learn_skill(FulminantLightningSkill)

    skill = RockArmorSkill(MAGE_CHARACTER)
    print(skill)
    print(MAGE_CHARACTER.cs.evasion)
    print(MAGE_CHARACTER.cs.physical_defense)
    print(skill.function())
    print(MAGE_CHARACTER.cs.evasion)
    print(MAGE_CHARACTER.cs.physical_defense)
    MAGE_CHARACTER.skill_tree.learn_skill(RockArmorSkill)
