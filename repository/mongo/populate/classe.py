'''
    Arquivo que salva as Classes base no banco de dados.

    Referência: https://ordempendragon.files.wordpress.com/2017/04/dd-5e-livro-do-jogador-fundo-branco-biblioteca-c3a9lfica.pdf
'''

from repository.mongo import ClasseModel
from rpgram.boosters import Classe

races = {
    'barbarian': {
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
        'bonus_strength': 30,
        'bonus_dexterity': 10,
        'bonus_constitution': 20,
        'bonus_intelligence': 0,
        'bonus_wisdom': 0,
        'bonus_charisma': 0,
        'multiplier_strength': 2,
        'multiplier_dexterity': 1,
        'multiplier_constitution': 1.5,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 0.5,
        'multiplier_charisma': 0.5,
    },
    'cleric': {
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
        'bonus_strength': 0,
        'bonus_dexterity': 0,
        'bonus_constitution': 0,
        'bonus_intelligence': 20,
        'bonus_wisdom': 20,
        'bonus_charisma': 20,
        'multiplier_strength': 0.1,
        'multiplier_dexterity': 0.7,
        'multiplier_constitution': 0.7,
        'multiplier_intelligence': 1.5,
        'multiplier_wisdom': 1.5,
        'multiplier_charisma': 1.5,
    },
    'druid': {
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
        'bonus_strength': 15,
        'bonus_dexterity': 10,
        'bonus_constitution': 15,
        'bonus_intelligence': 0,
        'bonus_wisdom': 15,
        'bonus_charisma': 5,
        'multiplier_strength': 1.4,
        'multiplier_dexterity': 1,
        'multiplier_constitution': 1.5,
        'multiplier_intelligence': 0.1,
        'multiplier_wisdom': 1.5,
        'multiplier_charisma': 0.5,
    },
    'sorcerer': {
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
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 10,
        'bonus_wisdom': 25,
        'bonus_charisma': 10,
        'multiplier_strength': 0.5,
        'multiplier_dexterity': 0.5,
        'multiplier_constitution': 0.5,
        'multiplier_intelligence': 1.5,
        'multiplier_wisdom': 2,
        'multiplier_charisma': 1,
    },
    'fighter': {
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
        'bonus_strength': 15,
        'bonus_dexterity': 15,
        'bonus_constitution': 15,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 1.5,
        'multiplier_dexterity': 1.5,
        'multiplier_constitution': 1.5,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 0.5,
        'multiplier_charisma': 0.5,
    },
    'rogue': {
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
        'bonus_strength': 10,
        'bonus_dexterity': 30,
        'bonus_constitution': 10,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 0,
        'multiplier_strength': 1,
        'multiplier_dexterity': 2,
        'multiplier_constitution': 1,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 1,
        'multiplier_charisma': 0.5,
    },
    'wizard': {
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
            'fadas) que são imersas em magia.\n\n'
        ),
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 25,
        'bonus_wisdom': 10,
        'bonus_charisma': 10,
        'multiplier_strength': 0.5,
        'multiplier_dexterity': 0.5,
        'multiplier_constitution': 0.5,
        'multiplier_intelligence': 2,
        'multiplier_wisdom': 1.5,
        'multiplier_charisma': 1,
    },
}

if __name__ == '__main__':
    classe_model = ClasseModel()

    for classe_definition in races.values():
        classe = Classe(**classe_definition)
        classe_model.save(classe)
