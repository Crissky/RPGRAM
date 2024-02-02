from bot.functions.chat import CALLBACK_KEY_LIST
from rpgram.enums import EmojiEnum


SELLER_NAME = 'Chrysus'

TOTAL_MEAN_LEVELS = 5
TOTAL_EQUIPMENTS = 20
TOTAL_CONSUMABLES = 50


# ACTIONS
CALLBACK_LEAVE_SHOP = 'LEAVE_SHOP'


# COMMANDS
COMMANDS = ['loja', 'shop', SELLER_NAME.lower()]
CANCEL_COMMANDS = ['cancel', 'close']


# ALERT BUTTON TEXTS
ACCESS_DENIED = (
    f'⛔VOCÊ NÃO TEM ACESSO A ESSA LOJA⛔\n\n'
    f'Use o comando !{COMMANDS[0]} para acessar A 🛍️LOJA.'
)


# ACTION BUTTON TEXTS
LEAVE_SHOP_BUTTON_TEXT = f'{EmojiEnum.EXIT_SHOP.value}Deixar Loja'
BUY_MANY_BUTTON_TEXT = (
    f'{EmojiEnum.BUY.value}Comprar x{{quantity_option}}'
)


# PATTERNS
PATTERN_SELL_PAGE = fr'^{{{CALLBACK_KEY_LIST.index("sell_page")}:'
PATTERN_SELL_ITEM = fr'^{{{CALLBACK_KEY_LIST.index("sell_item")}:'
PATTERN_BUY = fr'^{{{CALLBACK_KEY_LIST.index("buy")}:'
PATTERN_LEAVE_SHOP = (
    f'{{{CALLBACK_KEY_LIST.index("command")}:"{CALLBACK_LEAVE_SHOP}"'
)

# TEXTS
SECTION_TEXT_SHOP = SELLER_NAME.upper()
NOT_ENOUGH_MONEY = 'Você não tem dinheiro suficiente para compra este item.'


REPLY_TEXT_NEW_ITEMS_ARRIVED = [
    f'Saudações, aventureiros! {SELLER_NAME} tem o prazer de anunciar que novos '
    f'tesouros foram adicionados à nossa loja. '
    f'Venham conferir as maravilhas que agora adornam nossas prateleiras!',
    f'{SELLER_NAME} saúda a todos! Temos o prazer de informar que nossa '
    f'loja está repleta de novidades. '
    f'Itens extraordinários aguardam por aqueles que desejam explorar o que '
    f'de melhor há no mundo!',
    f'O vendedor {SELLER_NAME} tem uma emocionante revelação para todos os '
    f'clientes! Novos itens foram cuidadosamente selecionados e agora estão '
    f'disponíveis na loja. Venham descobrir o que preparamos para vocês!',
    f'{SELLER_NAME}, o comerciante sagaz, tem o prazer de informar que '
    f'sua loja está reabastecida com uma variedade de itens recém-chegados. '
    f'Não percam a chance de adquirir as últimas novidades do mercado!',
    f'Aqueles que buscam aventuras e riquezas, ouçam! A loja de {SELLER_NAME} '
    f'acaba de receber uma entrega de itens incríveis. Não deixem de dar uma '
    f'espiada e encontrar algo que potencialize suas habilidades!',
    f'{SELLER_NAME} cumprimenta os intrépidos exploradores! '
    f'Uma seleção fresca de itens extraordinários está '
    f'disponível agora em nossa loja. '
    f'Venham conferir as novas adições e aprimorar suas jornadas!',
    f'{SELLER_NAME} tem o prazer de anunciar que sua loja foi agraciada '
    f'com novos tesouros. Aventureiros, corram para descobrir as últimas '
    f'adições que certamente serão de grande interesse para vocês!',
    f'Saudações, valentes heróis! {SELLER_NAME} tem o prazer de informar '
    f'que uma série de novos itens foi adicionada à sua loja. '
    f'Vocês estão convidados a explorar e encontrar algo que se '
    f'alinhe com suas necessidades e desejos!',
    f'O vendedor {SELLER_NAME} tem uma notícia emocionante para compartilhar! '
    f'A loja está agora repleta de itens recém-chegados. Venham conferir '
    f'as maravilhas que esperam por vocês nas prateleiras!',
    f'{SELLER_NAME}, o mercador renomado, tem o orgulho de apresentar a '
    f'todos os aventureiros a chegada de novos itens à sua loja. '
    f'Não percam a chance de encontrar algo único e poderoso para '
    f'suas futuras empreitadas!',
    f'A loja de {SELLER_NAME} está brilhando com novidades! Itens fresquinhos '
    f'foram adicionados ao estoque. Aventureiros, não deixem de dar uma '
    f'olhada e ver o que acabou de chegar para aprimorar suas jornadas!',
    f'Saudações, bravos aventureiros! {SELLER_NAME} anuncia com entusiasmo a '
    f'chegada de novos produtos à sua loja. Se preparem para descobrir '
    f'tesouros incríveis e melhorar suas habilidades com as últimas adições!',
    f'{SELLER_NAME}, o vendedor experiente, tem o prazer de compartilhar que '
    f'sua loja foi renovada com itens excepcionais. Venham, exploradores, e '
    f'descubram as maravilhas que agora estão disponíveis para vocês!',
    f'Novidades emocionantes na loja de {SELLER_NAME}! Itens únicos e '
    f'poderosos aguardam por heróis destemidos. '
    f'Não percam a oportunidade de adquirir algo especial '
    f'para suas próximas jornadas!',
    f'{SELLER_NAME} cumprimenta os corajosos aventureiros com uma notícia '
    f'empolgante! A loja foi abastecida com uma nova coleção de itens. '
    f'Venham logo e encontrem algo que elevará suas '
    f'experiências no mundo!',
    f'Saudações, intrépidos exploradores! {SELLER_NAME} tem o prazer de '
    f'anunciar a chegada de novos produtos à sua loja. Estejam preparados '
    f'para encontrar tesouros incríveis e aprimorar suas habilidades '
    f'com as últimas adições!',
    f'A loja de {SELLER_NAME} está mais empolgante do que nunca! '
    f'Itens fresquinhos e fascinantes agora estão disponíveis. '
    f'Aventureiros, venham e descubram as oportunidades que '
    f'esperam por vocês nas prateleiras!',
    f'{SELLER_NAME}, o hábil mercador, tem o prazer de informar que novos '
    f'itens foram acrescentados à sua loja. Explore as opções e '
    f'encontre algo que eleve o nível de suas aventuras!',
    f'{SELLER_NAME} saúda todos os aventureiros com uma notícia emocionante! '
    f'A loja agora exibe novos tesouros. Não percam a chance de encontrar '
    f'algo especial para suas jornadas épicas!',
    f'Novidades quentes na loja de {SELLER_NAME}! Itens excepcionais foram '
    f'recentemente adicionados. Aventureiros, corram para conferir e '
    f'adquirir algo que fará toda a diferença em suas futuras conquistas!',

    f'Prezados aventureiros, é com grande alegria que informo a chegada de '
    f'novos tesouros à loja {SELLER_NAME}! Venham explorar as '
    f'maravilhas que acabaram de chegar e encontrem o equipamento '
    f'perfeito para as suas jornadas.',
    f'Olar, bravos exploradores! {SELLER_NAME} tem o prazer de anunciar '
    f'que uma nova leva de itens extraordinários acaba de chegar à loja. '
    f'Visitem-nos e descubram as maravilhas que estão esperando por vocês!',
    f'Atenção, nobres clientes! {SELLER_NAME} tem o orgulho de apresentar '
    f'as últimas adições ao nosso catálogo. Visitem-nos agora e encontrem '
    f'os artefatos que tornarão suas aventuras ainda mais grandiosas.',
    f'Salve, aventureiros destemidos! A loja {SELLER_NAME} recebeu uma '
    f'entrega especial de itens únicos e poderosos. Corram até aqui para '
    f'garantir suas escolhas e preparar-se para os desafios que virão!',
    f'{SELLER_NAME} cumprimenta seus clientes com a notícia emocionante '
    f'de que novas mercadorias acabaram de chegar! Descubram os tesouros '
    f'recém-adquiridos e escolham os itens que se alinham com seus destinos.',
    f'A todos os corajosos viajantes, a loja {SELLER_NAME} tem o prazer '
    f'de anunciar a chegada de novos estoques! Não percam a oportunidade '
    f'de conferir as novidades e elevar seus equipamentos a um novo patamar.',
    f'Saudações, aventureiros audaciosos! {SELLER_NAME} tem o prazer de '
    f'informar que nossa seleção foi ampliada com itens incríveis. '
    f'Visitem-nos agora e preparem-se para conquistar terras '
    f'desconhecidas com estilo!',
    f'Para todos os que buscam o extraordinário, a loja {SELLER_NAME} '
    f'tem algo especial para vocês! Acabamos de receber novos itens que '
    f'certamente irão encantar e fortalecer sua jornada. '
    f'Venham dar uma olhada!',
    f'Atenção, heróis destemidos! {SELLER_NAME} tem o prazer de anunciar '
    f'a chegada de itens exclusivos que podem mudar o rumo de suas aventuras. '
    f'Visitem-nos e deixem-se maravilhar pela qualidade incomparável.',
    f'Olá, intrépidos exploradores! Grandes novidades chegaram à loja '
    f'{SELLER_NAME}, aguardando para serem descobertas por aqueles que '
    f'buscam a excelência. Venham agora e escolham entre as últimas '
    f'adições ao nosso inventário!',
    f'{SELLER_NAME} acaba de receber uma entrega repleta de itens '
    f'fascinantes e poderosos. Aventureiros, não percam a chance de '
    f'conferir essas maravilhas que certamente transformarão suas jornadas!',
    f'Caros clientes, é com grande satisfação que informo que a loja '
    f'{SELLER_NAME} está repleta de novos itens que acabaram de chegar. '
    f'Visitem-nos agora e explorem as opções que podem aprimorar suas '
    f'habilidades e aparência!',
    f'Bem-vindos, nobres viajantes! {SELLER_NAME} tem a honra de '
    f'apresentar os mais recentes acréscimos à nossa seleção de mercadorias. '
    f'Venham nos visitar e descubram os tesouros que podem ser seus!',
    f'Prezados aventureiros, a loja {SELLER_NAME} tem o privilégio de '
    f'anunciar a chegada de novas mercadorias excepcionais. Venham conferir '
    f'as últimas adições ao nosso inventário e preparem-se '
    f'para grandes conquistas!',
    f'Saudações, heróis destemidos! {SELLER_NAME} tem o prazer de '
    f'informar que nossa loja foi renovada com itens de alta qualidade. '
    f'Visitem-nos agora e escolham entre as novidades que podem '
    f'impulsionar sua jornada.',
    f'Atenção, bravos guerreiros! {SELLER_NAME} tem o prazer de apresentar '
    f'os mais recentes tesouros em nosso acervo. Corram até aqui e descubram '
    f'os itens que podem fazer toda a diferença em suas futuras batalhas.',
    f'Olar, aventureiros corajosos! A loja {SELLER_NAME} está radiante com a '
    f'chegada de novos itens imperdíveis. Não deixem de nos visitar e '
    f'conferir as opções que podem elevar suas habilidades a um novo patamar.',
    f'Caros clientes, a loja {SELLER_NAME} recebeu uma carga especial de '
    f'itens únicos e empolgantes. Visitem-nos agora para explorar as '
    f'últimas adições ao nosso catálogo e encontrar os companheiros '
    f'perfeitos para suas jornadas.',
    f'Bem-vindos, nobres aventureiros! {SELLER_NAME} tem o prazer de '
    f'anunciar a chegada de novos tesouros à nossa loja. Venham agora e '
    f'descubram os artefatos que podem tornar suas missões ainda mais épicas.',
    f'Para todos os buscadores de maravilhas, {SELLER_NAME} tem o '
    f'privilégio de apresentar os itens mais recentes e exclusivos '
    f'em nossa loja. Corram até aqui e escolham entre as últimas adições '
    f'que podem moldar o destino de suas aventuras.',
]
