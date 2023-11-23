from repository.mongo.models.status import StatusModel
from rpgram.conditions.debuff import IMMOBILIZED_DEBUFFS_NAMES
from rpgram.enums.debuff import CONFUSION


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
    '''Retorna um dicionário caso o status do personagem a condição CONFUSION.
    '''
    status_model = StatusModel()
    query = {'player_id': user_id, 'condition_args.name': CONFUSION}
    status = status_model.get(query=query, fields=['condition_args'])
    return status
