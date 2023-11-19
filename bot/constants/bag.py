import re

from rpgram.enums.emojis import EmojiEnum


# COMMANDS
COMMANDS = ['bolsa', 'bag', 'inventario']
CANCEL_COMMANDS = ['cancel', 'close']

# ITEMS CONSTANTS
ITEMS_PER_PAGE = 10
DROPUSE_MANY_MAX = 10
DROPUSE_QUANTITY_OPTION_LIST = [1, 3, 5, 10]


# ACTIONS
CALLBACK_CLOSE_BAG = 'CLOSE_BAG'
CALLBACK_TEXT_DESTROY_ITEM = '$destroy_item'
CALLBACK_TEXT_SORT_ITEMS = '$sort_items'
ESCAPED_CALLBACK_TEXT_DESTROY_ITEM = re.escape(CALLBACK_TEXT_DESTROY_ITEM)
ESCAPED_CALLBACK_TEXT_SORT_ITEMS = re.escape(CALLBACK_TEXT_SORT_ITEMS)


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
