import re
from bot.functions.chat import CALLBACK_KEY_LIST

from rpgram.enums.emojis import EmojiEnum


# COMMANDS
COMMANDS = ['bolsa', 'bag', 'inventario']
CANCEL_COMMANDS = ['cancel', 'close']


# ITEMS CONSTANTS
SEND_DROP_MESSAGE_TIME_SLEEP = 1
ITEMS_PER_PAGE = 10
DROPUSE_MANY_MAX = 10
DROPUSE_QUANTITY_OPTION_LIST = [1, 3, 5, 10, 30, 50]


# SECTIONS TEXTs
SECTION_TEXT_CONSUMABLE = 'CONSUMÍVEL'
SECTION_TEXT_EQUIPMENT = 'EQUIPAMENTO'


# ACTIONS
CALLBACK_CLOSE_BAG = 'CLOSE_BAG'
CALLBACK_TEXT_DESTROY_ITEM = 'break_item'
CALLBACK_TEXT_SORT_ITEMS = '$sort_items'
ESCAPED_CALLBACK_TEXT_SORT_ITEMS = re.escape(CALLBACK_TEXT_SORT_ITEMS)


# PATTERNS
PATTERN_PAGE = fr'^{{{CALLBACK_KEY_LIST.index("page")}:'
PATTERN_ITEM = fr'^{{{CALLBACK_KEY_LIST.index("item")}:'
PATTERN_USE = fr'^{{{CALLBACK_KEY_LIST.index("use")}:'
PATTERN_DROP = fr'^{{{CALLBACK_KEY_LIST.index("drop")}:(1|3|5)'
PATTERN_SELL = fr'^{{{CALLBACK_KEY_LIST.index("sell")}:(1|3|5)'
PATTERN_IDENTIFY = fr'^{{{CALLBACK_KEY_LIST.index("identify")}:1'
PATTERN_SORT = fr'^{{{CALLBACK_KEY_LIST.index("sort")}:'
PATTERN_CLOSE_BAG = (
    f'{{{CALLBACK_KEY_LIST.index("command")}:"{CALLBACK_CLOSE_BAG}"'
)
PATTERN_SORT_ITEMS = (
    f'{{{CALLBACK_KEY_LIST.index("command")}:'
    f'"{ESCAPED_CALLBACK_TEXT_SORT_ITEMS}"'
)
PATTERN_DESTROY_ITEM = (
    f'{{{CALLBACK_KEY_LIST.index("act")}:"{CALLBACK_TEXT_DESTROY_ITEM}"'
)
PATTERN_GET_DROP = fr'^{{{CALLBACK_KEY_LIST.index("_id")}:'


# ALERT BUTTON TEXTS
ACCESS_DENIED = (
    f'⛔VOCÊ NÃO TEM ACESSO A ESSA BOLSA⛔\n\n'
    f'Use o comando !{COMMANDS[0]} para acessar OS SEUS 🎒ITENS.'
)
# ACTION BUTTON TEXTS
CLOSE_BAG_BUTTON_TEXT = f'Fechar Bolsa{EmojiEnum.CLOSE_BAG.value}'
DESTROY_ITEM_BUTTON_TEXT = f'Quebrar{EmojiEnum.DESTROY_ITEM.value}'
DISCARD_MANY_BUTTON_TEXT = (
    f'{EmojiEnum.DISCARD.value}Descartar x{{quantity_option}}'
)
SELL_MANY_BUTTON_TEXT = (
    f'{EmojiEnum.SELL.value}Vender x{{quantity_option}}'
)
EQUIP_BUTTON_TEXT = f'{EmojiEnum.TO_EQUIP.value}Equipar'
EQUIP_LEFT_BUTTON_TEXT = f'{EmojiEnum.LEFT.value}Equipar'
EQUIP_RIGHT_BUTTON_TEXT = f'Equipar{EmojiEnum.RIGHT.value}'
IDENTIFY_BUTTON_TEXT = f'Identificar{EmojiEnum.IDENTIFY.value}'
TAKE_BUTTON_TEXT = f'{EmojiEnum.TAKE.value}Coletar'
USE_MANY_BUTTON_TEXT = f'{EmojiEnum.USE_POTION.value}Usar x{{quantity_option}}'

# NAVIGATION BUTTON TEXTS
NAV_BACK_BUTTON_TEXT = f'Voltar{EmojiEnum.BACK.value}'
NAV_PREVIOUS_BUTTON_TEXT = f'{EmojiEnum.PREVIOUS_PAGE.value} Anterior'
NAV_NEXT_BUTTON_TEXT = f'Próxima {EmojiEnum.NEXT_PAGE.value}'
NAV_START_BUTTON_TEXT = f'{EmojiEnum.FIRST_PAGE.value} Primeira'
NAV_END_BUTTON_TEXT = f'Última {EmojiEnum.LAST_PAGE.value}'

# SORT BUTTON TEXTS
SORT_ITEMS_BUTTON_TEXT = f'{EmojiEnum.SORT_ITEMS.value}Ordenar'
CONSUMABLE_SORT_UP_BUTTON_TEXT = (
    f'Ordenar{EmojiEnum.CONSUMABLE.value}'
    f'{EmojiEnum.SORT_UP.value}'
)
CONSUMABLE_SORT_DOWN_BUTTON_TEXT = (
    f'Ordenar{EmojiEnum.CONSUMABLE.value}'
    f'{EmojiEnum.SORT_DOWN.value}'
)
EQUIPMENT_POWER_SORT_UP_BUTTON_TEXT = (
    f'Ordenar{EmojiEnum.EQUIPMENT_POWER.value}'
    f'{EmojiEnum.SORT_UP.value}'
)
EQUIPMENT_POWER_SORT_DOWN_BUTTON_TEXT = (
    f'Ordenar{EmojiEnum.EQUIPMENT_POWER.value}'
    f'{EmojiEnum.SORT_DOWN.value}'
)
EQUIPMENT_RARITY_SORT_UP_BUTTON_TEXT = (
    f'Ordenar{EmojiEnum.EQUIPMENT_RARITY.value}'
    f'{EmojiEnum.SORT_UP.value}'
)
EQUIPMENT_RARITY_SORT_DOWN_BUTTON_TEXT = (
    f'Ordenar{EmojiEnum.EQUIPMENT_RARITY.value}'
    f'{EmojiEnum.SORT_DOWN.value}'
)
