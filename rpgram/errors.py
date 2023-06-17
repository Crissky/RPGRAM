class CurrentPlayerTurnError(Exception):
    ''' Erro quando não é o turno do personagem.'''


class BattleIsNotOverError(Exception):
    ''' Erro quando a batalha ainda não acabou.'''


class EmptyTeamError(Exception):
    ''' Erro quando o time está vazio.'''


class EquipmentRequirementError(Exception):
    ''' Erro quando o personagem não tem os requisitos necessários para 
    equipar o item.'''
