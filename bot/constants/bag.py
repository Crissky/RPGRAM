import re
from bot.functions.chat import CALLBACK_KEY_LIST
from rpgram.consumables import (
    CureConsumable,
    HealingConsumable,
    ReviveConsumable
)

from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.trocado import TrocadoEnum


ALL_RESTORE_CONSUMABLES_TUPLE = (
    CureConsumable,
    HealingConsumable,
    ReviveConsumable
)

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
SECTION_TEXT_TROCADO_POUCH = f'BOLSA DE {TrocadoEnum.TROCADO.value}'.upper()
SECTION_TEXT_GEMSTONE = f'PEDRA PRECIOSA'
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
COLLECT_MANY_BUTTON_TEXT = (
    f'{EmojiEnum.TROCADO_POUCH.value}Coletar x{{quantity_option}}'
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


CHRYSUS_EQUIPMENT_SELL = [
    'Ah, que item incrível! Este equipamento é realmente magnífico. Agradeço de coração pela generosidade!',
    'Não consigo expressar o quanto estou grato por este equipamento. Com certeza, será de grande utilidade em nossas jornadas.',
    'Uau, que surpresa maravilhosa! Muito obrigado por esse equipamento incrível. Mal posso esperar para testá-lo em campo!',
    'Estou verdadeiramente agradecido por este item. Este equipamento será uma adição valiosa às minhas habilidades durante as aventuras.',
    'Incrível! Este é exatamente o equipamento que eu precisava. Agradeço sinceramente por pensar em mim dessa maneira.',
    'É difícil expressar o quanto isso significa para mim. Agradeço do fundo do coração por este equipamento excepcional.',
    'Este equipamento é simplesmente espetacular. Muito obrigado por essa incrível contribuição à minha jornada.',
    'Que generosidade! Este é um equipamento excepcional e fico profundamente agradecido por tê-lo recebido de você.',
    'Não estava esperando algo assim! Agradeço imensamente por esse equipamento valioso. Será de grande ajuda nas nossas futuras empreitadas.',
    'Estou verdadeiramente emocionado com este item. Muito obrigado por proporcionar um equipamento tão excepcional.',
    'É incrível como esse equipamento se encaixa perfeitamente nas minhas necessidades. Agradeço de coração por esse gesto tão generoso.',
    'Este é um dos melhores items que já recebi! Sinto-me extremamente grato por ter recebido este equipamento excepcional de você.',
    'Agradeço imensamente pela consideração. Este equipamento é excepcional, e vou usá-lo com grande apreço nas minhas futuras jornadas.',
    'Nunca imaginei receber algo tão valioso! Muito obrigado por este equipamento incrível. Certamente fará a diferença em nossas aventuras.',
    'Não tenho palavras para expressar o quanto estou agradecido por este equipamento incrível. É um item verdadeiramente especial.',
    'Que gentileza a sua! Agradeço sinceramente por este equipamento excepcional. Estou ansioso para colocá-lo em uso nas nossas próximas missões.',
    'Você fez meu dia! Este equipamento é incrível, e agradeço do fundo do coração por tê-lo recebido de você.',
    'Agradeço por essa contribuição incrível. Este equipamento será uma peça fundamental nas minhas futuras jornadas. Obrigado!',
    'Não posso expressar o suficiente o quão grato estou por este item. Este equipamento é simplesmente fenomenal!',
    'Que surpresa maravilhosa! Agradeço do fundo do coração por esse equipamento excepcional. Vai fazer uma grande diferença nas nossas aventuras.',
    'Sua generosidade é incrível! Agradeço sinceramente por este equipamento excepcional. É um item que será lembrado por muito tempo.',
    'Estou emocionado com este equipamento incrível. Muito obrigado por pensar em mim dessa maneira. Sua generosidade é inestimável.',
    'Não esperava algo tão incrível! Este equipamento é realmente excepcional. Agradeço de todo o coração por essa maravilhosa contribuição.',
    'Que item incrível! Este equipamento superou todas as minhas expectativas. Agradeço sinceramente por essa generosidade inigualável.',
    'Estou verdadeiramente agradecido por esse gesto incrível. Este equipamento é espetacular, e vou usá-lo com grande gratidão.',
    'Agradeço imensamente por esse equipamento excepcional. Sua generosidade não passará despercebida nas nossas futuras jornadas.',
    'Não tenho palavras para expressar o quanto estou agradecido por este item. Este equipamento será fundamental nas nossas aventuras futuras.',
    'Estou profundamente tocado por este gesto de generosidade. Agradeço sinceramente por esse equipamento incrível que recebi de você.',
    'Que item surpreendente! Este equipamento é exatamente o que eu precisava. Agradeço do fundo do coração por essa incrível contribuição.',
    'Agradeço imensamente pela bondade de me agraciar com este equipamento excepcional. É uma dádiva que será lembrada com carinho.',
]
CHRYSUS_POTION_SELL = [
    'Muito obrigado por esse item! Sua generosidade será lembrada quando estivermos enfrentando desafios.',
    'Estou verdadeiramente grato por este item. Certamente será útil nas batalhas que estão por vir. Obrigado!',
    'Que presente valioso! Este item será uma bênção em nossas jornadas. Agradeço do fundo do coração.',
    'Sua contribuição não passou despercebida. Agradeço sinceramente por este item que certamente salvará nossas vidas.',
    'Que gentileza a sua! Este item é exatamente o que precisávamos. Agradeço por pensar na nossa saúde.',
    'Não posso expressar o quanto estou agradecido por este item. Será um recurso vital em nossas futuras batalhas. Obrigado!',
    'Agradeço imensamente por este item. Sua consideração pela nossa saúde é realmente admirável.',
    'Estou emocionado com esse presente. Este item será uma fonte de alívio nas situações mais difíceis. Muito obrigado!',
    'Muito obrigado por este item excepcional. Sua generosidade não passará despercebida durante nossas aventuras.',
    'Que gesto incrível! Este item será um salva-vidas quando mais precisarmos. Agradeço profundamente por isso.',
    'Estou profundamente agradecido por este item. Certamente será um recurso valioso para a nossa equipe. Obrigado!',
    'Agradeço sinceramente por este item vital. É reconfortante saber que temos aliados tão atenciosos em nossa jornada.',
    'Não esperava algo tão valioso! Este item será um tesouro em nossas aventuras. Agradeço de todo o coração.',
    'Que generosidade incrível! Este item é exatamente o que precisávamos para manter nossa equipe saudável. Obrigado!',
    'Sua atenção à nossa saúde não passa despercebida. Agradeço imensamente por este item. Será fundamental para nosso sucesso.',
    'Estou verdadeiramente grato por este item. Com certeza, fará toda a diferença nas nossas batalhas futuras. Obrigado!',
    'Que surpresa maravilhosa! Este item é um presente que será lembrado com carinho. Agradeço sinceramente.',
    'Muito obrigado por este item excepcional. Sua contribuição para nossa equipe é inestimável. Agradeço do fundo do coração.',
    'Agradeço profundamente por este item. Sua generosidade é uma luz em nosso caminho desafiador. Obrigado!',
    'Estou emocionado com este presente. Este item será uma ferramenta essencial para nossa sobrevivência. Agradeço sinceramente.',
    'Sua consideração pela nossa saúde é notável. Agradeço de todo o coração por este item que certamente nos será útil.',
    'Muito obrigado por este item. Sua atenção às nossas necessidades é verdadeiramente tocante. Agradeço sinceramente.',
    'Agradeço imensamente por este item valioso. É reconfortante saber que temos aliados tão prestativos em nossa equipe.',
    'Que generosidade incrível! Este item é uma dádiva que será lembrada nas nossas jornadas. Obrigado por pensar em nós.',
    'Estou verdadeiramente agradecido por este item. Certamente será um recurso vital em nossas futuras batalhas. Obrigado!',
    'Que presente surpreendente! Este item é um tesouro que será usado com sabedoria. Agradeço profundamente por isso.',
    'Sua contribuição para a nossa saúde não passou despercebida. Agradeço sinceramente por este item excepcional. Será fundamental para nosso sucesso.',
    'Muito obrigado por este item excepcional. Sua generosidade é uma luz em nosso caminho desafiador. Agradeço do fundo do coração.',
    'Estou emocionado com este presente. Este item será uma ferramenta essencial para nossa sobrevivência. Agradeço sinceramente.',
    'Sua consideração pela nossa saúde é notável. Agradeço de todo o coração por este item que certamente nos será útil.',
]
CHRYSUS_GEMSTONE_SELL = [
    'Que surpresa incrível! Esta pedra preciosa é verdadeiramente magnífica. Agradeço profundamente por esse presente brilhante.',
    'Estou emocionado com tanta beleza! Esta pedra preciosa é um tesouro que guardarei com apreço. Muito obrigado por essa dádiva radiante.',
    'Não consigo expressar o quanto estou grato por esta pedra preciosa deslumbrante. Sua generosidade é realmente reluzente. Obrigado!',
    'Uau, que presente incrível! Esta pedra preciosa é uma verdadeira joia. Agradeço sinceramente por esse tesouro cintilante.',
    'Sua escolha desta pedra preciosa é simplesmente deslumbrante. Estou profundamente agradecido por esse presente exuberante. Obrigado!',
    'Estou maravilhado com a beleza desta pedra preciosa. Sua generosidade brilha tanto quanto ela. Muito obrigado por este presente resplandecente.',
    'Que presente espetacular! Esta pedra preciosa é um verdadeiro achado. Agradeço do fundo do coração por esse tesouro deslumbrante.',
    'Não esperava algo tão precioso! Esta pedra é realmente única e bela. Agradeço sinceramente por essa joia rara e radiante.',
    'Estou encantado com a beleza desta pedra preciosa. Seu presente é como um raio de luz em meu dia. Muito obrigado por essa dádiva luminosa.',
    'Que presente extraordinário! Esta pedra preciosa é de uma beleza incomparável. Agradeço sinceramente por esse tesouro reluzente.',
    'Estou verdadeiramente agradecido por esta pedra preciosa deslumbrante. É um presente que brilha tanto quanto sua generosidade. Obrigado!',
    'Uma escolha magnífica! Esta pedra preciosa é um presente de valor inestimável. Agradeço profundamente por esse tesouro radiante.',
    'Que presente surpreendente! Esta pedra preciosa é realmente única. Sua generosidade é tão rara quanto este tesouro. Obrigado!',
    'Estou maravilhado com a beleza desta pedra preciosa. Seu presente é como uma estrela brilhando em minha jornada. Muito obrigado por essa dádiva cintilante.',
    'Que escolha esplêndida! Esta pedra preciosa é verdadeiramente deslumbrante. Agradeço sinceramente por esse tesouro resplandecente.',
    'Não tenho palavras para expressar minha gratidão por esta pedra preciosa. É um presente de beleza inigualável. Obrigado!',
    'Que surpresa incrível! Esta pedra preciosa é verdadeiramente magnífica. Agradeço profundamente por esse presente brilhante.',
    'Estou emocionado com tanta beleza! Esta pedra preciosa é um tesouro que guardarei com apreço. Muito obrigado por essa dádiva radiante.',
    'Não consigo expressar o quanto estou grato por esta pedra preciosa deslumbrante. Sua generosidade é realmente reluzente. Obrigado!',
    'Uau, que presente incrível! Esta pedra preciosa é uma verdadeira joia. Agradeço sinceramente por esse tesouro cintilante.',
    'Sua escolha desta pedra preciosa é simplesmente deslumbrante. Estou profundamente agradecido por esse presente exuberante. Obrigado!',
    'Estou maravilhado com a beleza desta pedra preciosa. Sua generosidade brilha tanto quanto ela. Muito obrigado por este presente resplandecente.',
    'Que presente espetacular! Esta pedra preciosa é um verdadeiro achado. Agradeço do fundo do coração por esse tesouro deslumbrante.',
    'Não esperava algo tão precioso! Esta pedra é realmente única e bela. Agradeço sinceramente por essa joia rara e radiante.',
    'Estou encantado com a beleza desta pedra preciosa. Seu presente é como um raio de luz em meu dia. Muito obrigado por essa dádiva luminosa.',
    'Que presente extraordinário! Esta pedra preciosa é de uma beleza incomparável. Agradeço sinceramente por esse tesouro reluzente.',
    'Estou verdadeiramente agradecido por esta pedra preciosa deslumbrante. É um presente que brilha tanto quanto sua generosidade. Obrigado!',
    'Uma escolha magnífica! Esta pedra preciosa é um presente de valor inestimável. Agradeço profundamente por esse tesouro radiante.',
    'Que presente surpreendente! Esta pedra preciosa é realmente única. Sua generosidade é tão rara quanto este tesouro. Obrigado!',
    'Estou maravilhado com a beleza desta pedra preciosa. Seu presente é como uma estrela brilhando em minha jornada. Muito obrigado por essa dádiva cintilante.',
]
CHRYSUS_OTHERS_SELL = [
    'Ah, que presente incrível! Este item é realmente excepcional. Muito obrigado pela generosidade!',
    'Estou verdadeiramente emocionado com este presente. Este item será de grande utilidade. Agradeço de coração!',
    'Que escolha maravilhosa! Este item é perfeito para minhas necessidades. Sua generosidade não tem igual. Obrigado!',
    'Não esperava algo tão valioso! Este item é uma verdadeira preciosidade. Agradeço sinceramente por essa dádiva especial.',
    'Uau, que surpresa incrível! Este item é incrivelmente útil. Estou profundamente agradecido por esse presente excepcional.',
    'Estou impressionado com a qualidade deste item. É realmente extraordinário. Obrigado por essa generosidade sem igual!',
    'Que presente espetacular! Este item é mais do que eu poderia imaginar. Muito obrigado por essa escolha fantástica!',
    'Não tenho palavras para expressar minha gratidão por este item. É simplesmente incrível. Agradeço do fundo do coração!',
    'Estou encantado com a praticidade deste item. Sua escolha foi perfeita. Agradeço sinceramente por essa dádiva excepcional.',
    'Que surpresa agradável! Este item é exatamente o que eu precisava. Sua generosidade é inigualável. Obrigado!',
    'Estou verdadeiramente agradecido por este item excepcional. É um presente de grande valor. Muito obrigado!',
    'Uma escolha fantástica! Este item é simplesmente incrível. Agradeço profundamente por essa generosidade notável.',
    'Que presente incrível! Este item é realmente excepcional. Muito obrigado pela generosidade!',
    'Estou verdadeiramente emocionado com este presente. Este item será de grande utilidade. Agradeço de coração!',
    'Que escolha maravilhosa! Este item é perfeito para minhas necessidades. Sua generosidade não tem igual. Obrigado!',
    'Não esperava algo tão valioso! Este item é uma verdadeira preciosidade. Agradeço sinceramente por essa dádiva especial.',
    'Uau, que surpresa incrível! Este item é incrivelmente útil. Estou profundamente agradecido por esse presente excepcional.',
    'Estou impressionado com a qualidade deste item. É realmente extraordinário. Obrigado por essa generosidade sem igual!',
    'Que presente espetacular! Este item é mais do que eu poderia imaginar. Muito obrigado por essa escolha fantástica!',
    'Não tenho palavras para expressar minha gratidão por este item. É simplesmente incrível. Agradeço do fundo do coração!',
    'Estou encantado com a praticidade deste item. Sua escolha foi perfeita. Agradeço sinceramente por essa dádiva excepcional.',
    'Que surpresa agradável! Este item é exatamente o que eu precisava. Sua generosidade é inigualável. Obrigado!',
    'Estou verdadeiramente agradecido por este item excepcional. É um presente de grande valor. Muito obrigado!',
    'Uma escolha fantástica! Este item é simplesmente incrível. Agradeço profundamente por essa generosidade notável.',
    'Que presente incrível! Este item é realmente excepcional. Muito obrigado pela generosidade!',
    'Estou verdadeiramente emocionado com este presente. Este item será de grande utilidade. Agradeço de coração!',
    'Que escolha maravilhosa! Este item é perfeito para minhas necessidades. Sua generosidade não tem igual. Obrigado!',
    'Não esperava algo tão valioso! Este item é uma verdadeira preciosidade. Agradeço sinceramente por essa dádiva especial.',
    'Uau, que surpresa incrível! Este item é incrivelmente útil. Estou profundamente agradecido por esse presente excepcional.',
    'Estou impressionado com a qualidade deste item. É realmente extraordinário. Obrigado por essa generosidade sem igual!',
]
