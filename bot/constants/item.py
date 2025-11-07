import re

from rpgram.enums import DamageEnum
from rpgram.enums.debuff import (
    DebuffEnum
)


# Número máximo de itens que podem ser dropados por baú.
MAX_DROP_ITEMS = 10


# SECTIONS TEXTs
SECTION_TEXT_DROP_TREASURE = 'TESOURO'
SECTION_TEXT_OPEN_TREASURE = 'ABERTO'
SECTION_TEXT_ACTIVATED_TRAP = 'ARMADILHA'


# ACTIONS
CALLBACK_TEXT_GET = '$get_item'
CALLBACK_TEXT_IGNORE = '$ignore_item'
ESCAPED_CALLBACK_TEXT_GET = re.escape(CALLBACK_TEXT_GET)
ESCAPED_CALLBACK_TEXT_IGNORE = re.escape(CALLBACK_TEXT_IGNORE)


TRAP_DAMAGE_TYPE_RATIO = {
    DamageEnum.BLUDGEONING.name: 0.10,
    DamageEnum.HITTING.name: 0.10,
    DamageEnum.SLASHING.name: 0.20,
    DamageEnum.PIERCING.name: 0.25,
    DamageEnum.MAGIC.name: 0.40,
    DamageEnum.BLESSING.name: 0.05,
    DamageEnum.DIVINE.name: 0.50,
    DamageEnum.LIGHT.name: 0.12,
    DamageEnum.DARK.name: 0.40,
    DamageEnum.FIRE.name: 0.30,
    DamageEnum.WATER.name: 0.30,
    DamageEnum.COLD.name: 0.30,
    DamageEnum.LIGHTNING.name: 0.40,
    DamageEnum.WIND.name: 0.30,
    DamageEnum.ROCK.name: 0.30,
    DamageEnum.GROUND.name: 0.30,
    DamageEnum.ACID.name: 0.40,
    DamageEnum.POISON.name: 0.40,
    DamageEnum.CHAOS.name: 0.45,
    DamageEnum.CRYSTAL.name: 0.35,
    DamageEnum.BLAST.name: 0.50,
    DamageEnum.SONIC.name: 0.35,
}


REPLY_TEXTS_FIND_TREASURE_START = [
    'Durante a sua viagem, '
    'vocês se deparam com uma clareira tranquila na floresta, ',
    'Explorando uma caverna escura, '
    'vocês se deparam com uma passagem secreta, ',
    'Ao cruzar uma ponte antiga, vocês se deparam com uma ilha misteriosa, ',
    'Navegando pelo mar agitado, vocês se deparam com um navio naufragado, ',
    'No alto das montanhas, vocês se deparam com uma ruína esquecida, ',
    'Ao explorar um pântano sombrio, '
    'vocês se deparam com uma árvore gigante, ',
    'No deserto escaldante, vocês se deparam com um oásis escondido, ',
    'Enquanto atravessam uma floresta densa, '
    'vocês se deparam com uma clareira encantada, ',
    'Ao explorar uma cidade abandonada, '
    'vocês se deparam com uma mansão assombrada, ',
    'Escalando uma colina íngreme, '
    'vocês se deparam com uma caverna misteriosa, ',
    'Em uma estrada deserta, vocês se deparam com uma carroça abandonada, ',
    'No fundo de um vale isolado, '
    'vocês se deparam com uma fonte de água cristalina, ',
    'Ao atravessar uma floresta encantada, '
    'vocês se deparam com uma estátua enigmática, ',
    'Viajando pelo deserto vasto, vocês se deparam com uma ruína soterrada, ',
    'Navegando por um rio sinuoso, '
    'vocês se deparam com uma ilha desconhecida, ',
    'Enquanto exploram uma região glacial, '
    'vocês se deparam com uma caverna de gelo, ',
    'No meio de um campo verdejante, '
    'vocês se deparam com uma árvore ancestral, ',
    'Passando por um vale sombrio, '
    'vocês se deparam com um templo abandonado, ',
    'Caminhando pela praia, vocês se deparam com um naufrágio antigo, ',
    'Viajando pelas terras selvagens, '
    'vocês se deparam com uma rocha misteriosa, ',
    'Explorando um cânion profundo, vocês se deparam com uma gruta oculta, ',
    'Ao seguir um riacho, vocês se deparam com uma cachoeira majestosa, ',
    'Escalando uma montanha escarpada, '
    'vocês se deparam com uma caverna ventosa, ',
    'Cruzando uma floresta enevoada, '
    'vocês se deparam com uma clareira encantada, ',
    'Em uma cidade abandonada, '
    'vocês se deparam com uma biblioteca esquecida, ',
    'Percorrendo um deserto vasto, vocês se deparam com uma oásis escondido, ',
    'Ao explorar uma selva densa, '
    'vocês se deparam com uma ruína coberta de vegetação, ',
    'Navegando pelo mar tempestuoso, '
    'vocês se deparam com um naufrágio misterioso, ',
    'Em uma região vulcânica, vocês se deparam com uma caverna ígnea, ',
    'Durante uma caminhada na tundra congelada, '
    'vocês se deparam com um abrigo improvisado, ',
    'Viajando por uma planície vasta, vocês se deparam com uma pedra rúnica, ',
    'Ao atravessar uma floresta assombrada, '
    'vocês se deparam com um altar místico, ',
    'Em um vale escondido, vocês se deparam com uma nascente de água quente, ',
    'Caminhando por um desfiladeiro estreito, '
    'vocês se deparam com uma abertura subterrânea, ',
    'Passando por um pântano enevoado, '
    'vocês se deparam com uma árvore retorcida, ',
    'No meio de um campo de flores, vocês se deparam com um marco antigo, ',
    'Percorrendo uma região desértica, '
    'vocês se deparam com uma ruína enterrada, ',
    'Explorando uma floresta encantada, '
    'vocês se deparam com um círculo de pedras, ',
    'Enquanto seguem um rio serpenteante, '
    'vocês se deparam com uma ilha pitoresca, ',
    'Viajando por uma região montanhosa, '
    'vocês se deparam com uma passagem estreita, ',
    'Ao cruzar um planalto ventoso, '
    'vocês se deparam com um abrigo improvisado, ',
    'Em uma cidade em ruínas, vocês se deparam com uma cripta esquecida, ',
    'Caminhando por uma praia deserta, '
    'vocês se deparam com um baú enterrado, ',
    'No fundo de um vale verdejante, '
    'vocês se deparam com uma nascente de água pura, ',
    'Atravessando um pântano lamacento, '
    'vocês se deparam com uma árvore solitária, ',
    'No topo de uma colina, vocês se deparam com um monumento antigo, ',
    'Percorrendo uma floresta enigmática, '
    'vocês se deparam com um altar oculto, ',
    'Explorando uma caverna úmida, vocês se deparam com um veio de minério, ',
    'Ao seguir um riacho murmurante, '
    'vocês se deparam com uma cachoeira majestosa, ',
    'Em um deserto vasto, vocês se deparam com um oásis escondido, ',
    'Cruzando uma floresta antiga, vocês se deparam com uma pedra rúnica, ',
    'Viajando por uma região selvagem, '
    'vocês se deparam com uma caverna escondida, ',
    'Ao atravessar uma planície vasta, '
    'vocês se deparam com uma ruína coberta de hera, ',
    'Em uma cidade abandonada, vocês se deparam com um templo em ruínas, ',
    'No meio de uma selva densa, vocês se deparam com um altar misterioso, ',
    'Percorrendo uma praia deserta, '
    'vocês se deparam com um naufrágio antigo, ',
    'Caminhando por uma floresta encantada, '
    'vocês se deparam com uma clareira radiante, ',
    'Em uma região vulcânica, vocês se deparam com uma gruta ígnea, ',
    'Passando por um desfiladeiro estreito, '
    'vocês se deparam com uma passagem subterrânea, ',
    'No alto de uma montanha, '
    'vocês se deparam com um observatório abandonado, ',
    'Explorando uma floresta sombria, '
    'vocês se deparam com uma árvore centenária, ',
    'Viajando por um planalto ventoso, '
    'vocês se deparam com um monumento enigmático, ',
    'Ao seguir um rio sereno, '
    'vocês se deparam com uma nascente de água cristalina, ',
    'No meio de um campo verdejante, vocês se deparam com uma pedra rúnica, ',
    'Atravessando uma floresta antiga, '
    'vocês se deparam com um altar esculpido, ',
    'Em uma cidade em ruínas, vocês se deparam com uma câmara secreta, ',
    'Percorrendo uma região selvagem, '
    'vocês se deparam com um poço misterioso, ',
    'Explorando uma caverna escura, vocês se deparam com um brilho no chão, ',
    'Ao atravessar um desfiladeiro íngreme, '
    'vocês se deparam com um abismo profundo, ',
    'Caminhando por um pântano enevoado, '
    'vocês se deparam com um santuário oculto, ',
    'Em uma região glacial, vocês se deparam com uma gruta de gelo, ',
    'Passando por um vale tranquilo, '
    'vocês se deparam com uma ruína coberta de neve, ',
    'No alto de uma colina, vocês se deparam com um círculo de pedras, ',
    'Enquanto seguem uma trilha estreita, '
    'vocês se deparam com uma bifurcação, ',
    'Em uma cidade abandonada, vocês se deparam com uma loja misteriosa, ',
    'Atravessando uma floresta encantada, '
    'vocês se deparam com uma clareira radiante, ',
    'Viajando por uma região montanhosa, '
    'vocês se deparam com um vale verdejante, ',
    'No meio de uma planície vasta, vocês se deparam com um marco antigo, ',
    'Explorando um templo esquecido, vocês se deparam com um altar secreto, ',
    'Ao cruzar um deserto vasto, vocês se deparam com um oásis escondido, ',
    'Percorrendo uma floresta densa, '
    'vocês se deparam com uma árvore ancestral, ',
    'Passando por um riacho sereno, '
    'vocês se deparam com uma cachoeira majestosa, ',
    'Em uma cidade em ruínas, vocês se deparam com uma câmara subterrânea, ',
    'Caminhando por uma praia deserta, '
    'vocês se deparam com um naufrágio antigo, ',
    'No alto de uma montanha, vocês se deparam com uma vista panorâmica, ',
    'Explorando uma caverna escura, vocês se deparam com um brilho no chão, ',
    'Ao seguir um rio sinuoso, vocês se deparam com uma cachoeira majestosa, ',
    'Em uma floresta encantada, '
    'vocês se deparam com um círculo de cogumelos, ',
    'Percorrendo uma região selvagem, '
    'vocês se deparam com um abismo profundo, ',
    'Passando por um vale tranquilo, '
    'vocês se deparam com um monumento antigo, ',
    'No meio de um campo verdejante, '
    'vocês se deparam com um poço misterioso, ',
    'Atravessando um pântano sombrio, '
    'vocês se deparam com um santuário oculto, ',
    'Viajando por uma região vulcânica, '
    'vocês se deparam com uma gruta ígnea, ',
    'Explorando uma cidade abandonada, '
    'vocês se deparam com uma mansão sinistra, ',
    'Caminhando por uma floresta sombria, '
    'vocês se deparam com um altar esculpido, ',
    'No alto de uma colina, vocês se deparam com um círculo de pedras, ',
    'Percorrendo uma praia deserta, vocês se deparam com um baú enterrado, ',
    'Em uma região glacial, vocês se deparam com uma nascente de água pura, ',
    'Passando por um vale verdejante, '
    'vocês se deparam com uma ruína coberta de hera, ',
    'Ao explorar um templo antigo, vocês se deparam com um altar iluminado, ',
]


REPLY_TEXTS_FIND_TREASURE_MIDDLE = [
    'e investigando vocês notam ',
    'e observando com atenção vocês percebem ',
    'e ao olhar com mais detalhe vocês se deparam com',
    'e examinando cuidadosamente vocês descobrem ',
    'e inspecionando minuciosamente vocês avistam ',
    'e ao analisar com mais profundidade vocês constatam ',
    'e explorando mais a fundo vocês identificam ',
    'e ao vistoriar a área vocês detectam ',
    'e ao estudar a região vocês notam ',
    'e ao investigar cuidadosamente vocês reconhecem ',
    'e examinando minuciosamente vocês notam ',
    'e ao observar com atenção vocês percebem ',
    'e investigando com mais detalhes vocês avistam ',
    'e olhando com mais profundidade vocês descobrem ',
    'e ao inspecionar minuciosamente vocês constatam ',
    'e observando com mais detalhes vocês identificam ',
    'e ao explorar a área vocês detectam ',
    'e estudando cuidadosamente vocês notam ',
    'e ao vistoriar a região vocês reconhecem ',
    'e ao investigar com mais profundidade vocês notam ',
    'e examinando a área vocês percebem ',
    'e ao observar minuciosamente vocês avistam ',
    'e investigando com atenção vocês descobrem ',
    'e olhando com mais detalhes vocês constatam ',
    'e ao inspecionar com mais profundidade vocês identificam ',
    'e observando cuidadosamente vocês detectam ',
    'e ao explorar minuciosamente vocês notam ',
    'e estudando com mais detalhes vocês reconhecem ',
    'e ao vistoriar com mais profundidade vocês notam ',
    'e examinando a região vocês percebem ',
    'e ao observar com atenção vocês avistam ',
    'e investigando minuciosamente vocês descobrem ',
    'e olhando com mais profundidade vocês constatam ',
    'e ao inspecionar com mais detalhes vocês identificam ',
    'e observando com mais detalhes vocês detectam ',
    'e ao explorar com mais profundidade vocês notam ',
    'e estudando a área vocês reconhecem ',
    'e ao vistoriar minuciosamente vocês notam ',
    'e examinando com mais detalhes vocês percebem ',
    'e ao observar com mais profundidade vocês avistam ',
    'e investigando a região vocês descobrem ',
    'e olhando com mais detalhes vocês constatam ',
    'e ao inspecionar com atenção vocês identificam ',
    'e observando minuciosamente vocês detectam ',
    'e ao explorar com mais detalhes vocês notam ',
    'e estudando com mais profundidade vocês reconhecem ',
    'e ao vistoriar a área vocês notam ',
    'e examinando cuidadosamente vocês percebem ',
    'e ao observar a região vocês avistam ',
    'e investigando com mais detalhes vocês descobrem ',
    'e olhando com mais profundidade vocês constatam ',
    'e ao inspecionar minuciosamente vocês identificam ',
    'e observando com atenção vocês detectam ',
    'e ao explorar minuciosamente vocês notam ',
    'e estudando com mais detalhes vocês reconhecem ',
    'e ao vistoriar com mais profundidade vocês notam ',
    'e examinando a área vocês percebem ',
    'e ao observar com atenção vocês avistam ',
    'e investigando minuciosamente vocês descobrem ',
    'e olhando com mais detalhes vocês constatam ',
    'e ao inspecionar com mais profundidade vocês identificam ',
    'e observando com mais detalhes vocês detectam ',
    'e ao explorar a região vocês notam ',
    'e estudando cuidadosamente vocês reconhecem ',
    'e ao vistoriar minuciosamente vocês notam ',
    'e examinando com mais detalhes vocês percebem ',
    'e ao observar com mais profundidade vocês avistam ',
    'e investigando a área vocês descobrem ',
    'e olhando com mais profundidade vocês constatam ',
    'e ao inspecionar minuciosamente vocês identificam ',
    'e observando com atenção vocês detectam ',
    'e ao explorar minuciosamente vocês notam ',
    'e estudando com mais detalhes vocês reconhecem ',
    'e ao vistoriar com mais profundidade vocês notam ',
    'e examinando a região vocês percebem ',
    'e ao observar com atenção vocês avistam ',
    'e investigando minuciosamente vocês descobrem ',
    'e olhando com mais detalhes vocês constatam ',
    'e ao inspecionar com mais profundidade vocês identificam ',
    'e observando com mais detalhes vocês detectam ',
    'e ao explorar a área vocês notam ',
    'e estudando com mais profundidade vocês reconhecem ',
    'e ao vistoriar minuciosamente vocês notam ',
    'e examinando com mais detalhes vocês percebem ',
    'e ao observar com mais profundidade vocês avistam ',
    'e investigando a região vocês descobrem ',
    'e olhando com mais profundidade vocês constatam ',
    'e ao inspecionar com atenção vocês identificam ',
    'e observando minuciosamente vocês detectam ',
    'e ao explorar minuciosamente vocês notam ',
    'e estudando com mais detalhes vocês reconhecem ',
    'e ao vistoriar com mais profundidade vocês notam ',
    'e examinando a área vocês percebem ',
    'e ao observar com atenção vocês avistam ',
    'e investigando minuciosamente vocês descobrem ',
    'e olhando com mais detalhes vocês constatam ',
    'e ao inspecionar com mais profundidade vocês identificam ',
    'e observando com mais detalhes vocês detectam ',
    'e ao explorar a região vocês notam ',
    'e estudando com mais profundidade vocês reconhecem ',
]


REPLY_TEXTS_FIND_TREASURE_END = [
    'um baú de madeira envelhecida com ornamentos entalhados nas bordas.',
    'uma bolsa de couro gasta pelo tempo e marcada por sinais de uso.',
    'um cofre de metal, reforçado com dobradiças e fechaduras complexas.',
    'uma caixa de pedra esculpida, adornada com símbolos desconhecidos.',
    'uma arca de tecido ricamente bordado, com fios dourados reluzentes.',
    'um estojo de madeira contendo compartimentos cuidadosamente dispostos.',
    'uma sacola de linho simples, amarrada com um cordão resistente.',
    'um pote de cerâmica selado com cera, revelando marcas de selos antigos.',
    'uma urna de vidro transparente, permitindo ver o interior.',
    'uma mala de viagem de couro robusto, com alças reforçadas.',
    'um engradado de metal corroído pela ferrugem, mas ainda trancado.',
    'uma caixa esculpida de osso, exibindo figuras intrincadas entrelaçadas.',
    'um estojo de veludo negro, forrado com seda e fechado com elegância.',
    'uma caixa de pedra lapidada, refletindo luzes coloridas.',
    'uma cesta de vime trançado com uma tampa tecida em padrões complexos.',
    'um baú de ferro com inscrições rúnicas gravadas na superfície.',
    'uma bolsa de veludo vermelho com um brilho sutil e bordas desgastadas.',
    'um cofre selado com cera quente, mantendo seu conteúdo em segredo.',
    'um jarro de barro selado com um selo de cera antigo.',
    'uma maleta de madeira com cantos reforçados e alças de couro.',
    'uma caixa de metal enferrujada repousa no canto da sala.',
    'uma bolsa de couro gasta está jogada sobre uma mesa.',
    'um cofre de pedra está embutido na parede, '
    'com uma roda giratória na frente.',
    'uma arca de carvalho maciço repousa no centro da sala, '
    'com fechos de ferro.',
    'um saco de lona está pendurado em um gancho na parede.',
    'uma pequena urna de cerâmica está posicionada '
    'cuidadosamente em uma prateleira.',
    'um baú de madeira envernizada está empoleirado no topo de um pedestal.',
    'uma sacola de linho bordada está caída perto da porta.',
    'um pequeno estojo de couro está preso ao lado de uma estante, '
    'com fechos intricados.',
    'uma caixa esculpida que está em exibição em um nicho na parede.',
    'um baú de metal polido está embutido no chão, com um símbolo gravado.',
    'uma bolsa de veludo está jogada despretensiosamente sobre uma cadeira.',
    'uma urna finamente trabalhada repousa sobre uma almofada de seda.',
    'um pequeno baú de madeira de cerejeira está embutido na parede, '
    'com um entalhe de folhas.',
    'uma sacola de lã está pendurada perto da lareira.',
    'um estojo de couro austero está preso a um suporte de madeira simples.',
    'uma caixa de pedra entalhada com runas '
    'está posicionada no centro da sala.',
    'uma bolsa de couro decorada está descansando em um banco de pedra.',
    'um cofre de mogno está embutido no chão, com relevos intrincados.',
    'uma pequena urna de vidro colorido '
    'está posicionada em um pedestal de metal.',
    'uma caixa de metal fortemente trancada, com marcas de uso evidentes.',
    'uma bolsa de pano simples, amarrada com um cordão de couro desgastado.',
    'um cofre de madeira nobre, esculpido com padrões geométricos.',
    'um baú de couro envelhecido, adornado com fechos de bronze.',
    'uma arca finamente martelada, refletindo a luz em padrões cintilantes.',
    'uma bolsa de camurça macia, com franjas nas bordas.',
    'um estojo de ébano, detalhado com incrustações de madrepérola.',
    'um baú de ferro fundido, gravado com símbolos misteriosos.',
    'uma sacola de linho grossa, com alças de couro cru.',
    'um jarro de cerâmica selado com um nó de corda.',
    'uma caixa de madeira polida, com um fecho delicado em formato de flor.',
    'um cofre de bronze maciço, com uma fechadura ornamental.',
    'uma bolsa de veludo azul-marinho, com um brilho sutil.',
    'uma arca de madeira entalhada, retratando cenas antigas.',
    'um estojo de metal adornado com padrões entrelaçados.',
    'um baú de couro robusto, reforçado com pregos de cobre.',
    'uma urna de mármore branco, esculpida com figuras angelicais.',
    'uma bolsa de tecido colorido, com bordados intricados.',
    'um pequeno cofre com uma inscrição enigmática.',
    'um pote de cerâmica vidrada, com um selo de cera intacto.',
    'uma caixa de madeira escura, com um entalhe de olho na tampa.',
    'um jarro de vidro soprado à mão, selado com cera colorida.',
    'uma arca de carvalho envernizada, com detalhes em cobre.',
    'uma sacola de couro desgastado, com manchas de tinta.',
    'um estojo de pedra coloridas, incrustado com maestria.',
    'um baú de ferro reforçado, com correntes em volta.',
    'uma bolsa de veludo verde-esmeralda, com bordas desfiadas.',
    'uma urna de porcelana delicada, pintada à mão.',
    'uma caixa de metal martelado, com fechos de latão.',
    'um jarro de barro decorado, com uma tampa de cortiça.',
    'um pequeno estojo de madeira escura, com dobradiças douradas.',
    'um baú de couro envernizado, com pregos prateados.',
    'uma sacola de linho bordada com fios de dourados.',
    'um cofre de pedra cinza, com inscrições enigmáticas.',
    'uma arca de mogno maciço, com entalhes de folhas.',
    'uma bolsa de seda vermelha, com um brilho intenso.',
    'uma urna de vidro fosco, com detalhes em metal escuro.',
    'um pequeno baú de madeira clara, com cantos arredondados.',
    'um estojo de couro trabalhado à mão, com costuras elaboradas.',
    'uma caixa finamente gravada, com padrões abstratos.',
    'um jarro de cerâmica decorada, com uma rolha de cortiça.',
    'um baú de madeira esculpida, representando figuras mitológicas.',
    'uma bolsa de couro preto, com um aroma distinto.',
    'uma arca de bronze envelhecido, com gravuras desgastadas.',
    'uma sacola de lona resistente, com alças de couro entrelaçado.',
    'um cofre de vidro transparente, com fechos de metal prateado.',
    'um estojo de madeira tingida, com padrões entrelaçados.',
    'um jarro de metal envernizado, com uma rolha de cortiça.',
    'um pequeno baú de madeira crua, com pregos de ferro.',
    'uma urna de pedra esculpida, representando uma figura angelical.',
    'uma caixa de couro macio, com entalhes de flores na tampa.',
    'um pote de cerâmica decorada, com um selo de cera intacto.',
    'um baú de metal ornamentado, com detalhes dourados.',
    'uma bolsa de veludo roxo, com um brilho suave.',
    'uma arca de ébano entalhado, retratando cenas de batalha.',
    'um estojo de madeira envernizada, com dobradiças de latão.',
    'um cofre de couro reforçado, com amarrações de corda.',
    'uma sacola de seda fina, com bordados delicados.',
    'um jarro de vidro colorido, com uma tampa de metal.',
    'uma caixa de pedra rústica, com runas esculpidas.',
    'um pequeno baú de mogno, com detalhes desenhados.',
    'uma urna de cerâmica vidrada, com um padrão em espiral.',
    'uma bolsa de linho cru, com um toque áspero.',
    'um estojo de couro escuro, com fechos de cobre.',
    'um baú de metal forjado, com inscrições antigas.',
    'uma arca de madeira trabalhada, com detalhes em marfim.',
    'uma sacola de camurça, com franjas na abertura.',
    'um jarro de metal polido, com uma rolha de cortiça apertada.',
    'uma caixa gravada, com padrões intrincados.',
    'um cofre de pedra esculpida, com relevos abstratos.',
    'uma bolsa de veludo cintilante, com um toque suave.',
    'uma urna de vidro translúcido, com ornamentos de metal.',
    'um pequeno baú de madeira entalhada, com um símbolo enigmático.',
    'um estojo de metal envelhecido, com gravuras desbotadas.',
    'um baú de couro gasto, com amarrações de corda.',
    'uma sacola de linho resistente, com alças de couro entrançado.',
    'um jarro de cerâmica simples, com uma tampa de cortiça.',
    'uma caixa de madeira envernizada, com detalhes prateados.',
    'um cofre de vidro fosco, com um fecho de metal.',
    'uma arca de bronze esculpido, retratando figuras mitológicas.',
    'uma bolsa de couro envelhecido, com marcas de uso.',
    'uma urna de madeira escura, com entalhes de animais.',
    'um pequeno baú de pedra, com uma inscrição enigmática.',
    'um estojo de couro macio, com costuras simples.',
    'um baú de metal reforçado, com correntes enferrujadas.',
    'uma sacola de veludo macio, com um brilho aveludado.',
    'um jarro de barro simples, com uma rolha de cortiça.',
    'uma caixa de metal envelhecido, com fechos de bronze.',
    'um cofre de couro trabalhado, com detalhes em relevo.',
    'uma arca de madeira nobre, esculpida com padrões florais.',
    'uma bolsa de pano resistente, com amarrações de corda.',
    'um estojo de pedra esculpida, com símbolos rúnicos.',
    'um baú de vidro transparente, com detalhes de metal.',
    'uma urna de cerâmica vidrada, com um padrão geométrico.',
    'um pequeno baú de mogno, com dobradiças de latão.',
    'uma sacola de couro liso, com um toque suave.',
    'um jarro de metal ornamentado, com uma tampa de cortiça.',
    'uma caixa trabalhada com entalhes detalhados.',
    'um cofre de pedra esculpida, com inscrições antigas.',
    'uma arca de madeira envernizada, com detalhes em marfim.',
]


REPLY_TEXTS_FIND_TREASURE_OPEN = [
    'Com cuidado, você abre o objeto e encontra algo dentro.',
    'Ao destrancar e abrir, uma surpresa aguarda dentro.',
    'Deslizando a abertura, você revela o que está escondido dentro.',
    'Ao remover a cobertura, você se depara com algo guardado ali.',
    'Desprendendo as presilhas, você revela o conteúdo oculto.',
    'Abraçando a curiosidade, você abre o objeto e descobre algo.',
    'Com um clique, o mecanismo se abre, revelando o que estava dentro.',
    '"Clic", você se depara com algo inesperado.',
    'Com um puxão cuidadoso, você expõe o conteúdo escondido.',
    'Ao soltar os lacres, você encontra algo surpreendente dentro.',
    'Empurrando as bordas, você revela o que estava contido ali.',
    'Rompendo o selo, você se depara com algo precioso dentro.',
    'Ao desamarrar as cordas, o interior é revelado a você.',
    'Com um movimento suave, você abre o objeto e encontra algo dentro.',
    'Desprendendo os grampos, você revela o que estava resguardado.',
    'Ao erguer, uma revelação aguarda dentro.',
    'Com um toque delicado, você abre e descobre o que estava escondido.',
    'Ao destravar, dentro, uma descoberta te aguarda.',
    'Com um deslize, você abre o objeto e revela algo especial.',
    'Desatando o lacre, você se depara com algo intrigante dentro.',
    'Ao retirar a capa, a revelação do interior é emocionante.',
    'Com um movimento preciso, você abre o objeto e encontra algo valioso.',
    'Deslizando as partes, você expõe o que estava contido ali.',
    'Ao romper o lacre, você encontra algo interessante dentro.',
    'Com um gesto cuidadoso, você revela o que estava oculto.',
    'Desvendando as dobras, você se depara com algo único dentro.',
    'Ao desatar o fecho, a surpresa revela o que está guardado.',
    'Com um simples movimento, você abre o objeto e descobre algo incrível.',
    'Desprendendo os clipes, você revela o conteúdo escondido.',
    'Ao erguer a aba, uma revelação aguarda dentro.',
    'Com um toque suave, você abre e encontra algo dentro.',
    'Ao destravar, uma descoberta aguarda você dentro.',
    'Com um giro, você abre o objeto e revela algo emocionante.',
    'Desfazendo o lacre, você se depara com algo intrigante dentro.',
    'Ao remover a cobertura, a revelação do interior é gratificante.',
    'Com um movimento hábil, você abre o objeto e encontra algo especial.',
    'Deslizando as partes, você expõe o que estava guardado.',
    'Ao quebrar o selo, você encontra algo cativante dentro.',
    'Com um gesto delicado, você revela o que estava resguardado.',
    'Ao desatar os seles, a surpresa revela o que está contido ali.',
    'Desvendando o fecho, você se depara com algo inesperado dentro.',
    'Com um simples movimento, você abre o objeto e encontra algo único.',
    'Desprendendo as travas, você revela o conteúdo oculto.',
    'Ao erguer a tampa, uma revelação aguarda você dentro.',
    'Com um toque suave, você abre e descobre o que estava guardado.',
    'Ao destravar, uma descoberta aguarda você dentro.',
    'Com um giro rápido, você abre o objeto e revela algo intrigante.',
    'Desfazendo o feche, você se depara com algo fascinante dentro.',
    'Ao remover a capa, a revelação do interior é envolvente.',
    'Com um movimento habilidoso, você abre o objeto e '
    'encontra algo cativante.',
    'Deslizando as partes, você expõe o que estava escondido.',
    'Ao romper o lacre, você encontra algo memorável dentro.',
    'Com um gesto cuidadoso, você revela o que estava oculto.',
    'Ao desamarrar os cordões, a surpresa revela o que está contido ali.',
    'Desvendando o fecho, você se depara com algo surpreendente dentro.',
    'Com um simples movimento, você abre o objeto e encontra algo valioso.',
    'Desprendendo as abas, você revela o conteúdo escondido.',
    'Ao erguer a aba, uma revelação aguarda dentro.',
    'Com um toque delicado, você abre e descobre o que estava dentro.',
    'Ao destrancar, uma descoberta aguarda você dentro.',
    'Com um giro, você abre o objeto e revela algo emocionante.',
    'Desfazendo o sele, você se depara com algo intrigante dentro.',
    'Ao retirar a capa, a revelação do interior é gratificante.',
    'Com um movimento hábil, você abre o objeto e encontra algo especial.',
    'Desprendendo os clipes, você revela o que estava resguardado.',
    'Ao romper o lacre, você encontra algo encantador dentro.',
    'Com um gesto cuidadoso, você revela o que estava escondido.',
    'Ao desatar os lacres, a surpresa revela o que está guardado.',
    'Desvendando o fecho, você se depara com algo cativante dentro.',
    'Com um simples movimento, você abre o objeto e encontra algo único.',
    'Deslizando as partes, você expõe o que estava contido ali.',
    'Ao desvendar o selo, você encontra algo memorável dentro.',
    'Com um gesto delicado, você revela o que estava oculto.',
    'Ao desfazer os laços, a revelação do interior é envolvente.',
    'Com um movimento habilidoso, você abre o objeto e '
    'descobre algo cativante.',
    'Desprendendo as travas, você revela o conteúdo escondido.',
    'Ao romper o selo, você encontra algo surpreendente dentro.',
    'Com um gesto cuidadoso, você revela o que estava guardado.',
    'Ao desamarrar os feches, a surpresa revela o que está contido ali.',
    'Desvendando o fecho, você se depara com algo encantador dentro.',
    'Com um simples movimento, você abre o objeto e encontra algo valioso.',
    'Desprendendo as partes, você revela o conteúdo oculto.',
    'Ao retirar a capa, você encontra algo intrigante dentro.',
    'Com um toque suave, você revela o que estava resguardado.',
    'Ao destravar, uma descoberta aguarda você dentro.',
    'Com um giro, você abre o objeto e descobre algo fascinante.',
    'Desfazendo o lacre, você se depara com algo emocionante dentro.',
    'Ao remover a cobertura, a revelação do interior é cativante.',
    'Com um movimento hábil, você abre o objeto e encontra algo único.',
    'Desprendendo os grampos, você revela o que estava escondido.',
    'Ao romper o lacre, você encontra algo envolvente dentro.',
    'Com um gesto cuidadoso, você revela o que estava oculto.',
    'Ao desamarrar as amarras, a surpresa revela o que está guardado.',
    'Desvendando o fecho, você se depara com algo memorável dentro.',
    'Com um simples movimento, você abre o objeto e encontra algo cativante.',
    'Desprendendo as travas, você revela o conteúdo oculto.',
    'Ao destrancar, uma descoberta aguarda você dentro.',
    'Com um giro, você abre o objeto e descobre algo envolvente.',
    'Desfazendo o sele, você se depara com algo intrigante dentro.',
]


REPLY_TEXTS_FIND_TREASURE_FINDING = [
    '{user_name} ganhou:',
    '{user_name} obteve:',
    '{user_name} adquiriu:',
    'Parabéns, {user_name} ganhou:',
    'Parabéns, {user_name} obteve:',
    'Parabéns, {user_name} adquiriu:',
    'Como recompensa, {user_name} ganhou:',
    'Como recompensa, {user_name} obteve:',
    'Como recompensa, {user_name} adquiriu:',
]


REPLY_TEXTS_IGNORE_TREASURE = [
    'Sem dar atenção, vocês seguem adiante.',
    'Sem notar, vocês prosseguem em sua jornada.',
    'Desprezando o detalhe, vocês continuam avançando.',
    'Deixando para trás, vocês seguem em frente.',
    'Sem dar importância, vocês seguem o caminho.',
    'Desconsiderando o indício, vocês prosseguem.',
    'Sem se deter, vocês avançam na trilha.',
    'Ignorando a sugestão, vocês seguem adiante.',
    'Sem perceber o sinal, vocês continuam a jornada.',
    'Deixando para trás o mistério, vocês prosseguem.',
    'Desviando o olhar, vocês desdenham e seguem.',
    'Focando em outra direção, vocês deixam para trás.',
    'Sem pensar duas vezes, vocês prosseguem em sua jornada.',
    'Sem hesitar, vocês continuam avançando.',
    'Desprezando o enigma, vocês seguem o caminho.',
    'Deixando a curiosidade de lado, vocês prosseguem.',
    'Ignorando a pista, vocês seguem adiante.',
    'Sem dar ouvidos, vocês continuam a jornada.',
    'Desconsiderando o mistério, vocês seguem em frente.',
    'Sem investigar mais, vocês prosseguem.',
    'Deixando para trás a dúvida, vocês avançam.',
    'Desviando o olhar rapidamente, vocês desdenham e continuam.',
    'Focando em outra direção, vocês seguem adiante.',
    'Sem se deter, vocês continuam a jornada.',
    'Ignorando o sinal misterioso, vocês prosseguem.',
    'Deixando para trás a incerteza, vocês seguem.',
    'Sem considerar a possibilidade, vocês avançam.',
    'Desconsiderando o elemento estranho, vocês continuam em frente.',
    'Ignorando a presença suspeita, vocês prosseguem.',
    'Sem perceber o detalhe, vocês seguem o caminho.',
    'Desprezando a estranheza, vocês continuam a jornada.',
    'Deixando para trás a pergunta sem resposta, vocês prosseguem.',
    'Sem dar atenção ao enigma, vocês avançam.',
    'Desviando o olhar do mistério, vocês desdenham e seguem.',
    'Focando em outros pensamentos, vocês seguem adiante.',
    'Sem se deter para investigar, vocês continuam a jornada.',
    'Ignorando o detalhe intrigante, vocês prosseguem.',
    'Deixando para trás a incógnita, vocês seguem.',
    'Sem considerar o mistério, vocês avançam.',
    'Desconsiderando o indício misterioso, vocês continuam.',
    'Ignorando o elemento desconhecido, vocês seguem em frente.',
    'Deixando a questão sem resposta, vocês prosseguem.',
    'Sem dar atenção à anomalia, vocês seguem adiante.',
    'Desviando o olhar do enigma, vocês desdenham e continuam.',
    'Focando em outros aspectos, vocês continuam a jornada.',
    'Sem se deter para explorar, vocês prosseguem.',
    'Ignorando o elemento fora do comum, vocês avançam.',
    'Deixando para trás o questionamento, vocês seguem.',
    'Sem dar atenção à curiosidade, vocês continuam em frente.',
    'Desprezando a suspeita, vocês seguem adiante.',
    'Ignorando o detalhe peculiar, vocês prosseguem.',
    'Deixando para trás o enigma sem solução, vocês prosseguem.',
    'Sem investigar mais, vocês avançam.',
    'Desconsiderando o detalhe intrigante, vocês continuam a jornada.',
    'Ignorando a pista sutil, vocês seguem em frente.',
    'Deixando a questão em aberto, vocês prosseguem.',
    'Sem dar atenção ao mistério, vocês continuam adiante.',
    'Desprezando o elemento desconhecido, vocês seguem.',
    'Ignorando o detalhe enigmático, vocês prosseguem.',
    'Deixando para trás a incerteza, vocês continuam a jornada.',
    'Sem considerar o sinal misterioso, vocês seguem em frente.',
    'Desviando o olhar do enigma sem resposta, vocês desdenham e continuam.',
    'Ignorando o elemento estranho, vocês avançam.',
    'Deixando a pergunta sem solução, vocês prosseguem.',
    'Sem dar atenção ao indício, vocês continuam adiante.',
    'Desprezando a anomalia, vocês seguem em frente.',
    'Ignorando o detalhe curioso, vocês desdenham e continuam.',
    'Deixando para trás o enigma intrigante, vocês prosseguem.',
    'Sem perceber a pista sutil, vocês avançam.',
    'Desconsiderando o elemento peculiar, vocês seguem a jornada.',
    'Ignorando o mistério inexplicável, vocês continuam.',
    'Deixando a questão sem resposta, vocês prosseguem.',
    'Sem dar atenção ao elemento desconhecido, vocês seguem em frente.',
    'Desprezando o detalhe fora do comum, vocês continuam.',
    'Ignorando a dúvida presente, vocês prosseguem.',
    'Deixando para trás o indício misterioso, vocês avançam.',
    'Sem considerar o sinal intrigante, vocês seguem.',
    'Desconsiderando a suspeita, vocês continuam a jornada.',
    'Ignorando o enigma sem solução, vocês prosseguem.',
    'Deixando para trás o detalhe enigmático, vocês seguem.',
    'Sem dar atenção ao elemento estranho, vocês continuam adiante.',
    'Desprezando a curiosidade, vocês prosseguem.',
    'Ignorando a pista desconhecida, vocês seguem.',
    'Deixando para trás a questão sem resposta, vocês avançam.',
    'Sem perceber o detalhe incomum, vocês continuam.',
    'Desviando o olhar do mistério sem explicação, vocês desdenham e seguem.',
    'Ignorando o indício fora do comum, vocês prosseguem.',
    'Deixando para trás o enigma intrigante, vocês seguem.',
    'Sem considerar a possibilidade, vocês continuam a jornada.',
    'Desconsiderando a pergunta sem resposta, vocês avançam.',
    'Ignorando o elemento estranho, vocês seguem em frente.',
    'Deixando para trás o mistério não resolvido, vocês prosseguem.',
    'Sem dar atenção ao detalhe incompreensível, vocês continuam.',
    'Desprezando o elemento intrigante, vocês seguem adiante.',
    'Ignorando a suspeita presente, vocês prosseguem.',
    'Deixando para trás o enigma sem solução, vocês avançam.',
    'Sem perceber a questão desconhecida, vocês continuam.',
    'Desviando o olhar da pista misteriosa, vocês desdenham e seguem.',
    'Ignorando o detalhe intrigante, vocês prosseguem.',
    'Deixando para trás a incógnita sem resposta, vocês seguem.',
]


REPLY_TEXTS_FIND_TRAP_OPEN = [
    (
        'Com cuidado, você abre o objeto, mas antes que perceba, uma explosão '
        'irrompe.',
        DamageEnum.BLAST,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Ao destrancar e abrir, um gás venenoso escapa, preenchendo o ar ao '
        'seu redor.',
        DamageEnum.POISON,
        [
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.75},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
        ]
    ),
    (
        'Deslizando a tampa, você ativa um mecanismo oculto que dispara uma '
        'chuva de dardos afiados.',
        DamageEnum.PIERCING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
        ]
    ),
    (
        'Ao remover a cobertura, um líquido corrosivo começa a se derramar, '
        'causando estragos.',
        DamageEnum.ACID,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Desprendendo as presilhas, você inadvertidamente desencadeia uma '
        'descarga de magia elétrica.',
        DamageEnum.LIGHTNING,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.50},
        ]
    ),
    (
        'Abraçando a curiosidade, você abre o objeto e aciona uma armadilha '
        'de alçapão.',
        DamageEnum.BLUDGEONING,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Com um clique, o mecanismo se abre, liberando uma enxurrada '
        'de ácido.',
        DamageEnum.ACID,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Desdobrando as abas, você desencadeia um vento forte que varre tudo '
        'em seu caminho.',
        DamageEnum.WIND,
        [
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Com um giro da chave, o invólucro se abre e um enxame de '
        'insetos venenosos emerge.',
        DamageEnum.POISON,
        [
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
        ]
    ),
    (
        'Com um puxão cuidadoso, você ativa uma rede de fogo mágico que o '
        'envolve instantaneamente.',
        DamageEnum.FIRE,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
        ]
    ),
    (
        'Ao soltar os lacres, você percebe tarde demais que um veneno mortal '
        'foi liberado.',
        DamageEnum.POISON,
        [
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.75},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
        ]
    ),
    (
        'Empurrando as bordas, você aciona uma mola que o arremessa '
        'para trás.',
        DamageEnum.BLUDGEONING,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Rompendo o selo, você dispara uma série de flechas afiadas '
        'em sua direção.',
        DamageEnum.PIERCING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Ao desamarrar as cordas, uma pedra pesada cai, o atingindo.',
        DamageEnum.BLUDGEONING,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Com um movimento suave, você ativa uma armadilha e virotes '
        'são disparados em sua direção.',
        DamageEnum.PIERCING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Desprendendo os grampos, você desencadeia uma cascata de rochas '
        'sobre ti.',
        DamageEnum.ROCK,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Ao erguer a tampa, uma explosão de fogo se espalha, queimando tudo '
        'em seu alcance.',
        DamageEnum.FIRE,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Com um toque delicado, você aciona uma armadilha de alçapão '
        'subterrânea.',
        DamageEnum.BLUDGEONING,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Ao destravar, uma lâmina afiada aparece, visando seus pés.',
        DamageEnum.SLASHING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
        ]
    ),
    (
        'Com um deslize, você abre o objeto e ativa uma rede de arame '
        'que o envolve.',
        DamageEnum.PIERCING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Desatando o nó, você desencadeia um alçapão que o faz cair em um '
        'poço escuro.',
        DamageEnum.BLUDGEONING,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Ao retirar o sele, você aciona uma chuva de ácido que queima '
        'tudo à sua volta.',
        DamageEnum.ACID,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
        ]
    ),
    (
        'Com um movimento impreciso, você dispara uma armadilha de '
        'flechas letais.',
        DamageEnum.PIERCING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.8},
        ]
    ),
    (
        'Deslizando as partes, você aciona um veneno paralisante que se '
        'espalha por seu corpo.',
        DamageEnum.POISON,
        [
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.50},
        ]
    ),
    (
        'Ao romper o lacre, você ativa uma armadilha que solta uma '
        'criatura feroz.',
        DamageEnum.CHAOS,
        [
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.25},
        ]
    ),
    (
        'Com um gesto descuidado, você desencadeia uma explosão mágica.',
        DamageEnum.MAGIC,
        [
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.EXHAUSTION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PETRIFIED, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.SILENCE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Desvendando as dobras, você aciona um mecanismo que lhe '
        'arremessa para longe.',
        DamageEnum.BLUDGEONING,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Ao desatar o fecho, uma armadilha de espinhos afiados é ativada.',
        DamageEnum.PIERCING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Com um simples movimento, você abre o objeto e é engolido '
        'por um redemoinho.',
        DamageEnum.WIND,
        [
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Desprendendo os clipes, você ativa uma armadilha que '
        'prende seus pés.',
        DamageEnum.PIERCING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Ao erguer a aba, uma armadilha de alçapão o faz cair '
        'em um abismo escuro.',
        DamageEnum.BLUDGEONING,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Com um toque suave, você aciona uma armadilha que libera um '
        'gás paralisante.',
        DamageEnum.POISON,
        [
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.50},
        ]
    ),
    (
        'Ao destravar, uma explosão sônica ensurdecedora faz você perder '
        'a audição temporariamente.',
        DamageEnum.SONIC,
        [
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.50},
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.25},
        ]
    ),
    (
        'Com um giro, você abre o objeto e ativa uma armadilha de '
        'água turbulenta.',
        DamageEnum.WATER,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Desfazendo o nó, você ativa uma armadilha que o faz '
        'escorregar e cair.',
        DamageEnum.BLUDGEONING,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Ao remover o sele, você aciona uma armadilha causando '
        'uma explosão de virotes.',
        DamageEnum.PIERCING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Com um movimento inábil, você ativa uma armadilha que '
        'dispara estacas afiadas.',
        DamageEnum.PIERCING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.75},
        ]
    ),
    (
        'Desprendendo as travas, você ativa uma armadilha que o '
        'envolve em trevas anômalas.',
        DamageEnum.DARK,
        [
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.25},
        ]
    ),
    (
        'Ao romper o selo, uma armadilha de correntes de fogo o '
        'prende, imobilizando-o.',
        DamageEnum.FIRE,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
        ]
    ),
    (
        'Com um gesto descuidado, você aciona uma armadilha de '
        'pedras que caem sobre ti.',
        DamageEnum.ROCK,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Ao desamarrar os cordões, você ativa uma armadilha que '
        'libera um gás.',
        DamageEnum.POISON,
        [
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
        ]
    ),
    (
        'Desvendando o fecho, você aciona uma armadilha que '
        'despeja dardos flamejantes sobre você.',
        DamageEnum.FIRE,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
        ]
    ),
    (
        'Com um simples movimento, você abre o objeto e é '
        'engolido por uma correnteza violenta.',
        DamageEnum.WATER,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Desprendendo as partes, você ativa uma armadilha que o '
        'lança para um fosso fundo.',
        DamageEnum.BLUDGEONING,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Ao desvendar o selo, você ativa uma armadilha de '
        'flechas envenenadas.',
        DamageEnum.POISON,
        [
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
        ]
    ),
    (
        'Com um gesto delicado, você aciona uma armadilha que o envolve em '
        'uma teia ácida pegajosa.',
        DamageEnum.ACID,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.75},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.75},
        ]
    ),
    (
        'Ao desfazer os laços, você ativa uma armadilha que o prende em uma '
        'rede de espinhos de aço.',
        DamageEnum.PIERCING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Com um movimento habilidoso, você ativa uma armadilha que '
        'desencadeia uma tempestade de granizo.',
        DamageEnum.COLD,
        [
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.50},
        ]
    ),
    (
        'Desprendendo as travas, você ativa uma armadilha que libera '
        'gás congelante.',
        DamageEnum.COLD,
        [
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.75},
        ]
    ),
    (
        'Ao romper o lacre, uma armadilha de fogo é ativada, '
        'queimando tudo ao seu redor.',
        DamageEnum.FIRE,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 1.00},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
        ]
    ),
    (
        'Com um gesto descuidado, você aciona uma armadilha que o '
        'prende em um vórtice de vento.',
        DamageEnum.WIND,
        [
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Desfazendo o nó, você ativa uma armadilha que o faz cair em um '
        'abismo interdimensional.',
        DamageEnum.CHAOS,
        [
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.SILENCE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.SILENCE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Ao retirar a capa, você aciona uma armadilha que libera uma '
        'chuva de pedras.',
        DamageEnum.ROCK,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Com um movimento inábil, você ativa uma armadilha que o envolve em '
        'sombras aterrorizantes.',
        DamageEnum.DARK,
        [
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 1.00},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.75},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.50},
        ]
    ),
    (
        'Desprendendo os clipes, você ativa uma armadilha que libera '
        'criaturas esfomeadas.',
        DamageEnum.CHAOS,
        [
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.25},
        ]
    ),
    (
        'Ao erguer a aba, uma armadilha de alçapão o faz cair em um '
        'labirinto subterrâneo.',
        DamageEnum.BLUDGEONING,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Com um toque suave, você aciona uma armadilha que libera um '
        'gás alucinógeno.',
        DamageEnum.POISON,
        [
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.75},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
        ]
    ),
    (
        'Ao destravar, você aciona uma explosão que o arremessa longe.',
        DamageEnum.BLAST,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.75},
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.50},
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.25},
        ]
    ),
    (
        'Com um giro, você abre o objeto e ativa uma armadilha de '
        'ácido corrosivo.',
        DamageEnum.ACID,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Desfazendo o laço, você aciona uma armadilha que o prende '
        'em uma ilusão terrível.',
        DamageEnum.CHAOS,
        [
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Ao remover a cobertura, você ativa uma armadilha que despeja '
        'óleo flamejante.',
        DamageEnum.FIRE,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 1.00},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
        ]
    ),
    (
        'Com um movimento preciso, você aciona uma armadilha que '
        'libera um enxame de insetos venenosos.',
        DamageEnum.POISON,
        [
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
        ]
    ),
    (
        'Deslizando as partes, você ativa uma armadilha que '
        'cria um vácuo repentino.',
        DamageEnum.WIND,
        [
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
        ]
    ),
    (
        'Ao destrancar, você ativa uma armadilha que o faz '
        'cair em um fosso com espetos.',
        DamageEnum.PIERCING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 1.00},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
        ]
    ),
    (
        'Com um giro da chave, uma explosão mágica irrompe.',
        DamageEnum.MAGIC,
        [
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.EXHAUSTION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.EXHAUSTION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PETRIFIED, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PETRIFIED, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.SILENCE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.SILENCE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Desprezando as presilhas, você aciona uma armadilha '
        'que liberta um monstro furioso.',
        DamageEnum.CHAOS,
        [
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.25},
        ]
    ),
    (
        'Seguindo a curiosidade, você abre o objeto e ativa '
        'uma armadilha de vento cortante.',
        DamageEnum.WIND,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
        ]
    ),
    (
        'Com um clique, o mecanismo se abre, disparando raios '
        'elétricos em todas as direções.',
        DamageEnum.LIGHTNING,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.75},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.75},
        ]
    ),
    (
        'Desdobrando as abas, você ativa uma armadilha que cria '
        'um terremoto.',
        DamageEnum.GROUND,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Ao remover a cobertura, uma tempestade de fogo irrompe, '
        'causando estragos.',
        DamageEnum.FIRE,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 1.00},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
        ]
    ),
    (
        'Desprendendo as presilhas, você aciona uma armadilha que '
        'solta um gás alucinógeno.',
        DamageEnum.POISON,
        [
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.75},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
        ]
    ),
    (
        'Seguindo a curiosidade, você abre o objeto e ativa uma '
        'armadilha de água em fúria.',
        DamageEnum.WATER,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Com um clique, o mecanismo se abre, liberando uma '
        'torrente de pedras.',
        DamageEnum.ROCK,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Desdobrando as abas, você aciona uma armadilha que dispara '
        'lâminas afiadas.',
        DamageEnum.SLASHING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.75},
        ]
    ),
    (
        'Ao remover a cobertura, uma explosão sônica ensurdecedora enche '
        'o ambiente.',
        DamageEnum.SONIC,
        [
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.75},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.75},
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.50},
        ]
    ),
    (
        'Com um gesto descuidado, você ativa uma armadilha cortante que '
        'prende seus membros.',
        DamageEnum.BLUDGEONING,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Seguindo a curiosidade, você abre o objeto e ativa uma armadilha de '
        'fumaça mágica.',
        DamageEnum.MAGIC,
        [
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.EXHAUSTION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.EXHAUSTION, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PETRIFIED, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PETRIFIED, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.SILENCE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.SILENCE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
        ]
    ),
    (
        'Desprendendo as presilhas, você aciona uma armadilha que o '
        'envolve em trevas de perdição.',
        DamageEnum.DARK,
        [
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 0.90},
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 0.90},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.75},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Com um clique, o mecanismo se abre, liberando um veneno paralisante.',
        DamageEnum.POISON,
        [
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.75},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.75},
        ]
    ),
    (
        'Desdobrando as abas, você aciona uma armadilha que libera '
        'uma chuva de rochas.',
        DamageEnum.ROCK,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Seguindo a curiosidade, você abre o objeto e ativa uma '
        'armadilha de correntes letais.',
        DamageEnum.BLUDGEONING,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Com um gesto descuidado, você ativa uma armadilha que '
        'libera um gás venenoso.',
        DamageEnum.POISON,
        [
            {'condition': DebuffEnum.POISONING, 'effectiveness': 1.00},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.75},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.75},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
        ]
    ),
    (
        'Ao remover a cobertura, uma rede de fios afiados de aço é '
        'disparada em sua direção.',
        DamageEnum.SLASHING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
        ]
    ),
    (
        'Desprendendo as presilhas, você aciona uma armadilha que o '
        'envolve em uma teia incandescente pegajosa.',
        DamageEnum.FIRE,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
        ]
    ),
    (
        'Seguindo a curiosidade, você abre o objeto e ativa '
        'uma armadilha de granizo.',
        DamageEnum.COLD,
        [
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.25},
        ]
    ),
    (
        'Com um clique, o mecanismo se abre, causando uma explosão de fogo.',
        DamageEnum.FIRE,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 1.00},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Desdobrando as abas, você aciona uma armadilha que dispara '
        'flechas envenenadas.',
        DamageEnum.POISON,
        [
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
        ]
    ),
    (
        'Seguindo a curiosidade, você abre o objeto e ativa uma '
        'armadilha de ácido corrosivo.',
        DamageEnum.ACID,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Com um gesto descuidado, você aciona uma armadilha que libera um '
        'enxame de insetos venenosos.',
        DamageEnum.POISON,
        [
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
        ]
    ),
    (
        'Ao remover a cobertura, um líquido viscoso começa a se derramar, '
        'corroendo tudo em seu alcance.',
        DamageEnum.ACID,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Desprendendo as presilhas, você aciona uma armadilha que liberta '
        'criaturas famintas.',
        DamageEnum.CHAOS,
        [
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.75},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.25},
        ]
    ),
    (
        'Seguindo a curiosidade, você abre o objeto e ativa uma armadilha '
        'que o faz escorregar em direção a um poço escuro.',
        DamageEnum.BLUDGEONING,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Com um clique, o mecanismo se abre, desencadeando uma '
        'tempestade de granizo.',
        DamageEnum.COLD,
        [
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.50},
        ]
    ),
    (
        'Desdobrando as abas, você ativa uma armadilha que o prende '
        'em uma rede de fios abrolhosos de aço.',
        DamageEnum.SLASHING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
        ]
    ),
    (
        'Seguindo a curiosidade, você abre o objeto e ativa uma '
        'armadilha de pedras que caem em você.',
        DamageEnum.ROCK,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Com um gesto descuidado, você aciona uma armadilha que '
        'desencadeia uma chuva de ácido.',
        DamageEnum.ACID,
        [
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.75},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Ao remover a cobertura, uma rede de arame é disparada '
        'em sua direção.',
        DamageEnum.PIERCING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Desprendendo as presilhas, você aciona uma armadilha que o faz '
        'cair em um poço profundo.',
        DamageEnum.BLUDGEONING,
        [
            {'condition': DebuffEnum.STUNNED, 'effectiveness': 0.90},
        ]
    ),
    (
        'Seguindo a curiosidade, você abre o objeto e ativa uma armadilha '
        'de flechas afiadas.',
        DamageEnum.PIERCING,
        [
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
        ]
    ),
    (
        'Com um clique, o mecanismo se abre, soltando uma criatura '
        'aterrorizante em sua direção.',
        DamageEnum.CHAOS,
        [
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FEARING, 'effectiveness': 0.25},
        ]
    ),
    (
        'Ao desvendar o objeto sagrado, um vento gélido emerge, ecoando um '
        'sussurro antigo: "Belendë ar mornië!"',
        DamageEnum.DIVINE,
        [
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.25},
            {'condition': DebuffEnum.EXHAUSTION, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.25},
            {'condition': DebuffEnum.PETRIFIED, 'effectiveness': 0.25},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.SILENCE, 'effectiveness': 0.25},
        ]
    ),
    (
        'Enquanto abre o artefato sagrado, uma chama divina emerge, e uma '
        'voz etérea proclama: "Fëanturi vahai!"',
        DamageEnum.DIVINE,
        [
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.25},
            {'condition': DebuffEnum.EXHAUSTION, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.25},
            {'condition': DebuffEnum.PETRIFIED, 'effectiveness': 0.25},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.SILENCE, 'effectiveness': 0.25},
        ]
    ),
    (
        'Ao tocar o objeto sagrado, uma energia divina irrompe, emitindo uma '
        'sentença: "Ainuvalë melin!"',
        DamageEnum.DIVINE,
        [
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.25},
            {'condition': DebuffEnum.EXHAUSTION, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.25},
            {'condition': DebuffEnum.PETRIFIED, 'effectiveness': 0.25},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.SILENCE, 'effectiveness': 0.25},
        ]
    ),
    (
        'Ao desvendar o artefato sagrado, uma tempestade mágica se forma, e '
        'uma voz ecoa: "Nai tiruvantel ar varyuvantel!"',
        DamageEnum.DIVINE,
        [
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.25},
            {'condition': DebuffEnum.EXHAUSTION, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.25},
            {'condition': DebuffEnum.PETRIFIED, 'effectiveness': 0.25},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.SILENCE, 'effectiveness': 0.25},
        ]
    ),
    (
        'Enquanto abre o objeto sagrado, uma aura negra o envolve, e uma voz '
        'ancestral decreta: "Aina i ahërë!"',
        DamageEnum.DIVINE,
        [
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.25},
            {'condition': DebuffEnum.EXHAUSTION, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.25},
            {'condition': DebuffEnum.PETRIFIED, 'effectiveness': 0.25},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.SILENCE, 'effectiveness': 0.25},
        ]
    ),
    (
        'Ao tocar o artefato sagrado, uma marca negra aparece em sua pele, '
        'acompanhada por uma voz severa: "Erë enesselmo!"',
        DamageEnum.DIVINE,
        [
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.25},
            {'condition': DebuffEnum.EXHAUSTION, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.25},
            {'condition': DebuffEnum.PETRIFIED, 'effectiveness': 0.25},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.SILENCE, 'effectiveness': 0.25},
        ]
    ),
    (
        'Ao abrir o objeto sagrado, uma energia maligna o envolve, e uma voz '
        'sinistra murmura: "Nai tiruvantes!"',
        DamageEnum.DIVINE,
        [
            {'condition': DebuffEnum.BERSERKER, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BLINDNESS, 'effectiveness': 0.25},
            {'condition': DebuffEnum.BURN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CONFUSION, 'effectiveness': 0.25},
            {'condition': DebuffEnum.CURSE, 'effectiveness': 0.25},
            {'condition': DebuffEnum.EXHAUSTION, 'effectiveness': 0.25},
            {'condition': DebuffEnum.FROZEN, 'effectiveness': 0.25},
            {'condition': DebuffEnum.PARALYSIS, 'effectiveness': 0.25},
            {'condition': DebuffEnum.PETRIFIED, 'effectiveness': 0.25},
            {'condition': DebuffEnum.POISONING, 'effectiveness': 0.25},
            {'condition': DebuffEnum.SILENCE, 'effectiveness': 0.25},
        ]
    ),
    (
        'Ao girar a chave, um brilho intenso de cristais o envolveu.',
        DamageEnum.CRYSTAL,
        [
            {'condition': DebuffEnum.CRYSTALLIZED, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CRYSTALLIZED, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Assim que o lacre foi rompido, estilhaços cristalinos surgiram.',
        DamageEnum.CRYSTAL,
        [
            {'condition': DebuffEnum.CRYSTALLIZED, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Com um estalo, uma rajada de cristais disparou em sua direção.',
        DamageEnum.CRYSTAL,
        [
            {'condition': DebuffEnum.CRYSTALLIZED, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Ao levantar a tampa, uma explosão de cristais se espalhou pelo ar.',
        DamageEnum.CRYSTAL,
        [
            {'condition': DebuffEnum.CRYSTALLIZED, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
        ]
    ),
    (
        'Ao soltar o fecho, você foi imediatamente cercado por cristais '
        'cintilantes.',
        DamageEnum.CRYSTAL,
        [
            {'condition': DebuffEnum.CRYSTALLIZED, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CRYSTALLIZED, 'effectiveness': 0.50},
            {'condition': DebuffEnum.CRYSTALLIZED, 'effectiveness': 0.50},
            {'condition': DebuffEnum.BLEEDING, 'effectiveness': 0.50},
        ]
    ),
]

REPLY_TEXTS_FIND_TRAP_DAMAGE = [
    '{user_name} perdeu',
    '{user_name} sofreu',
    '{user_name} levou',
    '{user_name} recebeu',
    'Lamentavelmente, {user_name} perdeu',
    'Infelizmente, {user_name} sofreu',
    'Tristemente, {user_name} levou',
    'Desafortunadamente, {user_name} recebeu',
    'Inesperadamente, {user_name} levou',
    'Infortunadamente, {user_name} recebeu',
    'De forma inesperada, {user_name} sofreu',
]


if __name__ == '__main__':
    for i, tt in enumerate(REPLY_TEXTS_FIND_TRAP_OPEN):
        try:
            print(i, end=',')
            _, _, conditions = tt
            for condition in conditions:
                acc = condition['effectiveness']
                if acc > 1.0:
                    raise ValueError(
                        f'Effectiveness {acc} é maior que 1.0.\n{tt}'
                    )
                if acc < 0.0:
                    raise ValueError(
                        f'Effectiveness {acc} é menor que 0.0.\n{tt}'
                    )
        except ValueError as error:
            print(tt)
            raise error
    print('OK!!!')
