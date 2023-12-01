from rpgram.enums import EmojiEnum


# COMMANDS
COMMANDS = ['raca', 'racas', 'race', 'races']


# ALERT BUTTON TEXTS
ACCESS_DENIED = (
    f'⛔VOCÊ NÃO TEM ACESSO A ESSA MENSAGEM⛔\n\n'
    f'Use o comando !{COMMANDS[0]} para acessar '
    f'as {EmojiEnum.RACE.value}RAÇAS.'
)
