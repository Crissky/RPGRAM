from rpgram.skills.classes.multiclasse.physical_defense import (
    GuardianShieldSkill,
    HeavyChargeSkill,
    RobustBlockSkill
)


SKILL_WAY_DESCRIPTION = {
    'name': 'Protetor Implacável',
    'description': (
        'O Protetor Implacável encarna a força indomável para proteger. '
        'Sua devoção à causa da justiça o torna um defensor inflexível '
        'dos fracos e oprimidos. Ele é um escudo inquebrantável, '
        'capaz de absorver o impacto de qualquer ataque e retaliar '
        'com força brutal.'
    ),
    'skill_list': [
        GuardianShieldSkill,
        HeavyChargeSkill,
        RobustBlockSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import HERALD_CHARACTER

    skill = RobustBlockSkill(HERALD_CHARACTER)
    print(skill)
    print(HERALD_CHARACTER.bs.constitution)
    print(HERALD_CHARACTER.cs.physical_defense)
    print(skill.function())
    print(HERALD_CHARACTER.cs.physical_defense)
    HERALD_CHARACTER.skill_tree.learn_skill(RobustBlockSkill)

    skill = GuardianShieldSkill(HERALD_CHARACTER)
    print(skill)
    print(HERALD_CHARACTER.cs.physical_defense)
    print(skill.function(HERALD_CHARACTER))
    HERALD_CHARACTER.skill_tree.learn_skill(GuardianShieldSkill)

    skill = HeavyChargeSkill(HERALD_CHARACTER)
    print(skill)
    print(HERALD_CHARACTER.cs.physical_attack)
    print(HERALD_CHARACTER.cs.physical_defense)
    HERALD_CHARACTER.skill_tree.learn_skill(HeavyChargeSkill)
