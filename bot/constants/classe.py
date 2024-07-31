from rpgram.enums import EmojiEnum


# COMMANDS
COMMANDS = ['classe', 'classes', 'class']


# ALERT BUTTON TEXTS
ACCESS_DENIED = (
    f'⛔VOCÊ NÃO TEM ACESSO A ESSA MENSAGEM⛔\n\n'
    f'Use o comando !{COMMANDS[0]} para acessar '
    f'as {EmojiEnum.CLASSE.value}CLASSES.'
)
