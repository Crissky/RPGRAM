from telegram import InlineKeyboardMarkup


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
