class CurrentPlayerTurnError(Exception):
    ''' Erro quando não é o turno do personagem.'''


class EmptyTeamError(Exception):
    ''' Erro quando o time está vazio.'''


class RequirementError(Exception):
    ''' Erro quando o personagem não tem os requisitos necessários.'''


class EquipmentRequirementError(Exception):
    ''' Erro quando o personagem não tem os requisitos necessários para
    equipar o item.'''


class SkillRequirementError(Exception):
    ''' Erro quando o personagem não tem os requisitos necessários para
    usar a habilidade.'''


class InvalidWordError(Exception):
    ''' Erro quando é enviada uma palavra que não atende aos critérios
    do WordGame (SecretWord)'''
