from bot.functions.chat import CALLBACK_KEY_LIST
from constant.text import (
    SECTION_HEAD_MAGICAL_ATTACK_END,
    SECTION_HEAD_MAGICAL_ATTACK_START,
    SECTION_HEAD_PHYSICAL_ATTACK_END,
    SECTION_HEAD_PHYSICAL_ATTACK_START,
    SECTION_HEAD_PRECISION_ATTACK_END,
    SECTION_HEAD_PRECISION_ATTACK_START
)
from rpgram.enums import EmojiEnum


# TIME FOR ATTACK ALLY
MIN_MINUTES_FOR_ATTACK = 30
MAX_MINUTES_FOR_ATTACK = 50

# ACTIONS
CALLBACK_TEXT_DEFEND = 'defend'
CALLBACK_TEXT_ATTACK = 'attack'

# BUTTON TEXTS
DEFEND_BUTTON_TEXT = (
    f'{EmojiEnum.DEFEND.value}DEFENDER ALIADO{EmojiEnum.DEFEND.value}'
)
ATTACK_BUTTON_TEXT = (
    f'{EmojiEnum.ATTACK.value}ATACAR INIMIGO{EmojiEnum.ATTACK.value}'
)

# PATTERNS
PATTERN_DEFEND = (
    f'{{{CALLBACK_KEY_LIST.index("command")}:'
    f'"{CALLBACK_TEXT_DEFEND}"'
)
PATTERN_ATTACK = (
    f'{{{CALLBACK_KEY_LIST.index("command")}:'
    f'"{CALLBACK_TEXT_ATTACK}"'
)

# SECTION_TEXT
SECTION_TEXT_AMBUSH = 'EMBOSCADA'
SECTION_TEXT_AMBUSH_ATTACK = 'ATAQUE EMBOSCADA'
SECTION_TEXT_AMBUSH_COUNTER = 'CONTRA EMBOSCADA'
SECTION_TEXT_AMBUSH_DEFENSE = 'DEFESA EMBOSCADA'
SECTION_TEXT_AMBUSH_XP = 'XP EMBOSCADA'
SECTION_TEXT_FAIL = 'EMBOSCADA FALHOU'

SECTION_START_DICT = {
    'Physical Attack': SECTION_HEAD_PHYSICAL_ATTACK_START,
    'Precision Attack': SECTION_HEAD_PRECISION_ATTACK_START,
    'Magical Attack': SECTION_HEAD_MAGICAL_ATTACK_START,
}
SECTION_END_DICT = {
    'Physical Attack': SECTION_HEAD_PHYSICAL_ATTACK_END,
    'Precision Attack': SECTION_HEAD_PRECISION_ATTACK_END,
    'Magical Attack': SECTION_HEAD_MAGICAL_ATTACK_END,
}

AMBUSH_TEXTS = [
    (
        'Enquanto cruzavam a densa floresta, um ruído estranho alertou o '
        'grupo, sinalizando uma emboscada iminente.'
    ),
    (
        'Na tranquila estrada montanhosa, a névoa espessa encobria o '
        'horizonte quando o ataque surpresa se desenrolou.'
    ),
    (
        'Em uma clareira iluminada pelo sol do meio-dia, sombras surgiram '
        'rapidamente ao redor do grupo, indicando a emboscada.'
    ),
    (
        'À beira do rio sereno, o murmúrio das águas foi abruptamente '
        'interrompido pelo som de arcos tensos, anunciando a emboscada '
        'imprevista.'
    ),
    (
        'Enquanto exploravam a antiga ruína, ruídos de passos se aproximando '
        'rapidamente denunciaram a emboscada.'
    ),
    (
        'Sob o céu estrelado, o silêncio noturno foi quebrado por ruídos '
        'suspeitos, revelando uma emboscada iminente.'
    ),
    (
        'Durante a jornada pelas terras áridas, uma rajada de vento trouxe '
        'consigo os sons de cavalos galopando, antecipando a emboscada.'
    ),
    (
        'No vilarejo aparentemente tranquilo, gritos de guerra repentinos '
        'anunciaram a emboscada dos invasores.'
    ),
    (
        'Na encruzilhada movimentada, a multidão dispersou-se em pânico '
        'quando uma emboscada surpresa se desencadeou.'
    ),
    (
        'Ao avançarem pelo pântano silencioso, bolhas borbulhantes indicaram '
        'a aproximação furtiva de inimigos na emboscada.'
    ),
    (
        'No desfiladeiro estreito, rochas caíram estrondosamente, revelando '
        'a emboscada nas alturas.'
    ),
    (
        'Em uma clareira verdejante, os sons pacíficos da natureza foram '
        'interrompidos pelo ruído de armadilhas ativadas na emboscada.'
    ),
    (
        'Ao se aventurarem pela estrada deserta, o céu se encheu de flechas, '
        'revelando uma emboscada dos arredores.'
    ),
    (
        'Enquanto desciam pelas escarpas íngremes, o estrondo de uma '
        'avalanche obscureceu os sons da emboscada que se aproximava.'
    ),
    (
        'No interior do castelo abandonado, sombras se moveram rapidamente, '
        'preparando uma emboscada para o grupo.'
    ),
    (
        'Nas águas calmas do lago, uma onda repentina de ataques submarinos '
        'indicou uma emboscada inesperada.'
    ),
    (
        'Sob as copas das árvores gigantes, um rugido distante ecoou, '
        'anunciando uma emboscada dos predadores da floresta.'
    ),
    (
        'No mercado movimentado da cidade, o barulho ensurdecedor de uma '
        'explosão revelou a emboscada armada.'
    ),
    (
        'No terreno árido do deserto, nuvens de areia surgiram, ocultando a '
        'abordagem sorrateira de uma emboscada.'
    ),
    (
        'Em uma caverna escura e úmida, os ecos dos passos inimigos se '
        'aproximando prenunciaram a emboscada.'
    ),
    (
        'Na fortaleza imponente, traiçoeiros corredores escondiam a '
        'aproximação silenciosa de uma emboscada.'
    ),
    (
        'Enquanto navegavam pelo rio calmo, setas voaram do horizonte, '
        'revelando a emboscada na margem.'
    ),
    (
        'Nas alturas das montanhas, o eco de um sinal de alerta foi ouvido, '
        'indicando a emboscada planejada.'
    ),
    (
        'Ao atravessarem a ponte desgastada, tábuas quebraram-se sob seus '
        'pés, mostrando uma emboscada armadilhada.'
    ),
    (
        'No vale vasto e aberto, os sons de um rugido distante anunciaram a '
        'aproximação de uma emboscada de feras selvagens.'
    ),
    (
        'Entre as ruínas ancestrais, as sombras dos inimigos se moveram '
        'rapidamente, preparando a emboscada.'
    ),
    (
        'No coração da floresta densa, sons misteriosos levaram a crer em '
        'uma emboscada iminente.'
    ),
    (
        'Em um campo florido, uma explosão de fogo interrompeu a '
        'tranquilidade, revelando a emboscada.'
    ),
    (
        'Na estrada deserta à noite, uma sequência de luzes inesperadas '
        'desencadeou uma emboscada surpresa.'
    ),
    (
        'À beira-mar sereno, um repentino agitar das águas prenunciou a '
        'chegada de uma emboscada naval.'
    ),
    (
        'No topo da colina, uma neblina densa ocultou a emboscada '
        'prestes a acontecer.'
    ),
    (
        'Enquanto avançavam pela passagem estreita, pedras rolaram do '
        'topo das montanhas, indicando uma emboscada.'
    ),
    (
        'Sob o sol escaldante do deserto, miragens desorientaram o grupo, '
        'facilitando a emboscada.'
    ),
    (
        'Durante a exploração das catacumbas, armadilhas mortais se ativaram, '
        'evidenciando a emboscada planejada.'
    ),
    (
        'Nas profundezas do labirinto, sons indecifráveis alertaram para a '
        'proximidade da emboscada.'
    ),
    (
        'Enquanto viajavam pelas estradas desconhecidas, um sinalizador '
        'brilhante revelou a emboscada à frente.'
    ),
    (
        'No acampamento tranquilo, sombras se moviam silenciosamente, '
        'preparando uma emboscada noturna.'
    ),
    (
        'Em uma clareira serena, o farfalhar das folhas denunciou a '
        'aproximação da emboscada.'
    ),
    (
        'Ao atravessarem a ponte estreita, cordas tensionadas revelaram '
        'uma emboscada à espreita.'
    ),
    (
        'No vale coberto de neblina, sons estranhos pairavam no ar, '
        'antecipando a emboscada iminente.'
    ),
    (
        'Enquanto exploravam as ruínas antigas, ruídos sinistros indicaram '
        'uma emboscada entre as sombras.'
    ),
    (
        'Nas montanhas gélidas, uma tempestade de neve encobriu a emboscada '
        'que se aproximava.'
    ),
    (
        'No palácio grandioso, corredores sinuosos escondiam a emboscada '
        'planejada.'
    ),
    (
        'Em um campo de batalha recente, restos do combate antecedente '
        'esconderam a emboscada que se aproximava.'
    ),
    (
        'Durante a travessia do rio caudaloso, uma correnteza repentina '
        'evidenciou a emboscada das margens.'
    ),
    (
        'Na clareira iluminada pela lua cheia, sombras sinistras indicaram a '
        'emboscada na penumbra.'
    ),
    (
        'Enquanto desciam pelas escarpas íngremes, pedras soltas alertaram '
        'para a emboscada nas alturas.'
    ),
    (
        'No terreno pantanoso, as águas agitadas indicaram a aproximação '
        'furtiva da emboscada.'
    ),
    (
        'Sob a chuva torrencial, trovões encobriram os sinais sonoros da '
        'emboscada eminente.'
    ),
    (
        'Nas planícies vastas, um véu de poeira escondeu a emboscada que se '
        'aproximava.'
    ),
    (
        'Em uma floresta encantada, sons etéreos revelaram a aproximação da '
        'emboscada sobrenatural.'
    ),
    (
        'No vale sombrio, a escuridão densa ocultava a emboscada prestes a '
        'acontecer.'
    ),
    (
        'Durante a caminhada pela ravina estreita, o eco de vozes distantes '
        'indicou uma emboscada planejada.'
    ),
    (
        'Enquanto seguiam a trilha sinuosa, sombras inquietantes prenunciaram '
        'a emboscada à frente.'
    ),
    (
        'Ao cruzarem o riacho sereno, ondulações suspeitas na água '
        'denunciaram a emboscada dos arredores.'
    ),
    (
        'No acampamento à noite, o farfalhar das folhas se transformou em '
        'sons de emboscada.'
    ),
    (
        'Entre as dunas do deserto, areia movediça sinalizou a emboscada '
        'iminente.'
    ),
    (
        'Ao explorarem a caverna escura, o arrepio na espinha alertou para a '
        'emboscada nas profundezas.'
    ),
    (
        'Nas estepes vastas, um rugido distante revelou a aproximação de uma '
        'emboscada de bestas selvagens.'
    ),
    (
        'Em uma vila tranquila, janelas se fecharam apressadamente, '
        'antecipando a emboscada iminente.'
    ),
    (
        'No coração da floresta encantada, sussurros inquietantes anunciaram '
        'a emboscada sobrenatural.'
    ),
    (
        'Ao atravessarem o campo aberto, o estampido de galhos quebrados '
        'indicou a emboscada na vegetação.'
    ),
    (
        'Na estrada esquecida, sinais de batalha antiga alertaram para a '
        'emboscada armada.'
    ),
    (
        'Enquanto avançavam pelo desfiladeiro estreito, um silêncio repentino '
        'pressagiou a emboscada nas alturas.'
    ),
    (
        'Sob o céu noturno estrelado, sons inaudíveis perturbaram a '
        'tranquilidade, revelando a emboscada iminente.'
    ),
    (
        'Durante a exploração das catacumbas, um pressentimento sinistro '
        'indicou a emboscada planejada.'
    ),
    (
        'Em uma clareira repleta de flores, o silêncio repentino prenunciou a '
        'emboscada à frente.'
    ),
    (
        'No topo da montanha nevada, a calmaria incomum anunciou a emboscada '
        'na imensidão branca.'
    ),
    (
        'Enquanto atravessavam o pântano enevoado, borbulhas na lama '
        'denunciaram a emboscada sorrateira.'
    ),
    (
        'Nas ruínas antigas, marcas estranhas no chão indicaram a emboscada '
        'nas sombras.'
    ),
    (
        'No acampamento tranquilo à noite, um farfalhar repentino alertou '
        'para a emboscada.'
    ),
    (
        'Ao explorarem a caverna escura, murmúrios assombrosos pressagiaram a '
        'emboscada nas profundezas.'
    ),
    (
        'Em meio aos campos de batalha passados, destroços espalhados '
        'ocultaram a emboscada que se aproximava.'
    ),
    (
        'No coração da floresta densa, um suspiro repentino alertou para a '
        'emboscada sorrateira.'
    ),
    (
        'Enquanto seguiam o rio calmo, uma ondulação suspeita na água revelou '
        'a emboscada dos arredores.'
    ),
    (
        'Nas montanhas rochosas, o eco estrondoso alertou para a emboscada '
        'planejada.'
    ),
    (
        'Em uma clareira ensolarada, sombras inquietantes indicaram a '
        'emboscada na luz do dia.'
    ),
    (
        'Durante a travessia do deserto árido, ilusões distorcidas '
        'prenunciaram a emboscada iminente.'
    ),
    (
        'Na estrada sinuosa, sinais de arapucas armadas alertaram para a '
        'emboscada nas trilhas.'
    ),
    (
        'Enquanto atravessavam uma densa floresta, o grupo foi surpreendido '
        'por flechas voando de todos os lados.'
    ),
    (
        'Ao chegarem a uma estreita garganta entre montanhas, uma horda de '
        'inimigos emergiu das sombras das rochas.'
    ),
    (
        'Durante a travessia de um pântano nebuloso, uma emboscada foi '
        'armada por criaturas emergindo das águas lamacentas.'
    ),
    (
        'No interior de uma antiga ruína, uma armadilha foi ativada, '
        'bloqueando a saída e revelando inimigos escondidos nas '
        'sombras.'
    ),
    (
        'Enquanto descansavam à beira de um rio tranquilo, foram cercados '
        'por uma investida sorrateira de arqueiros '
        'inimigos.'
    ),
    (
        'Ao adentrarem uma cidade abandonada, o silêncio foi quebrado por '
        'um ataque coordenado de adversários espreitando dos '
        'telhados.'
    ),
    (
        'Enquanto atravessavam um desfiladeiro, pedras foram lançadas de '
        'uma emboscada nas encostas das montanhas.'
    ),
    (
        'Ao passarem por um estreito desfiladeiro, foram confrontados por '
        'uma emboscada organizada por saqueadores.'
    ),
    (
        'Em meio a uma densa névoa na planície aberta, o grupo foi pego de '
        'surpresa por uma investida de cavalaria inimiga.'
    ),
    (
        'Durante uma tempestade intensa, inimigos emergiram das sombras da '
        'escuridão, pegando o grupo desprevenido.'
    ),
    (
        'No coração de uma densa floresta, armadilhas foram acionadas, '
        'prendendo-os enquanto inimigos avançavam.'
    ),
    (
        'Ao cruzarem uma ponte antiga e instável, uma emboscada foi '
        'preparada com arqueiros posicionados nas colinas ao '
        'redor.'
    ),
    (
        'Enquanto passavam por um campo aberto, uma emboscada foi lançada '
        'por inimigos escondidos entre as plantações.'
    ),
    (
        'Em uma estrada estreita, uma explosão surpreendeu o grupo, '
        'revelando uma emboscada com explosivos.'
    ),
    (
        'Durante uma passagem por um estreito desfiladeiro, inimigos '
        'surgiram de buracos nas paredes rochosas.'
    ),
    (
        'Ao explorarem uma caverna sombria, foram cercados por criaturas '
        'emergindo das sombras mais profundas.'
    ),
    (
        'Enquanto acampavam em uma clareira, uma chuva de flechas partiu do '
        'matagal ao redor.'
    ),
    (
        'Durante uma tempestade de areia no deserto, inimigos emergiram de '
        'dunas ocultas, surpreendendo o grupo.'
    ),
    (
        'No meio de um labirinto urbano, foram emboscados por uma gangue '
        'espreitando becos estreitos.'
    ),
    (
        'Enquanto seguiam por um riacho tranquilo, foram emboscados por '
        'arqueiros escondidos entre as árvores.'
    ),
    (
        'Ao explorarem uma mina abandonada, foram surpreendidos por '
        'emboscadores emergindo das sombras escuras.'
    ),
    (
        'Durante a travessia por um pântano, o grupo foi atacado por '
        'criaturas emergindo da vegetação aquática.'
    ),
    (
        'No interior de uma fortaleza abandonada, uma emboscada foi '
        'orquestrada por inimigos posicionados nas '
        'torres.'
    ),
    (
        'Enquanto exploravam uma praia deserta, uma emboscada foi lançada '
        'por piratas emergindo das cavernas.'
    ),
    (
        'Ao adentrarem uma caverna nebulosa, foram surpreendidos por '
        'inimigos escondidos entre as estalactites.'
    ),
    (
        'Durante a travessia de um campo aberto, uma emboscada foi armada '
        'por inimigos escondidos nas moitas.'
    ),
    (
        'Em uma passagem estreita nas montanhas, uma avalanche foi '
        'provocada, revelando uma emboscada preparada.'
    ),
    (
        'Ao seguirem por um caminho sinuoso, foram atacados por '
        'emboscadores posicionados nas curvas.'
    ),
    (
        'No interior de uma floresta densa, foram cercados por inimigos '
        'emergindo das copas das árvores.'
    ),
    (
        'Durante a travessia de um rio turbulento, inimigos emergiram das '
        'margens inundadas.'
    ),
    (
        'Em um vale escondido, o grupo foi emboscado por atiradores '
        'camuflados nas encostas.'
    ),
    (
        'Ao atravessarem um desfiladeiro estreito, foram emboscados por '
        'inimigos escondidos entre as rochas.'
    ),
    (
        'Em meio a uma neblina densa, o grupo foi surpreendido por '
        'emboscadores surgindo das sombras.'
    ),
    (
        'Durante a travessia de uma ponte frágil, uma armadilha foi '
        'ativada, isolando-os de inimigos emergentes.'
    ),
    (
        'Enquanto seguiam por uma trilha íngreme, foram atacados por '
        'emboscadores posicionados nas colinas.'
    ),
    (
        'No coração de um labirinto urbano, foram emboscados por uma gangue '
        'espreitando em vielas escuras.'
    ),
    (
        'Ao adentrarem uma caverna antiga, foram cercados por inimigos '
        'emergindo de túneis ocultos.'
    ),
    (
        'Durante a travessia de um bosque tranquilo, inimigos surgiram das '
        'sombras das árvores.'
    ),
    (
        'Em uma noite escura, foram surpreendidos por emboscadores '
        'emergindo da escuridão densa.'
    ),
    (
        'Enquanto acampavam em uma clareira, uma emboscada foi orquestrada '
        'por atiradores ocultos.'
    ),
    (
        'Durante a travessia de um campo aberto, uma emboscada foi '
        'preparada por inimigos escondidos nas moitas.'
    ),
    (
        'Ao explorarem uma mina abandonada, foram atacados por emboscadores '
        'emergindo das sombras escuras.'
    ),
    (
        'No interior de uma fortaleza abandonada, foram emboscados por '
        'inimigos posicionados nas muralhas.'
    ),
    (
        'Enquanto atravessavam um pântano, foram surpreendidos por '
        'criaturas emergindo da vegetação aquática.'
    ),
    (
        'Durante a travessia por um desfiladeiro, o grupo foi atacado por '
        'emboscadores escondidos entre as rochas.'
    ),
    (
        'Em uma passagem estreita nas montanhas, uma emboscada foi armada '
        'por inimigos espreitando nas encostas.'
    ),
    (
        'Ao seguirem por um caminho sinuoso, foram emboscados por '
        'emboscadores posicionados nas curvas.'
    ),
    (
        'No interior de uma floresta densa, uma emboscada foi preparada por '
        'inimigos emergindo das copas das árvores.'
    ),
    (
        'Durante a travessia de um rio turbulento, foram cercados por '
        'inimigos emergindo das margens.'
    ),
    (
        'Em um vale escondido, o grupo foi surpreendido por atiradores '
        'camuflados nas encostas.'
    ),
    (
        'Ao atravessarem um desfiladeiro estreito, foram emboscados por '
        'inimigos ocultos entre as rochas.'
    ),
    (
        'Em meio a uma neblina densa, foram atacados por emboscadores '
        'surgindo das sombras.'
    ),
    (
        'Durante a travessia de uma ponte frágil, uma armadilha foi '
        'ativada, isolando-os de emboscadores emergentes.'
    ),
    (
        'Enquanto seguiam por uma trilha íngreme, foram surpreendidos por '
        'inimigos posicionados nas colinas.'
    ),
    (
        'No coração de um labirinto urbano, foram emboscados por uma gangue '
        'espreitando em vielas escuras.'
    ),
    (
        'Ao adentrarem uma caverna antiga, foram cercados por emboscadores '
        'emergindo de túneis ocultos.'
    ),
    (
        'Durante a travessia de um bosque tranquilo, inimigos surgiram das '
        'sombras das árvores.'
    ),
    (
        'Em uma noite escura, foram atacados por emboscadores emergindo da '
        'escuridão densa.'
    ),
    (
        'Enquanto acampavam em uma clareira, uma emboscada foi orquestrada '
        'por atiradores ocultos.'
    ),
    (
        'Durante a travessia de um campo aberto, uma emboscada foi '
        'preparada por inimigos escondidos nas moitas.'
    ),
    (
        'Ao explorarem uma mina abandonada, foram emboscados por '
        'emboscadores emergindo das sombras escuras.'
    ),
    (
        'No interior de uma fortaleza abandonada, foram surpreendidos por '
        'inimigos posicionados nas muralhas.'
    ),
    (
        'Enquanto atravessavam um pântano, foram emboscados por criaturas '
        'emergindo da vegetação aquática.'
    ),
    (
        'Durante a travessia por um desfiladeiro, o grupo foi atacado por '
        'emboscadores escondidos entre as rochas.'
    ),
    (
        'Em uma passagem estreita nas montanhas, uma emboscada foi armada '
        'por inimigos espreitando nas encostas.'
    ),
    (
        'Ao seguirem por um caminho sinuoso, foram emboscados por '
        'emboscadores posicionados nas curvas.'
    ),
    (
        'No interior de uma floresta densa, uma emboscada foi preparada por '
        'inimigos emergindo das copas das árvores.'
    ),
    (
        'Durante a travessia de um rio turbulento, foram cercados por '
        'inimigos emergindo das margens.'
    ),
    (
        'Em um vale escondido, o grupo foi surpreendido por atiradores '
        'camuflados nas encostas.'
    ),
    (
        'Ao atravessarem um desfiladeiro estreito, foram emboscados por '
        'inimigos ocultos entre as rochas.'
    ),
    (
        'Em meio a uma neblina densa, foram atacados por emboscadores '
        'surgindo das sombras.'
    ),
    (
        'Durante a travessia de uma ponte frágil, uma armadilha foi '
        'ativada, isolando-os de emboscadores emergentes.'
    ),
    (
        'Enquanto seguiam por uma trilha íngreme, foram surpreendidos por '
        'inimigos posicionados nas colinas.'
    ),
    (
        'No coração de um labirinto urbano, foram emboscados por uma gangue '
        'espreitando em vielas escuras.'
    ),
    (
        'Ao adentrarem uma caverna antiga, foram cercados por emboscadores '
        'emergindo de túneis ocultos.'
    ),
    (
        'Durante a travessia de um bosque tranquilo, inimigos surgiram das '
        'sombras das árvores.'
    ),
    (
        'Em uma noite escura, foram atacados por emboscadores emergindo da '
        'escuridão densa.'
    ),
    (
        'Enquanto acampavam em uma clareira, uma emboscada foi orquestrada '
        'por atiradores ocultos.'
    ),
    (
        'Durante a travessia de um campo aberto, uma emboscada foi '
        'preparada por inimigos escondidos nas moitas.'
    ),
    (
        'Ao explorarem uma mina abandonada, foram emboscados por '
        'emboscadores emergindo das sombras escuras.'
    ),
    (
        'No interior de uma fortaleza abandonada, foram surpreendidos por '
        'inimigos posicionados nas muralhas.'
    ),
    (
        'Enquanto atravessavam um pântano, foram emboscados por criaturas '
        'emergindo da vegetação aquática.'
    ),
]
