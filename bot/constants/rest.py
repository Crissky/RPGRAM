COMMANDS = ['descanso', 'rest']
SECTION_TEXT_REST = 'DESCANSO'
SECTION_TEXT_WAKEUP = 'REVIGORADO!'
SECTION_TEXT_REST_MIDNIGHT = 'A MIMIR'
SECTION_TEXT_ACTION_PONTOS = 'PONTOS DE AÇÃO'
MINUTES_TO_RECOVERY_HIT_POINTS = 15
MINUTES_TO_RECOVERY_ACTION_POINTS = 10
REPLY_TEXTS_ALREADY_RESTING = [
    '{char_name}, já está descansando.',
    '{char_name}, já está aproveitando uma merecida pausa.',
    '{char_name}, já está descansando. Aguarde um pouco mais.',
    'Descanso é importante, mas {char_name}, já está fazendo isso.',
    'Hmm, acho que {char_name}, já está fazendo isso.',
    'Acalme-se! {char_name}, já está aproveitando um merecido descanso.',
    'Relaxe! {char_name}, já está descansando neste momento.',
    'Descanse um pouco você também! {char_name}, já está descansando.',
    '{char_name}, já está descansando e recuperando suas energias.',
    'Acalme-se! {char_name}, já está descansando, então aproveite '
    'o momento de tranquilidade.',
    'Descansar é importante para o bem-estar de {char_name}, '
    'mas ele já está descansando agora.',
    '{char_name}, já está relaxando e recarregando as energias.',
]
REPLY_TEXTS_NO_NEED_REST = [
    '{char_name}, já está totalmente recuperado. '
    'Não precisa descansar agora.',
    '{char_name}, está cheio de energia! Descansar seria um desperdício.',
    'Não há necessidade de descansar no momento. {char_name}, está pronto '
    'para qualquer desafio.',
    '{char_name}, sente uma energia renovada pulsando em suas veias. '
    'Descansar agora seria redundante.',
    '{char_name}, está com a saúde perfeita. '
    'Descansar seria apenas um capricho.',
    'Descansar agora seria como descansar eternamente. '
    '{char_name}, está pronto para enfrentar qualquer obstáculo.',
    '{char_name}, se sente revigorado e pronto para prosseguir. '
    'Não há motivo para descansar.',
    'A energia no corpo de {char_name}, é palpável. '
    'Descansar seria um desperdício de tempo precioso.',
    '{char_name}, está radiante de vitalidade. '
    'Descansar não é necessário neste momento.',
    '{char_name}, já está completamente revigorado e '
    'pronto para a próxima aventura!',
    'O poder flui através das veias de {char_name}. '
    'Descansar agora seria como sufocar uma chama ardente.',
    '{char_name}, respira fundo e sente uma energia vibrante percorrer '
    'todo o seu ser. Não há necessidade de descansar.',
]
REPLY_TEXTS_STARTING_REST = [
    '{char_name}, senta e começa a descansar.',
    '{char_name}, encontra um local confortável para descansar.',
    '{char_name}, se acomoda e começa a relaxar.',
    '{char_name}, decide parar por um momento e recarregar suas energias.',
    '{char_name}, deita no chão e começa a descansar.',
    '{char_name}, se recosta em uma parede e relaxa.',
    '{char_name}, encontra uma sombra agradável para descansar.',
    '{char_name}, decide fazer uma pausa e recuperar suas forças.',
    '{char_name}, se senta em uma rocha e começa a descansar.',
    '{char_name}, encontra um local tranquilo e decide descansar um pouco.',
    '{char_name}, encontra um tronco caído e se senta para descansar.',
    '{char_name}, se deita em um leito de grama e relaxa.',
    '{char_name}, se ajoelha e começa a descansar.',
    '{char_name}, senta em uma pedra e decide descansar por um tempo.',
    '{char_name}, encontra uma fonte e se senta para descansar.',
    '{char_name}, decide parar um momento e recuperar o fôlego.',
    '{char_name}, se deita em uma cama improvisada e começa a descansar.',
    '{char_name}, se senta em uma árvore caída e relaxa.',
    '{char_name}, encontra um banco vazio e se senta para descansar.',
    '{char_name}, se recolhe em um canto e decide descansar um pouco.',
]

REPLY_TEXT_REST_MIDNIGHT = [
    'Com o sol já desaparecido no horizonte e a escuridão assumindo seu '
    'reinado, a meia-noite se aproxima. A jornada foi longa e exaustiva, os '
    'ferimentos ainda ardem e os olhos pesam. É hora de descansar e permitir '
    'que as feridas se curem.',
    'O relógio marca a meia-noite, o mundo mergulha na quietude. '
    'As dores dos ferimentos se intensificam, clamando por repouso. '
    'O tempo de cura é essencial, a noite exige que os aventureiros se '
    'abriguem para recuperar suas forças.',
    'À medida que a meia-noite se aproxima, as sombras crescem e os '
    'ferimentos dos heróis clamam por alívio. Descansar é essencial, '
    'pois o tempo não poupa aqueles que estão fracos e fatigados.',
    'O sino da meia-noite ecoa, sinalizando o momento crucial para os '
    'feridos. Os aventureiros sentem cada golpe e contusão, a necessidade de '
    'repouso se torna mais urgente. É hora de encontrar um refúgio e permitir '
    'que a cura se inicie.',
    'Com a meia-noite se aproximando, os aventureiros feridos sentem o peso '
    'de suas batalhas. Descansar é imperativo; as horas noturnas oferecem a '
    'chance de cura e renovação.',
    'O relógio toca as doze badaladas, trazendo consigo a lembrança de que a '
    'noite é o melhor remédio para os corpos cansados. Os ferimentos '
    'reclamam por descanso, é hora de encontrar um lugar seguro.',
    'A meia-noite se anuncia, os personagens feridos sentem o peso de '
    'suas lutas. O corpo clama por repouso, é essencial procurar abrigo '
    'para iniciar o processo de recuperação.',
    'Ao soar da meia-noite, os ferimentos dos aventureiros se intensificam. '
    'O tempo é precioso e a noite oferece a oportunidade necessária para a '
    'cura. Descansar é a chave para a restauração.',
    'Enquanto a meia-noite se aproxima, os personagens machucados sentem a '
    'exaustão das batalhas. É hora de buscar abrigo e permitir que a noite '
    'traga alívio às dores, enquanto a cura se inicia.',
    'Com a meia-noite se aproximando, os aventureiros feridos sentem cada '
    'arranhão e contusão. Descansar é essencial para permitir que seus corpos '
    'se recuperem das lutas travadas.',
    'À medida que a noite se aprofunda, o céu assume uma escuridão profunda. '
    'As estrelas cintilam acima de vocês, e vocês começam a sentir o peso '
    'do dia desgastante. Seus ferimentos começam a latejar, clamando por '
    'descanso e cuidados.',
    'O relógio anuncia a meia-noite com um eco solene que ressoa pelo '
    'acampamento. Suas feridas, antes ignoradas pela urgência da situação, '
    'agora parecem mais agudas, exigindo atenção e repouso.',
    'O silêncio da noite é interrompido pelo sino da meia-noite '
    'ecoando no ar. Cada um de vocês sente o peso de suas feridas e a '
    'exaustão acumulada. O momento pede descanso para permitir a recuperação.',
    'A lua paira alta no céu, lançando uma luz prateada sobre o grupo. '
    'O cansaço se instala profundamente em seus corpos, e cada ferida se '
    'faz sentir com mais intensidade. É hora de permitir que seus corpos se '
    'curem durante o repouso noturno.',
    'Com a chegada da meia-noite, o grupo se sente sobrecarregado pelo peso '
    'das batalhas passadas. Cada arranhão, contusão e ferida se tornam mais '
    'evidentes, clamando por cuidados e repouso.',
    'Enquanto a noite avança, a exaustão dos confrontos recentes se torna '
    'mais palpável. Cada um de vocês sente a necessidade inegável de '
    'descansar para se recuperar das lutas e curar suas feridas.',
    'Os minutos se arrastam até a meia-noite, e vocês sentem a exaustão da '
    'jornada tomar conta. Cada dor e ferida adquiridas nas batalhas do dia '
    'precisam de atenção imediata por meio do descanso.',
    'O tic-tac do relógio parece ressoar mais alto à medida que a meia-noite '
    'se aproxima. As feridas, anteriormente toleráveis, agora parecem mais '
    'dolorosas, exigindo que cada um de vocês descanse e se cure.',
    'Sob o céu estrelado, vocês percebem a necessidade crescente de descanso. '
    'Cada arranhão e machucado adquiridos nas provações do dia clamam por '
    'cuidados enquanto a meia-noite se aproxima.',
    'Com a meia-noite se aproximando, vocês notam a fadiga pesar mais sobre '
    'seus ombros. Cada ferida pulsando é um lembrete constante de que o '
    'repouso é essencial para a recuperação.',
]
REPLY_TEXT_REST_MIDDAY = [
    'Enquanto o sol atinge seu ponto mais alto no céu, o meio dia chegou. '
    'Seus personagens, feridos pela jornada, começam a sentir o peso da '
    'fadiga. Seria prudente considerar um descanso para recarregar suas '
    'energias e curar as feridas.',
    'A luz do meio dia banha o cenário ao redor, revelando a fadiga nos '
    'rostos de seus heróis. Talvez seja hora de buscar um local seguro, '
    'descansar e permitir que suas habilidades se recuperem antes da próxima '
    'etapa da jornada.',
    'O calor do meio dia é intenso, e seus personagens sentem a exaustão da '
    'batalha. Pensar em um breve repouso pode ser a chave para restaurar as '
    'forças antes de enfrentarem os desafios que ainda os aguardam.',
    'Sob o sol ardente do meio dia, os sinais de cansaço são evidentes nos '
    'olhos de seus aventureiros. Um breve descanso pode ser crucial para '
    'garantir que estejam prontos para os desafios futuros.',
    'O relógio solar indica que o meio dia chegou, e seus heróis estão '
    'visivelmente fatigados. Encontrar um local seguro para descansar pode '
    'ser a decisão mais sábia neste momento.',
    'O sol atinge o pico no céu, e seus personagens, marcados pelas batalhas '
    'recentes, sentem a necessidade de uma pausa. Considerem um breve '
    'descanso para recuperar as energias e curar as feridas.',
    'Ao meio dia, o calor é implacável, e seus aventureiros começam a '
    'demonstrar sinais de exaustão. Pode ser a hora certa para procurar '
    'abrigo e permitir que seus corpos se recuperem.',
    'Sob a luz forte do meio dia, seus heróis estão claramente desgastados. '
    'Talvez seja o momento ideal para um descanso estratégico e restaurador.',
    'Enquanto o sol alcança o zênite, seus personagens sentem o peso da '
    'jornada. Uma pausa ao meio dia pode ser a oportunidade perfeita para '
    'recuperar forças e vitalidade.',
    'O meio dia está sobre vocês, e os efeitos das batalhas passadas se '
    'fazem sentir. Considerem descansar para que possam enfrentar os '
    'desafios vindouros com renovada determinação.',
    'Sob a luz intensa do meio dia, seus aventureiros sentem o cansaço '
    'acumulado. Um breve repouso pode ser a chave para enfrentar os perigos '
    'futuros com vigor renovado.',
    'O relógio solar indica que é meio dia, e seus heróis, mesmo corajosos, '
    'não são imunes à fadiga. Pensar em um breve descanso pode ser uma '
    'escolha sábia neste momento.',
    'Com o sol atingindo o pico no céu, seus personagens mostram sinais '
    'de cansaço. Talvez seja prudente encontrar um local seguro e repousar '
    'antes da próxima etapa da jornada.',
    'O calor do meio dia se faz presente, e seus heróis, mesmo os mais '
    'resilientes, começam a sentir a exaustão. Considerar um descanso '
    'agora pode ser crucial para a continuidade da jornada.',
    'Enquanto o sol está diretamente acima, seus aventureiros percebem a '
    'necessidade de um intervalo. Um breve descanso ao meio dia pode ser a '
    'chave para superar os desafios subsequentes.',
    'Sob a luz do meio dia, seus heróis exibem sinais visíveis de desgaste. '
    'Encontrar um local seguro para descansar pode ser a decisão mais sensata '
    'neste momento.',
    'O meio dia traz consigo o calor intenso, e seus personagens, embora '
    'valentes, começam a sentir a exaustão. Um breve repouso pode ser a '
    'solução para enfrentar os perigos que ainda virão.',
    'Com o sol no auge, seus aventureiros sentem a necessidade de uma pausa. '
    'Pensar em descansar ao meio dia pode ser fundamental para a saúde e '
    'vigor do grupo.',
    'O relógio solar aponta para o meio dia, e seus heróis, mesmo os mais '
    'resilientes, não podem ignorar a fadiga. Um descanso estratégico pode '
    'ser a resposta para renovar as energias.',
    'Ao meio dia, seus personagens, marcados por batalhas e desafios, '
    'sentem a necessidade de um breve descanso. Considerem encontrar um '
    'refúgio para recarregar as energias antes da próxima jornada.',
]


REPLY_TEXT_REST_INDAY = [
    'Sob o cálido abraço do astro-rei, vossos corpos repousarão '
    'em breve alívio.',
    'Eis que a jornada cessa por ora, e o cansaço encontra sua cura no '
    'silêncio do dia.',
    'Sob o céu diáfano, permiti que a exaustão seja lavada pelo '
    'sopro manso da tarde.',
    'Aqui, onde a brisa é leve e o solo acolhedor, o descanso vos espera.',
    'Pousai vossas armas e armaduras, pois a paz do momento clama por vós.',
    'O tempo aquieta sua marcha e convida-vos a '
    'partilhar do banquete do repouso.',
    'No véu dourado da aurora tardia, vossas almas encontrarão refrigério.',
    'Deixai que o calor suave do dia afaste a exaustão que '
    'vos pesa o espírito.',
    'O sol vos guia à sombra benigna onde o descanso é promessa e renovo.',
    'Sob a canção do vento, aqui fareis vossa pausa '
    'entre os rigores do destino.',
    'Deixai que o murmúrio das folhas vos embale ao '
    'refúgio do breve descanso.',
    'Eis um instante sagrado, onde a paz e o alívio vos '
    'aguardam como velhos amigos.',
    'No âmago do dia, a trégua vos saúda; deixai o fardo '
    'cair e a calma reinar.',
    'A lida cessará, ainda que por momentos, e o alento '
    'vos restaurará o vigor.',
    'Nos braços generosos do dia, repousai, pois a jornada ainda é longa.',
    'O fulgor da tarde anuncia a hora de abrandar vossos corpos e mentes.',
    'No fulcro do dia, até mesmo os guerreiros mais bravos hão de '
    'sucumbir ao descanso.',
    'Sob o firmamento diáfano, que a quietude vos abrace como um '
    'manto de seda.',
    'O crepitar do fogo e o sussurro do vento anunciam o momento de pausa.',
    'Deixai que o canto dos pássaros vos acompanhe ao breve reino do repouso.',
    'No éden efêmero do descanso, o sol é o guardião de '
    'vossos sonhos diurnos.',
    'O calor do solo e a sombra das árvores vos convidam a '
    'repousar sem temor.',
    'Aqui o mundo se aquieta; aqui a luta cede lugar à serenidade.',
    'Entre os sussurros da brisa e os raios do sol, vosso '
    'cansaço será dissipado.',
    'Sob os céus benevolentes, o descanso é vosso direito conquistado.',
    'As forças do dia vos protegem; repousai sem pressa, pois o '
    'perigo dorme também.',
    'No coração do mundo desperto, vós também podereis vos render à calma.',
    'O sol altivo vos contempla, mas não vos pressiona; a pausa é bem-vinda.',
    'Nos minutos de trégua, que o calor do dia vos console e revigore.',
    'Cessai vossos passos, pois a terra oferece seu abraço para '
    'vossa recuperação.',
    'Sob a abóbada celeste, que o tempo vos conceda o dom do '
    'alívio passageiro.',
    'A jornada silencia, e o horizonte vos concede uma pausa abençoada.',
    'Entre o crepitar da fogueira e o canto do vento, o '
    'descanso vos confortará.',
    'O sol caminha devagar no firmamento, tal como vós '
    'deveis abrandar vosso ritmo.',
    'Sob os olhares do dia eterno, fazei morada breve no refúgio do repouso.',
    'Permiti que o tempo vos toque suavemente, levando convosco as '
    'dores da jornada.',
    'No altar do descanso, deitai vosso cansaço e elevai vossas '
    'forças novamente.',
    'No fulgor do meio-dia, mesmo os mais destemidos encontram '
    'alívio na pausa.',
    'O mundo respira ao vosso redor; uni-vos ao seu ritmo e repousai.',
    'Deixai que a vida, por um breve instante, cesse seu tumulto em '
    'vossos corações.',
    'Os deuses vos oferecem a sombra amiga; aceitai-a como bênção.',
    'Sob o olhar plácido do firmamento, vossas almas podem descansar em paz.',
    'Deixai o cansaço dissipar-se como a névoa que o sol dispersa.',
    'Neste momento sagrado, a paz reina; não há inimigo que vos perturbe.',
    'Os campos vos acolhem, e o sussurro do vento vos embala ao '
    'sono reparador.',
    'O sol generoso vos aquece, enquanto o espírito se renova na pausa.',
    'Sob a árvore frondosa, o tempo se estica para vos ofertar serenidade.',
    'No breve intervalo do dia, deixai que vossos corpos comunguem com a '
    'terra.',
    'O tempo concede uma trégua; aceitai-a, pois ela é rara e preciosa.',
    'No teatro da vida, esta é a cena onde o descanso é o protagonista.',
    'Sob o manto dourado do sol, o tempo se curva, e vós, heróis, tendes o '
    'direito de repousar.',
    'A luz do meio-dia acaricia os vossos corpos fatigados, '
    'que a sombra do descanso vos abrace.',
    'A jornada, embora árdua, faz-se breve diante do descanso que '
    'o céu vos oferece.',
    'Que a calma do dia alcance vossos corações, '
    'e que a paz vos envolva como um manto.',
    'Em meio à alvorada, é tempo de repouso, onde o '
    'vento sussurra histórias antigas aos vossos ouvidos.',
    'Que o brilho do sol a vossos olhos traga a serenidade, '
    'e a quietude envolva vossas almas.',
    'Agora, os pés que pisaram os caminhos árduos encontram alívio, '
    'e os corpos cansados se estendem à sombra acolhedora.',
    'O dia, em sua plenitude, oferece-vos uma pausa, como um '
    'suspiro profundo no tempo que passa.',
    'Aqui, neste instante, o fardo cessa, e os guerreiros de '
    'grande coragem se entregam à breve paz do descanso.',
    'À sombra das árvores e sob o olhar atento do céu, vós descansais, '
    'como merecem os filhos da batalha.',
    'O sol está alto, e a terra se oferece a vós, como um leito macio para '
    'vossos corpos fatigados.',
    'Que o silêncio do meio-dia vos acalme, '
    'e que as horas passadas se dissipem como névoa ao vento.',
    'O tempo, agora, repousa como vós, e o ritmo da '
    'jornada desacelera neste breve refúgio.',
    'Em meio à vastidão do dia, a calma chegou, como um '
    'bálsamo para vossos espíritos cansados.',
    'A luz dourada do sol se derrama sobre vós, como um '
    'véu de tranquilidade que se estende sobre a terra.',
    'Agora, vós repousais sob o abraço caloroso do sol, '
    'como guerreiros que merecem a graça do descanso.',
    'As folhas sussurram com a brisa, e vossos corpos, por fim, '
    'encontram a paz sob o manto do dia.',
    'O calor do sol aquece, e o peso da jornada se dissipa, '
    'tal qual as sombras da noite ao amanhecer.',
    'Vós descansais, como heróis que retornam ao lar, '
    'temporariamente afastados das guerras da existência.',
    'Que os vossos corpos, exaustos pela luta, encontrem alívio na '
    'quietude do dia que se estende à vossa frente.',
    'O sol, guardião da luz, vela por vós enquanto repousais, '
    'e o mundo à vossa volta sussurra serenidade.',
    'Vós, aventureiros incansáveis, agora sois acariciados pelo descanso, '
    'como a brisa suave que beija o rosto.',
    'A fatiga de mil passos se dissolve enquanto o dia, '
    'em sua magnificência, vos oferece um breve descanso.',
    'Na calma deste momento, o sol se põe como um guardião que '
    'vigia vossos sonhos.',
    'É hora de repouso, de alívio, quando o tempo, como um rio, '
    'flui tranquilo e sereno.',
    'A batalha, embora distante, faz-se nublada enquanto o '
    'dia vos concede sua quietude.',
    'O calor do dia é um convite a vós, viajantes, para pausardes e '
    'renovardes vossas forças.',
    'Que o vento suave e o brilho solar restaurarem vossos corpos e '
    'mentes fatigadas.',
    'Agora, como reis e rainhas em seus palácios, vós repousais sob a '
    'misericórdia do sol.',
    'Em pleno dia, onde as sombras se fazem suaves, vós encontrais um '
    'refúgio para vossos corações.',
    'Que o sol, generoso em seu domínio, vos conceda a calma merecida após '
    'tanta dureza.',
    'Os campos ao redor, serenos e vastos, convidam-vos a descansar, '
    'como flores que se abrem ao sol.',
    'Agora, neste compasso tranquilo, vossas armas repousam ao lado, '
    'e vossos espíritos se acalmam.',
    'Em meio ao campo, onde o sol dança entre as folhas, vós encontrais o '
    'alívio desejado.',
    'Que o som das folhas sussurrantes e o calor da luz tragam descanso aos '
    'guerreiros que merecem paz.',
    'Vós descansais, entre o céu e a terra, enquanto o sol observa com seus '
    'olhos dourados.',
    'A jornada continua, mas neste breve intervalo, o sol se torna vosso '
    'companheiro de descanso.',
    'Que a quietude do momento acalme o furor do dia e traga a serenidade '
    'que vossos corpos buscam.',
    'Assim, entre o brilho dourado e a sombra acolhedora, vós repousais, '
    'longe da luta que tanto vos consome.',
    'O céu, em sua plenitude, sorri para vós enquanto encontrais descanso na '
    'glória do meio-dia.',
    'Em cada respiração, o dia se torna um véu que vos protege do peso do '
    'mundo exterior.',
    'As horas do sol passam lentas e brandas, e vós, guerreiros, '
    'encontrais serenidade nos braços do descanso.',
    'Por um breve momento, os corações batem em paz, '
    'enquanto a terra oferece descanso aos vossos corpos fatigados.',
    'O calor suave do dia, como um abraço acolhedor, '
    'acalma as almas inquietas de vós, filhos da guerra.',
    'Os ecos das batalhas se apagam, e o silêncio acolhedor do '
    'descanso se faz presente.',
    'Na vastidão do dia, a paz reina, e vossos corpos podem se '
    'entregar ao alívio do repouso.',
    'O sol, em sua majestade, vos convida a pausar, como um pai que '
    'acalma os filhos cansados.',
    'Vós sois abençoados por este descanso, como o campo que se '
    'acalma sob a carícia do vento.',
    'Que o mundo que vos rodeia seja um campo tranquilo onde vossos '
    'corpos encontrem alívio.',
    'Agora, heróis, sob o brilho dourado, vós repousais, como estrelas que '
    'piscam brevemente antes de uma nova jornada.',
]
