from bot.functions.chat import CALLBACK_KEY_LIST
from rpgram.constants.text import MAGICAL_DEFENSE_EMOJI_TEXT, PHYSICAL_DEFENSE_EMOJI_TEXT
from rpgram.enums.emojis import EmojiEnum


COMMANDS = ['habilidade', 'skill', 'habilidades', 'skills']


# TEXTS
LIST_USE_SKILL_BUTTON_TEXT = f'{EmojiEnum.USE_SKILL.value}Usar'
LIST_LEARN_SKILL_BUTTON_TEXT = f'Aprender{EmojiEnum.LEARN_SKILL.value}'
LIST_UPGRADE_SKILL_BUTTON_TEXT = f'Aprimorar{EmojiEnum.UPGRADE_SKILL.value}'
ACTION_USE_SKILL_BUTTON_TEXT = f'{EmojiEnum.USE_SKILL.value}Usar'
ACTION_LEARN_SKILL_BUTTON_TEXT = f'{EmojiEnum.LEARN_SKILL.value}Aprender'
ACTION_UPGRADE_SKILL_BUTTON_TEXT = f'{EmojiEnum.UPGRADE_SKILL.value}Aprimorar'
SECTION_TEXT_SKILL_TREE = 'ÁRVOVE DE HABILIDADES'
SECTION_TEXT_USE_SKILL_TREE = 'USAR HABILIDADE'
SECTION_TEXT_LEARN_SKILL_TREE = 'APRENDER HABILIDADE'
SECTION_TEXT_UPGRADE_SKILL_TREE = 'APRIMORAR HABILIDADE'
REFRESH_SKILL_TREE_PATTERN = 'refresh_view_skill_tree'
INTRO_SKILL_TEXT = (
    'Aqui você terá acesso a um arsenal de '
    'habilidades poderosas que moldarão seu caminho para a vitória. '
    'Cada habilidade possui características únicas que a tornam '
    'ideal para diferentes situações e estratégias.\n\n'

    '*Lembre-se: cada classe possui um conjunto único de habilidades.*\n\n'

    f'{EmojiEnum.TARGET_TYPE.value}*TIPO DE ALVO*:\n'
    '*Si Mesmo*: Direciona o efeito da habilidade para quem a usa.\n'
    '*Único*: Seleciona um único alvo para receber o efeito da habilidade.\n'
    '*Equipe*: Aplica o efeito da habilidade a todos os '
    'membros da uma equipe, aliada ou inimiga.\n'
    '*Todes*: Alcança todos os personagens em campo, '
    'tanto aliados quanto inimigos.\n\n'

    f'{EmojiEnum.SKILL_DEFENSE.value}*TIPO DE DANO*:\n'
    '*Físico*: Dano físico que é diminuido de acordo com a '
    f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}*.\n'
    '*Mágico*: Dano Mágico que é diminuido de acordo com a '
    f'*{MAGICAL_DEFENSE_EMOJI_TEXT}*.\n'
    '*Verdadeiro*: Dano que não é afetado por nenhuma das defesas.\n'
)


# PATTERNS
PATTERN_MAIN = fr'^{{"{REFRESH_SKILL_TREE_PATTERN}":1'

PATTERN_LIST_USE_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("list_use_skill")}:'
PATTERN_LIST_LEARN_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("list_learn_skill")}:'
PATTERN_LIST_UPGRADE_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("list_upgrade_skill")}:'

PATTERN_CHECK_USE_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("check_use_skill")}:'
PATTERN_CHECK_LEARN_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("check_learn_skill")}:'
PATTERN_CHECK_UPGRADE_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("check_upgrade_skill")}:'

PATTERN_ACTION_USE_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("action_use_skill")}:'
PATTERN_ACTION_LEARN_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("action_learn_skill")}:'
PATTERN_ACTION_UPGRADE_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("action_upgrade_skill")}:'

PATTERN_SKILL_BACK_MAIN = fr'^{{{CALLBACK_KEY_LIST.index("skill_back")}:"main"'
PATTERN_SKILL_BACK_LIST_USE = fr'^{{{CALLBACK_KEY_LIST.index("skill_back")}:"list_use"'
PATTERN_SKILL_BACK_LIST_LEARN = fr'^{{{CALLBACK_KEY_LIST.index("skill_back")}:"list_learn"'
PATTERN_SKILL_BACK_LIST_UPGRADE = fr'^{{{CALLBACK_KEY_LIST.index("skill_back")}:"list_upgrade"'


# ALERT BUTTON TEXTS
ACCESS_DENIED = (
    f'⛔VOCÊ NÃO TEM ACESSO A ESSA ÁRVORE DE HABILIDADES⛔\n\n'
    f'Use o comando !{COMMANDS[0]} para acessar a SUA ÁRVORE.'
)
