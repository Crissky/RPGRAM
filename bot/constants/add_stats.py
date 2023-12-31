from rpgram.enums import EmojiEnum


# COMMANDS
COMMANDS = ['stats', 'add_stats']


# ATTRIBUTES CONSTANTS
ATTRIBUTE_LIST = ['FOR', 'DES', 'CON', 'INT', 'SAB', 'CAR']
POINTS_OPTION_LIST = [1, 3, 5]


# TEXTS
SECTION_TEXT_STATS = 'ESTATÍSTICAS'


# ALERT BUTTON TEXTS
ACCESS_DENIED = (
    f'⛔VOCÊ NÃO TEM ACESSO A ESSAS ESTATÍSTICAS⛔\n\n'
    f'Use o comando !{COMMANDS[0]} para acessar '
    f'SUAS {EmojiEnum.BASE_ATTRIBUTES.value}ESTATÍSTICAS.'
)
