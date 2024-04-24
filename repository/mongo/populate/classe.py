'''
    Arquivo que salva as Classes base no banco de dados.

    Referência: https://ordempendragon.files.wordpress.com/2017/04/dd-5e-livro-do-jogador-fundo-branco-biblioteca-c3a9lfica.pdf
'''

from repository.mongo import ClasseModel
from rpgram.boosters import Classe

CLASSES = [
    # Player 6.5 Points
    {
        'name': 'Bárbaro',
        'description': (
            'Bárbaros são definidos por sua fúria: '
            'desenfreada, inextinguível e irracional fúria. '
            'Mais que uma mera emoção, sua raiva é '
            'a ferocidade de um predador acuado, o assalto implacável '
            'de uma tempestade, a turbulência agitada do mar.\n\n'

            'Para alguns, suas fúrias emerge da comunhão com '
            'ferozes espíritos animais. Outras provem de um '
            'reservatório turvo de raiva de um mundo cheio de dor. '
            'Para cada bárbaro, a fúria é um poder que preenche não '
            'apenas o frenesi de batalha, mas também reflexos, '
            'resiliência e proezas de força incríveis.\n\n'

            'As pessoas das cidades e vilas costumam se vangloriar de '
            'como seus meios civilizados os diferencia dos animais, '
            'como se renegar sua própria natureza fosse um indicio de '
            'superioridade. Para um bárbaro, no entanto, a civilização '
            'não é nenhuma virtude, mas um sinal de fraqueza. Os '
            'fortes abraçam a sua natureza selvagem '
            '– instintos '
            'aguçados, fisicalidade primitiva e fúria voraz. Bárbaros '
            'ficam desconfortáveis quando estão cercados por '
            'muralhas e multidões. Eles crescem na natureza '
            'selvagem de suas terras natais: a tundra, selva ou '
            'pradarias onde suas tribos vivem e caçam.\n\n'

            'Os bárbaros se sentem mais vivos em meio ao caos do '
            'combate. Eles podem entrar num estado de furor quando '
            'sua fúria toma controle, concedendo-lhes força e '
            'resiliência sobre-humanas. Um bárbaro pode consumir '
            'desse reservatório de fúria apenas algumas vezes antes '
            'de descansar, mas essas poucas fúrias geralmente são '
            'suficientes para derrotar seja lá o que está ameaçando o '
            'seu caminho.'
        ),
        'enemy': False,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 2,
        'multiplier_dexterity': 1,
        'multiplier_constitution': 2,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 0.5,
        'multiplier_charisma': 0.5,
    },
    {
        'name': 'Clérigo',
        'description': (
            'Clérigos são intermediadores entre o mundo mortal e o '
            'distante plano dos deuses. Tão variados quanto os deuses '
            'que servem, clérigos se esforçam para ser a própria mão '
            'de seus deuses. Não é apenas um sacerdote comum, mas '
            'alguém investido de poder divino.\n\n'

            'Magia divina, como o nome sugere, é o poder dos deuses '
            'fluindo deles para o mundo mortal. Clérigos são os '
            'condutores desse poder, manifestando-o através de efeitos '
            'milagrosos. Os deuses não conferem esse poder a '
            'qualquer um que o queira, mas apenas àqueles escolhidos '
            'para cumprir o chamado.\n\n'

            'Fazer uso do poder divino não envolve estudo ou '
            'treinamento. Um clérigo pode aprender ritos antigos e '
            'preces específicas, mas a habilidade de usar magias '
            'divinas depende de devoção e de uma intuição poderosa '
            'sobre os desejos da divindade.\n\n'

            'Clérigos combinam o poder mágico de curar e inspirar '
            'seus aliados com magias que ferem e debilitam seus '
            'inimigos. Eles podem causar medo e pavor, espalhar '
            'pragas ou venenos, e até lançar fogo divino para consumir '
            'seus inimigos. Para aqueles malfeitores que merecem '
            'uma maça na têmpora, o clérigo se utiliza de seu '
            'treinamento de combate para enfrentar seus inimigos '
            'corpo-a-corpo, auxiliado pelo poder divino.'
        ),
        'enemy': False,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.1,
        'multiplier_dexterity': 0.5,
        'multiplier_constitution': 1,
        'multiplier_intelligence': 1.5,
        'multiplier_wisdom': 2,
        'multiplier_charisma': 1.4,
    },
    {
        'name': 'Druida',
        'description': (
            'Quer seja convocando as forças elementais da '
            'natureza, ou emulando as criaturas do mundo animal, os '
            'druidas são encarnações da resistência, astúcia e fúria da '
            'natureza. Eles não se consideram donos da natureza. Ao '
            'invés disso, eles se veem como extensões da vontade '
            'indomável da natureza.\n\n'

            'Os druidas reverenciam a natureza acima de tudo, '
            'adquirindo suas magias e outros poderes mágicos, ou da '
            'força da natureza per si ou de uma divindade da '
            'natureza. Muitos druidas buscam uma espiritualidade '
            'mística de união transcendental com a natureza ao invés '
            'de se devotarem a uma entidade divina, enquanto outros '
            'servem deuses da natureza selvagem, animais ou forças '
            'elementais. As antigas tradições druídicas, algumas vezes '
            'são chamadas de Crença Antiga, contrastando com a '
            'adoração de deuses em templos ou santuários.\n\n'

            'As magias de druida são orientadas para a natureza e '
            'para os animais – o poder da presa e garra, do sol e da '
            'lua, do fogo e da tormenta. Os druidas também adquirem '
            'a habilidade de transformarem em animais e alguns '
            'druidas fazem estudos pessoais dessa pratica, chegando '
            'até mesmo ao ponto de preferirem formas animais a suas '
            'formas naturais.'
        ),
        'enemy': False,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 1.7,
        'multiplier_dexterity': 1,
        'multiplier_constitution': 1.7,
        'multiplier_intelligence': 0.1,
        'multiplier_wisdom': 1.5,
        'multiplier_charisma': 0.5,
    },
    {
        'name': 'Feiticeiro',
        'description': (
            'Os feiticeiros carregam um patrimônio mágico '
            'conferido a eles por uma linhagem exótica, alguma '
            'influência de outro mundo ou exposição a forças cósmicas '
            'desconhecidas. Não é possível estudar feitiçaria como se '
            'aprende um idioma, assim como não se aprende a viver '
            'uma vida lendária. Ninguém escolhe a feitiçaria: os '
            'poderes escolhem o feiticeiro.\n\n'

            'A magia é parte de todo feiticeiro, inundando corpo, '
            'mente e espirito com um poder latente que espera para '
            'ser dominado. Alguns feiticeiro carregam magia que '
            'emerge de uma antiga linhagem infundida com a magia '
            'dos dragões. Outros carregam uma magia bruta, '
            'incontrolável dentro de si, uma tormenta caótica que se '
            'manifesta de formas inexplicáveis.\n\n'

            'A aparência dos poderes de feitiçaria são vastamente '
            'imprevisíveis. Algumas linhagens dracônicas produzem '
            'apenas um feiticeiro por geração, porém, em outras linhas '
            'de descendência, todos os indivíduos serão feiticeiros. A '
            'maior parte do tempo, os talentos de feitiçaria aparecem '
            'aparentemente ao acaso. Alguns feiticeiros não '
            'conseguem determinar a origem do seu poder, enquanto '
            'outros o relacionam com estranhos eventos de suas vidas. '
            'O toque de um corruptor, a bênção de uma dríade no '
            'nascimento de um bebê ou experimentar a água de uma '
            'fonte misteriosa podem conceder o dom da feitiçaria. '
            'Também é possível adquirir esse dom de uma divindade '
            'da magia, da exposição as forças elementais dos Planos '
            'Interiores ou do caos alucinante do Limbo ou ao '
            'vislumbrar o funcionamento interno da realidade.\n\n'

            'Os feiticeiros não veem serventia em grimórios ou '
            'antigos tomos de conhecimento místico buscados pelos '
            'magos, nem buscam um patrono para conceder-lhes suas '
            'magias, como um bruxo faz. Ao aprender a explorar e '
            'canalizar sua própria magia inata, eles descobrem novas '
            'e incríveis formas de liberar esse poder.'
        ),
        'enemy': False,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.1,
        'multiplier_dexterity': 1,
        'multiplier_constitution': 0.5,
        'multiplier_intelligence': 2,
        'multiplier_wisdom': 2,
        'multiplier_charisma': 0.9,
    },
    {
        'name': 'Guerreiro',
        'description': (
            'Cavaleiros em missões, lordes '
            'conquistadores, campeões reais, infantaria de elite, '
            'mercenários rígidos e bandidos reis, como guerreiros, eles '
            'compartilham de uma maestria com armas e armaduras '
            'sem precedentes, bem como um vasto conhecimento e '
            'habilidades em combate. E eles estão bem familiarizados '
            'com a morte, seja simplesmente conhecendo-a ou '
            'desafiando-a cara a cara.\n\n'

            'Guerreiros aprendem o básico de todos os estilos de '
            'combate. Todo guerreiro sabe brandir um machado, '
            'esgrimir com uma rapieira, empunhar uma espada longa '
            'ou uma espada grande, usar um arco ou mesmo prender '
            'inimigos em uma rede com algum grau de perícia. Da '
            'mesma forma, um guerreiro sabe usar escudos e qualquer '
            'tipo de armadura. Além do conhecimento básico, cada '
            'guerreiro se especializa em certo estilo de combate. '
            'Alguns se concentram na arquearia, outros em lutar com '
            'duas armas ao mesmo tempo e ainda existem aqueles que '
            'aprimoram suas habilidades marciais com magia. Essas '
            'combinações de ampla capacidade generalista e uma '
            'vasta especialização tornam os guerreiros combatentes '
            'superiores nos campos de batalha e masmorras.'
        ),
        'enemy': False,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 2,
        'multiplier_dexterity': 1.5,
        'multiplier_constitution': 1.5,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 0.5,
        'multiplier_charisma': 0.5,
    },
    {
        'name': 'Ladino',
        'description': (
            'Ladinos contam com sua perícia, furtividade e as '
            'vulnerabilidades de seus inimigos para obter vantagem '
            'em qualquer situação. Eles possuem uma habilidade '
            'especial para encontrar a solução para praticamente '
            'qualquer problema, demonstrando desenvoltura e '
            'versatilidade, a chave de qualquer grupo aventureiro de '
            'sucesso.\n\n'

            'Ladinos dedicam muito de seus recursos para se '
            'tornarem mestres em várias perícias, bem como '
            'aperfeiçoar suas habilidades em combate, adquirindo '
            'uma vasta experiência que poucos personagens podem '
            'alcançar. Muitos ladinos focam na furtividade e trapaça, '
            'enquanto outros refinam suas perícias para ajudá-los nas '
            'masmorras, como escalada, encontrar e desarmar '
            'armadilhas, e abrir fechaduras.\n\n'

            'Em combate, ladinos priorizam astúcia em vez de '
            'força bruta. O ladino sempre prefere desferir um ataque '
            'preciso, bem naquele lugar que mais machuca, do que '
            'derrubar um oponente com uma série de ataques. Ladinos '
            'possuem uma habilidade quase sobrenatural de evitar o '
            'perigo, e alguns poucos aprendem truques de magia para '
            'incrementar suas outras habilidades.'
        ),
        'enemy': False,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 1,
        'multiplier_dexterity': 2.5,
        'multiplier_constitution': 1.2,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 1.2,
        'multiplier_charisma': 0.1,
    },
    {
        'name': 'Mago',
        'description': (
            'Os magos são usuários de magia soberanos, unidos e '
            'definidos como uma classe pelas magias que conjuram. '
            'Usufruindo de uma trama sutil de magia que permeia o '
            'cosmos, os magos conjuram magias explosivas de fogo, '
            'arcos de relâmpagos, enganos sutis e controle de mentes '
            'de força bruta. Sua magia invoca monstros de outros '
            'planos de existência, vislumbra o futuro ou transforma '
            'inimigos mortos em zumbis. Suas magias mais poderosas '
            'podem transformar uma substância em outra, evocar '
            'meteoros que caem do céu ou abrir portais para outros '
            'mundos.\n\n'

            'Selvagem e enigmático, variado nas formas e funções, o '
            'poder da magia atrai estudiosos que buscam dominar '
            'seus mistérios. Alguns aspiram ser como deuses, '
            'moldando a realidade à sua vontade. Embora, conjurar '
            'uma magia básica requeira meramente a pronúncia de '
            'algumas palavras estranhas, gestos fugazes, e às vezes '
            'um punhado ou um grupo de materiais exóticos, esses '
            'materiais mal denotam a experiência alcançada após anos '
            'de aprendizagem e incontáveis horas de estudo.\n\n'

            'Magos vivem e morrem por suas magias. Todo o resto '
            'é secundário. Eles aprendem novas magias à medida que '
            'eles experimentam e crescem em experiência. Também '
            'podem aprender magias de outros magos, de tomos '
            'antigos ou escrituras, e de criaturas anciãs (como as '
            'fadas) que são imersas em magia.'
        ),
        'enemy': False,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.5,
        'multiplier_dexterity': 0.5,
        'multiplier_constitution': 0.5,
        'multiplier_intelligence': 2.5,
        'multiplier_wisdom': 1.5,
        'multiplier_charisma': 1,
    },
    {
        'name': 'Paladino',
        'description': (
            'Os paladinos treinam por anos para aprender as perícias de '
            'combate, dominando uma variedade de armas e armaduras. '
            'Mesmo assim, suas perícias marciais são secundárias ao poder '
            'mágico que ele empunha: o poder de curar os doentes e feridos, '
            'de destruir os cruéis e os mortos-vivos e de proteger os '
            'inocentes e aqueles que se unirem à eles na '
            'luta pela justiça.\n\n'

            'Seja lá quais forem suas origens e suas missões, paladinos são '
            'unidos pelos seus juramentos de se imporem contra as forças do '
            'mal. '
            'Quer seja jurado ante o altar de um deus com um clérigo '
            'como testemunha, quer seja em uma clareira sagrada diante dos '
            'espíritos da natureza e seres feéricos, ou em um momento de '
            'desespero e aflição com os mortos como únicas testemunhas, o '
            'juramento de um paladino é um laço poderoso. '
            'Ele é uma fonte de poder que transforma um guerreiro devotado '
            'em um campeão abençoado.'
        ),
        'enemy': False,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 1.2,
        'multiplier_dexterity': 1,
        'multiplier_constitution': 1,
        'multiplier_intelligence': 1,
        'multiplier_wisdom': 1.3,
        'multiplier_charisma': 1,
    },
    {
        'name': 'Guardião',
        'description': (
            'Os Guardiões são mestres na arte da proteção, '
            'dedicando suas habilidades e vida à defesa de seus aliados. '
            'Armados com escudos imponentes e uma determinação inabalável, '
            'eles se destacam no campo de batalha como baluartes da '
            'segurança, capazes de suportar os ataques mais ferozes com '
            'bravura e resiliência. Seu principal objetivo é garantir a '
            'sobrevivência daqueles que juraram proteger, colocando suas '
            'próprias vidas em risco para cumprir esse dever sagrado.\n\n'

            'Com um treinamento rigoroso em técnicas de defesa e resistência, '
            'os Guardiões são capazes de enfrentar qualquer ameaça de frente, '
            'usando sua armadura pesada e escudos maciços para bloquear '
            'ataques e desviar perigos iminentes. '
            'Além de sua habilidade física, os Guardiões também são '
            'conhecidos por sua coragem e lealdade inabaláveis, '
            'dispostos a enfrentar qualquer desafio para proteger seus '
            'protegidos. '
            'Sua presença no campo de batalha inspira confiança e '
            'segurança naqueles que lutam ao seu lado, tornando-os '
            'indispensáveis em qualquer grupo.'
        ),
        'enemy': False,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 1.5,
        'multiplier_dexterity': 0.5,
        'multiplier_constitution': 3,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 0.5,
        'multiplier_charisma': 0.5,
    },
    {
        'name': 'Duelista',
        'description': (
            'Os Duelistas são mestres da agilidade e da destreza, '
            'especialistas em combate corpo a corpo com armas '
            'leves e rápidas. '
            'Sua habilidade em esquivar-se de golpes e atacar com precisão '
            'faz deles adversários temíveis em duelos individuais, '
            'onde sua destreza e rapidez são colocadas à prova. '
            'Eles são conhecidos por sua habilidade em desferir golpes '
            'rápidos e precisos, causando danos significativos aos seus '
            'oponentes enquanto evitam seus ataques.\n\n'

            'Além de suas habilidades físicas superiores, os Duelistas '
            'também são mestres na arte da estratégia e da astúcia. '
            'Eles são capazes de ler seus oponentes e antecipar seus '
            'movimentos, dando-lhes uma vantagem significativa em combate. '
            'Sua capacidade de improvisar e se adaptar rapidamente às '
            'mudanças no campo de batalha os torna combatentes '
            'versáteis e imprevisíveis, capazes de superar até mesmo os '
            'adversários mais poderosos.\n\n'
        ),
        'enemy': False,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.5,
        'multiplier_dexterity': 3.5,
        'multiplier_constitution': 1,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 0.5,
        'multiplier_charisma': 0.5,
    },
    # Enemies 8 Points
    {
        'name': 'Arauto',
        'description': (
            'O Arauto é um mestre na arte da defesa, '
            'dedicando-se a proteger seus aliados e garantir a segurança do '
            'grupo em batalha. '
            'Com habilidades defensivas, '
            'o Arauto é capaz de absorver ataques e mitigar danos, '
            'tornando-se uma muralha impenetrável diante dos inimigos.\n\n'

            'Além de sua proficiência defensiva, '
            'o Arauto também possui habilidades que inspiram coragem e '
            'determinação em seus companheiros, '
            'elevando sua moral e resistência. '
            'Sua presença no campo de batalha é reconfortante, '
            'pois os aliados sabem que podem confiar na sua proteção e '
            'liderança para enfrentar qualquer desafio com mais '
            'confiança e segurança.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 1,
        'multiplier_dexterity': 1,
        'multiplier_constitution': 3,
        'multiplier_intelligence': 1,
        'multiplier_wisdom': 1,
        'multiplier_charisma': 1,
    },
    {
        'name': 'Arcanista',
        'description': (
            'Os Arcanistas são estudiosos dedicados à arte da magia arcana, '
            'uma forma poderosa de magia que manipula os elementos '
            'fundamentais do universo. '
            'Compreendem os segredos dos planos de existência e '
            'são capazes de canalizar essa energia para realizar '
            'feitos incríveis. '
            'Suas habilidades variam desde lançar bolas de fogo até '
            'controlar mentes e alterar a própria realidade.\n\n'

            'Esses praticantes da magia são frequentemente vistos como '
            'sábios e eruditos, passando longos anos em estudo e prática '
            'para dominar seus poderes. '
            'Suas vestes muitas vezes são adornadas com símbolos arcanos '
            'e suas mentes são afiadas como lâminas, '
            'capazes de resolver os enigmas mais complexos e superar os '
            'desafios mais difíceis com sua magia. '
            'Em combate, os Arcanistas podem se posicionar '
            'como uma força formidável, '
            'capazes de virar o curso de uma batalha com um único '
            'feitiço poderoso.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.1,
        'multiplier_dexterity': 1,
        'multiplier_constitution': 0.5,
        'multiplier_intelligence': 4,
        'multiplier_wisdom': 1.9,
        'multiplier_charisma': 0.5,
    },
    {
        'name': 'Bardo',
        'description': (
            'Os bardos são artistas itinerantes e contadores de histórias, '
            'cuja magia se manifesta através da música, '
            'poesia e encantamento. '
            'São mestres na arte da performance, capazes de cativar plateias '
            'e influenciar mentes com suas habilidades. '
            'Além de entreter, os bardos também possuem um profundo '
            'conhecimento sobre o mundo e suas histórias, '
            'sendo fontes valiosas de informações e sabedoria.\n\n'

            'Em batalha, '
            'os bardos utilizam sua música para inspirar aliados e '
            'desmoralizar inimigos, '
            'podendo também lançar feitiços mágicos através de suas canções. '
            'Sua versatilidade os torna capazes de se adaptar a '
            'diversas situações, '
            'seja no campo de batalha, '
            'em negociações diplomáticas ou na resolução '
            'de enigmas e mistérios. '
            'Os bardos são, portanto, tanto artistas quanto heróis, '
            'cujas canções ecoam através do tempo, '
            'inspirando gerações futuras.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.5,
        'multiplier_dexterity': 0.5,
        'multiplier_constitution': 0.5,
        'multiplier_intelligence': 1,
        'multiplier_wisdom': 2,
        'multiplier_charisma': 3.5,
    },
    {
        'name': 'Caçador de Recompensas',
        'description': (
            'Os Caçadores de Recompensas são mestres na arte da captura '
            'de fugitivos e criminosos procurados. '
            'Com habilidades de rastreamento altamente desenvolvidas, '
            'eles são capazes de localizar seus alvos em qualquer lugar, '
            'seja em florestas densas, '
            'cidades labirínticas ou desertos escaldantes. '
            'Além disso, possuem habilidades de combate excepcionais, '
            'tornando-os formidáveis adversários em confrontos diretos.\n\n'

            'Esses profissionais são conhecidos por sua determinação '
            'e sagacidade, muitas vezes aceitando missões perigosas '
            'em troca de recompensas substanciais. '
            'Eles podem trabalhar de forma independente ou serem '
            'contratados por autoridades locais ou organizações '
            'para lidar com ameaças específicas. '
            'Sua reputação é construída com base em sua eficácia e no '
            'cumprimento bem-sucedido de contratos, '
            'tornando-os figuras respeitadas e '
            'temidas no mundo mercenário.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 2,
        'multiplier_dexterity': 1.5,
        'multiplier_constitution': 1.5,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 1,
        'multiplier_charisma': 1.5,
    },
    {
        'name': 'Cavaleiro',
        'description': (
            'Os Cavaleiros são guerreiros treinados na arte da equitação '
            'e da guerra montada, '
            'cuja destreza e habilidade com a espada são igualadas apenas '
            'pela sua habilidade no controle de seus imponentes corcéis. '
            'Eles são uma visão impressionante no campo de batalha, '
            'galopando com graça e poder enquanto lideram suas tropas em '
            'cargas audaciosas ou engajam os inimigos em combate '
            'corpo a corpo.\n\n'

            'Com suas montarias como extensões de si mesmos, '
            'os Cavaleiros são capazes de realizar manobras habilidosas e '
            'ataques precisos, '
            'aproveitando a velocidade e a força de seus cavalos para '
            'superar seus oponentes. '
            'Além de sua proficiência no combate montado, '
            'muitos Cavaleiros também juram fidelidade a um código de honra '
            'e lealdade, dedicando suas vidas à defesa de seu reino e '
            'à proteção dos indefesos.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 1,
        'multiplier_dexterity': 3,
        'multiplier_constitution': 1.5,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 0.5,
        'multiplier_charisma': 1.5,
    },
    {
        'name': 'Curandeiro',
        'description': (
            'O Curandeiro é um especialista em cura e restauração, '
            'dedicado a manter seus aliados saudáveis e '
            'prontos para o combate. '
            'Com habilidades de cura divinas ou naturais, '
            'o Curandeiro pode fechar ferimentos, '
            'remover doenças e até mesmo trazer os mortos de volta à vida. '
            'Sua presença em um grupo é essencial, '
            'pois sua capacidade de manter a equipe saudável pode fazer a '
            'diferença entre a vitória e a derrota em batalhas difíceis.\n\n'

            'Além de suas habilidades de cura, '
            'o Curandeiro também pode ser treinado em técnicas de '
            'proteção e suporte, como criar barreiras mágicas para '
            'proteger seus aliados ou fortalecer sua resistência '
            'contra ataques. '
            'Sua dedicação ao bem-estar dos outros muitas vezes o '
            'torna um líder natural, '
            'inspirando confiança e coragem naqueles ao seu redor.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.1,
        'multiplier_dexterity': 0.1,
        'multiplier_constitution': 1,
        'multiplier_intelligence': 2.3,
        'multiplier_wisdom': 3,
        'multiplier_charisma': 1.5,
    },
    {
        'name': 'Gladiador',
        'description': (
            'Os gladiadores são mestres na arte do combate, '
            'treinados desde jovens para enfrentar adversários em '
            'arenas em batalhas épicas. '
            'São habilidosos com uma variedade de armas e técnicas de luta, '
            'adaptando-se a diferentes estilos de combate '
            'conforme necessário. '
            'Sua destreza e agilidade são tão importantes quanto sua '
            'força bruta, permitindo-lhes desferir golpes precisos e '
            'esquivar-se de ataques inimigos com facilidade.\n\n'

            'Além de suas habilidades físicas, '
            'os gladiadores também possuem uma forte presença mental, '
            'capaz de manter a calma e a concentração mesmo nas '
            'situações mais adversas. '
            'São resistentes e determinados, capazes de suportar ferimentos '
            'e continuar lutando até o fim. '
            'Sua coragem e determinação os tornam figuras admiradas e '
            'respeitadas, tanto dentro quanto fora da arena.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 2,
        'multiplier_dexterity': 1,
        'multiplier_constitution': 1.5,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 1.5,
        'multiplier_charisma': 1.5,
    },
    {
        'name': 'Invocador',
        'description': (
            'Os Invocadores são mestres das artes arcanas que se '
            'especializam em convocar e controlar criaturas de outras '
            'dimensões ou planos de existência para auxiliá-los em batalha. '
            'Utilizando rituais complexos e poderosos feitiços de invocação, '
            'eles são capazes de trazer seres mágicos e elementais para o '
            'mundo físico, para servir como guardiões, '
            'combatentes ou mesmo como fonte de conhecimento e sabedoria.\n\n'

            'Essa classe geralmente requer um profundo conhecimento '
            'das criaturas que pretendem invocar, '
            'bem como habilidades de comunicação e controle mental para '
            'garantir que as criaturas convocadas ajam de acordo com a '
            'vontade do Invocador. '
            'Muitos veem os Invocadores com desconfiança, '
            'devido ao seu poder de manipular seres de outros planos, '
            'e há aqueles que os temem pela imprevisibilidade e perigosidade '
            'das criaturas que podem convocar.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.1,
        'multiplier_dexterity': 0.5,
        'multiplier_constitution': 1,
        'multiplier_intelligence': 4,
        'multiplier_wisdom': 2.3,
        'multiplier_charisma': 0.1,
    },
    {
        'name': 'Mercenário',
        'description': (
            'Os Mercenários são guerreiros contratados para realizar '
            'tarefas que vão desde proteção pessoal até missões '
            'de extermínio. '
            'Conhecidos por sua versatilidade e pragmatismo, '
            'eles não seguem um código de honra rígido como os paladinos, '
            'mas sim a lógica de que o trabalho deve ser feito, '
            'desde que o preço seja justo.\n\n'

            'Esses combatentes são habilidosos em várias formas de combate, '
            'adaptando-se a diferentes situações com facilidade. '
            'Sua lealdade é para com quem os contratou, '
            'e não costumam se envolver em questões morais ou políticas, '
            'a menos que isso afete diretamente seu pagamento. '
            'Os Mercenários são uma presença comum em áreas de conflito e '
            'muitas vezes são vistos como indivíduos pragmáticos, '
            'dispostos a fazer o que for preciso para sobreviver e '
            'prosperar em um mundo perigoso.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 2.4,
        'multiplier_dexterity': 1.5,
        'multiplier_constitution': 2.5,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 1,
        'multiplier_charisma': 0.1,
    },
    {
        'name': 'Necromante',
        'description': (
            'O Necromante é um praticante das artes obscuras da necromancia, '
            'um ramo da magia que lida com a manipulação da '
            'morte e dos mortos. '
            'Estudioso e muitas vezes isolado, '
            'o Necromante busca compreender os segredos da vida e da morte, '
            'utilizando seu conhecimento para controlar cadáveres e '
            'canalizar energia negra para diversos fins.\n\n'

            'Por meio de rituais e feitiços proibidos, '
            'o Necromante é capaz de criar e controlar servos mortos-vivos, '
            'como zumbis e esqueletos, que obedecem às suas ordens. '
            'Além disso, ele pode lançar maldições poderosas sobre '
            'seus inimigos, enfraquecendo-os e trazendo ruína aos que '
            'ousam desafiá-lo.\n\n'

            'Apesar de ser frequentemente visto com desconfiança e medo '
            'pelas sociedades mais tradicionais, '
            'o Necromante muitas vezes enxerga a si mesmo como um estudioso '
            'em busca do equilíbrio entre vida e morte, '
            'explorando os limites da magia e da moralidade em sua busca '
            'pelo conhecimento supremo.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.1,
        'multiplier_dexterity': 1,
        'multiplier_constitution': 1,
        'multiplier_intelligence': 3.3,
        'multiplier_wisdom': 2.5,
        'multiplier_charisma': 0.1,
    },
    {
        'name': 'Patrulheiro',
        'description': (
            'Os Patrulheiros são mestres dos ermos, '
            'hábeis caçadores e rastreadores que guardam as fronteiras '
            'selvagens contra as ameaças que espreitam nas sombras. '
            'Com um profundo conhecimento da natureza, '
            'eles são capazes de se mover com facilidade em terrenos '
            'difíceis, encontrando trilhas e passagens secretas que '
            'passam despercebidas pelos olhos menos treinados.\n\n'

            'Além de suas habilidades de sobrevivência, '
            'os Patrulheiros são exímios arqueiros e combatentes furtivos, '
            'capazes de emboscar seus inimigos com precisão mortal. '
            'Sua ligação com a natureza também lhes confere a capacidade '
            'de invocar aliados animais para auxiliá-los em suas missões, '
            'tornando-os ainda mais formidáveis em combate.\n\n'

            'Apesar de sua preferência pela solidão das fronteiras, '
            'os Patrulheiros são aliados valiosos para qualquer grupo '
            'que busque explorar terras desconhecidas ou enfrentar perigos '
            'naturais e sobrenaturais. '
            'Sua dedicação em proteger a natureza e suas habilidades '
            'únicas fazem deles guardiões essenciais em qualquer jornada.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 1,
        'multiplier_dexterity': 3,
        'multiplier_constitution': 2,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 1,
        'multiplier_charisma': 0.5,
    },
    {
        'name': 'Xamã',
        'description': (
            'O Xamã é um mestre das artes espirituais, '
            'um mediador entre o mundo físico e o espiritual. '
            'Por meio de rituais ancestrais e comunhão com os espíritos '
            'da natureza, o Xamã invoca poderes divinos para curar '
            'ferimentos, proteger os companheiros e conjurar elementos '
            'da natureza para auxiliar em batalhas.\n\n'

            'Além de suas habilidades de cura e proteção, '
            'o Xamã também possui o dom da previsão, '
            'podendo ter visões do futuro e orientar seu grupo em '
            'direções mais seguras. '
            'Sua conexão com os espíritos também lhe confere conhecimento '
            'sobre criaturas sobrenaturais e como lidar com elas, '
            'tornando-o um guia valioso em terras '
            'desconhecidas e perigosas.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.1,
        'multiplier_dexterity': 0.5,
        'multiplier_constitution': 1,
        'multiplier_intelligence': 2,
        'multiplier_wisdom': 3,
        'multiplier_charisma': 1.4,
    },
    {
        'name': 'Samurai',
        'description': (
            'Os samurais são guerreiros honrados e disciplinados, '
            'cujas habilidades em combate são lendárias. '
            'Treinados desde jovens nas artes marciais e no código de conduta '
            'bushido, os samurais são mestres da espada e da estratégia de '
            'batalha. '
            'Com um profundo senso de dever e lealdade, eles servem seus '
            'senhores com devoção, prontos para sacrificar suas vidas em '
            'nome da honra e do dever.\n\n'

            'Em combate, os samurais são conhecidos por sua habilidade com a '
            'katana, uma espada longa e afiada, e sua destreza em técnicas de '
            'combate corpo a corpo. Eles são mestres em usar sua força '
            'interior para aumentar sua velocidade e precisão em batalha, '
            'tornando-os adversários formidáveis. '
            'Além disso, os samurais são habilidosos arqueiros e cavaleiros, '
            'capazes de se adaptar a diferentes situações de combate com '
            'facilidade e graça.\n\n'

            'A moralidade e o código de conduta dos samurais são fundamentais '
            'em sua vida diária e em suas batalhas. '
            'Eles seguem princípios de justiça, coragem, compaixão, cortesia, '
            'honestidade e honra, buscando sempre agir com integridade e '
            'respeito. '
            'Esses valores não apenas guiam suas ações, '
            'mas também os distinguem como guerreiros respeitados e '
            'admirados por seu povo e por seus inimigos.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.5,
        'multiplier_dexterity': 3,
        'multiplier_constitution': 2,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 0.5,
        'multiplier_charisma': 1.5,
    },
    # Enemies 13 Points
    {
        'name': 'Berserkir',
        'description': (
            'O Berserkir é um guerreiro feroz e destemido que entra '
            'em um estado de fúria incontrolável durante o combate. '
            'Movido pela intensa emoção da batalha, ele ignora dor e medo, '
            'buscando apenas destruir seus inimigos com pura força bruta.\n\n'

            'Durante sua fúria, '
            'o Berserkir se torna uma força imparável, '
            'capaz de infligir danos devastadores e superar adversidades '
            'que seriam insuperáveis em condições normais. '
            'No entanto, essa fúria vem com um preço, '
            'pois o Berserkir muitas vezes perde o controle de si mesmo, '
            'colocando em risco não apenas seus inimigos, '
            'mas também seus aliados e até mesmo sua própria vida.\n\n'

            'Apesar de sua natureza selvagem, '
            'o Berserkir é frequentemente reverenciado por sua coragem e '
            'determinação inabaláveis, '
            'sendo visto como um símbolo de força e bravura no '
            'campo de batalha.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 5,
        'multiplier_dexterity': 2.5,
        'multiplier_constitution': 4,
        'multiplier_intelligence': 0.1,
        'multiplier_wisdom': 1.3,
        'multiplier_charisma': 0.1,
    },
    {
        'name': 'Mestre das Armas',
        'description': (
            'O Mestre das Armas é um especialista na arte do combate '
            'corpo a corpo, dominando uma variedade de '
            'armas e estilos de luta. '
            'Sua perícia e treinamento excepcionais o tornam um '
            'combatente formidável, '
            'capaz de enfrentar inimigos de todas as formas e '
            'tamanhos com confiança e habilidade. '
            'Ele é conhecido por sua destreza com armas de todas as formas, '
            'desde espadas e machados até lanças e martelos, '
            'adaptando-se a cada situação de combate com maestria.\n\n'

            'Além de sua proficiência no manejo de armas, '
            'o Mestre das Armas também possui um profundo conhecimento '
            'sobre o campo de batalha e táticas de combate. '
            'Ele é capaz de avaliar rapidamente uma situação e '
            'tomar decisões estratégicas que podem virar o curso '
            'de uma batalha a seu favor. '
            'Sua presença no campo de batalha inspira aliados e '
            'intimida inimigos, tornando-o um líder natural '
            'em situações de conflito.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 4,
        'multiplier_dexterity': 3,
        'multiplier_constitution': 3,
        'multiplier_intelligence': 1,
        'multiplier_wisdom': 1,
        'multiplier_charisma': 1,
    },
    {
        'name': 'Feiticeiro Supremo',
        'description': (
            'O Feiticeiro Supremo é o ápice do poder arcano, '
            'um mestre absoluto das artes mágicas. '
            'Seu conhecimento sobre os segredos do universo e sua '
            'habilidade em manipular a energia mística são incomparáveis. '
            'Com um simples gesto, ele pode desencadear tempestades de fogo, '
            'erguer barreiras impenetráveis ou até mesmo distorcer a '
            'realidade ao seu redor.\n\n'

            'Além de seu poder impressionante, '
            'o Feiticeiro Supremo também é um guardião do equilíbrio mágico. '
            'Ele usa sua sabedoria para evitar que o uso irresponsável '
            'da magia cause danos ao mundo. '
            'Sua presença é muitas vezes vista como uma garantia de paz '
            'e segurança, mas também como um lembrete do poder avassalador '
            'que a magia pode ter em mãos erradas.\n\n'

            'A jornada para se tornar um Feiticeiro Supremo é longa e árdua, '
            'exigindo anos de estudo e prática dedicada. '
            'Aqueles que alcançam esse nível de maestria são poucos '
            'e geralmente são figuras lendárias, '
            'cujos feitos são contados em histórias e '
            'canções por gerações.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.2,
        'multiplier_dexterity': 2,
        'multiplier_constitution': 1,
        'multiplier_intelligence': 4,
        'multiplier_wisdom': 4,
        'multiplier_charisma': 1.8,
    },
    {
        'name': 'Senhor dos Ladinos',
        'description': (
            'O Senhor dos Ladinos é um mestre na arte da astúcia e da '
            'furtividade, combinando habilidades de luta com técnicas de '
            'engano e dissimulação. '
            'Este mestre dos ladinos não apenas domina o combate '
            'corpo a corpo, mas também é um líder entre os ladrões, '
            'capaz de orquestrar ataques coordenados e '
            'elaborar planos complexos.\n\n'

            'Com sua destreza e perspicácia, o Senhor dos Ladinos '
            'é capaz de contornar até mesmo as defesas mais sólidas, '
            'encontrando pontos fracos em armaduras e estratégias inimigas. '
            'Além disso, ele possui um talento especial para '
            'identificar e desarmar armadilhas, '
            'tornando-o essencial em missões que exigem furtividade '
            'e agilidade.\n\n'

            'Seu conhecimento extenso sobre o submundo e suas conexões '
            'com outras figuras do crime lhe conferem uma vantagem '
            'única em lidar com situações de conflito e intriga. '
            'Por meio de sua inteligência afiada e sua habilidade de '
            'improvisar, o Senhor dos Ladinos se destaca como um '
            'líder entre os marginais, capaz de superar desafios '
            'com sagacidade e astúcia.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 2,
        'multiplier_dexterity': 5,
        'multiplier_constitution': 2.4,
        'multiplier_intelligence': 1,
        'multiplier_wisdom': 2.4,
        'multiplier_charisma': 0.2,
    },
]

if __name__ == '__main__':
    classe_model = ClasseModel()
    fields = ['_id', 'name', 'created_at']
    for classe_dict in CLASSES:
        classe_name = classe_dict['name']
        mongo_dict = classe_model.get(
            query={'name': classe_name},
            fields=fields,
        )
        if mongo_dict:
            for field in fields:
                classe_dict[field] = mongo_dict[field]
        classe = Classe(**classe_dict)
        print(classe)
        classe_model.save(classe, replace=True)
