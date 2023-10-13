from repository.mongo import ConditionModel
from rpgram.boosters import Condition
from rpgram.enums import TurnEnum

CONDITIONS = [
    {
        'name': 'Minor Healing Potion',
        'description': 'Cura 100 de HP em 5 Turnos.',
        'function': (
            'report = target.combat_stats.cure_hit_points(20 * self.turn);'
            'self.last_turn()'
        ),
        'battle_function': 'report = target.combat_stats.cure_hit_points(20)',
        'frequency': TurnEnum.START,
        'turn': 5,
    },
    {
        'name': 'Light Healing Potion',
        'description': 'Cura 250 de HP em 5 Turnos.',
        'function': (
            'report = target.combat_stats.cure_hit_points(50 * self.turn);'
            'self.last_turn()'
        ),
        'battle_function': 'report = target.combat_stats.cure_hit_points(50)',
        'frequency': TurnEnum.START,
        'turn': 5,
    },
    {
        'name': 'Healing Potion',
        'description': 'Cura 500 de HP em 5 Turnos.',
        'function': (
            'report = target.combat_stats.cure_hit_points(100 * self.turn);'
            'self.last_turn()'
        ),
        'battle_function': 'report = target.combat_stats.cure_hit_points(100)',
        'frequency': TurnEnum.START,
        'turn': 5,
    },
    {
        'name': 'Greater Healing Potion',
        'description': 'Cura 1000 de HP em 5 Turnos.',
        'function': (
            'report = target.combat_stats.cure_hit_points(200 * self.turn);'
            'self.last_turn()'
        ),
        'battle_function': 'report = target.combat_stats.cure_hit_points(200)',
        'frequency': TurnEnum.START,
        'turn': 5,
    },
    {
        'name': 'Rare Healing Potion',
        'description': 'Cura 2000 de HP em 5 Turnos.',
        'function': (
            'report = target.combat_stats.cure_hit_points(400 * self.turn);'
            'self.last_turn()'
        ),
        'battle_function': 'report = target.combat_stats.cure_hit_points(400)',
        'frequency': TurnEnum.START,
        'turn': 5,
    },
    {
        'name': 'Epic Healing Potion',
        'description': 'Cura 5000 de HP em 5 Turnos.',
        'function': (
            'report = target.combat_stats.cure_hit_points(1000 * self.turn);'
            'self.last_turn()'
        ),
        'battle_function': 'report = target.combat_stats.cure_hit_points(1000)',
        'frequency': TurnEnum.START,
        'turn': 5,
    },
    {
        'name': 'Legendary Healing Potion',
        'description': 'Cura 10000 de HP em 5 Turnos.',
        'function': (
            'report = target.combat_stats.cure_hit_points(2000 * self.turn);'
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
