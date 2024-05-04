from bot.functions.chat import CALLBACK_KEY_LIST
from constant.text import (
    SECTION_HEAD_MAGICAL_ATTACK_END,
    SECTION_HEAD_MAGICAL_ATTACK_START,
    SECTION_HEAD_PHYSICAL_ATTACK_END,
    SECTION_HEAD_PHYSICAL_ATTACK_START,
    SECTION_HEAD_PRECISION_ATTACK_END,
    SECTION_HEAD_PRECISION_ATTACK_START
)
from rpgram.enums import AlignmentEnum, EmojiEnum, EnemyStarsEnum


# TIME FOR ATTACK ALLY
MIN_MINUTES_TO_ATTACK = 60
MAX_MINUTES_TO_ATTACK = 90
MIN_MINUTES_TO_ATTACK_FROM_RANK_DICT = {
    EnemyStarsEnum.ONE.name: 30,
    EnemyStarsEnum.TWO.name: 40,
    EnemyStarsEnum.THREE.name: 50,
    EnemyStarsEnum.FOUR.name: 60,
    EnemyStarsEnum.FIVE.name: 70,
    EnemyStarsEnum.SUB_BOSS.name: 80,
    EnemyStarsEnum.BOSS.name: 90,
}
MAX_MINUTES_TO_ATTACK_FROM_RANK_DICT = {
    EnemyStarsEnum.ONE.name: 60,
    EnemyStarsEnum.TWO.name: 70,
    EnemyStarsEnum.THREE.name: 80,
    EnemyStarsEnum.FOUR.name: 90,
    EnemyStarsEnum.FIVE.name: 100,
    EnemyStarsEnum.SUB_BOSS.name: 110,
    EnemyStarsEnum.BOSS.name: 120,
}

ENEMY_CHANCE_TO_ATTACK_AGAIN_DICT = {
    EnemyStarsEnum.ONE.name: 0.40,
    EnemyStarsEnum.TWO.name: 0.50,
    EnemyStarsEnum.THREE.name: 0.60,
    EnemyStarsEnum.FOUR.name: 0.70,
    EnemyStarsEnum.FIVE.name: 0.80,
    EnemyStarsEnum.SUB_BOSS.name: 0.90,
    EnemyStarsEnum.BOSS.name: 0.95,
}


# ACTIONS
CALLBACK_TEXT_DEFEND = 'defend'
CALLBACK_TEXT_ATTACK = 'attack'
CALLBACK_TEXT_BASE_ATTRIBUTES = 'base_attr'
CALLBACK_TEXT_COMBAT_ATTRIBUTES = 'combat_attr'

# BUTTON TEXTS
ATTACK_BUTTON_TEXT = (
    f'{EmojiEnum.ATTACK.value}ATACAR'
)
DEFEND_BUTTON_TEXT = (
    f'DEFENDER{EmojiEnum.DEFEND.value}'
)
BASE_ATTRIBUTES_BUTTON_TEXT = (
    f'{EmojiEnum.BASE_ATTRIBUTES.value}ATR BASE'
)
COMBAT_ATTRIBUTES_BUTTON_TEXT = (
    f'ATR COMBATE{EmojiEnum.COMBAT_ATTRIBUTES.value}'
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
PATTERN_ATTRIBUTES = (
    f'{{{CALLBACK_KEY_LIST.index("command")}:'
    f'"({CALLBACK_TEXT_BASE_ATTRIBUTES}|'
    f'{CALLBACK_TEXT_COMBAT_ATTRIBUTES})"'
)

# SECTION_TEXT
SECTION_TEXT_AMBUSH = 'EMBOSCADA'
SECTION_TEXT_AMBUSH_ATTACK = 'ATAQUE EMBOSCADA'
SECTION_TEXT_AMBUSH_COUNTER = 'CONTRA EMBOSCADA'
SECTION_TEXT_FAIL_AMBUSH_COUNTER = 'CONTRA FALHOU'
SECTION_TEXT_AMBUSH_DEFENSE = 'DEFESA EMBOSCADA'
SECTION_TEXT_FAIL_AMBUSH_DEFENSE = 'DEFESA FALHOU'
SECTION_TEXT_AMBUSH_XP = 'XP EMBOSCADA'
SECTION_TEXT_FAIL = 'EMBOSCADA FALHOU'
SECTION_TEXT_FLEE = 'FUGIU'

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

COUNTER_LINES = {
    AlignmentEnum.ASSASSIN.name: [
        'Já era.',
        'Eu sou a morte.',
        'A morte é doce.',
        'Você não é nada.',
        'Descanse em paz.',
        'Seu tempo acabou.',
        'Tudo acaba agora.',
        'A morte é eterna.',
        'A morte te espera.',
        'Chegou a sua hora.',
        'Adeus, mundo cruel.',
        'Você nunca me verá.',
        'Aceite seu destino.',
        'A vingança é minha.',
        'Você está condenado.',
        'Diga adeus ao mundo.',
        'Você será esquecido.',
        'Apenas um corpo frio.',
        'A morte é silenciosa.',
        'A morte é inevitável.',
        'Você não sentirá dor.',
        'A morte é libertadora.',
        'A dor é o seu destino.',
        'A morte é o fim de tudo.',
        'Sinta a lâmina da morte.',
        'Você não passará de mim.',
        'Prometo que será rápido.',
        'A escuridão te consumirá.',
        'A morte é a única verdade.',
        'Você não é páreo para mim.',
        'A morte é a única certeza.',
        'Prepare-se para o inferno.',
        'Chegou a hora do julgamento.',
        'Você pagará por seus crimes.',
        'Você é apenas mais um inseto.',
        'A morte é sua única redenção.',
        'Sou a personificação da morte.',
        'Sofra como você me fez sofrer.',
        'Ninguém escapa da minha lâmina.',
        'A morte te espera ansiosamente.',
        'Você não verá o que te atingiu.',
        'Você não tem chance contra mim.',
        'Você foi um tolo em me desafiar.',
        'Eu sou a sombra que te assombra.',
        'Você não verá o próximo amanhecer.',
        'Você está livre de seu sofrimento.',
        'Você não pode escapar do seu destino.',
        'Você não pode lutar contra o destino.',
        'Você subestimou o poder de um assassino.',
        'Prepare-se para encontrar seus ancestrais.'
    ],
    AlignmentEnum.BERSERK.name: [
        'ABRAÇE A DOR!',
        'EU SOU A MORTE!',
        'A DOR É PRAZER!',
        'O CAOS REINARÁ!',
        'PROVE MEU PODER!',
        'NÃO HÁ SALVAÇÃO!',
        'EU SOU A VINGANÇA!',
        'NÃO HÁ ESCAPATÓRIA!',
        'SEU FIM SE APROXIMA!',
        'EU SOU A DESTRUIÇÃO!',
        'NÃO HÁ LUZ NA MORTE!',
        'EU SOU A VERDADE CRU!',
        'EU SOU A FOME ETERNA!',
        'A DOR É A ÚNICA VIDA!',
        'EU SOU A IRA DE DEUS!',
        'EU SOU A MORTE ETERNA!',
        'EU SOU O CICLO ETERNO!',
        'EU SOU O VAZIO ETERNO!',
        'SEU DESTINO É A MORTE!',
        'PREPARE-SE PARA MORRER!',
        'SINTA A MINHA VINGANÇA!',
        'NÃO HÁ LUGAR PARA MEDO!',
        'PREPARE-SE PARA SOFRER!',
        'EU SOU A LOUCURA ETERNA!',
        'A DOR É A ÚNICA VERDADE!',
        'EU SOU A MORTE ENCARNADA!',
        'NÃO HÁ FUGA DO MEU FÚRIA!',
        'A DOR É A ÚNICA SANIDADE!',
        'A DOR É O ÚNICO ALIMENTO!',
        'EU SOU O PESADELO ETERNO!',
        'A DOR É A ÚNICA CONSTANTE!',
        'A DOR É A ÚNICA REALIDADE!',
        'EU SOU A TERNIDADE DA DOR!',
        'NÃO HÁ PAZ PARA OS ÍMPIOS!',
        'PREPARE-SE PARA O INFERNO!',
        'SEU DESTINO É A ESCURIDÃO!',
        'EU SOU A FÚRIA DA NATUREZA!',
        'NÃO HÁ ESCAPATÓRIA DA FOME!',
        'A DOR É A ÚNICA EXISTÊNCIA!',
        'NÃO HÁ ESCAPATÓRIA DO VAZIO!',
        'NÃO HÁ MERCÊ PARA OS FRACOS!',
        'NÃO HÁ ESCAPATÓRIA DA MORTE!',
        'NÃO HÁ ESCAPATÓRIA DO CICLO!',
        'PREPARE-SE PARA ENLOUQUECER!',
        'SEU SANGUE MANCHARÁ A TERRA!',
        'O SANGUE SERÁ SEU PAGAMENTO!',
        'NÃO HÁ FUTURO PARA OS FRACOS!',
        'PREPARE-SE PARA SER DEVORADO!',
        'A MORTE É A ÚNICA LIBERTAÇÃO!',
        'NÃO HÁ ESCAPATÓRIA DA VERDADE!',
        'NÃO HÁ ESCAPATÓRIA DA LOUCURA!',
        'PREPARE-SE PARA SER CONSUMIDO!',
        'NÃO HÁ LUGAR PARA ESCONDER-SE!',
        'NÃO HÁ ESCAPATÓRIA DO PESADELO!',
        'NÃO HÁ ESCAPATÓRIA DA REALIDADE!',
        'PREPARE-SE PARA SER PRESO NA DOR!',
        'PREPARE-SE PARA ENFRENTAR A REALIDADE!',
        'PREPARE-SE PARA SER PERDIDO NO PESADELO!',
        'PREPARE-SE PARA SER DEVORADO PELO VAZIO!',
        'PREPARE-SE PARA MORRER DE NOVO E DE NOVO!',
        'PREPARE-SE PARA SER DESPERTADO PARA A VERDADE!'
    ],
    AlignmentEnum.CAREGIVER.name: [
        'Pare com isso agora!',
        'A esperança nunca morre!',
        'Ninguém vai se machucar!',
        'Lute com bravura e honra!',
        'Afaste-se dos meus amigos!',
        'Lute com honra e dignidade!',
        'Eu protegerei os inocentes!',
        'Lute com bravura e coragem!',
        'A justiça sempre será feita!',
        'O futuro está em nossas mãos!',
        'Nunca perca a fé em si mesmo!',
        'Acredite no poder da sua voz!',
        'O bem sempre triunfa no final!',
        'Nunca desista dos seus sonhos!',
        'O futuro é o que você faz dele!',
        'Não tenha medo de ser diferente!',
        'O perdão é o caminho para a cura!',
        'A compaixão é a chave para a paz!',
        'Eu não vou deixar você fazer isso!',
        'Você não vai machucar ninguém aqui!',
        'Você não pode escapar do seu destino!',
        'O perdão é o caminho para a redenção!',
        'A força da verdade sempre prevalecerá!',
        'Acredite em si mesmo, você pode vencer!',
        'Prepare-se para enfrentar a sua derrota!',
        'Juntos, vamos superar qualquer obstáculo!',
        'A paz é o único caminho para a felicidade!',
        'Juntos, podemos construir um mundo melhor!',
        'Não tenha medo de enfrentar seus desafios!',
        'O amor é a força mais poderosa do universo!',
        'Você está enganado, o caminho certo é outro!',
        'Eu vou te mostrar o que é a verdadeira força!',
        'Não vamos desistir, a esperança ainda existe!',
        'A esperança é a luz que nos guia na escuridão!',
        'A força da amizade é capaz de mover montanhas!',
        'Lembre-se sempre do que você realmente importa!',
        'O poder da compaixão é maior que qualquer arma!',
        'Eu vou te mostrar o verdadeiro significado do amor!',
        'Chega de teorias da conspiração, vamos resolver isso!',
        'A força da mente é capaz de superar qualquer obstáculo!',
        'Acredite em si mesmo e você poderá conquistar qualquer coisa!',
        'Nunca desista dos seus sonhos, mesmo que pareçam impossíveis!'
    ],
    AlignmentEnum.PROTECTOR.name: [
        'Experimente isso!',
        'Você não passará!',
        'Você não me assusta!',
        'A justiça será feita!',
        'O bem sempre triunfa!',
        'Nem pense em me ferir!',
        'Eu nunca vou desistir!',
        'Você não me machucará!',
        'Eu sou a força do bem!',
        'Você não pode me vencer!',
        'Meu escudo é invencível!',
        'Proteger e contra-atacar!',
        'Chegou a hora do seu fim!',
        'Eu nunca me curvo ao mal!',
        'A coragem é a minha arma!',
        'Você não é páreo para mim!',
        'A justiça sempre prevalece!',
        'Minha vontade é inabalável!',
        'Meus poderes te protegerão!',
        'Nunca perca a fé na justiça!',
        'Que a paz reine neste mundo!',
        'Prepare-se para o meu poder!',
        'Você não vai escapar impune!',
        'Eu sou o escudo contra o mal!',
        'Meus aliados precisam de mim!',
        'Prepare-se para a minha fúria!',
        'Obrigado por lutar ao meu lado!',
        'A luz sempre vence a escuridão!',
        'Você vai pagar por seus crimes!',
        'Chega de conversa, vamos lutar!',
        'Um novo amanhecer está chegando!',
        'Juntos, podemos fazer a diferença!',
        'Minha vingança será rápida e justa!',
        'Eu sou mais forte do que você pensa!',
        'Eu sou a esperança neste mundo cruel!',
        'Eu sou o herói que este mundo precisa!',
        'Meu coração é puro e minha alma é forte!',
        'Lutei contra algo pior que você e venci!',
        'O mundo precisa de mais heróis como você!',
        'Chega de sofrimento, agora é hora da paz!',
        'Minha espada está pronta para te defender!',
        'Você vai se arrepender de ter me desafiado!',
        'Eu sou a luz que guia o caminho para a paz!',
        'Chega de brincadeira, agora é hora de lutar!',
        'Espero que você esteja pronto para a derrota!',
        'Nunca desistirei de lutar pelo o que é certo!',
        'Lute pelo que é certo, mesmo que seja difícil!',
        'Eu sou a prova de que a esperança ainda existe!',
        'Ninguém vai se machucar enquanto eu estiver aqui!',
        'Meu dever é te proteger, mesmo que isso custe minha vida!',
        (
            'Espero que você esteja pronto para a misericórdia, '
            'porque eu não vou te mostrar nenhuma!'
        ),
    ],
    AlignmentEnum.SUPPORTER.name: [
        'A paz é o caminho.',
        'Tome isso em troca!',
        'Justiça será feita!',
        'Chega de brincadeira!',
        'A justiça prevalecerá.',
        'A fé é o nosso escudo.',
        'A paz é o nosso legado.',
        'O amor é a nossa força.',
        'A verdade é a nossa luz.',
        'A fé é a nossa redenção.',
        'Nunca perca a esperança!',
        'A igualdade é para todos.',
        'A paz é o nosso objetivo.',
        'A verdade é a nossa arma.',
        'A igualdade é a nossa lei.',
        'A fé nos move para frente.',
        'Juntos, somos invencíveis!',
        'A esperança é o nosso guia.',
        'A justiça é a nossa espada.',
        'A esperança sempre triunfa!',
        'O bem triunfará sobre o mal.',
        'O bem sempre vence no final!',
        'Lute pelo que você acredita!',
        'O amor é a nossa eternidade.',
        'Lute com honra, não com ódio!',
        'A felicidade é o nosso futuro.',
        'A liberdade é a nossa vitória.',
        'Nunca desista dos seus sonhos!',
        'Você não me derruba tão fácil!',
        'A liberdade é o nosso direito.',
        'A esperança é a nossa salvação.',
        'O amor é mais forte que o medo!',
        'A justiça é a nossa recompensa.',
        'A verdade sempre será revelada.',
        'A amizade é a nossa maior força!',
        'Não subestime a força da bondade!',
        'O perdão é o caminho para a cura.',
        'É hora de você pagar pelo que fez!',
        'O amor nos conecta uns aos outros.',
        'A felicidade é a nossa recompensa.',
        'Minha força vem do meu coração puro!',
        'Não se atreva a machucar meus amigos!',
        'A compaixão é a chave para a redenção.',
        'Acredite em si mesmo, você pode vencer!',
        'Você não pode silenciar a voz da verdade!',
        'Não vou permitir que você cause mais dano!',
        'Juntos, podemos superar qualquer obstáculo!',
        'O amor é a resposta para todos os problemas!',
        'A esperança é a luz que nos guia na escuridão.',
        'Vou te mostrar o verdadeiro poder da compaixão!'
    ],
}
