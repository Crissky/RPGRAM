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
    f'⛔VOCÊ NÃO TEM ACESSO A ESSA LOJA⛔\n\n'
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

REPLY_TEXT_NO_HAVE_ITEMS = [
    f'A loja {SELLER_NAME} ainda não tem itens disponíveis. '
    f'Por favor, volte mais tarde.',
    f'Oh, nobre aventureiro, lamentavelmente estamos temporariamente '
    f'esgotados de estoque. Pedimos desculpas pela inconveniência e '
    f'sugerimos que retorne '
    f'mais tarde para conferir nossas novas mercadorias.',
    f'Caro cliente, infelizmente estamos com nossas prateleiras vazias no '
    f'momento. Pedimos desculpas e contamos com sua compreensão. Volte em '
    f'breve para descobrir nossas novas aquisições.',
    f'Aventureiro valente, {SELLER_NAME} se desculpa por não ter mais itens '
    f'disponíveis no momento. Por favor, aceite nossas desculpas e volte mais '
    f'tarde para encontrar tesouros frescos em nossa loja.',
    f'Caríssimo cliente, estamos temporariamente sem estoque para oferecer a '
    f'você. Pedimos desculpas pelo transtorno e esperamos sua compreensão. '
    f'Não deixe de voltar quando tivermos mais novidades!',
    f'Oh, explorador intrépido, lamentamos informar que nossos estoques estão '
    f'vazios neste momento. Pedimos desculpas e sugerimos que volte em breve '
    f'para conferir as novidades que teremos para você.',
    f'Nobre aventureiro, {SELLER_NAME} expressa sinceras desculpas pela falta '
    f'de itens neste momento. Esperamos contar com sua paciência e '
    f'pedimos que retorne mais tarde para descobrir as '
    f'novas maravilhas em nossa loja.',
    f'Cliente valioso, estamos temporariamente sem mercadorias para oferecer. '
    f'Pedimos desculpas pelo inconveniente e aguardamos ansiosos para '
    f'recebê-lo novamente quando tivermos novos itens em estoque.',
    f'Prezado aventureiro, {SELLER_NAME} lamenta informar que estamos '
    f'temporariamente sem produtos. Pedimos desculpas e sugerimos que retorne '
    f'mais tarde para conferir as incríveis adições que teremos em breve.',
    f'Oh, destemido explorador, lamentamos dizer que nossas prateleiras estão '
    f'vazias no momento. Aceite nossas desculpas e volte em breve para '
    f'encontrar itens empolgantes em sua próxima visita.',
    f'Caro cliente, nossos estoques estão temporariamente esgotados. '
    f'Pedimos desculpas pelo transtorno e esperamos que compreenda. '
    f'Conte conosco para novas surpresas quando retornar.',
    f'Nobre aventureiro, {SELLER_NAME} pede desculpas pela falta de itens '
    f'disponíveis agora. Agradecemos sua compreensão e convidamos você a '
    f'voltar mais tarde para explorar nossos novos achados.',
    f'Caríssimo cliente, nossos estoques estão temporariamente esgotados, '
    f'e pedimos desculpas pelo inconveniente. Esteja certo de que estamos '
    f'trabalhando para trazer novas maravilhas em breve. Volte e confira!',
    f'Oh, bravos exploradores, lamentamos informar que nossas mercadorias se '
    f'esgotaram momentaneamente. Pedimos desculpas e esperamos recebê-los '
    f'novamente quando tivermos mais itens à disposição.',
    f'Aventureiro corajoso, {SELLER_NAME} se desculpa por não ter mais itens '
    f'no momento. Agradecemos por sua compreensão e aguardamos sua próxima '
    f'visita, quando teremos novidades fresquinhas para oferecer.',
    f'Cliente valioso, infelizmente estamos temporariamente sem estoque. '
    f'Pedimos desculpas pelo transtorno e contamos com sua paciência. '
    f'Esteja certo de que voltaremos com novidades emocionantes.',
    f'Prezado aventureiro, {SELLER_NAME} sente muito por não ter mais itens '
    f'disponíveis neste momento. Pedimos desculpas e convidamos '
    f'você a retornar em breve para explorar os novos '
    f'tesouros que teremos em estoque.',
    f'Oh, destemidos exploradores, lamentamos informar que nossos produtos '
    f'estão temporariamente esgotados. Pedimos desculpas pelo inconveniente e '
    f'esperamos recebê-los novamente em breve.',
    f'Caro cliente, nossas prateleiras estão temporariamente vazias, e '
    f'{SELLER_NAME} pede desculpas por isso. Agradecemos sua compreensão '
    f'e esperamos ansiosos por sua próxima visita, quando teremos novos '
    f'itens para encantar você.',
    f'Nobre aventureiro, lamentamos dizer que nossos estoques estão '
    f'momentaneamente esgotados. Pedimos desculpas pelo transtorno '
    f'e esperamos contar com sua visita '
    f'em breve para conferir nossas novidades.',
    f'Caríssimo cliente, {SELLER_NAME} está temporariamente sem itens para '
    f'oferecer. Pedimos desculpas pelo inconveniente e garantimos que estamos '
    f'trabalhando para repor nosso estoque. Volte em breve para descobrir as '
    f'surpresas que teremos para você.',
    f'Oh, bravos exploradores, {SELLER_NAME} sente muito por não ter mais '
    f'itens disponíveis no momento. Pedimos desculpas e esperamos que '
    f'retorne em breve para conferir os tesouros que em breve '
    f'estarão em nossas prateleiras.',
    f'Aventureiro corajoso, infelizmente estamos temporariamente sem estoque. '
    f'Pedimos desculpas pelo transtorno e garantimos que estamos empenhados '
    f'em trazer novidades emocionantes para você. Volte em breve!',
    f'Cliente valioso, nossos produtos se esgotaram temporariamente, e '
    f'{SELLER_NAME} pede desculpas por isso. Agradecemos sua compreensão e '
    f'aguardamos ansiosamente sua próxima visita, quando teremos '
    f'novos itens para encantar você.',
    f'Prezado aventureiro, lamentamos informar que estamos temporariamente '
    f'sem produtos em estoque. Pedimos desculpas pelo inconveniente e '
    f'convidamos você a voltar em breve para explorar as novas maravilhas '
    f'que teremos para oferecer.',
    f'Oh, destemidos exploradores, {SELLER_NAME} sente muito por não ter '
    f'mais itens disponíveis neste momento. Pedimos desculpas e contamos '
    f'com sua compreensão. Esteja certo de que trabalhamos para trazer '
    f'novidades em breve.',
    f'Caro cliente, nossos estoques estão temporariamente vazios, e '
    f'{SELLER_NAME} lamenta por isso. Pedimos desculpas pelo transtorno e '
    f'esperamos contar com sua visita em breve, quando teremos '
    f'novos tesouros para encantar você.',
    f'Nobre aventureiro, infelizmente estamos temporariamente sem estoque. '
    f'Pedimos desculpas e garantimos que estamos empenhados em trazer '
    f'novidades emocionantes para você. Volte em breve e confira!',
    f'Caríssimo cliente, {SELLER_NAME} está temporariamente sem '
    f'itens para oferecer. Pedimos desculpas pelo inconveniente e contamos '
    f'com sua paciência. Esteja certo de que voltaremos com novidades '
    f'incríveis para sua próxima visita.',
    f'Oh, bravos exploradores, lamentamos dizer que nossos estoques '
    f'estão momentaneamente esgotados. Pedimos desculpas pelo '
    f'inconveniente e esperamos recebê-los novamente '
    f'em breve para descobrir nossas novidades.',
    f'Aventureiro corajoso, {SELLER_NAME} sente muito por não ter mais itens '
    f'disponíveis no momento. Pedimos desculpas e garantimos que estamos '
    f'trabalhando duro para repor nosso estoque. Volte em breve e descubra as '
    f'surpresas que teremos para você.',
]

if __name__ == '__main__':
    print(max(REPLY_TEXT_NO_HAVE_ITEMS, key=len))
