'''
    Arquivo que salva as Raças base no banco de dados.

    Referência: https://ordempendragon.files.wordpress.com/2017/04/dd-5e-livro-do-jogador-fundo-branco-biblioteca-c3a9lfica.pdf  # noqa
'''

from repository.mongo import RaceModel
from rpgram.boosters import Race

RACES = [
    # Player 6.5 Points
    {
        'name': 'Anão',
        'description': (
            'Audazes e resistentes, os anões são '
            'conhecidos como hábeis guerreiros, '
            'mineradores e trabalhadores em pedra e '
            'metal. Embora tenham menos de 1,50 metro '
            'de altura, os anões são tão largos e '
            'compactos que podem pesar tanto quanto '
            'um humano 60 centímetros mais alto. Sua '
            'coragem e resistência compete facilmente '
            'com qualquer povo mais alto. A pele dos '
            'anões varia do marrom escuro a um matiz '
            'mais pálido, tingido de vermelho, mas os tons mais '
            'comuns são o castanho claro ou bronzeado, como certos '
            'tons terrosos. O cabelo é longo, mas de estilo simples, '
            'geralmente negro, cinzento ou castanho, embora anões '
            'mais pálidos frequentemente possuem cabelos ruivos. '
            'Anões machos valorizam altamente suas barbas e '
            'preparam-nas com cuidado.\n\n'

            'Reinos ricos de antiga grandeza, salões esculpidos nas '
            'raízes das montanhas, o eco de picaretas e martelos nas '
            'minas profundas e nas forjas ardentes, um compromisso '
            'com o clã e a tradição, e um ódio impetuoso contra goblins '
            'e orcs – essas linhas comuns unem todos os anões.'
        ),
        'enemy': False,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 1,
        'multiplier_dexterity': 1,
        'multiplier_constitution': 2,
        'multiplier_intelligence': 1,
        'multiplier_wisdom': 1,
        'multiplier_charisma': 0.5,
    },
    {
        'name': 'Elfo',
        'description': (
            'Elfos possuem graça sobrenatural e seus traços finos, os elfos '
            'parecem assustadoramente belos para os humanos e os '
            'membros de muitas outras raças. Em média, eles são '
            'ligeiramente mais baixos do que os humanos, variando de '
            'pouco menos de 1,50 metro até pouco mais de 1,80 metro '
            'de altura. Eles são mais delgados que os humanos, '
            'pesando entre 50 kg a 72 kg apenas. Os machos e as '
            'fêmeas são quase da mesma altura, mas os machos são '
            'um pouco mais pesados do que as fêmeas.\n\n'

            'A coloração da pele dos elfos varia da mesma maneira '
            'que os humanos, e também incluem peles em tons de '
            'cobre, bronze, até o branco-azulado, os cabelos podem ser '
            'de tons verdes ou azuis, e os olhos podem ser como '
            'piscinas douradas ou prateadas. Elfos não possuem pelos '
            'faciais e poucos pelos no corpo. Eles preferem roupas '
            'elegantes em cores brilhantes, e gostam de joias simples, '
            'mas belas.\n\n'

            'Elfos são um povo mágico de graça sobrenatural, vivendo '
            'no mundo sem pertencer inteiramente à ele. Eles vivem '
            'em lugares de beleza etérea, no meio de antigas florestas '
            'ou em torres prateadas brilhando com luz feérica, onde '
            'uma música suave ecoa através do ar e fragrâncias '
            'suaves flutuam na brisa. Elfos amam a natureza e a '
            'magia, a arte e o estudo, a música e a poesia, e as coisas '
            'boas do mundo.'
        ),
        'enemy': False,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.5,
        'multiplier_dexterity': 1,
        'multiplier_constitution': 1,
        'multiplier_intelligence': 1.5,
        'multiplier_wisdom': 1.5,
        'multiplier_charisma': 1,
    },
    {
        'name': 'Halfling',
        'description': (
            'Os pequeninos halflings sobrevivem em um mundo cheio '
            'de criaturas maiores ao evitar serem notados, ou evitando '
            'o combate direto. Com uns 90 centímetros de altura, eles '
            'parecem inofensivos e assim conseguiram sobreviver por '
            'séculos às sombras dos impérios e à margem de guerras e '
            'conflitos políticos. Eles normalmente são robustos, '
            'pesando entre 20 kg e 22,5 kg.\n\n'

            'A pele dos halflings varia do bronzeado ao pálido com '
            'um tom corado, e seu cabelo é geralmente castanho ou '
            'castanho claro e ondulado. Eles têm olhos castanhos ou '
            'amendoados. Halflings do sexo masculino muitas vezes '
            'ostentam costeletas longas, mas barbas são raras entre '
            'eles e bigodes são quase inexistentes. Eles gostam de usar '
            'roupas simples, confortáveis e práticas, preferindo as '
            'cores claras.\n\n'

            'A praticidade dos halflings se estende para além de '
            'suas roupas. Eles se preocupam com as necessidades '
            'básicas e os prazeres simples, e não são inclinados à '
            'ostentação. Mesmo o mais rico dos halflings mantém seus '
            'tesouros trancados em um porão, em vez de expostos à '
            'vista de todos. Eles possuem um talento especial para '
            'encontrar a solução mais simples para um problema e '
            'têm pouca paciência para indecisões.\n\n'

            'Os confortos de um lar são os objetivos da maioria dos '
            'halflings: um lugar para viver em paz e sossego, longe de '
            'monstros saqueadores e embates de exércitos, com um '
            'fogo aceso e uma refeição generosa, e também uma bebida '
            'fina e boa conversa. Embora alguns halflings vivam seus '
            'dias em remotas comunidades agrícolas, outros formam '
            'bandos nômades que viajam constantemente, atraídos '
            'pela estrada afora e o vasto horizonte para descobrir as '
            'maravilhas de novas terras e povos. Mas mesmo esses '
            'halflings andarilhos amam a paz, a comida, uma lareira e '
            'um lar, mesmo que o lar seja em uma carruagem, '
            'empurrada ao longo de uma estrada de terra, ou uma '
            'balsa flutuando rio abaixo.'
        ),
        'enemy': False,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.5,
        'multiplier_dexterity': 1.5,
        'multiplier_constitution': 1,
        'multiplier_intelligence': 1,
        'multiplier_wisdom': 1.5,
        'multiplier_charisma': 1,
    },
    {
        'name': 'Humano',
        'description': (
            'Os humanos são os mais adaptáveis, flexíveis e '
            'ambiciosos entre todas as raças comuns. Eles têm amplos '
            'e distintos gostos, moralidades e hábitos nas muitas '
            'diferentes regiões onde eles se instalaram. Quando se '
            'estabelecem em um lugar, eles permanecem: eles '
            'constroem cidades que duram por eras, e grandes reinos '
            'que podem persistir por longos séculos. Um único humano '
            'pode ter uma vida relativamente curta, mas uma nação '
            'ou cultura humana preserva tradições com origens muito '
            'além do alcance da memória de qualquer um dos '
            'humanos. Eles vivem plenamente o presente – '
            'tornandoos bem adaptados a uma vida de aventuras – mas '
            'também planejam o futuro, esforçando-se para deixar um '
            'legado duradouro. Individualmente e como grupo, os '
            'humanos são oportunistas adaptáveis, e permanecem '
            'alerta às dinâmicas mudanças políticas e sociais.\n\n'

            'Com sua propensão para a migração e conquista, os '
            'humanos são fisicamente mais diversificados que as '
            'outras raças comuns. Não há um humano típico. Um '
            'indivíduo pode ter entre 1,65 metro a 1,90 metro de '
            'altura e pesar entre 62,5 kg e 125 kg. Os tons de pele '
            'podem variar do negro ao muito pálido, e os cabelos '
            'podem ir do negro ao loiro (encaracolado, crespo ou liso). '
            'Homens podem possuir pelos faciais esparsos ou '
            'abundantes. A diversidade dos humanos pode ter uma '
            'pitada de sangue não humano, revelando indícios de elfos, '
            'orcs ou outras linhagens. Os humanos chegam à idade '
            'adulta no fim da adolescência e raramente vivem um '
            'século.\n\n'

            'Nos confins da maioria dos mundos, os humanos são a '
            'mais jovem das raças comuns, chegando mais tarde no '
            'cenário mundial e com uma vida curta, se comparados aos '
            'anões, elfos e dragões. Talvez seja por causa de suas vidas '
            'mais curtas que eles se esforcem para alcançar o máximo '
            'que podem nos anos que têm. Ou talvez eles sintam que '
            'têm algo a provar às raças mais antigas, e é por esta '
            'razão que eles constroem seus poderosos impérios através '
            'da conquista e do comércio. O que quer que os motive, os '
            'humanos são os inovadores, os realizadores e os pioneiros '
            'dos mundos.\n\n'
        ),
        'enemy': False,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 1.2,
        'multiplier_dexterity': 1.2,
        'multiplier_constitution': 1.2,
        'multiplier_intelligence': 1,
        'multiplier_wisdom': 1,
        'multiplier_charisma': 1,
    },
    {
        'name': 'Orque',
        'description': (
            'A pigmentação acinzentada dos orques, suas testas '
            'avantajadas, mandíbulas salientes, dentes proeminentes '
            'e corpos grandes torna sua herança orque notável para todos '
            'os observadores. Orques tem entre 1,80 metro e 2,10 '
            'metros e, normalmente pesam entre 90 kg e 125 kg. '
            'Orques ostentam cicatrizes de batalha como peças de '
            'orgulho e consideram cicatrizes ornamentais como coisas '
            'bonitas. Outras cicatrizes, no entanto, marcam um orque ou '
            'orque como um ex-escravo ou um exilado desonrado. '
            'Qualquer orque que tenha vivido entre ou próximo dos '
            'orques terá cicatrizes, independentemente de serem marcas '
            'de humilhação ou de orgulho, recontando suas façanhas e '
            'ferimentos do passado. Até mesmo um orque que viva '
            'entre os humanos deverá mostrar essas cicatrizes '
            'orgulhosamente ou escondê-las com vergonha.\n\n'

            'Quer estejam unidos sob a liderança de um poderoso '
            'bruxo ou estejam lutando por um impasse após anos de '
            'conflito, tribos orques e humanas as vezes formam alianças, '
            'unindo forças em uma vasta horda para o pavor das '
            'terras civilizadas próximas. '
            'Alguns orques crescem e se tornam orgulhosos '
            'comandantes de tribos orques. Alguns arriscam sair pelo mundo '
            'para provar seu valor entre os humanos e outras raças mais '
            'civilizadas. Muitos desses se tornam aventureiros, '
            'adquirindo renome pelos seus poderosos feitos e '
            'notoriedade por seus costumes bárbaros e fúria selvagem.\n\n'
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
        'multiplier_constitution': 1.5,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 1,
        'multiplier_charisma': 0.5,
    },
    # Enemies
    {
        'name': 'Drow',
        'description': (
            'Os Drows, também conhecidos como Elfos Negros, são uma raça '
            'élfica notável por sua natureza sombria e sociedade subterrânea. '
            'Com uma estatura semelhante aos elfos, os Drows possuem uma '
            'pele de tom escuro, variando de matizes de azul profundo até '
            'tons de ébano, muitas vezes contrastando vividamente com seus '
            'cabelos prateados ou brancos como a neve. '
            'Seus olhos são frequentemente vermelhos, violetas ou em tons de '
            'amarelo brilhante, adicionando um ar sinistro à sua aparência. '
            'O senso de elegância e refinamento é uma característica marcante '
            'dos Drows, refletida em seus trajes elaborados, geralmente '
            'compostos por sedas escuras e peças de armadura adornadas '
            'com detalhes complexos.\n\n'

            'Os Drows habitam principalmente regiões subterrâneas, '
            'como vastas redes de cidades e complexos labirínticos abaixo '
            'da superfície. Sua sociedade é extremamente hierárquica e '
            'frequentemente governada por casas nobres, cada uma competindo '
            'por poder e prestígio. Conhecidos por sua habilidade em artes '
            'arcanas, os Drows são naturalmente talentosos na prática da '
            'magia, especialmente nas vertentes das sombras e da ilusão, '
            'tornando-os formidáveis tanto em batalha quanto na manipulação '
            'política dentro de sua sociedade.\n\n'

            'Infelizmente, sua história está repleta de conflitos com outras '
            'raças, principalmente os elfos e anões, devido a diferenças '
            'culturais e disputas territoriais. Estereotipados como '
            'cruéis e implacáveis ​​devido à sociedade impiedosa e às '
            'estratégias astutas de guerra, os Drows são frequentemente '
            'temidos e evitados por outras raças, tornando-se uma presença '
            'intimidante nos reinos subterrâneos que chamam de lar.\n\n'
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
        'multiplier_constitution': 1,
        'multiplier_intelligence': 1.75,
        'multiplier_wisdom': 1.75,
        'multiplier_charisma': 1,
    },
    {
        'name': 'Goblin',
        'description': (
            'Os Goblins são uma raça diminuta, ágil e astuta, conhecida por '
            'sua natureza travessa e propensão à malícia. Com uma estatura '
            'pequena e corpos esguios, os Goblins geralmente não ultrapassam '
            'um metro de altura. Suas peles variam de tonalidades verdes, '
            'cinzentas e ocres, adaptando-se facilmente aos ambientes '
            'diversos em que habitam. Possuem narizes pontiagudos, '
            'orelhas alongadas e olhos brilhantes, muitas vezes amarelados, '
            'avermelhados ou em tons de laranja, conferindo uma aparência '
            'cativante, porém astuta.\n\n'

            'Essa raça é conhecida por sua habilidade manual e engenhosidade, '
            'criando armadilhas elaboradas, artefatos e armas improvisadas. '
            'Apesar de terem uma estrutura social caótica e desorganizada, '
            'os Goblins ocasionalmente se reúnem em tribos ou clãs liderados '
            'por um chefe ou xamã, embora essa hierarquia nem sempre seja '
            'estável. Suas moradias são frequentemente cavernas ou '
            'construções precárias, onde podem ser encontrados acumulando '
            'tesouros, seja por sua utilidade ou por simples capricho.\n\n'

            'Goblins são conhecidos por sua natureza travessa e inclinação '
            'para causar problemas. Eles muitas vezes se envolvem em '
            'pilhagens, furtos e trapaças, não apenas entre si, mas também '
            'em relação a outras raças. Apesar de sua reputação como '
            'criaturas travessas, sua inteligência inata e habilidades '
            'táticas tornam os Goblins adversários formidáveis em embates, '
            'onde sua agilidade e sagacidade são suas maiores armas.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.5,
        'multiplier_dexterity': 2.5,
        'multiplier_constitution': 1,
        'multiplier_intelligence': 2,
        'multiplier_wisdom': 0.25,
        'multiplier_charisma': 0.25,
    },
    {
        'name': 'Troll',
        'description': (
            'Os Trolls são uma raça formidável e temível, conhecidos por sua '
            'estatura imponente, força física monstruosa e uma constituição '
            'resistente. Possuindo uma estatura geralmente acima dos dois '
            'metros, essas criaturas apresentam músculos robustos, '
            'pele áspera e densa, variando entre tons de verde, cinza ou '
            'marrom, muitas vezes com aspecto rochoso ou escamoso. '
            'Seus olhos brilham em cores vibrantes, como amarelo, vermelho '
            'ou até mesmo azul fosforescente, conferindo-lhes '
            'uma aura intimidante.\n\n'

            'Sua aparência é caracterizada por feições marcantes, '
            'com queixos proeminentes, narizes largos e orelhas alongadas. '
            'Os Trolls são conhecidos por sua regeneração extraordinária, '
            'sendo capazes de se recuperar de ferimentos graves rapidamente, '
            'mesmo chegando a regenerar membros perdidos, embora esse '
            'processo demande tempo. Sua natureza, por vezes, solitária, '
            'leva-os a habitar regiões isoladas, como florestas densas, '
            'montanhas inexploradas ou cavernas profundas.\n\n'

            'Embora muitas vezes retratados como criaturas hostis e '
            'violentas, os Trolls não são completamente desprovidos de '
            'racionalidade. Alguns mostram habilidades em artesanato '
            'rudimentar, enquanto outros possuem uma cultura tribal e '
            'sistemas sociais próprios. No entanto, essas sociedades '
            'geralmente são simples e voltadas para a sobrevivência, '
            'sem se envolverem muito com outras raças. Sua força e '
            'resistência os tornam inimigos formidáveis, capazes de enfrentar '
            'desafios consideráveis, tornando-os figuras a serem temidas e '
            'respeitadas em muitos reinos.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 2,
        'multiplier_dexterity': 0.25,
        'multiplier_constitution': 2.5,
        'multiplier_intelligence': 0.75,
        'multiplier_wisdom': 0.75,
        'multiplier_charisma': 0.25,
    },
    {
        'name': 'Kobold',
        'description': (
            'Os Kobolds são seres pequenos e ágeis, frequentemente medindo '
            'cerca de um metro de altura. Apresentam uma estrutura esbelta e '
            'ágil, com pele escamosa que varia em tonalidades de marrom, '
            'cinza ou tons terrosos. Suas feições faciais lembram as de '
            'répteis, com olhos grandes e luminosos, normalmente de cores '
            'amareladas ou avermelhadas, e rostos marcados por focinhos '
            'alongados. Sua natureza furtiva e astuta é complementada por '
            'suas orelhas pontiagudas e caudas finas, que contribuem para '
            'sua agilidade e habilidades furtivas.\n\n'

            'Organizam-se frequentemente em grupos ou tribos, liderados por '
            'um xamã ou líder carismático, mantendo uma hierarquia rígida, '
            'em que cada membro possui uma função específica na sociedade.\n\n'

            'Apesar de seu tamanho modesto, os Kobolds são criaturas astutas '
            'e, em número, podem ser uma força considerável em batalha. '
            'Geralmente preferem emboscadas e estratégias de guerrilha, '
            'utilizando suas habilidades furtivas para confundir e '
            'surpreender seus oponentes. Sua inteligência aguçada e '
            'natureza determinada fazem dos Kobolds um desafio formidável '
            'para aventureiros desprevenidos que se aventuram em '
            'seus territórios.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 1.5,
        'multiplier_dexterity': 2.5,
        'multiplier_constitution': 1,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 0.5,
        'multiplier_charisma': 0.5,
    },
    {
        'name': 'Espectro',
        'description': (
            'Os Espectros são entidades sobrenaturais, manifestações de '
            'almas atormentadas e consumidas por emoções negativas após a '
            'morte. Desprovidos de uma forma física sólida, eles se '
            'manifestam como aparições etéreas e translúcidas, emanando '
            'uma aura de desespero e tristeza. Sua aparência varia de acordo '
            'com a história de sua morte, mas geralmente apresentam uma '
            'forma fantasmagórica, com contornos nebulosos e distorcidos.\n\n'

            'Essas criaturas são ligadas a eventos trágicos, muitas vezes '
            'presas a locais específicos onde sofreram a morte ou '
            'experimentaram um grande sofrimento. Sua presença é acompanhada '
            'por uma aura de arrepios e uma sensação de frio intenso. '
            'Normalmente, não são seres malignos por natureza, mas sua '
            'ligação com a dor e a tragédia pode levá-los a agir de maneira '
            'hostil quando perturbados ou quando tentam atrair a atenção para '
            'o que os aflige.\n\n'

            'Os Espectros são conhecidos por suas habilidades sobrenaturais, '
            'podendo atravessar objetos sólidos, tornar-se invisíveis e até '
            'manipular as emoções daqueles ao seu redor. Frequentemente, a '
            'libertação dessas almas atormentadas envolve a resolução dos '
            'problemas não resolvidos que as mantêm presas, '
            'proporcionando-lhes paz e permitindo-lhes encontrar a redenção '
            'ou seguir adiante para o além.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.25,
        'multiplier_dexterity': 2.5,
        'multiplier_constitution': 0.25,
        'multiplier_intelligence': 1.5,
        'multiplier_wisdom': 1.5,
        'multiplier_charisma': 0.5,
    },
    {
        'name': 'Ogro',
        'description': (
            'Os Ogros são seres imponentes e brutais, conhecidos por sua '
            'estatura massiva e musculatura poderosa. Com uma altura média '
            'variando entre 2,5 e 3 metros, essas criaturas apresentam corpos '
            'robustos, pele grossa e geralmente tonalidades que variam entre '
            'tons de verde, marrom ou cinza. Suas feições são marcadas por '
            'rostos largos, queixos proeminentes e dentes afiados, '
            'conferindo-lhes uma aparência temível e selvagem.\n\n'

            'A inteligência dos Ogros muitas vezes é subestimada, mas '
            'apesar de sua reputação de seres rudes e selvagens, possuem uma '
            'forma de cultura própria, geralmente tribal e simples. '
            'Suas moradias são frequentemente cavernas ou áreas isoladas, '
            'onde mantêm uma sociedade primitiva, mas com rituais e tradições '
            'próprias. Costumam caçar em grupos e são habilidosos na arte de '
            'construir armas e ferramentas grosseiras.\n\n'

            'Dotados de força física impressionante, os Ogros são combatentes '
            'formidáveis em batalha. Sua resistência e brutalidade os tornam '
            'oponentes temíveis, capazes de causar estragos significativos '
            'em confrontos. Apesar de sua natureza geralmente hostil, '
            'alguns Ogros são conhecidos por terem laços com outras raças ou '
            'por desejarem uma vida pacífica, embora essa seja uma exceção à '
            'regra em suas sociedades.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 3,
        'multiplier_dexterity': 0.25,
        'multiplier_constitution': 2,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 0.5,
        'multiplier_charisma': 0.25,
    },
    {
        'name': 'Licantropo',
        'description': (
            'Os Licantropos são seres míticos capazes de alternar entre a '
            'forma humana e a forma de licantrópica. Geralmente, durante a '
            'lua cheia, sua transformação é inevitável, mas alguns possuem '
            'a habilidade de controlar essa metamorfose em outros momentos. '
            'Na forma humana, eles são indistinguíveis de outros seres '
            'humanos, muitas vezes possuindo características atraentes e '
            'carismáticas. Por outro lado, na forma de lobo, apresentam uma '
            'pelagem densa, olhos selvagens e presas afiadas.\n\n'

            'Os Licantropos são frequentemente retratados como seres '
            'solitários, isolados devido ao medo e à incompreensão que sua '
            'condição gera nas comunidades humanas. Alguns buscam refúgio '
            'em clãs ou grupos similares, onde compartilham experiências e '
            'aprendem a controlar sua natureza animalesca.\n\n'

            'Em sua forma de bestial, os Licantropos possuem sentidos '
            'aguçados, velocidade e força consideráveis, tornando-os '
            'caçadores formidáveis. No entanto, a dualidade entre sua '
            'humanidade e instintos animalescos muitas vezes se torna uma '
            'luta interna, e controlar essa fera interior pode ser uma '
            'batalha constante. A luta para equilibrar ambas as naturezas é '
            'uma narrativa recorrente entre os Licantropos, apresentando '
            'desafios emocionais e físicos que moldam suas histórias.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 2,
        'multiplier_dexterity': 1.75,
        'multiplier_constitution': 2,
        'multiplier_intelligence': 0.25,
        'multiplier_wisdom': 0.25,
        'multiplier_charisma': 0.25,
    },
    {
        'name': 'Harpia',
        'description': (
            'As Harpias são criaturas míticas com características de aves de '
            'rapina e corpos femininos. Essas criaturas possuem a cabeça, '
            'torso e braços de mulher, enquanto o restante do corpo é similar '
            'ao de uma águia, incluindo asas poderosas e garras afiadas. '
            'Sua plumagem varia em tons de marrom, cinza ou preto, '
            'adaptando-se ao ambiente onde habitam, geralmente regiões '
            'montanhosas, penhascos ou cavernas isoladas.\n\n'

            'Conhecidas por sua agilidade e velocidade impressionantes '
            'durante o voo, as Harpias são mestras na arte da caça, sendo '
            'predadoras habilidosas que utilizam suas garras e agilidade '
            'para capturar suas presas. Essas criaturas têm uma voz '
            'melodiosa, usada tanto para atrair presas como para se comunicar '
            'entre si. Seu comportamento muitas vezes é territorial e '
            'agressivo, especialmente quando sentem ameaças próximas aos seus '
            'ninhos ou locais de descanso.\n\n'

            'Em algumas lendas, as Harpias são descritas como seres malignos, '
            'sequestrando pessoas ou lançando maldições sobre aqueles que '
            'invadem seus territórios. No entanto, em outras histórias, '
            'são retratadas como seres sábios e protetores da natureza, '
            'guardiãs de segredos antigos ou mensageiras dos deuses. Essas '
            'criaturas mitológicas frequentemente têm um papel variado nas '
            'narrativas, podendo ser antagonistas ou aliadas dependendo da '
            'história contada.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 1.5,
        'multiplier_dexterity': 1.5,
        'multiplier_constitution': 1.5,
        'multiplier_intelligence': 0.75,
        'multiplier_wisdom': 1,
        'multiplier_charisma': 0.25,
    },
    {
        'name': 'Lâmia',
        'description': (
            'As Lâmias são criaturas místicas com corpo de serpente da '
            'cintura para baixo e torso humano da cintura para cima. '
            'Conhecidas por sua beleza sedutora e habilidades encantadoras, '
            'as Lâmias habitam regiões selvagens e secretas, '
            'muitas vezes associadas a mitos e lendas. '
            'Sua natureza mítica lhes confere habilidades especiais, '
            'como uma incrível agilidade e a capacidade de hipnotizar e '
            'seduzir aqueles que se aproximam, '
            'tornando-as tanto temidas quanto admiradas.\n\n'

            'Apesar de sua aparência exótica e muitas vezes intimidante, '
            'as Lâmias são seres inteligentes e astutos, com uma cultura '
            'rica e complexa. '
            'Elas são conhecidas por sua habilidade em adivinhação, '
            'sendo consideradas guardiãs de segredos antigos e conhecimentos '
            'ocultos. '
            'Embora sejam criaturas solitárias por natureza, '
            'as Lâmias são capazes de formar laços fortes com aqueles que '
            'ganham sua confiança, mostrando-se leais e protetoras com seus '
            'aliados mais próximos.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.25,
        'multiplier_dexterity': 2.5,
        'multiplier_constitution': 1,
        'multiplier_intelligence': 1,
        'multiplier_wisdom': 0.25,
        'multiplier_charisma': 1.5,
    },
    {
        'name': 'Draconiano',
        'description': (
            'Os Draconianos são uma raça mística e poderosa, '
            'com características que lembram os lendários dragões. '
            'Possuem escamas resistentes que cobrem seus corpos, '
            'asas membranosas que lhes permitem voar e garras afiadas que '
            'servem como armas naturais. '
            'Sua aparência imponente e majestosa inspira respeito e temor, '
            'refletindo a nobreza de seu sangue ancestral.\n\n'

            'Esses seres são conhecidos por sua grande força e habilidades '
            'mágicas, muitas vezes associadas aos dragões. '
            'Alguns Draconianos possuem a capacidade de lançar feitiços '
            'de fogo, gelo ou eletricidade, enquanto outros são adeptos em '
            'formas mais sutis de magia, como a manipulação de ilusões ou a '
            'comunicação telepática. '
            'Sua sociedade é organizada em clãs liderados por indivíduos '
            'poderosos, cada um com sua própria linhagem e tradições antigas. '
            'Apesar de sua reputação de ferocidade em batalha, '
            'os Draconianos são seres complexos, com uma cultura rica e uma '
            'forte conexão com a honra e a lealdade.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 10,
        'bonus_dexterity': 10,
        'bonus_constitution': 10,
        'bonus_intelligence': 10,
        'bonus_wisdom': 10,
        'bonus_charisma': 10,
        # Soma de 10,5 pontos nos multiplicadores, ao invés de 6,5 pontos
        'multiplier_strength': 2,
        'multiplier_dexterity': 2,
        'multiplier_constitution': 2,
        'multiplier_intelligence': 2,
        'multiplier_wisdom': 2,
        'multiplier_charisma': 0.5,
    },
    {
        'name': 'Dríade',
        'description': (
            'As Dríades são seres feéricos da floresta, '
            'conhecidas por sua ligação íntima com a natureza e sua '
            'aparência que mescla características humanas e vegetais. '
            'Elas possuem a capacidade de se fundir com as árvores, '
            'tornando-se indistinguíveis da flora ao seu redor. '
            'Sua pele é suave como a casca de uma árvore e seus cabelos '
            'muitas vezes se assemelham a folhagem verdejante.\n\n'

            'Essas criaturas guardiãs das florestas são protetoras e '
            'reverenciadoras do mundo natural, '
            'muitas vezes sendo consideradas as próprias manifestações '
            'da alma das árvores. '
            'Elas são dotadas de habilidades relacionadas ao '
            'crescimento e cura das plantas, sendo capazes de acelerar o '
            'crescimento de uma semente ou curar uma árvore doente com um '
            'simples toque. '
            'Apesar de sua natureza pacífica, '
            'as Dríades são ferozmente protetoras de seus lares, '
            'utilizando sua ligação com a natureza para afastar '
            'qualquer ameaça que se aproxime de suas florestas.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.5,
        'multiplier_dexterity': 2,
        'multiplier_constitution': 0.5,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 1.5,
        'multiplier_charisma': 1.5,
    },
    {
        'name': 'Sílfide',
        'description': (
            'As Sílfides são seres etéreos e graciosos, '
            'dotados de asas transparentes que lhes permitem voar com '
            'facilidade pelos céus. '
            'Sua pele brilha suavemente como a luz da lua, e seus olhos '
            'refletem a sabedoria dos ventos. '
            'São conhecidos por sua ligação profunda com a natureza e '
            'sua habilidade de controlar os elementos, '
            'especialmente o vento.\n\n'

            'Vivendo em comunidades aéreas nas regiões mais altas das '
            'montanhas ou em bosques encantados, '
            'as Sílfides são guardiãs dos segredos do ar. '
            'Elas são reverenciadas como mensageiras dos deuses e '
            'protetoras das criaturas aladas. '
            'Sua sociedade é baseada em um forte senso de comunidade e '
            'respeito pela natureza, e são habilidosas em artes místicas '
            'e na cura de ferimentos com ervas e magia.\n\n'
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
        'multiplier_intelligence': 2,
        'multiplier_wisdom': 2,
        'multiplier_charisma': 1,
    },
    {
        'name': 'Gnoll',
        'description': (
            'Os Gnolls são criaturas humanoides híbridas, '
            'com características físicas que lembram hienas. '
            'Possuem corpos robustos, cobertos por uma pelagem áspera e '
            'manchada, além de cabeças alongadas, mandíbulas poderosas e '
            'olhos amarelos que brilham com malícia. '
            'São conhecidos por sua agressividade e natureza predatória, '
            'muitas vezes vivendo em bandos liderados '
            'por um líder dominante.\n\n'

            'Apesar de sua reputação como saqueadores e bandidos, '
            'os Gnolls possuem uma sociedade própria, '
            'com rituais e tradições únicas. '
            'Eles são habilidosos caçadores e rastreadores, '
            'capazes de sobreviver em ambientes hostis. '
            'Seus acampamentos são muitas vezes improvisados e móveis, '
            'refletindo sua natureza nômade e adaptável. '
            'Em combate, os Gnolls são ferozes e implacáveis, '
            'usando táticas brutais para subjugar seus inimigos.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 2.5,
        'multiplier_dexterity': 1.5,
        'multiplier_constitution': 1,
        'multiplier_intelligence': 0.5,
        'multiplier_wisdom': 0.5,
        'multiplier_charisma': 0.5,
    },
    {
        'name': 'Fomori',
        'description': (
            'Os Fomori são seres grotescos e deformados, '
            'conhecidos por sua aparência monstruosa e tamanho imponente. '
            'Possuem corpos distorcidos e disformes, com membros '
            'desproporcionais e pele áspera e escamosa. '
            'Seus rostos são marcados por feições brutais, '
            'com presas afiadas e olhos selvagens que refletem sua natureza '
            'selvagem e primitiva.\n\n'

            'Apesar de sua aparência assustadora, '
            'os Fomori possuem uma cultura própria, '
            'com tradições e rituais que são passados de geração em geração. '
            'Vivem em comunidades isoladas, longe das civilizações humanas, '
            'e são conhecidos por sua hostilidade em relação a estranhos. '
            'São habilidosos em artes marciais e muitas vezes usam sua força '
            'bruta em combate, sendo temidos por sua ferocidade e '
            'resistência.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 2.65,
        'multiplier_dexterity': 1,
        'multiplier_constitution': 2,
        'multiplier_intelligence': 0.25,
        'multiplier_wisdom': 0.5,
        'multiplier_charisma': 0.1,
    },
    {
        'name': 'Nefilim',
        'description': (
            'Os Nefilim são seres de linhagem divina, '
            'fruto da união entre humanos e entidades celestiais. '
            'Possuem uma aparência impressionante, com traços angélicos '
            'mesclados com características humanas.\n\n'

            'Além de sua beleza física, '
            'os Nefilim possuem habilidades especiais, '
            'como a capacidade de canalizar energia divina e '
            'realizar milagres. '
            'São vistos como seres de grande importância e muitas vezes '
            'são considerados como messias ou salvadores em suas '
            'comunidades.\n\n'
        ),
        'enemy': True,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        # Soma de 10,5 pontos nos multiplicadores, ao invés de 6,5 pontos
        'multiplier_strength': 1.5,
        'multiplier_dexterity': 1.5,
        'multiplier_constitution': 1.5,
        'multiplier_intelligence': 1.75,
        'multiplier_wisdom': 1.75,
        'multiplier_charisma': 2.5,
    },
]

if __name__ == '__main__':
    race_model = RaceModel()
    fields = ['_id', 'name', 'created_at']
    for race_dict in RACES:
        race_name = race_dict['name']
        mongo_dict: dict = race_model.get(
            query={'name': race_name},
            fields=fields,
        )
        if mongo_dict:
            for field in fields:
                race_dict[field] = mongo_dict[field]
        race = Race(**race_dict)
        print(race)
        race_model.save(race, replace=True)
