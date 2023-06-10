class CurrentPlayerTurnError(Exception):
    ''' Erro quando não é o turno do personagem.'''

class BattleNotEndError(Exception):
    ''' Erro quando a batalha ainda não acabou.'''