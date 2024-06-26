from bot.functions.chat import CALLBACK_KEY_LIST


COMMANDS = ['habilidade', 'skill', 'habilidades', 'skills']


# TEXTS
SECTION_TEXT_SKILL_TREE = 'ÁRVOVE DE HABILIDADES'
REFRESH_SKILL_TREE_PATTERN = 'refresh_view_skill_tree'


# PATTERNS
PATTERN_MAIN = fr'^{{"{REFRESH_SKILL_TREE_PATTERN}":1'
PATTERN_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("skill")}:'
PATTERN_SKILL_BACK = fr'^{{{CALLBACK_KEY_LIST.index("skill_back")}:'

# ALERT BUTTON TEXTS
ACCESS_DENIED = (
    f'⛔VOCÊ NÃO TEM ACESSO A ESSA ÁRVORE DE HABILIDADES⛔\n\n'
    f'Use o comando !{COMMANDS[0]} para acessar a SUA ÁRVORE.'
)
