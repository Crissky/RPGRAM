from bot.functions.chat import CALLBACK_KEY_LIST
from rpgram.enums.emojis import EmojiEnum


COMMANDS = ['habilidade', 'skill', 'habilidades', 'skills']


# TEXTS
LIST_USE_SKILL_BUTTON_TEXT = f'{EmojiEnum.USE_SKILL.value}Usar'
LIST_LEARN_SKILL_BUTTON_TEXT = f'Aprender{EmojiEnum.LEARN_SKILL.value}'
LIST_UPGRADE_SKILL_BUTTON_TEXT = f'Aprimorar{EmojiEnum.UPGRADE_SKILL.value}'
SECTION_TEXT_SKILL_TREE = 'ÁRVOVE DE HABILIDADES'
SECTION_TEXT_USE_SKILL_TREE = 'USAR HABILIDADE'
SECTION_TEXT_LEARN_SKILL_TREE = 'APRENDER HABILIDADE'
SECTION_TEXT_UPGRADE_SKILL_TREE = 'APRIMORAR HABILIDADE'
REFRESH_SKILL_TREE_PATTERN = 'refresh_view_skill_tree'


# PATTERNS
PATTERN_MAIN = fr'^{{"{REFRESH_SKILL_TREE_PATTERN}":1'
PATTERN_LIST_USE_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("list_use_skill")}:'
PATTERN_LIST_LEARN_SKILL = (
    fr'^{{{CALLBACK_KEY_LIST.index("list_learn_skill")}:'
)
PATTERN_LIST_UPGRADE_SKILL = (
    fr'^{{{CALLBACK_KEY_LIST.index("list_upgrade_skill")}:'
)
PATTERN_CHECK_USE_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("check_use_skill")}:'
PATTERN_CHECK_LEARN_SKILL = (
    fr'^{{{CALLBACK_KEY_LIST.index("check_learn_skill")}:'
)
PATTERN_CHECK_UPGREDE_SKILL = (
    fr'^{{{CALLBACK_KEY_LIST.index("check_upgrede_skill")}:'
)
PATTERN_USE_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("use_skill")}:'
PATTERN_LEARN_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("learn_skill")}:'
PATTERN_SKILL_BACK = fr'^{{{CALLBACK_KEY_LIST.index("skill_back")}:'

# ALERT BUTTON TEXTS
ACCESS_DENIED = (
    f'⛔VOCÊ NÃO TEM ACESSO A ESSA ÁRVORE DE HABILIDADES⛔\n\n'
    f'Use o comando !{COMMANDS[0]} para acessar a SUA ÁRVORE.'
)
