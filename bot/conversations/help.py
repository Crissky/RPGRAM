'''
Módulo responsável por gerenciar os comandos de ajuda.
'''

from enum import Enum
from typing import Iterable

from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    PrefixHandler,
)

from bot.constants.help import (
    ACCESS_DENIED,
    CALLBACK_BASE_ATTRIBUTES,
    CALLBACK_CLASSES,
    CALLBACK_DEBUFFS,
    CALLBACK_EQUIPS,
    CALLBACK_GENERAL,
    CALLBACK_COMBAT_ATTRIBUTES,
    CALLBACK_GROUP,
    CALLBACK_HEALSTATUS,
    CALLBACK_ITEMS,
    CALLBACK_PLAYER,
    CALLBACK_RACES,
    CALLBACK_STATS,
    COMMANDS
)
from bot.constants.add_stats import COMMANDS as add_stats_commands
from bot.constants.bag import COMMANDS as bag_commands
from bot.constants.battle import COMMANDS as battle_commands
from bot.constants.classe import COMMANDS as classe_commands
from bot.constants.config_group import COMMANDS as config_group_commands
from bot.constants.config_player import COMMANDS as config_player_commands
from bot.constants.create_char import COMMANDS as create_char_commands
from bot.constants.equips import COMMANDS as equips_commands
from bot.constants.race import COMMANDS as race_commands
from bot.constants.rest import COMMANDS as rest_commands
from bot.constants.sign_up_group import COMMANDS as sign_up_group_commands
from bot.constants.sign_up_player import COMMANDS as sign_up_player_commands
from bot.constants.view_char import COMMANDS as view_char_commands
from bot.constants.view_group import COMMANDS as view_group_commands
from bot.constants.view_player import COMMANDS as view_player_commands
from bot.constants.filters import (
    BASIC_COMMAND_FILTER,
    PREFIX_COMMANDS
)
from bot.conversations.close import get_close_button
from bot.decorators import print_basic_infos
from bot.functions.general import get_attribute_group_or_player

from constant.text import SECTION_HEAD, TEXT_SEPARATOR

from function.text import escape_basic_markdown_v2
from rpgram.conditions.debuff import DEBUFFS
from rpgram.conditions.heal import HEALSTATUS
from rpgram.enums import (
    EmojiEnum,
    EquipmentEnum,
    AccessoryMaterialsEnum,
    MagicalGrimoireMaterialEnum,
    MagicalStonesMaterialEnum,
    MagicalWearableMaterialEnum,
    MagicalMaskMaterialEnum,
    MagicalQuillMaterialEnum,
    WeaponMaterialEnum,
    WearableMaterialEnum,
    TacticalWearableMaterialEnum,
    RarityEnum
)
from rpgram.enums.consumable import HealingConsumableEnum
from rpgram.enums.debuff import DebuffEnum


@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id
    option = None
    if query:
        data = eval(query.data)
        option = data['option']
        data_user_id = data['user_id']
        # Não executa se outro usuário mexer na ajuda
        if data_user_id != user_id:
            await query.answer(text=ACCESS_DENIED, show_alert=True)
            return ConversationHandler.END

    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    text = get_details_text(option)

    if query:
        await query.edit_message_text(
            text=text,
            reply_markup=get_help_reply_markup(update),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    else:
        await update.effective_message.reply_markdown_v2(
            text=text,
            disable_notification=silent,
            reply_markup=get_help_reply_markup(update),
        )


def get_details_text(option: str) -> str:
    text = ''
    if option == CALLBACK_GENERAL or option is None:
        add_stats_cmd = command_to_string(add_stats_commands)
        bag_cmd = command_to_string(bag_commands)
        battle_cmd = command_to_string(battle_commands)
        classe_cmd = command_to_string(classe_commands)
        config_group_cmd = command_to_string(config_group_commands)
        config_player_cmd = command_to_string(config_player_commands)
        create_char_cmd = command_to_string(create_char_commands)
        equips_cmd = command_to_string(equips_commands)
        race_cmd = command_to_string(race_commands)
        rest_cmd = command_to_string(rest_commands)
        sign_up_group_cmd = command_to_string(sign_up_group_commands)
        sign_up_player_cmd = command_to_string(sign_up_player_commands)
        view_char_cmd = command_to_string(view_char_commands)
        view_group_cmd = command_to_string(view_group_commands)
        view_player_cmd = command_to_string(view_player_commands)
        text = (
            f'{SECTION_HEAD.format("COMANDOS")}\n\n'

            f'{EmojiEnum.GROUP.value}'
            f'*CRIAR CONTA DO GRUPO*: /{sign_up_group_commands[0]}\n'
            f'INFO: Cria uma conta para o grupo.\n'
            f'Atalhos: {sign_up_group_cmd}\n\n'

            f'{EmojiEnum.PLAYER.value}'
            f'*CRIAR CONTA DE JOGADOR*: /{sign_up_player_commands[0]}\n'
            f'INFO: Cria uma conta para o jogador.\n'
            f'Atalhos: {sign_up_player_cmd}\n\n'

            f'{EmojiEnum.CHARACTER.value}'
            f'*CRIAR PERSONAGEM*: /{create_char_commands[0]}\n'
            f'INFO: Cria um personagem para o jogador.\n'
            f'Atalhos: {create_char_cmd}\n\n'

            f'{EmojiEnum.GROUP.value}'
            f'*INFORMAÇÕES DO GRUPO*: /{view_group_commands[0]}\n'
            f'INFO: Exibe as informações do grupo.\n'
            f'Atalhos: {view_group_cmd}\n\n'

            f'{EmojiEnum.PLAYER.value}'
            f'*INFORMAÇÕES DO JOGADOR*: /{view_player_commands[0]}\n'
            f'INFO: Exibe as informações do jogador.\n'
            f'Atalhos: {view_player_cmd}\n\n'

            f'{EmojiEnum.CHARACTER.value}'
            f'*INFORMAÇÕES DO PERSONAGEM*: /{view_char_commands[0]}\n'
            f'INFO: Exibe as informações do personagem.\n'
            f'Atalhos: {view_char_cmd}\n\n'

            f'{EmojiEnum.STATS.value}'
            f'*ADICIONAR/EXIBIR ESTATISTICAS*: /{add_stats_commands[0]}\n'
            f'INFO: Exibe ou Adiciona estatisticas no personagem.\n'
            f'Atalhos: {add_stats_cmd}\n\n'

            f'{EmojiEnum.CONFIG.value}'
            f'*CONFIGURAÇÃO DO GRUPO*: /{config_group_commands[0]}\n'
            f'INFO: Configura preferências do grupo.\n'
            f'Atalhos: {config_group_cmd}\n\n'

            f'{EmojiEnum.CONFIG.value}'
            f'*CONFIGURAÇÃO DO JOGADOR*: /{config_player_commands[0]}\n'
            f'INFO: Configura preferências do jogador.\n'
            f'Atalhos: {config_player_cmd}\n\n'

            f'{EmojiEnum.BATTLE.value}*CRIAR BATALHA*: /{battle_commands[0]}\n'
            f'INFO: Inicia uma batalha no grupo.\n'
            f'Atalhos: {battle_cmd}\n\n'

            f'{EmojiEnum.REST.value}*INICIAR DESCANSO*: /{rest_commands[0]}\n'
            f'INFO: Recupera HP do personagem a cada hora '
            f'(mesmo se estiver 0).\n'
            f'Atalhos: {rest_cmd}\n\n'

            f'{EmojiEnum.CLASS.value}*CLASSES*: /{classe_commands[0]}\n'
            f'INFO: Exibe as classes existentes no jogo, tanto para os '
            f'jogadores, quanto as classes exclusivas para os NPCs.'
            f'Atalhos: {classe_cmd}\n\n'

            f'{EmojiEnum.RACE.value}*RAÇAS*: /{race_commands[0]}\n'
            f'INFO: Exibe as raças existentes no jogo, tanto para os '
            f'jogadores, quanto as raças exclusivas para os NPCs.'
            f'Atalhos: {race_cmd}\n\n'

            f'{EmojiEnum.ITEMS.value}*BOLSA*: /{bag_commands[0]}\n'
            f'INFO: Exibe o conteúdo da bolsa.\n'
            f'Atalhos: {bag_cmd}\n\n'

            f'{EmojiEnum.EQUIPS.value}*EQUIPAMENTOS*: /{equips_commands[0]}\n'
            f'INFO: Exibe os itens equipados no personagem.\n'
            f'Atalhos: {equips_cmd}\n\n'
        )
    elif option == CALLBACK_STATS:
        add_stats_cmd = command_to_string(add_stats_commands)
        text = (
            f'*ADICIONAR/EXIBIR ESTATISTICAS*: /{add_stats_commands[0]}\n'
            f'Argumentos: [<ATRIBUTO> <VALOR>]\n\n'

            f'Exemplo: "/{add_stats_commands[0]} FOR 10" '
            f'(Adiciona 10 pontos em FORÇA).\n\n'

            f'OBS: Pode ser usado sem argumentos para exibir as estatísticas '
            f'do personagem. '
            f'Use o argumento "verbose" ou "v" para exibir as estatísticas '
            f'com mais detalhes.\n\n'

            f'Atalhos: {add_stats_cmd}'
        )
    elif option == CALLBACK_GROUP:
        config_group_cmd = command_to_string(config_group_commands)
        sign_up_group_cmd = command_to_string(sign_up_group_commands)
        view_group_cmd = command_to_string(view_group_commands)
        text = (
            f'*CRIAR CONTA DO GRUPO*: /{sign_up_group_commands[0]}\n'
            f'INFO: Cria uma conta para o grupo.\n\n'

            f'Atalhos: {sign_up_group_cmd}\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'*CONFIGURAÇÃO DO GRUPO*: /{config_group_commands[0]}\n'
            f'Argumentos: [<CONFIGURAÇÃO> <VALOR>]\n\n'

            f'Configurações:\n'
            f'    "verbose": [true/false]. Configura se o bot vai falar muito.'
            f'\n'
            f'    "silent": [true/false]. Configura se as notificações do bot '
            f'no '
            f'grupo terão som.\n'
            f'    "spawn_start_time": inteiro[0-24]. Hora de início do spawn.'
            f'\n'
            f'    "spawn_end_time": inteiro[0-24]. Hora de fim do spawn.\n'
            f'    "multiplier_xp": decimal[0-5]. Multiplicador de XP.\n'
            f'    "char_multiplier_xp": decimal[0-10]. Multiplicador do bônus '
            f'de '
            f'XP baseado no nível do personagem.\n\n'

            f'Outros Argumentos:\n'
            f'    "default": Retorna a configuração do grupo para o padrão.\n'
            f'    "update": Atualiza as informações do grupo.\n\n'

            f'Atalhos: {config_group_cmd}\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'*INFORMAÇÕES DO GRUPO*: /{view_group_commands[0]}\n'
            f'INFO: Exibe as informações do grupo.\n\n'

            f'Atalhos: {view_group_cmd}\n\n'
        )
    elif option == CALLBACK_PLAYER:
        config_player_cmd = command_to_string(config_player_commands)
        sign_up_player_cmd = command_to_string(sign_up_player_commands)
        view_player_cmd = command_to_string(view_player_commands)
        text = (
            f'*CRIAR CONTA DE JOGADOR*: /{sign_up_player_commands[0]}\n'
            f'INFO: Cria uma conta para o jogador.\n\n'

            f'Atalhos: {sign_up_player_cmd}\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'*CONFIGURAÇÃO DO JOGADOR*: /{config_player_commands[0]}\n'
            f'Argumentos: [<CONFIGURAÇÃO> <VALOR>]\n\n'

            f'Configurações:\n'
            f'    "verbose": [true/false]. Configura se o bot vai envia '
            f'mensagens privadas para o jogador.\n'
            f'    "silent": [true/false]. Configura se as notificações do bot '
            f'no chat privado terão som.\n\n'

            f'Outros Argumentos:\n'
            f'    "default": Retorna a configuração do jogador para o padrão.\n'
            f'    "update": Atualiza as informações do jogador.\n\n'

            f'Atalhos: {config_player_cmd}\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'*INFORMAÇÕES DO JOGADOR*: /{view_player_commands[0]}\n'
            f'INFO: Exibe as informações do jogador.\n\n'

            f'Atalhos: {view_player_cmd}\n\n'
        )
    elif option == CALLBACK_EQUIPS:
        equips_cmd = command_to_string(equips_commands)
        text = (
            f'*EQUIPAMENTOS*: /{equips_commands[0]}\n'
            f'INFO: Mostra os equipamentos do personagem.\n\n'

            f'OBS: Use o argumento "verbose" ou "v" para exibir os '
            f'equipamentos e as estatísticas que os equipamentos garantem '
            f'com mais detalhes.\n\n'

            f'Atalhos: {equips_cmd}\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'{EmojiEnum.EQUIPMENT_POWER.value}*PODER*\n\n'
            f'O poder de um equipamento é calculado como a soma poderada de '
            f'todos os atributos que o equipamento garante. Existem alguns '
            f'fatores que influenciam no total de pontos de atributo que um '
            f'equipamento vai possuir. Os principais fatores são: '
            f'`Nível do Equipamento`, `Tipo do Equipamento`, '
            f'`Raridade` e `Material`.\n\n'

            f'{EmojiEnum.EQUIPMENT_LEVEL.value}*NÍVEL DO EQUIPAMENTO*\n\n'

            f'O `Nível do Equipamento` é o requisitos que todos os '
            f'equipamentos possuem. Personagens com um `Nível` inferior ao '
            f'`Nível do Equipamento` não poderão utilizar o equipamento.\n\n'
            f'O `Nível do Equipamento` também é a base da distribuição dos '
            f'atributos dos equipamentos. Ele será multiplicado pela valor do '
            f'`Tipo do Equipamento`, `Raridade` e `Material` para definir '
            f'o valor total de pontos que serão distribuídos entre os '
            f'`Atributos de Combate` do equipamento.\n\n'

            f'{EmojiEnum.EQUIPS.value}*TIPO DE EQUIPAMENTO*\n\n'

            f'Os tipos de equipamentos são {len(EquipmentEnum)} ao todo. '
            f'Cada tipo de equipamento possui um multiplicador diferente.\n'
            f'Os tipos de equipamento são:\n'
            f'{EmojiEnum.HELMET.value}`{EquipmentEnum.HELMET.value}` (x0,5), '
            f'{EmojiEnum.ONE_HAND.value}`{EquipmentEnum.ONE_HAND.value}` (x1), '
            f'{EmojiEnum.TWO_HANDS.value}`{EquipmentEnum.TWO_HANDS.value}` (x2,5), '
            f'{EmojiEnum.ARMOR.value}`{EquipmentEnum.ARMOR.value}` (x2,5), '
            f'{EmojiEnum.BOOTS.value}`{EquipmentEnum.BOOTS.value}` (x0,5), '
            f'{EmojiEnum.RING.value}`{EquipmentEnum.RING.value}` (x0,25), '
            f'{EmojiEnum.AMULET.value}`{EquipmentEnum.AMULET.value}` (x0,25).\n\n'

            f'{EmojiEnum.EQUIPMENT_RARITY.value}*RARIDADE*\n\n'

            f'Os tipos de raridade são {len(RarityEnum)} ao todo. '
            f'Cada raridade possui um multiplicador diferente. Além disso, '
            f'as raridades acima da `{list(RarityEnum)[1].value}` possuem a '
            f'chance de ter `Atributos Ocultos` que precisam ser identificados '
            f'para que o personagem possa garantir esses bônus. Esses '
            f'`Atributos Ocultos` são pontos extras que podem ser '
            f'distribuídos nos `Atributos de Combate` e também nos '
            f'`Atributos Base`.\n'
            f'As raridades são:\n'
            f'{help_enum(RarityEnum)}.\n\n'

            f'{EmojiEnum.EQUIPMENT_MATERIAL.value}*MATERIAIS*\n\n'

            f'Os materias variam de acordo com o `Tipo do Equipamento` '
            f'podendo variar entre equipamentos de um mesmo tipo. '
            f'Os materias dos equipamentos são:\n'

            f'*Armas* : {help_enum(WeaponMaterialEnum)}.\n\n'
            f'*Penas* : {help_enum(MagicalQuillMaterialEnum)}.\n\n'
            f'*Grimórios* : {help_enum(MagicalGrimoireMaterialEnum)}.\n\n'
            f'*Pedras Mágicas* : {help_enum(MagicalStonesMaterialEnum)}.\n\n'
            f'*Vestes* : {help_enum(WearableMaterialEnum)}.\n\n'
            f'*Vestes Mágicas* : {help_enum(MagicalWearableMaterialEnum)}.\n\n'
            f'*Máscaras* : {help_enum(MagicalMaskMaterialEnum)}.\n\n'
            f'*Capas* : {help_enum(TacticalWearableMaterialEnum)}.\n\n'
            f'*Acessórios* : {help_enum(AccessoryMaterialsEnum)}.\n\n'
        )
    elif option == CALLBACK_BASE_ATTRIBUTES:
        text = (
            f'{EmojiEnum.BASE_ATTRIBUTES.value}*ATRIBUTOS BASE*\n\n'

            f'Os Atributos Base do personagem representam suas '
            'características que vão além do combate. Os seis Atributos Base '
            f'são os seguintes:\n\n'

            f'{EmojiEnum.STRENGTH.value}'
            f'*Força* (FOR): Representa a força física do personagem. '
            f'A força influencia bastante no `Ataque Físico` e um pouco nos '
            f'`Pontos de Vida`.\n\n'

            f'{EmojiEnum.DEXTERITY.value}'
            f'*Destreza* (DES): Representa a habilidade e a ligeireza do '
            f'personagem. A destreza influencia bastante no '
            f'`Ataque de Precisão`, `Acerto` e `Evasão`, possui influência '
            f'moderada na `Iniciativa` e um pouco de influência no '
            f'`Ataque Físico` e na `Defesa Física`.\n\n'

            f'{EmojiEnum.CONSTITUTION.value}'
            f'*Constituição* (CON): Representa o vigor físico do '
            f'personagem e a capacidade de resistir à ataques de qualquer '
            f'origem. A contituição influencia bastante nos `Pontos de Vida` '
            f'e na `Defesa Física` e também influencia um pouco da '
            f'`Defesa Mágica`.\n\n'

            f'{EmojiEnum.INTELLIGENCE.value}'
            f'*Inteligência* (INT): Representa a capacidade do personagem '
            f'de pensar e aprender coisas por meio de estudo. '
            f'A inteligência influencia consideravelmente no '
            f'`Ataque Mágico`.\n\n'

            f'{EmojiEnum.WISDOM.value}'
            f'*Sabedoria* (SAB): Representa a capacidade de raciocício '
            f'inata e a habilidade de compreender o mundo do personagem. '
            f'A sabedoria influencia bastante na `Iniciativa` e na '
            f'`Defesa Mágica` e tem pouca influência no `Ataque Mágico`, '
            f'`Acerto` e `Evasão`.\n\n'

            f'{EmojiEnum.CHARISMA.value}'
            f'*Carisma* (CAR): Representa a capacidade do personagem de '
            f'inspirar, persuadir, sugestionar ou manipular outras pessoas, '
            f'seja de maneira positiva ou negativa. '
            f'O carisma influencia bastante na `Iniciativa` e contribui '
            f'um pouco no `Acerto` e na `Evasão`.\n\n'
        )
    elif option == CALLBACK_COMBAT_ATTRIBUTES:
        text = (
            f'{EmojiEnum.COMBAT_ATTRIBUTES.value}*ATRIBUTOS DE COMBATE*\n\n'

            f'Os Atributos de Combate do personagem representam suas '
            f'habilidades ofensivas e defensivas em lutas. Esses atributos '
            f'são diretamente influenciados pelos `Atributos Base` '
            f'do personagem. Os nove Atributos de Combate '
            f'são os seguintes:\n\n'

            f'{EmojiEnum.HIT_POINT.value}'
            f'*Pontos de Vida (HP)*: Representam a '
            f'vitalidade do personagem. Quando os `Pontos de Vida` chegam a '
            f'zero o personagem ficará incapacidado até que recupere ao menos '
            f'um `Ponto de Vida`.\n'
            f'Os Atributos Base que compoem os `Pontos de Vida` são:\n'
            f'A `Constituição`(x15) e a `Força`(x8).\n\n'

            f'{EmojiEnum.INITIATIVE.value}'
            f'*Iniciativa*: Representa o quão rápido e sagaz um '
            f'personagem é para agir em combate. Quanto maior o valor da '
            f'`Iniciativa` em relação a dos demais lutadores, mais a frente o '
            f'personagem estará na ordem de ataque.\n'
            f'Os Atributos Base que compoem a `Iniciativa` são:\n'
            f'A `Sabedoria`(x3), o `Carisma`(x3) e a `Destreza`(x2).\n\n'

            f'{EmojiEnum.PHYSICAL_ATTACK.value}'
            f'*Ataque Físico*: Representa o poder dos '
            f'golpes baseados na força física do personagem. Quanto maior o '
            f'valor do `Ataque Físico` em relação ao da `Defesa Física` '
            f'do alvo, maior será o dano causado aos `Pontos de Vida`.\n'
            f'Os Atributos Base que compoem o `Ataque Físico` são:\n'
            f'A `Força`(x3) e a `Destreza`(x2).\n\n'

            f'{EmojiEnum.PRECISION_ATTACK.value}'
            f'*Ataque de Precisão*: Representa o '
            f'poder dos golpes de visam atingir os pontos vitais do oponente '
            f'para causar mais dano sem a necessidade de possuir uma grande '
            f'força física. Quanto maior o valor do `Ataque de Precisão` em '
            f'relação ao da `Defesa Física` do alvo, maior será o dano '
            f'causado aos `Pontos de Vida` do oponente.\n'
            f'Os Atributos Base que compoem o `Ataque de Precisão` são:\n'
            f'`Destreza`(x4).\n\n'

            f'{EmojiEnum.MAGICAL_ATTACK.value}'
            f'*Ataque Mágico*: Representa o poder dos '
            f'feitiços, magias e quaisquer outras habilidades sobrenaturais '
            f'do personagem. Quanto maior o valor do `Ataque Mágico` em '
            f'relação ao da `Defesa Mágica` do alvo, maior será o dano '
            f'causado aos `Pontos de Vida` do inimigo.\n'
            f'Os Atributos Base que compoem o `Ataque Mágico` são:\n'
            f'`Inteligência`(x4) e `Sabedoria`(x2).\n\n'

            f'{EmojiEnum.PHYSICAL_DEFENSE.value}'
            f'*Defesa Física*: Representa a habilidade '
            f'que o personagem possui para bloquear o dano de um '
            f'golpe físico (aqueles baseados em `Ataque Físico` ou '
            f'`Ataque de Precisão`).\n'
            f'Os Atributos Base que compoem a `Defesa Física` são:\n'
            f'`Constituição`(x3) e `Destreza`(x2).\n\n'

            f'{EmojiEnum.MAGICAL_DEFENSE.value}'
            f'*Defesa Mágica*: Representa a capacidade '
            f'que o personagem possui para bloquear o dano oriundo '
            f'de ataques sobrenaturais (aqueles baseados em '
            f'`Ataque Mágico`).\n'
            f'Os Atributos Base que compoem a `Defesa Mágica` são:\n'
            f'`Sabedoria`(x4), `Inteligência`(x2) e `Constituição`(x2).\n\n'

            f'{EmojiEnum.HIT.value}'
            f'*Acerto*: Representa a perícia que o '
            f'personagem possui para ter êxito em atingir um alvo com '
            f'os seus ataques. Quanto maior o valor do `Acerto` em relação '
            f'ao da `Evasão` do alvo, maior será a chance de acerto.\n'
            f'Os Atributos Base que compoem o `Acerto` são:\n'
            f'`Destreza`(x3), `Sabedoria`(x2) e `Carisma`(x2).\n\n'

            f'{EmojiEnum.EVASION.value}'
            f'*Evasão*: Representa a maestria que o '
            f'personagem possui para evitar qualquer ataque. Quanto maior '
            f'o valor da `Evasão` em relação ao do `Acerto` do atacante, '
            f'maior será a chance de evitar o ataque.\n'
            f'Os Atributos Base que compoem o `Evasão` são:\n'
            f'`Destreza`(x3), `Sabedoria`(x2) e `Carisma`(x2).\n\n'
        )
    elif option == CALLBACK_ITEMS:
        text = (
            f'{EmojiEnum.ITEMS.value}*ITEMS*\n\n'

            f'Os itens são divididos em duas categorias: `Consumíveis` e '
            f'`Equipamentos`.\n'
            f'Os itens `Consumíveis` são aqueles que o personagem pode usar '
            f'somente uma vez, como beber uma poção de cura para recuperar os '
            f'`Pontos de Vida`.\n'
            f'Os `Equipamentos` são itens que o personagem pode usar para '
            f'obter poderes enquanto estiver com ele equipado, como os '
            f'pontos de `Ataque Físico` que uma espada pode fornecer ao '
            f'personagem.'
        )
    elif option == CALLBACK_DEBUFFS:
        text = (
            f'{EmojiEnum.STATUS.value}*Status(Debuffs)*\n\n'

            f'Debuffs são *condições* que prejudicam o personagem de diversas '
            f'maneiras - como causar dano ou reduzir as estatísticas.\n\n'

            f'Os debuffs podem durar uma quantidade fixa de turnos ou por '
            f'tempo indeterminado.\n\n'

            f'Quando o personagem com um debuff de um tipo recebe novamente '
            f'um debuff do mesmo tipo, o número de turnos para se curar '
            f'retorna para o valor inicial e o '
            f'nível do debuff é aumentado.\n\n'

            f'O nível do debuff pode influenciar em quanto de prejuízo '
            f'ele ira causar ao personagem ou somente dificultar na cura '
            f'por meio de itens.\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'*Lista de Debuffs*:\n\n'
        )
        for debuff in DEBUFFS:
            debuff_name = debuff.name.upper()
            debuff_name = DebuffEnum[debuff_name].value
            text += f'*Nome*: {debuff.emoji}{debuff.name} ({debuff_name})\n'
            text += f'*Descrição*: {debuff.description}\n\n'
    elif option == CALLBACK_HEALSTATUS:
        text = (
            f'{EmojiEnum.STATUS.value}*Status(Cura)*\n\n'

            f'*Condições* de cura recuperam os Pontos de Vida (HP) do '
            f'personagem a cada turno.\n\n'

            f'Essas *condições* geralmente são recebidas pelo uso de itens ou '
            f'magias de cura durante a batalha, podendo durar alguns '
            f'turnos ou por um número indefinido de turnos.\n\n'

            f'Fora de batalha, essas *condições* duram somente um turno, '
            f'recebendo a cura de um turno multiplicada pelo total de turnos '
            f'faltantes.\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'*Lista de Condições de Cura*:\n\n'
        )

        for heal_status in HEALSTATUS:
            text += f'*Nome*: {heal_status.emoji}{heal_status.name}\n'
            text += f'*Descrição*: {heal_status.description}\n\n'
    elif option == CALLBACK_CLASSES:
        text = (
            f'Página de ajuda das CLASSES ainda não foi escrita. '
            f'Contacte do admininastrô.'
        )
    elif option == CALLBACK_RACES:
        text = (
            f'Página de ajuda das RAÇAS ainda não foi escrita. '
            f'Contacte do admininastrô.'
        )
    else:
        raise ValueError(f'Opção de ajuda não encontrada: {option}')

    return escape_basic_markdown_v2(text)


def get_help_reply_markup(update: Update):
    user_id = update.effective_user.id
    query = update.callback_query
    option = None
    if query:
        data = eval(query.data)
        option = data['option']

    stats_text = f'{EmojiEnum.STATS.value}Estatísticas'
    config_text = f'Grupo{EmojiEnum.GROUP.value}'
    player_text = f'{EmojiEnum.PLAYER.value}Jogador'
    equips_text = f'Equipamentos{EmojiEnum.EQUIPS.value}'
    base_attributes_text = f'{EmojiEnum.BASE_ATTRIBUTES.value}Atributos Base'
    combat_attributes_text = (
        f'Atributos de Combate{EmojiEnum.COMBAT_ATTRIBUTES.value}'
    )
    items_text = f'{EmojiEnum.ITEMS.value}Itens'
    debuffs_text = f'{EmojiEnum.STATUS.value}Status(Debuffs)'
    heal_status_text = f'Status(Cura){EmojiEnum.STATUS.value}'
    general_text = f'Geral{EmojiEnum.GENERAL.value}'
    classes_text = f'{EmojiEnum.CLASS.value}Classes'
    races_text = f'Raças{EmojiEnum.RACE.value}'

    (
        buttons1,
        buttons2,
        buttons3,
        buttons4,
        buttons5,
        buttons6
    ) = [], [], [], [], [], []
    if option != CALLBACK_PLAYER:
        buttons1.append(
            InlineKeyboardButton(
                text=player_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_PLAYER}","user_id":{user_id}}}'
                )
            )
        )
    if option != CALLBACK_GROUP:
        buttons1.append(
            InlineKeyboardButton(
                text=config_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_GROUP}","user_id":{user_id}}}'
                )
            )
        )
    if option != CALLBACK_STATS:
        buttons2.append(
            InlineKeyboardButton(
                text=stats_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_STATS}","user_id":{user_id}}}'
                )
            )
        )
    if option != CALLBACK_EQUIPS:
        buttons2.append(
            InlineKeyboardButton(
                text=equips_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_EQUIPS}","user_id":{user_id}}}'
                )
            )
        )
    if option != CALLBACK_BASE_ATTRIBUTES:
        buttons3.append(
            InlineKeyboardButton(
                text=base_attributes_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_BASE_ATTRIBUTES}",'
                    f'"user_id":{user_id}}}'
                )
            )
        )
    if option != CALLBACK_COMBAT_ATTRIBUTES:
        buttons3.append(
            InlineKeyboardButton(
                text=combat_attributes_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_COMBAT_ATTRIBUTES}",'
                    f'"user_id":{user_id}}}'
                )
            )
        )
    if option != CALLBACK_CLASSES:
        buttons4.append(
            InlineKeyboardButton(
                text=classes_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_CLASSES}","user_id":{user_id}}}'
                )
            )
        )
    if option != CALLBACK_RACES:
        buttons4.append(
            InlineKeyboardButton(
                text=races_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_RACES}","user_id":{user_id}}}'
                )
            )
        )
    if option != CALLBACK_ITEMS:
        buttons5.append(
            InlineKeyboardButton(
                text=items_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_ITEMS}","user_id":{user_id}}}'
                )
            )
        )
    if option != CALLBACK_GENERAL and query is not None:
        buttons5.append(
            InlineKeyboardButton(
                text=general_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_GENERAL}","user_id":{user_id}}}'
                )
            )
        )
    if option != CALLBACK_DEBUFFS:
        buttons6.append(
            InlineKeyboardButton(
                text=debuffs_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_DEBUFFS}","user_id":{user_id}}}'
                )
            )
        )
    if option != CALLBACK_HEALSTATUS:
        buttons6.append(
            InlineKeyboardButton(
                text=heal_status_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_HEALSTATUS}","user_id":{user_id}}}'
                )
            )
        )
    close_button = [get_close_button(user_id=user_id)]
    reply_markup = InlineKeyboardMarkup([
        buttons1, buttons2, buttons3,
        buttons4, buttons5, buttons6,
        close_button
    ])
    return reply_markup


def command_to_string(commands: Iterable) -> str:
    return ', '.join([f'`!{cmd}`'for cmd in commands])


def help_enum(enum_class: Enum) -> str:
    text = []
    for index, enum in enumerate(enum_class):
        text.append(f'`{enum.value}` (x{index + 1})')

    return ', '.join(text)


HELP_HANDLERS = [
    PrefixHandler(
        PREFIX_COMMANDS,
        COMMANDS,
        start,
        BASIC_COMMAND_FILTER
    ),
    CommandHandler(
        COMMANDS,
        start,
        BASIC_COMMAND_FILTER
    ),
    CallbackQueryHandler(start, pattern=r'^{"option":'),
]
