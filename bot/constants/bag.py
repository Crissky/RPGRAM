import re


# COMMANDS
COMMANDS = ['bolsa', 'bag', 'inventario']
CANCEL_COMMANDS = ['cancel', 'close']


ITEMS_PER_PAGE = 10


# ACTIONS
CALLBACK_CLOSE_BAG = 'CLOSE_BAG'
CALLBACK_TEXT_DESTROY_ITEM = '$destroy_item'
ESCAPED_CALLBACK_TEXT_DESTROY_ITEM = re.escape(CALLBACK_TEXT_DESTROY_ITEM)


# TEXTS
ACCESS_DENIED = (
    f'⛔VOCÊ NÃO TEM ACESSO A ESSA BOLSA⛔\n\n'
    f'Use o comando !{COMMANDS[0]} para acessar OS SEUS 🎒ITENS.'
)
