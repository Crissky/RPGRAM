from random import random
from repository.mongo.models.status import StatusModel
from rpgram.enums.debuff import (
    CONFUSION_DEBUFFS_NAMES,
    IMMOBILIZED_DEBUFFS_NAMES
)


def immobilized_status(user_id: int) -> dict:
    '''Retorna um dicionário caso o status do personagem tenha ao menos uma
    das condições de IMMOBILIZED_DEBUFFS_NAMES.
    '''
    status_model = StatusModel()
    query = {
        'player_id': user_id,
        'condition_args.name': {
            '$in': IMMOBILIZED_DEBUFFS_NAMES
        }
    }
    status = status_model.get(query=query, fields=['condition_args'])
    return status


def confusion_status(user_id: int) -> dict:
    '''Retorna um dicionário caso o status do personagem exista 
    a condição CONFUSION.
    '''
    status_model = StatusModel()
    query = {
        'player_id': user_id,
        'condition_args.name': {'$in': CONFUSION_DEBUFFS_NAMES}
    }
    status = status_model.get(query=query, fields=['condition_args'])
    return status


def activated_condition(condition_score: float = 0.5) -> bool:
    resist_score = random()
    return resist_score < condition_score
