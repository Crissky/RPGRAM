import re
from rpgram.enums import EmojiEnum


# CALLBACKS
CALLBACK_CLOSE = '$close'
ESCAPED_CALLBACK_CLOSE = re.escape(CALLBACK_CLOSE)

# TEXTS
LEFT_CLOSE_BUTTON_TEXT = f'{EmojiEnum.CLOSE.value}Fechar'
RIGHT_CLOSE_BUTTON_TEXT = f'Fechar{EmojiEnum.CLOSE.value}'
REFRESH_BUTTON_TEXT = f'{EmojiEnum.REFRESH.value}Atualizar'
DETAIL_BUTTON_TEXT = f'{EmojiEnum.DETAIL.value}Detalhar'

# ALERT BUTTON TEXTS
ACCESS_DENIED = f'⛔VOCÊ NÃO TEM ACESSO A ESSA CONVERSA⛔'
