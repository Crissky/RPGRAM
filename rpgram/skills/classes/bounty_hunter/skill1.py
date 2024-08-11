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
        f'Se aproxima do inimigo e com um movimento súbito, '
        f'inflige um golpe mortal com sua arma, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (200% + 5% x Rank x Nível) e '
        f'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BLEEDING)}* com nível igual ao '
        f'(Rank x Nível), '
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


class HuntingNetSkill(BaseSkill):
    NAME = BountyHunterSkillEnum.HUNTING_NET.value
    DESCRIPTION = (
        f'Lança sobre o oponente uma *Rede* feita de fios cortantes de metal, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível) e '
        f'adicionando a condição '
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
            CombatStatsEnum.PHYSICAL_ATTACK: 1.00,
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
            bleeding_condition = ImprisonedCondition(level=level)
            status_report = target.status.add_condition(bleeding_condition)
            report['status_text'] = status_report['text']

        return report


class SharpFaroSkill(BaseSkill):
    NAME = BountyHunterSkillEnum.SHARP_FARO.value
    DESCRIPTION = (
        f'Se conentra em usa o *Olfato Apurado* para rastrear os oponentes, '
        f'aumentando o '
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
                f'aumentando o '
                f'*{HIT_EMOJI_TEXT}*.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class InvestigationSkill(BaseSkill):
    NAME = BountyHunterSkillEnum.INVESTIGATION.value
    DESCRIPTION = (
        f'Estuda os movimentos dos oponentes no *Campo de Batalha*, '
        f'aumentando o '
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
                f'aumentando o '
                f'*{HIT_EMOJI_TEXT}* e a *{EVASION_EMOJI_TEXT}*.\n\n'
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
        HuntingNetSkill,
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

    skill = HuntingNetSkill(BOUNTY_HUNTER_CHARACTER)
    print(skill)
    print(BOUNTY_HUNTER_CHARACTER.cs.physical_attack)
    print(BOUNTY_HUNTER_CHARACTER.to_attack(
        defender_char=BOUNTY_HUNTER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BOUNTY_HUNTER_CHARACTER.skill_tree.learn_skill(HuntingNetSkill)

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
