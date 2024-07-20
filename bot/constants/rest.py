COMMANDS = ['descanso', 'rest']
SECTION_TEXT_REST = 'DESCANSO'
SECTION_TEXT_WAKEUP = 'REVIGORADO!'
SECTION_TEXT_REST_MIDNIGHT = 'A MIMIR'
SECTION_TEXT_ACTION_PONTOS = 'PONTOS DE AÇÃO'
MINUTES_TO_RECOVERY_HIT_POINTS = 20
MINUTES_TO_RECOVERY_ACTION_POINTS = 10
REPLY_TEXTS_ALREADY_RESTING = [
    'Seu personagem já está descansando.',
    'Seu personagem já está aproveitando uma merecida pausa.',
    'Seu personagem já está descansando. Aguarde um pouco mais.',
    'Descanso é importante, mas seu personagem já está fazendo isso.',
    'Hmm, acho que seu personagem já está fazendo isso.',
    'Acalme-se! Seu personagem já está aproveitando um merecido descanso.',
    'Relaxe! Seu personagem já está descansando neste momento.',
    'Descanse um pouco você também! Seu personagem já está descansando.',
    'Seu personagem já está descansando e recuperando suas energias.',
    'Acalme-se! Seu personagem já está descansando, então aproveite o momento de tranquilidade.',
    'Descansar é importante para o bem-estar do seu personagem, mas ele já está descansando agora.',
    'Seu personagem já está relaxando e recarregando as energias.',
]
REPLY_TEXTS_NO_NEED_REST = [
    'Seu personagem já está totalmente recuperado. '
    'Não precisa descansar agora.',
    'Seu personagem está cheio de energia! Descansar seria um desperdício.',
    'Não há necessidade de descansar no momento. Seu personagem está pronto '
    'para qualquer desafio.',
    'Seu personagem sente uma energia renovada pulsando em suas veias. '
    'Descansar agora seria redundante.',
    'Seu personagem está com a saúde perfeita. '
    'Descansar seria apenas um capricho.',
    'Descansar agora seria como descansar eternamente. '
    'Seu personagem está pronto para enfrentar qualquer obstáculo.',
    'Seu personagem se sente revigorado e pronto para prosseguir. '
    'Não há motivo para descansar.',
    'A energia em seu corpo é palpável. '
    'Descansar seria um desperdício de tempo precioso.',
    'Seu personagem está radiante de vitalidade. '
    'Descansar não é necessário neste momento.',
    'Seu personagem já está completamente revigorado e '
    'pronto para a próxima aventura!',
    'O poder flui através de suas veias. '
    'Descansar agora seria como sufocar uma chama ardente.',
    'Seu personagem respira fundo e sente uma energia vibrante percorrer '
    'todo o seu ser. Não há necessidade de descansar.',
]
REPLY_TEXTS_STARTING_REST = [
    'Seu personagem senta e começa a descansar.',
    'Seu personagem encontra um local confortável para descansar.',
    'Seu personagem se acomoda e começa a relaxar.',
    'Seu personagem decide parar por um momento e recarregar suas energias.',
    'Seu personagem deita no chão e começa a descansar.',
    'Seu personagem se recosta em uma parede e relaxa.',
    'Seu personagem encontra uma sombra agradável para descansar.',
    'Seu personagem decide fazer uma pausa e recuperar suas forças.',
    'Seu personagem se senta em uma rocha e começa a descansar.',
    'Seu personagem encontra um local tranquilo e decide descansar um pouco.',
    'Seu personagem encontra um tronco caído e se senta para descansar.',
    'Seu personagem se deita em um leito de grama e relaxa.',
    'Seu personagem se ajoelha e começa a descansar.',
    'Seu personagem senta em uma pedra e decide descansar por um tempo.',
    'Seu personagem encontra uma fonte e se senta para descansar.',
    'Seu personagem decide parar um momento e recuperar o fôlego.',
    'Seu personagem se deita em uma cama improvisada e começa a descansar.',
    'Seu personagem se senta em uma árvore caída e relaxa.',
    'Seu personagem encontra um banco vazio e se senta para descansar.',
    'Seu personagem se recolhe em um canto e decide descansar um pouco.',
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
