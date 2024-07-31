from bot.functions.chat import CALLBACK_KEY_LIST
from rpgram.constants.text import BARRIER_POINT_FULL_EMOJI_TEXT, HIT_POINT_FULL_EMOJI_TEXT, MAGICAL_DEFENSE_EMOJI_TEXT, PHYSICAL_DEFENSE_EMOJI_TEXT
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import SkillDefenseEmojiEnum, SkillTypeEmojiEnum, TargetEmojiEnum


COMMANDS = ['habilidade', 'skill', 'habilidades', 'skills']


# TEXTS
LIST_USE_SKILL_BUTTON_TEXT = f'{EmojiEnum.USE_SKILL.value}Usar'
LIST_LEARN_SKILL_BUTTON_TEXT = f'Aprender{EmojiEnum.LEARN_SKILL.value}'
LIST_UPGRADE_SKILL_BUTTON_TEXT = f'Aprimorar{EmojiEnum.UPGRADE_SKILL.value}'
HELP_SKILL_BUTTON_TEXT = f'{EmojiEnum.DETAIL.value}Informações'
LIST_ALL_SKILL_BUTTON_TEXT = f'Classes{EmojiEnum.CLASSE.value}'
ACTION_USE_SKILL_BUTTON_TEXT = f'{EmojiEnum.USE_SKILL.value}Usar'
ACTION_LEARN_SKILL_BUTTON_TEXT = f'{EmojiEnum.LEARN_SKILL.value}Aprender'
ACTION_UPGRADE_SKILL_BUTTON_TEXT = f'{EmojiEnum.UPGRADE_SKILL.value}Aprimorar'
SECTION_TEXT_SKILL_TREE = ' HABILIDADES '
SECTION_TEXT_USE_SKILL_TREE = 'USAR HABILIDADE'
SECTION_TEXT_LEARN_SKILL_TREE = 'APRENDER HABILIDADE'
SECTION_TEXT_UPGRADE_SKILL_TREE = 'APRIMORAR HABILIDADE'
SECTION_TEXT_CHOICE_CLASSE_SKILL_TREE = 'ESCOLHA UMA CLASSE'
SECTION_TEXT_CHOICE_WAY_SKILL_TREE = 'ESCOLHA UM CAMINHO'
SECTION_TEXT_WAY_SKILL_TREE = 'CAMINHO'
REFRESH_SKILL_TREE_PATTERN = 'refresh_view_skill_tree'
INTRO_SKILL_TEXT = (
    'Aqui você terá acesso a um arsenal de '
    '*habilidades* poderosas que moldarão seu caminho para a vitória. '
    'Cada *habilidade* possui características únicas que a tornam '
    'ideal para diferentes situações e estratégias.\n\n'

    '*Lembre-se: cada classe possui um conjunto único de habilidades.*'
)
HELP_SKILL_TEXT = (
    f'{EmojiEnum.TARGET_TYPE.value}*TIPO DE ALVO*:\n'
    f'{TargetEmojiEnum.SELF.value}*Si Mesmo*: '
    f'Direciona o efeito da habilidade para quem a usa.\n'
    f'{TargetEmojiEnum.SINGLE.value}*Único*: '
    f'Seleciona um único alvo para receber o efeito da habilidade.\n'
    f'{TargetEmojiEnum.TEAM.value}*Equipe*: '
    f'Aplica o efeito da habilidade a todos os '
    f'membros da uma equipe, aliada ou inimiga.\n'
    f'{TargetEmojiEnum.ALL.value}*Todes*: '
    f'Alcança todos os personagens em campo, '
    f'tanto aliados quanto inimigos.\n\n'

    f'{EmojiEnum.SKILL_TYPE.value}*TIPO DE HABILIDADE*:\n'
    f'{SkillTypeEmojiEnum.ATTACK.value}*Ofensiva*: '
    f'Habilidade de ataque focada em causar dano e '
    f'efeitos diversos ao oponente.\n'
    # f'{SkillTypeEmojiEnum.DEFENSE.value}*Defensivo*: '
    f'{SkillTypeEmojiEnum.HEALING.value}*Cura*: '
    f'Habilidade que cura {HIT_POINT_FULL_EMOJI_TEXT}.\n'
    f'{SkillTypeEmojiEnum.BUFF.value}:*Fortalecimento* '
    f'Habilidade que concede melhorias para o personagem.\n'
    f'{SkillTypeEmojiEnum.BARRIER.value}*Barreira*: '
    f'Habilidade que protege o personagem, concedendo '
    f'{BARRIER_POINT_FULL_EMOJI_TEXT} para mitigar dano.\n\n'

    f'{EmojiEnum.SKILL_DEFENSE.value}*TIPO DE DANO*:\n'
    f'{SkillDefenseEmojiEnum.PHYSICAL.value}*Físico*: '
    f'Dano físico que é diminuido de acordo com a '
    f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}*.\n'
    f'{SkillDefenseEmojiEnum.MAGICAL.value}*Mágico*: '
    f'Dano Mágico que é diminuido de acordo com a '
    f'*{MAGICAL_DEFENSE_EMOJI_TEXT}*.\n'
    f'{SkillDefenseEmojiEnum.TRUE.value}*Verdadeiro*: '
    f'Dano que não é afetado por nenhuma das defesas.'
)

# PATTERNS
PATTERN_MAIN = fr'^{{"{REFRESH_SKILL_TREE_PATTERN}":1'

PATTERN_HELP_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("help_skill")}:'
PATTERN_LIST_ALL_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("list_all_skill")}:'
PATTERN_LIST_CLASSE_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("list_classe_skill")}:'
PATTERN_LIST_WAY_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("list_way_skill")}:'

PATTERN_LIST_USE_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("list_use_skill")}:'
PATTERN_LIST_LEARN_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("list_learn_skill")}:'
PATTERN_LIST_UPGRADE_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("list_upgrade_skill")}:'

PATTERN_CHECK_USE_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("check_use_skill")}:'
PATTERN_CHECK_LEARN_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("check_learn_skill")}:'
PATTERN_CHECK_UPGRADE_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("check_upgrade_skill")}:'
PATTERN_CHECK_WAY_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("check_way_skill")}:'

PATTERN_ACTION_USE_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("action_use_skill")}:'
PATTERN_ACTION_LEARN_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("action_learn_skill")}:'
PATTERN_ACTION_UPGRADE_SKILL = fr'^{{{CALLBACK_KEY_LIST.index("action_upgrade_skill")}:'

PATTERN_SKILL_BACK_MAIN = fr'^{{{CALLBACK_KEY_LIST.index("skill_back")}:"main"'
PATTERN_SKILL_BACK_LIST_USE = fr'^{{{CALLBACK_KEY_LIST.index("skill_back")}:"list_use"'
PATTERN_SKILL_BACK_LIST_LEARN = fr'^{{{CALLBACK_KEY_LIST.index("skill_back")}:"list_learn"'
PATTERN_SKILL_BACK_LIST_UPGRADE = fr'^{{{CALLBACK_KEY_LIST.index("skill_back")}:"list_upgrade"'
PATTERN_SKILL_BACK_LIST_CLASSE = fr'^{{{CALLBACK_KEY_LIST.index("skill_back")}:"list_classe"'


# ALERT BUTTON TEXTS
ACCESS_DENIED = (
    f'⛔VOCÊ NÃO TEM ACESSO A ESSA ÁRVORE DE HABILIDADES⛔\n\n'
    f'Use o comando !{COMMANDS[0]} para acessar a SUA ÁRVORE.'
)
