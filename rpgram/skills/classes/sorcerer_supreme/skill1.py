from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.barrier import MagicShieldCondition
from rpgram.conditions.debuff import ImprisonedCondition
from rpgram.constants.text import (
    HIT_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    SkillDefenseEnum,
    SkillTypeEnum,
    SorcererSupremeSkillEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class MagicOrbSkill(BaseSkill):
    NAME = SorcererSupremeSkillEnum.MAGIC_ORB.value
    DESCRIPTION = (
        'Conjura uma *Esfera de Energia* pura e destrutiva que flutua '
        'diante do conjurador e irrompe contra o inimigo, '
        'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.MAGIC)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (155% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.SORCERER_SUPREME.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.55,
        }
        damage_types = [DamageEnum.MAGIC]

        super().__init__(
            name=MagicOrbSkill.NAME,
            description=MagicOrbSkill.DESCRIPTION,
            rank=MagicOrbSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=MagicOrbSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.90


class MagicalImprisonmentSkill(BaseSkill):
    NAME = SorcererSupremeSkillEnum.MAGICAL_IMPRISONMENT.value
    DESCRIPTION = (
        'Conjura e lança sobre o inimigo um *Artefato* ou *Animal Mágico*, '
        'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.MAGIC)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível) e '
        'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.IMPRISONED)}* com nível igual ao '
        f'(Rank x Nível) se tirar 15{EmojiEnum.DICE.value} ou mais.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.SORCERER_SUPREME.value,
        'skill_list': [MagicOrbSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.MAGIC]

        super().__init__(
            name=MagicalImprisonmentSkill.NAME,
            description=MagicalImprisonmentSkill.DESCRIPTION,
            rank=MagicalImprisonmentSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=MagicalImprisonmentSkill.REQUIREMENTS,
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

        return report


class MagicShieldSkill(BaseSkill):
    NAME = SorcererSupremeSkillEnum.MAGIC_SHIELD.value
    DESCRIPTION = (
        'Canaliza *Energia Mágica* para envolver um aliado em um *Manto '
        'Mágico* que o resguardar com uma barreira baseada no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.SORCERER_SUPREME.value,
        'skill_list': [MagicOrbSkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=MagicShieldSkill.NAME,
            description=MagicShieldSkill.DESCRIPTION,
            rank=MagicShieldSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BARRIER,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=MagicShieldSkill.REQUIREMENTS,
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
            power = dice.boosted_magical_attack
            level = self.level_rank
            condition = MagicShieldCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{player_name}* canaliza um *Manto Mágico* '
                    'para resguardar '
                    f'*{target_name}* com uma barreira '
                    f'*{condition.barrier_points_text}*({dice.text}).\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class MagicShotSkill(BaseSkill):
    NAME = SorcererSupremeSkillEnum.MAGIC_SHOT.value
    DESCRIPTION = (
        'Conjura uma *Centelha Mágica* na ponta do dedo e a dispara, '
        'ignorando as defesas do oponente e '
        'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.MAGIC)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (75% + 5% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.SORCERER_SUPREME.value,
        'skill_list': [
            MagicOrbSkill.NAME,
            MagicalImprisonmentSkill.NAME,
            MagicShieldSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 0.75,
        }
        damage_types = [DamageEnum.MAGIC]

        super().__init__(
            name=MagicShotSkill.NAME,
            description=MagicShotSkill.DESCRIPTION,
            rank=MagicShotSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.TRUE,
            char=char,
            use_equips_damage_types=False,
            requirements=MagicShotSkill.REQUIREMENTS,
            damage_types=damage_types
        )


SKILL_WAY_DESCRIPTION = {
    'name': 'Magia Bruta',
    'description': (
        'Abraça a Magia e não se limita a regras ou doutrinas, '
        'mas mergulha nas profundezas do Mágico. '
        'Dominado pelo ímpeto e ambição, '
        'explora os limites do que é possível, '
        'manipulando das Energias Mágicas em seu estado Bruto.'
    ),
    'skill_list': [
        MagicOrbSkill,
        MagicalImprisonmentSkill,
        MagicShieldSkill,
        MagicShotSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import SORCERER_SUPREME_CHARACTER

    skill = MagicOrbSkill(SORCERER_SUPREME_CHARACTER)
    print(skill)
    print(SORCERER_SUPREME_CHARACTER.cs.magical_attack)
    print(SORCERER_SUPREME_CHARACTER.to_attack(
        defender_char=SORCERER_SUPREME_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    SORCERER_SUPREME_CHARACTER.skill_tree.learn_skill(MagicOrbSkill)

    skill = MagicalImprisonmentSkill(SORCERER_SUPREME_CHARACTER)
    print(skill)
    print(SORCERER_SUPREME_CHARACTER.cs.magical_attack)
    print(SORCERER_SUPREME_CHARACTER.to_attack(
        defender_char=SORCERER_SUPREME_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    SORCERER_SUPREME_CHARACTER.skill_tree.learn_skill(MagicalImprisonmentSkill)

    skill = MagicShieldSkill(SORCERER_SUPREME_CHARACTER)
    print(skill)
    print(SORCERER_SUPREME_CHARACTER.cs.magical_attack)
    print(skill.function(SORCERER_SUPREME_CHARACTER))
    SORCERER_SUPREME_CHARACTER.skill_tree.learn_skill(MagicShieldSkill)

    skill = MagicShotSkill(SORCERER_SUPREME_CHARACTER)
    print(skill)
    print(SORCERER_SUPREME_CHARACTER.cs.magical_attack)
    print(SORCERER_SUPREME_CHARACTER.to_attack(
        defender_char=SORCERER_SUPREME_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    SORCERER_SUPREME_CHARACTER.skill_tree.learn_skill(MagicShotSkill)
