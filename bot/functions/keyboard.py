from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def remove_buttons_by_text(
    keyboard_markup: InlineKeyboardMarkup,
    *texts: str
) -> InlineKeyboardMarkup:
    '''
    Remove os botões que tem o texto idêntico a alguma das strings de texts
    '''
    buttons = []
    for row_buttons in keyboard_markup.inline_keyboard:
        buttons.append([
            button for button in row_buttons
            if button.text not in texts
        ])

    return InlineKeyboardMarkup(buttons)


def reshape_row_buttons(
    buttons: List[InlineKeyboardButton],
    buttons_per_row: int = 2
) -> List[List[InlineKeyboardButton]]:
    ''' Transforma uma lista de botões em uma lista de listas de botões,
        com um número de botões por linha definido pelo parâmetro
        buttons_per_row.
        Por exemplo, se buttons_per_row for 2, então será gerada uma lista com
        listas de botões, onde cada lista de botões terá no máximo 2 botões.
    '''

    final_buttons = []
    total_buttons = len(buttons)
    for i in range(0, total_buttons, buttons_per_row):
        final_buttons.append(buttons[i:i + buttons_per_row])

    return final_buttons
