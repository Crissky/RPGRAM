import re
from rpgram.enums import EmojiEnum


# CALLBACKS
CALLBACK_CLOSE = '$close'
ESCAPED_CALLBACK_CLOSE = re.escape(CALLBACK_CLOSE)


# ALERT BUTTON TEXTS
ACCESS_DENIED = f'⛔VOCÊ NÃO TEM ACESSO A ESSA CONVERSA⛔'
