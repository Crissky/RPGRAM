from bot.functions.chat import CALLBACK_KEY_LIST
from rpgram.enums import EmojiEnum


SELLER_NAME = 'Chrysus'
TOTAL_MEAN_LEVELS = 5
TOTAL_EQUIPMENTS = 35
TOTAL_CONSUMABLES = 100


# ACTIONS
CALLBACK_LEAVE_SHOP = 'LEAVE_SHOP'


# COMMANDS
COMMANDS = ['loja', 'shop', SELLER_NAME.lower()]
CANCEL_COMMANDS = ['cancel', 'close']


# ALERT BUTTON TEXTS
ACCESS_DENIED = (
    '⛔VOCÊ NÃO TEM ACESSO A ESSA LOJA⛔\n\n'
    f'Use o comando !{COMMANDS[0]} para acessar A 🉐LOJA.'
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
    f'Saudações, aventureiros! {SELLER_NAME} tem o prazer de anunciar que '
    'novos tesouros foram adicionados à nossa loja. '
    'Venham conferir as maravilhas que agora adornam nossas prateleiras!',
    f'{SELLER_NAME} saúda a todos! Temos o prazer de informar que nossa '
    'loja está repleta de novidades. '
    'Itens extraordinários aguardam por aqueles que desejam explorar o que '
    'de melhor há no mundo!',
    f'O vendedor {SELLER_NAME} tem uma emocionante revelação para todos os '
    'clientes! Novos itens foram cuidadosamente selecionados e agora estão '
    'disponíveis na loja. Venham descobrir o que preparamos para vocês!',
    f'{SELLER_NAME}, o comerciante sagaz, tem o prazer de informar que '
    'sua loja está reabastecida com uma variedade de itens recém-chegados. '
    'Não percam a chance de adquirir as últimas novidades do mercado!',
    f'Aqueles que buscam aventuras e riquezas, ouçam! A loja de {SELLER_NAME} '
    'acaba de receber uma entrega de itens incríveis. Não deixem de dar uma '
    'espiada e encontrar algo que potencialize suas habilidades!',
    f'{SELLER_NAME} cumprimenta os intrépidos exploradores! '
    'Uma seleção fresca de itens extraordinários está '
    'disponível agora em nossa loja. '
    'Venham conferir as novas adições e aprimorar suas jornadas!',
    f'{SELLER_NAME} tem o prazer de anunciar que sua loja foi agraciada '
    'com novos tesouros. Aventureiros, corram para descobrir as últimas '
    'adições que certamente serão de grande interesse para vocês!',
    f'Saudações, valentes heróis! {SELLER_NAME} tem o prazer de informar '
    'que uma série de novos itens foi adicionada à sua loja. '
    'Vocês estão convidados a explorar e encontrar algo que se '
    'alinhe com suas necessidades e desejos!',
    f'O vendedor {SELLER_NAME} tem uma notícia emocionante para compartilhar! '
    'A loja está agora repleta de itens recém-chegados. Venham conferir '
    'as maravilhas que esperam por vocês nas prateleiras!',
    f'{SELLER_NAME}, o mercador renomado, tem o orgulho de apresentar a '
    'todos os aventureiros a chegada de novos itens à sua loja. '
    'Não percam a chance de encontrar algo único e poderoso para '
    'suas futuras empreitadas!',
    f'A loja de {SELLER_NAME} está brilhando com novidades! Itens fresquinhos '
    'foram adicionados ao estoque. Aventureiros, não deixem de dar uma '
    'olhada e ver o que acabou de chegar para aprimorar suas jornadas!',
    f'Saudações, bravos aventureiros! {SELLER_NAME} anuncia com entusiasmo a '
    'chegada de novos produtos à sua loja. Se preparem para descobrir '
    'tesouros incríveis e melhorar suas habilidades com as últimas adições!',
    f'{SELLER_NAME}, o vendedor experiente, tem o prazer de compartilhar que '
    'sua loja foi renovada com itens excepcionais. Venham, exploradores, e '
    'descubram as maravilhas que agora estão disponíveis para vocês!',
    f'Novidades emocionantes na loja de {SELLER_NAME}! Itens únicos e '
    'poderosos aguardam por heróis destemidos. '
    'Não percam a oportunidade de adquirir algo especial '
    'para suas próximas jornadas!',
    f'{SELLER_NAME} cumprimenta os corajosos aventureiros com uma notícia '
    'empolgante! A loja foi abastecida com uma nova coleção de itens. '
    'Venham logo e encontrem algo que elevará suas '
    'experiências no mundo!',
    f'Saudações, intrépidos exploradores! {SELLER_NAME} tem o prazer de '
    'anunciar a chegada de novos produtos à sua loja. Estejam preparados '
    'para encontrar tesouros incríveis e aprimorar suas habilidades '
    'com as últimas adições!',
    f'A loja de {SELLER_NAME} está mais empolgante do que nunca! '
    'Itens fresquinhos e fascinantes agora estão disponíveis. '
    'Aventureiros, venham e descubram as oportunidades que '
    'esperam por vocês nas prateleiras!',
    f'{SELLER_NAME}, o hábil mercador, tem o prazer de informar que novos '
    'itens foram acrescentados à sua loja. Explore as opções e '
    'encontre algo que eleve o nível de suas aventuras!',
    f'{SELLER_NAME} saúda todos os aventureiros com uma notícia emocionante! '
    'A loja agora exibe novos tesouros. Não percam a chance de encontrar '
    'algo especial para suas jornadas épicas!',
    f'Novidades quentes na loja de {SELLER_NAME}! Itens excepcionais foram '
    'recentemente adicionados. Aventureiros, corram para conferir e '
    'adquirir algo que fará toda a diferença em suas futuras conquistas!',
    'Prezados aventureiros, é com grande alegria que informo a chegada de '
    f'novos tesouros à loja {SELLER_NAME}! Venham explorar as '
    'maravilhas que acabaram de chegar e encontrem o equipamento '
    'perfeito para as suas jornadas.',
    f'Olar, bravos exploradores! {SELLER_NAME} tem o prazer de anunciar '
    'que uma nova leva de itens extraordinários acaba de chegar à loja. '
    'Visitem-nos e descubram as maravilhas que estão esperando por vocês!',
    f'Atenção, nobres clientes! {SELLER_NAME} tem o orgulho de apresentar '
    'as últimas adições ao nosso catálogo. Visitem-nos agora e encontrem '
    'os artefatos que tornarão suas aventuras ainda mais grandiosas.',
    f'Salve, aventureiros destemidos! A loja {SELLER_NAME} recebeu uma '
    'entrega especial de itens únicos e poderosos. Corram até aqui para '
    'garantir suas escolhas e preparar-se para os desafios que virão!',
    f'{SELLER_NAME} cumprimenta seus clientes com a notícia emocionante '
    'de que novas mercadorias acabaram de chegar! Descubram os tesouros '
    'recém-adquiridos e escolham os itens que se alinham com seus destinos.',
    f'A todos os corajosos viajantes, a loja {SELLER_NAME} tem o prazer '
    'de anunciar a chegada de novos estoques! Não percam a oportunidade '
    'de conferir as novidades e elevar seus equipamentos a um novo patamar.',
    f'Saudações, aventureiros audaciosos! {SELLER_NAME} tem o prazer de '
    'informar que nossa seleção foi ampliada com itens incríveis. '
    'Visitem-nos agora e preparem-se para conquistar terras '
    'desconhecidas com estilo!',
    f'Para todos os que buscam o extraordinário, a loja {SELLER_NAME} '
    'tem algo especial para vocês! Acabamos de receber novos itens que '
    'certamente irão encantar e fortalecer sua jornada. '
    'Venham dar uma olhada!',
    f'Atenção, heróis destemidos! {SELLER_NAME} tem o prazer de anunciar '
    'a chegada de itens exclusivos que podem mudar o rumo de suas aventuras. '
    'Visitem-nos e deixem-se maravilhar pela qualidade incomparável.',
    'Olá, intrépidos exploradores! Grandes novidades chegaram à loja '
    f'{SELLER_NAME}, aguardando para serem descobertas por aqueles que '
    'buscam a excelência. Venham agora e escolham entre as últimas '
    'adições ao nosso inventário!',
    f'{SELLER_NAME} acaba de receber uma entrega repleta de itens '
    'fascinantes e poderosos. Aventureiros, não percam a chance de '
    'conferir essas maravilhas que certamente transformarão suas jornadas!',
    'Caros clientes, é com grande satisfação que informo que a loja '
    f'{SELLER_NAME} está repleta de novos itens que acabaram de chegar. '
    'Visitem-nos agora e explorem as opções que podem aprimorar suas '
    'habilidades e aparência!',
    f'Bem-vindos, nobres viajantes! {SELLER_NAME} tem a honra de '
    'apresentar os mais recentes acréscimos à nossa seleção de mercadorias. '
    'Venham nos visitar e descubram os tesouros que podem ser seus!',
    f'Prezados aventureiros, a loja {SELLER_NAME} tem o privilégio de '
    'anunciar a chegada de novas mercadorias excepcionais. Venham conferir '
    'as últimas adições ao nosso inventário e preparem-se '
    'para grandes conquistas!',
    f'Saudações, heróis destemidos! {SELLER_NAME} tem o prazer de '
    'informar que nossa loja foi renovada com itens de alta qualidade. '
    'Visitem-nos agora e escolham entre as novidades que podem '
    'impulsionar sua jornada.',
    f'Atenção, bravos guerreiros! {SELLER_NAME} tem o prazer de apresentar '
    'os mais recentes tesouros em nosso acervo. Corram até aqui e descubram '
    'os itens que podem fazer toda a diferença em suas futuras batalhas.',
    f'Olar, aventureiros corajosos! A loja {SELLER_NAME} está radiante com a '
    'chegada de novos itens imperdíveis. Não deixem de nos visitar e '
    'conferir as opções que podem elevar suas habilidades a um novo patamar.',
    f'Caros clientes, a loja {SELLER_NAME} recebeu uma carga especial de '
    'itens únicos e empolgantes. Visitem-nos agora para explorar as '
    'últimas adições ao nosso catálogo e encontrar os companheiros '
    'perfeitos para suas jornadas.',
    f'Bem-vindos, nobres aventureiros! {SELLER_NAME} tem o prazer de '
    'anunciar a chegada de novos tesouros à nossa loja. Venham agora e '
    'descubram os artefatos que podem tornar suas missões ainda mais épicas.',
    f'Para todos os buscadores de maravilhas, {SELLER_NAME} tem o '
    'privilégio de apresentar os itens mais recentes e exclusivos '
    'em nossa loja. Corram até aqui e escolham entre as últimas adições '
    'que podem moldar o destino de suas aventuras.',
]

REPLY_TEXT_NO_HAVE_ITEMS = [
    f'A loja {SELLER_NAME} ainda não tem itens disponíveis. '
    'Por favor, volte mais tarde.',
    'Oh, nobre aventureiro, lamentavelmente estamos temporariamente '
    'esgotados de estoque. Pedimos desculpas pela inconveniência e '
    'sugerimos que retorne '
    'mais tarde para conferir nossas novas mercadorias.',
    'Caro cliente, infelizmente estamos com nossas prateleiras vazias no '
    'momento. Pedimos desculpas e contamos com sua compreensão. Volte em '
    'breve para descobrir nossas novas aquisições.',
    f'Aventureiro valente, {SELLER_NAME} se desculpa por não ter mais itens '
    'disponíveis no momento. Por favor, aceite nossas desculpas e volte mais '
    'tarde para encontrar tesouros frescos em nossa loja.',
    'Caríssimo cliente, estamos temporariamente sem estoque para oferecer a '
    'você. Pedimos desculpas pelo transtorno e esperamos sua compreensão. '
    'Não deixe de voltar quando tivermos mais novidades!',
    'Oh, explorador intrépido, lamentamos informar que nossos estoques estão '
    'vazios neste momento. Pedimos desculpas e sugerimos que volte em breve '
    'para conferir as novidades que teremos para você.',
    f'Nobre aventureiro, {SELLER_NAME} expressa sinceras desculpas pela falta '
    'de itens neste momento. Esperamos contar com sua paciência e '
    'pedimos que retorne mais tarde para descobrir as '
    'novas maravilhas em nossa loja.',
    'Cliente valioso, estamos temporariamente sem mercadorias para oferecer. '
    'Pedimos desculpas pelo inconveniente e aguardamos ansiosos para '
    'recebê-lo novamente quando tivermos novos itens em estoque.',
    f'Prezado aventureiro, {SELLER_NAME} lamenta informar que estamos '
    'temporariamente sem produtos. Pedimos desculpas e sugerimos que retorne '
    'mais tarde para conferir as incríveis adições que teremos em breve.',
    'Oh, destemido explorador, lamentamos dizer que nossas prateleiras estão '
    'vazias no momento. Aceite nossas desculpas e volte em breve para '
    'encontrar itens empolgantes em sua próxima visita.',
    'Caro cliente, nossos estoques estão temporariamente esgotados. '
    'Pedimos desculpas pelo transtorno e esperamos que compreenda. '
    'Conte conosco para novas surpresas quando retornar.',
    f'Nobre aventureiro, {SELLER_NAME} pede desculpas pela falta de itens '
    'disponíveis agora. Agradecemos sua compreensão e convidamos você a '
    'voltar mais tarde para explorar nossos novos achados.',
    'Caríssimo cliente, nossos estoques estão temporariamente esgotados, '
    'pedimos desculpas pelo inconveniente. Esteja certo de que estamos '
    'trabalhando para trazer novas maravilhas em breve. Volte e confira!',
    'Oh, bravos exploradores, lamentamos informar que nossas mercadorias se '
    'esgotaram momentaneamente. Pedimos desculpas e esperamos recebê-los '
    'novamente quando tivermos mais itens à disposição.',
    f'Aventureiro corajoso, {SELLER_NAME} se desculpa por não ter mais itens '
    'no momento. Agradecemos por sua compreensão e aguardamos sua próxima '
    'visita, quando teremos novidades fresquinhas para oferecer.',
    'Cliente valioso, infelizmente estamos temporariamente sem estoque. '
    'Pedimos desculpas pelo transtorno e contamos com sua paciência. '
    'Esteja certo de que voltaremos com novidades emocionantes.',
    f'Prezado aventureiro, {SELLER_NAME} sente muito por não ter mais itens '
    'disponíveis neste momento. Pedimos desculpas e convidamos '
    'você a retornar em breve para explorar os novos '
    'tesouros que teremos em estoque.',
    'Oh, destemidos exploradores, lamentamos informar que nossos produtos '
    'estão temporariamente esgotados. Pedimos desculpas pelo inconveniente e '
    'esperamos recebê-los novamente em breve.',
    'Caro cliente, nossas prateleiras estão temporariamente vazias, e '
    f'{SELLER_NAME} pede desculpas por isso. Agradecemos sua compreensão '
    'e esperamos ansiosos por sua próxima visita, quando teremos novos '
    'itens para encantar você.',
    'Nobre aventureiro, lamentamos dizer que nossos estoques estão '
    'momentaneamente esgotados. Pedimos desculpas pelo transtorno '
    'e esperamos contar com sua visita '
    'em breve para conferir nossas novidades.',
    f'Caríssimo cliente, {SELLER_NAME} está temporariamente sem itens para '
    'oferecer. Pedimos desculpas pelo inconveniente e garantimos que estamos '
    'trabalhando para repor nosso estoque. Volte em breve para descobrir as '
    'surpresas que teremos para você.',
    f'Oh, bravos exploradores, {SELLER_NAME} sente muito por não ter mais '
    'itens disponíveis no momento. Pedimos desculpas e esperamos que '
    'retorne em breve para conferir os tesouros que em breve '
    'estarão em nossas prateleiras.',
    'Aventureiro corajoso, infelizmente estamos temporariamente sem estoque. '
    'Pedimos desculpas pelo transtorno e garantimos que estamos empenhados '
    'em trazer novidades emocionantes para você. Volte em breve!',
    'Cliente valioso, nossos produtos se esgotaram temporariamente, e '
    f'{SELLER_NAME} pede desculpas por isso. Agradecemos sua compreensão e '
    'aguardamos ansiosamente sua próxima visita, quando teremos '
    'novos itens para encantar você.',
    'Prezado aventureiro, lamentamos informar que estamos temporariamente '
    'sem produtos em estoque. Pedimos desculpas pelo inconveniente e '
    'convidamos você a voltar em breve para explorar as novas maravilhas '
    'que teremos para oferecer.',
    f'Oh, destemidos exploradores, {SELLER_NAME} sente muito por não ter '
    'is itens disponíveis neste momento. Pedimos desculpas e contamos '
    'com sua compreensão. Esteja certo de que trabalhamos para trazer '
    'novidades em breve.',
    'Caro cliente, nossos estoques estão temporariamente vazios, e '
    f'{SELLER_NAME} lamenta por isso. Pedimos desculpas pelo transtorno e '
    'esperamos contar com sua visita em breve, quando teremos '
    'novos tesouros para encantar você.',
    'Nobre aventureiro, infelizmente estamos temporariamente sem estoque. '
    'Pedimos desculpas e garantimos que estamos empenhados em trazer '
    'novidades emocionantes para você. Volte em breve e confira!',
    f'Caríssimo cliente, {SELLER_NAME} está temporariamente sem '
    'itens para oferecer. Pedimos desculpas pelo inconveniente e contamos '
    'com sua paciência. Esteja certo de que voltaremos com novidades '
    'incríveis para sua próxima visita.',
    'Oh, bravos exploradores, lamentamos dizer que nossos estoques '
    'estão momentaneamente esgotados. Pedimos desculpas pelo '
    'inconveniente e esperamos recebê-los novamente '
    'em breve para descobrir nossas novidades.',
    f'Aventureiro corajoso, {SELLER_NAME} sente muito por não ter mais itens '
    'disponíveis no momento. Pedimos desculpas e garantimos que estamos '
    'trabalhando duro para repor nosso estoque. Volte em breve e descubra as '
    'surpresas que teremos para você.',
]

if __name__ == '__main__':
    print(max(REPLY_TEXT_NO_HAVE_ITEMS, key=len))
