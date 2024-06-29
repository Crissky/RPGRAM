from random import random
from repository.mongo.models.character import CharacterModel
from rpgram.enums.debuff import (
    CONFUSION_DEBUFFS_NAMES,
    IMMOBILIZED_DEBUFFS_NAMES
)


def immobilized_status(user_id: int) -> dict:
    '''Retorna um dicionário caso o status do personagem tenha ao menos uma
    das condições de IMMOBILIZED_DEBUFFS_NAMES.
    '''
    char_model = CharacterModel()
    query = {
        'player_id': user_id,
        'status.condition_args.name': {
            '$in': IMMOBILIZED_DEBUFFS_NAMES
        }
    }
    status_dict: dict = char_model.get(query=query, fields=['status'])
    return status_dict['status'] if status_dict is not None else status_dict


def get_confusion_status(user_id: int) -> dict:
    '''Retorna um dicionário caso o status do personagem exista 
    a condição CONFUSION.
    '''

    char_model = CharacterModel()
    query = {
        'player_id': user_id,
        'status.condition_args.name': {'$in': CONFUSION_DEBUFFS_NAMES}
    }
    status_dict: dict = char_model.get(query=query, fields=['status'])
    return status_dict['status'] if status_dict is not None else status_dict


def activated_condition(condition_score: float = 0.5) -> bool:
    resist_score = random()
    return resist_score < condition_score
