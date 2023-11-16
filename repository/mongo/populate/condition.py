from repository.mongo import ConditionModel
from rpgram.boosters import Condition
from rpgram.enums import TurnEnum
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


CONDITIONS = [
    # Healing Potion Conditions
    {
        'name': 'Minor Healing Potion',
        'description': 'Cura 50 de HP em 5 Turnos.',
        'function': (
            'report = target.combat_stats.cure_hit_points(10 * self.turn);'
            'self.last_turn()'
        ),
        'battle_function': 'report = target.combat_stats.cure_hit_points(20)',
        'frequency': TurnEnum.START,
        'turn': 5,
    },
    {
        'name': 'Light Healing Potion',
        'description': 'Cura 100 de HP em 5 Turnos.',
        'function': (
            'report = target.combat_stats.cure_hit_points(20 * self.turn);'
            'self.last_turn()'
        ),
        'battle_function': 'report = target.combat_stats.cure_hit_points(50)',
        'frequency': TurnEnum.START,
        'turn': 5,
    },
    {
        'name': 'Healing Potion',
        'description': 'Cura 200 de HP em 5 Turnos.',
        'function': (
            'report = target.combat_stats.cure_hit_points(40 * self.turn);'
            'self.last_turn()'
        ),
        'battle_function': 'report = target.combat_stats.cure_hit_points(100)',
        'frequency': TurnEnum.START,
        'turn': 5,
    },
    {
        'name': 'Greater Healing Potion',
        'description': 'Cura 500 de HP em 5 Turnos.',
        'function': (
            'report = target.combat_stats.cure_hit_points(100 * self.turn);'
            'self.last_turn()'
        ),
        'battle_function': 'report = target.combat_stats.cure_hit_points(200)',
        'frequency': TurnEnum.START,
        'turn': 5,
    },
    {
        'name': 'Rare Healing Potion',
        'description': 'Cura 1000 de HP em 5 Turnos.',
        'function': (
            'report = target.combat_stats.cure_hit_points(200 * self.turn);'
            'self.last_turn()'
        ),
        'battle_function': 'report = target.combat_stats.cure_hit_points(400)',
        'frequency': TurnEnum.START,
        'turn': 5,
    },
    {
        'name': 'Epic Healing Potion',
        'description': 'Cura 2500 de HP em 5 Turnos.',
        'function': (
            'report = target.combat_stats.cure_hit_points(500 * self.turn);'
            'self.last_turn()'
        ),
        'battle_function': 'report = target.combat_stats.cure_hit_points(1000)',
        'frequency': TurnEnum.START,
        'turn': 5,
    },
    {
        'name': 'Legendary Healing Potion',
        'description': 'Cura 5000 de HP em 5 Turnos.',
        'function': (
            'report = target.combat_stats.cure_hit_points(1000 * self.turn);'
            'self.last_turn()'
        ),
        'battle_function': 'report = target.combat_stats.cure_hit_points(2000)',
        'frequency': TurnEnum.START,
        'turn': 5,
    },
    {
        'name': 'Mythic Healing Potion',
        'description': 'Cura 1000 de HP por Turno.',
        'function': (
            'report = target.combat_stats.cure_hit_points(1000 * self.turn);'
            'self.last_turn()'
        ),
        'battle_function': 'report = target.combat_stats.cure_hit_points(1000)',
        'frequency': TurnEnum.START,
        'turn': -1,
    },
    # Negative Conditions
    {
        'name': BLEEDING,
        'description': 'Causa (2% x Nível) de dano a cada turno.',
        'function': (
            'power = self.level * 0.02;'
            'damage = target.combat_stats.hp * power;'
            'report = target.combat_stats.damage_hit_points(damage);'
            f'report["text"] = "{BLEEDING} -> " + report["text"];'
            f'report["action"] = "{BLEEDING}";'
        ),
        'battle_function': None,
        'frequency': TurnEnum.START,
        'turn': -1,
    },
    {
        'name': BLINDNESS,
        'description': 'Reduz a chance de acerto.',
        'function': (
            'power = self.level + 1;'
            'self.bonus_evasion = -(10 * power);'
            'report = {};'
            'report["text"] = "Personagem está cego.";'
            f'report["action"] = "{BLINDNESS}";'
        ),
        'battle_function': None,
        'frequency': TurnEnum.CONTINUOUS,
        'turn': -1,
    },
    {
        'name': BURN,
        'description': 'Reduz o multiplicador de Constituição.',
        'function': (
            'power = self.level / 10;'
            'self.multiplier_constitution = 1 - power;'
            'report = {};'
            'report["text"] = "Personagem está com queimaduras.";'
            f'report["action"] = "{BURN}";'
        ),
        'battle_function': None,
        'frequency': TurnEnum.CONTINUOUS,
        'turn': -1,
    },
    {
        'name': CONFUSION,
        'description': (
            'O personagem pode fazer coisa inusitadas por 5 turnos.'
        ),
        'function': (
            'report = {};'
            'report["text"] = "Personagem está confuso.";'
            f'report["action"] = "{CONFUSION}";'
        ),
        'battle_function': None,
        'frequency': TurnEnum.START,
        'turn': 5,
    },
    {
        'name': CURSE,
        'description': 'Reduz os multiplicadores de Inteligência e Sabedoria.',
        'function': (
            'power = self.level / 10;'
            'self.multiplier_intelligence = 1 - power;'
            'self.multiplier_wisdom = 1 - power;'
            'report = {};'
            'report["text"] = "Personagem está amaldiçoado.";'
            f'report["action"] = "{CURSE}";'
        ),
        'battle_function': None,
        'frequency': TurnEnum.CONTINUOUS,
        'turn': -1,
    },
    {
        'name': EXHAUSTION,
        'description': 'Reduz os multiplicadores de Força e Destreza.',
        'function': (
            'power = self.level / 10;'
            'self.multiplier_strength = 1 - power;'
            'self.multiplier_dexterity = 1 - power;'
            'report = {};'
            'report["text"] = "Personagem está exausto.";'
            f'report["action"] = "{EXHAUSTION}";'
        ),
        'battle_function': None,
        'frequency': TurnEnum.CONTINUOUS,
        'turn': -1,
    },
    {
        'name': FROZEN,
        'description': 'O personagem não pode realizar ações por 10 turnos.',
        'function': (
            'report = {};'
            'report["text"] = "Personagem está congelado.";'
            f'report["action"] = "{FROZEN}";'
        ),
        'battle_function': None,
        'frequency': TurnEnum.START,
        'turn': 10,
    },
    {
        'name': PARALYSIS,
        'description': 'O personagem não pode realizar ações por 5 turnos.',
        'function': (
            'report = {};'
            'report["text"] = "Personagem está paralisado.";'
            f'report["action"] = "{PARALYSIS}";'
        ),
        'battle_function': None,
        'frequency': TurnEnum.START,
        'turn': 5,
    },
    {
        'name': PETRIFIED,
        'description': 'O personagem não pode realizar ações.',
        'function': (
            'report = {};'
            'report["text"] = "Personagem está petrificado.";'
            f'report["action"] = "{PETRIFIED}";'
        ),
        'battle_function': None,
        'frequency': TurnEnum.START,
        'turn': -1,
    },
    {
        'name': POISONING,
        'description': 'O personagem perde vida a cada turno.',
        'function': (
            'power = self.level;'
            'damage = 10 * power;'
            'report = target.combat_stats.damage_hit_points(damage);'
            f'report["text"] = "{POISONING} -> " + report["text"];'
            f'report["action"] = "{POISONING}";'
        ),
        'battle_function': None,
        'frequency': TurnEnum.START,
        'turn': -1,
    },
    {
        'name': SILENCE,
        'description': (
            'O personagem não pode usar feitiços, magias ou encantamentos.'
        ),
        'function': (
            'report = {};'
            'report["text"] = "Personagem está silenciado.";'
            f'report["action"] = "{SILENCE}";'
        ),
        'battle_function': None,
        'frequency': TurnEnum.START,
        'turn': -1,
    },
]

if __name__ == "__main__":
    conditions_model = ConditionModel()
    fields = ['_id', 'name', 'created_at']
    for condition_dict in CONDITIONS:
        condition_name = condition_dict['name']
        mongo_dict = conditions_model.get(
            query={'name': condition_name},
            fields=fields,
        )
        if mongo_dict:
            for field in fields:
                condition_dict[field] = mongo_dict[field]
        condition = Condition(**condition_dict)
        print(condition)
        conditions_model.save(condition)
