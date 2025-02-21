from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    # Sugestão para nomes do caminho:
    # Sentinela da Planície, Lâmina dos Reis, Lança Celeste, 
    # Arauto da Tempestade, Juramento de Aço, Guardião da Honra, 
    # Marechal de Guerra, Vanguarda da Justiça
    'name': 'Lâmina dos Reis',
    'description': (
        ''
    ),
    'skill_list': [
        
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import KNIGHT_CHARACTER
