
from typing import TYPE_CHECKING
from rpgram.conditions.debuff import PoisoningCondition
from rpgram.constants.text import (
    HIT_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    RogueSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.classes.multiclasse.precision_attack import (
    QuickAttackSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class VipersFangSkill(BaseSkill):
    NAME = RogueSkillEnum.VIPERÇÇÇS_FANGS.value
    DESCRIPTION = (
        f'Com um movimento rápido, golpeia o inimigo '
        f'após imbuir sua arma com *Veneno*, causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.POISON)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.ROGUE.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.POISON]

        super().__init__(
            name=VipersFangSkill.NAME,
            description=VipersFangSkill.DESCRIPTION,
            rank=VipersFangSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=VipersFangSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class DoubleFangsSkill(BaseSkill):
    NAME = RogueSkillEnum.DOUBLE_FANGS.value
    DESCRIPTION = (
        f'Com dois movimentos rápidos, golpeia o inimigo duas vezes '
        f'com uma arma *Envenenada*, causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.POISON)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.ROGUE.value,
        'skill_list': [VipersFangSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.POISON, DamageEnum.POISON]

        super().__init__(
            name=DoubleFangsSkill.NAME,
            description=DoubleFangsSkill.DESCRIPTION,
            rank=DoubleFangsSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=DoubleFangsSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class TaipanInoculateSkill(BaseSkill):
    NAME = RogueSkillEnum.TAIPAN_INOCULATE.value
    DESCRIPTION = (
        f'Lança um ataque com a arma banhada em uma toxina poderosa que '
        f'causa dano de '
        f'*{get_damage_emoji_text(DamageEnum.POISON)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.LIGHTNING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível) e '
        f'adiciona a condição '
        f'{get_debuff_emoji_text(DebuffEnum.POISONING)} com nível igual ao '
        f'2 x (Rank x Nível + {EmojiEnum.DICE.value}).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.ROGUE.value,
        'skill_list': [VipersFangSkill.NAME, DoubleFangsSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.POISON, DamageEnum.LIGHTNING]

        super().__init__(
            name=TaipanInoculateSkill.NAME,
            description=TaipanInoculateSkill.DESCRIPTION,
            rank=TaipanInoculateSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=TaipanInoculateSkill.REQUIREMENTS,
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
            level = (self.level_rank + self.dice.value) * 2

            poisoning_condition = PoisoningCondition(level=level)
            status_report = target.status.add_condition(poisoning_condition)
            report['status_text'] = status_report['text']

        return report


class PhantomStrikeSkill(BaseSkill):
    NAME = RogueSkillEnum.PHANTOM_STRIKE.value
    DESCRIPTION = (
        f'Ultrapassa o limiar da velocidade, '
        f'aparentando ser um espectro que atravessa a realidade, para '
        f'executar um único golpe furtivo que '
        f'causa dano '
        f'*{get_damage_emoji_text(DamageEnum.GHOSTLY)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível). '
        f'Essa habilidade possui *{HIT_EMOJI_TEXT}* acima do normal.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.ROGUE.value,
        'skill_list': [QuickAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.00
        }
        damage_types = [DamageEnum.GHOSTLY]

        super().__init__(
            name=PhantomStrikeSkill.NAME,
            description=PhantomStrikeSkill.DESCRIPTION,
            rank=PhantomStrikeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=PhantomStrikeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 1.50


class ElusiveAssaultSkill(BaseSkill):
    NAME = RogueSkillEnum.ELUSIVE_ASSAULT.value
    DESCRIPTION = (
        f'Avança como um raio contra o oponente, ricocheteando para '
        f'enganar suas defesas e '
        f'atacando-o com um movimento preciso, '
        f'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.GHOSTLY)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.LIGHTNING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível). '
        f'Essa habilidade não pode ser esquivada.'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.ROGUE.value,
        'skill_list': [QuickAttackSkill.NAME, PhantomStrikeSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.25
        }
        damage_types = [DamageEnum.GHOSTLY, DamageEnum.LIGHTNING]

        super().__init__(
            name=ElusiveAssaultSkill.NAME,
            description=ElusiveAssaultSkill.DESCRIPTION,
            rank=ElusiveAssaultSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            is_elusive=True,
            use_equips_damage_types=True,
            requirements=ElusiveAssaultSkill.REQUIREMENTS,
            damage_types=damage_types
        )


SKILL_WAY_DESCRIPTION = {
    'name': 'Assassino Letal',
    'description': (
        'Mestre na morte silenciosa, seu foco está em eliminar seus inimigos '
        'com eficiência. '
        'O Assassino Letal é um mestre da execução precisa, '
        'capaz de eliminar seus inimigos, utilizando armas afiadas e '
        'venenos para infligir feridas mortais.'
    ),
    'skill_list': [
        VipersFangSkill,
        DoubleFangsSkill,
        TaipanInoculateSkill,
        QuickAttackSkill,
        PhantomStrikeSkill,
        ElusiveAssaultSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import ROGUE_CHARACTER

    skill = VipersFangSkill(ROGUE_CHARACTER)
    print(skill)
    print(ROGUE_CHARACTER.cs.precision_attack)
    print(ROGUE_CHARACTER.to_attack(
        defender_char=ROGUE_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ROGUE_CHARACTER.skill_tree.learn_skill(VipersFangSkill)

    skill = DoubleFangsSkill(ROGUE_CHARACTER)
    print(skill)
    print(ROGUE_CHARACTER.cs.precision_attack)
    print(ROGUE_CHARACTER.to_attack(
        defender_char=ROGUE_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ROGUE_CHARACTER.skill_tree.learn_skill(DoubleFangsSkill)

    skill = TaipanInoculateSkill(ROGUE_CHARACTER)
    print(skill)
    print(ROGUE_CHARACTER.cs.precision_attack)
    print(ROGUE_CHARACTER.to_attack(
        defender_char=ROGUE_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ROGUE_CHARACTER.skill_tree.learn_skill(TaipanInoculateSkill)

    skill = QuickAttackSkill(ROGUE_CHARACTER)
    print(skill)
    print(ROGUE_CHARACTER.cs.precision_attack)
    print(ROGUE_CHARACTER.to_attack(
        defender_char=ROGUE_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ROGUE_CHARACTER.skill_tree.learn_skill(QuickAttackSkill)

    skill = PhantomStrikeSkill(ROGUE_CHARACTER)
    print(skill)
    print(ROGUE_CHARACTER.cs.precision_attack)
    print(ROGUE_CHARACTER.to_attack(
        defender_char=ROGUE_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ROGUE_CHARACTER.skill_tree.learn_skill(PhantomStrikeSkill)

    skill = ElusiveAssaultSkill(ROGUE_CHARACTER)
    print(skill)
    print(ROGUE_CHARACTER.cs.precision_attack)
    print(ROGUE_CHARACTER.to_attack(
        defender_char=ROGUE_CHARACTER,
        attacker_skill=skill,
        to_dodge=True,
        verbose=True,
    )['text'])
    ROGUE_CHARACTER.skill_tree.learn_skill(ElusiveAssaultSkill)
