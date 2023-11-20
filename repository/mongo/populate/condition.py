from repository.mongo import ConditionModel
from rpgram.consumables.heal import (
    MINOR_HEALING_POTION_POWER,
    LIGHT_HEALING_POTION_POWER,
    HEALING_POTION_POWER,
    GREATER_HEALING_POTION_POWER,
    RARE_HEALING_POTION_POWER,
    EPIC_HEALING_POTION_POWER,
    LEGENDARY_HEALING_POTION_POWER,
)
from rpgram.conditions import (
    HealingCondition,
    BleedingCondition,
    BlindnessCondition,
    BurnCondition,
    ConfusionCondition,
    CurseCondition,
    ExhaustionCondition,
    FrozenCondition,
    ParalysisCondition,
    PetrifiedCondition,
    PoisoningCondition,
    SilenceCondition,
)
from rpgram.enums import HealingConsumableEnum, TurnEnum
from rpgram.enums.condition import (
    BLEEDING,
    BLINDNESS,
    BURN,
    CONFUSION,
    CURSE,
    EXHAUSTION,
    FROZEN,
    PARALYSIS,
    PETRIFIED,
    POISONING,
    SILENCE,
)

MINOR_HEALING_POTION_TURNPOWER = MINOR_HEALING_POTION_POWER // 5
LIGHT_HEALING_POTION_TURNPOWER = LIGHT_HEALING_POTION_POWER // 5
HEALING_POTION_TURNPOWER = HEALING_POTION_POWER // 5
GREATER_HEALING_POTION_TURNPOWER = GREATER_HEALING_POTION_POWER // 5
RARE_HEALING_POTION_TURNPOWER = RARE_HEALING_POTION_POWER // 5
EPIC_HEALING_POTION_TURNPOWER = EPIC_HEALING_POTION_POWER // 5
LEGENDARY_HEALING_POTION_TURNPOWER = LEGENDARY_HEALING_POTION_POWER // 5
MYTHIC_HEALING_POTION_TURNPOWER = LEGENDARY_HEALING_POTION_TURNPOWER

CONDITIONS = [
    # Healing Potion Conditions
    {
        'name': HealingConsumableEnum.HEAL1.value,
        'description': f'Cura {MINOR_HEALING_POTION_POWER} de HP em 5 Turnos.',
        'power': MINOR_HEALING_POTION_TURNPOWER,
        'frequency': TurnEnum.START,
        'turn': 5,
        'class': HealingCondition
    },
    {
        'name': HealingConsumableEnum.HEAL2.value,
        'description': f'Cura {LIGHT_HEALING_POTION_POWER} de HP em 5 Turnos.',
        'power': LIGHT_HEALING_POTION_TURNPOWER,
        'frequency': TurnEnum.START,
        'turn': 5,
        'class': HealingCondition
    },
    {
        'name': HealingConsumableEnum.HEAL3.value,
        'description': f'Cura {HEALING_POTION_POWER} de HP em 5 Turnos.',
        'power': HEALING_POTION_TURNPOWER,
        'frequency': TurnEnum.START,
        'turn': 5,
        'class': HealingCondition
    },
    {
        'name': HealingConsumableEnum.HEAL4.value,
        'description': (
            f'Cura {GREATER_HEALING_POTION_POWER} de HP em 5 Turnos.'
        ),
        'power': GREATER_HEALING_POTION_TURNPOWER,
        'frequency': TurnEnum.START,
        'turn': 5,
        'class': HealingCondition
    },
    {
        'name': HealingConsumableEnum.HEAL5.value,
        'description': f'Cura {RARE_HEALING_POTION_POWER} de HP em 5 Turnos.',
        'power': RARE_HEALING_POTION_TURNPOWER,
        'frequency': TurnEnum.START,
        'turn': 5,
        'class': HealingCondition
    },
    {
        'name': HealingConsumableEnum.HEAL6.value,
        'description': f'Cura {EPIC_HEALING_POTION_POWER} de HP em 5 Turnos.',
        'power': EPIC_HEALING_POTION_TURNPOWER,
        'frequency': TurnEnum.START,
        'turn': 5,
        'class': HealingCondition
    },
    {
        'name': HealingConsumableEnum.HEAL7.value,
        'description': (
            f'Cura {LEGENDARY_HEALING_POTION_POWER} de HP em 5 Turnos.'
        ),
        'power': LEGENDARY_HEALING_POTION_TURNPOWER,
        'frequency': TurnEnum.START,
        'turn': 5,
        'class': HealingCondition
    },
    {
        'name': HealingConsumableEnum.HEAL8.value,
        'description': (
            f'Cura {MYTHIC_HEALING_POTION_TURNPOWER} de HP por Turno.'
        ),
        'power': MYTHIC_HEALING_POTION_TURNPOWER,
        'frequency': TurnEnum.START,
        'turn': -1,
        'class': HealingCondition
    },
    # Negative Conditions
    {
        'name': BLEEDING,
        'description': 'Causa (2% x Nível) de dano a cada turno.',
        'frequency': TurnEnum.START,
        'turn': -1,
        'class': BleedingCondition,
    },
    {
        'name': BLINDNESS,
        'description': 'Reduz o multiplicador de Destreza em (10% x Nível).',
        'frequency': TurnEnum.CONTINUOUS,
        'turn': -1,
        'class': BlindnessCondition,
    },
    {
        'name': BURN,
        'description': (
            'Reduz o multiplicador de Constituição em (10% x Nível).'
        ),
        'frequency': TurnEnum.CONTINUOUS,
        'turn': -1,
        'class': BurnCondition,
    },
    {
        'name': CONFUSION,
        'description': (
            'O personagem pode fazer coisa inusitadas por 5 turnos.'
        ),
        'frequency': TurnEnum.START,
        'turn': 5,
        'class': ConfusionCondition,
    },
    {
        'name': CURSE,
        'description': (
            'Reduz os multiplicadores de Inteligência e Sabedoria '
            'em (10% x Nível).'
        ),
        'frequency': TurnEnum.CONTINUOUS,
        'turn': -1,
        'class': CurseCondition,
    },
    {
        'name': EXHAUSTION,
        'description': (
            'Reduz os multiplicadores de Força e Destreza em (10% x Nível).'
        ),
        'frequency': TurnEnum.CONTINUOUS,
        'turn': -1,
        'class': ExhaustionCondition,
    },
    {
        'name': FROZEN,
        'description': 'O personagem não pode realizar ações por 5 turnos.',
        'frequency': TurnEnum.START,
        'turn': 5,
        'class': FrozenCondition,
    },
    {
        'name': PARALYSIS,
        'description': 'O personagem não pode realizar ações por 3 turnos.',
        'frequency': TurnEnum.START,
        'turn': 3,
        'class': ParalysisCondition,
    },
    {
        'name': PETRIFIED,
        'description': 'O personagem não pode realizar ações.',
        'frequency': TurnEnum.START,
        'turn': -1,
        'class': PetrifiedCondition,
    },
    {
        'name': POISONING,
        'description': 'O personagem perde vida a cada turno.',
        'frequency': TurnEnum.START,
        'turn': -1,
        'class': PoisoningCondition,
    },
    {
        'name': SILENCE,
        'description': (
            'O personagem não pode usar feitiços, magias ou encantamentos.'
        ),
        'frequency': TurnEnum.START,
        'turn': -1,
        'class': SilenceCondition,
    },
]

if __name__ == "__main__":
    conditions_model = ConditionModel()
    fields = ['_id', 'name', 'created_at']
    for condition_dict in CONDITIONS:
        condition_name = condition_dict['name']
        condition_class = condition_dict.pop('class')
        mongo_dict = conditions_model.get(
            query={'name': condition_name},
            fields=fields,
        )
        if mongo_dict:
            for field in fields:
                condition_dict[field] = mongo_dict[field]
        condition = condition_class(**condition_dict)
        print(condition)
        conditions_model.save(condition, replace=True)
