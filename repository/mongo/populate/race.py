'''
    Arquivo que salva as Raças base no banco de dados.

    Referência: https://ordempendragon.files.wordpress.com/2017/04/dd-5e-livro-do-jogador-fundo-branco-biblioteca-c3a9lfica.pdf
'''

from repository.mongo import RaceModel
from rpgram.boosters import Race

races = {
    'dwarf': {
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
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 1,
        'multiplier_dexterity': 1,
        'multiplier_constitution': 1.5,
        'multiplier_intelligence': 1,
        'multiplier_wisdom': 1,
        'multiplier_charisma': 0.5,
    },
    'elf': {
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
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.5,
        'multiplier_dexterity': 1.3,
        'multiplier_constitution': 0.5,
        'multiplier_intelligence': 1.3,
        'multiplier_wisdom': 1,
        'multiplier_charisma': 1.4,
    },
    'halfling': {
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
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 0.5,
        'multiplier_dexterity': 1.5,
        'multiplier_constitution': 0.5,
        'multiplier_intelligence': 1,
        'multiplier_wisdom': 1.5,
        'multiplier_charisma': 1,
    },
    'human': {
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
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 1,
        'multiplier_dexterity': 1,
        'multiplier_constitution': 1,
        'multiplier_intelligence': 1,
        'multiplier_wisdom': 1,
        'multiplier_charisma': 1,
    },
    'orc': {
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
            'comandantes de tribos orques. Alguns arriscam sair pelo mundo para '
            'provar seu valor entre os humanos e outras raças mais '
            'civilizadas. Muitos desses se tornam aventureiros, '
            'adquirindo renome pelos seus poderosos feitos e '
            'notoriedade por seus costumes bárbaros e fúria selvagem.\n\n'
        ),
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'bonus_constitution': 5,
        'bonus_intelligence': 5,
        'bonus_wisdom': 5,
        'bonus_charisma': 5,
        'multiplier_strength': 1.9,
        'multiplier_dexterity': 1,
        'multiplier_constitution': 1.3,
        'multiplier_intelligence': 0.7,
        'multiplier_wisdom': 1,
        'multiplier_charisma': 0.1,
    }
}

if __name__ == '__main__':
    race_model = RaceModel()

    for race_definition in races.values():
        race = Race(**race_definition)
        race_model.save(race)
