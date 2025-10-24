'''
Módulo responsável por gerenciar os comandos de ajuda.
'''

from random import sample
import re
from enum import Enum
from operator import attrgetter
from typing import Iterable

from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.help import (
    ACCESS_DENIED,
    CALLBACK_BASE_ATTRIBUTES,
    CALLBACK_BUFFS,
    CALLBACK_CLASSES,
    CALLBACK_CURE_CONSUMABLE,
    CALLBACK_DEBUFFS,
    CALLBACK_EQUIPS,
    CALLBACK_GEMSTONE_CONSUMABLE,
    CALLBACK_GENERAL,
    CALLBACK_COMBAT_ATTRIBUTES,
    CALLBACK_GROUP,
    CALLBACK_HEALING_CONSUMABLE,
    CALLBACK_HEALSTATUS,
    CALLBACK_ITEMS,
    CALLBACK_OTHER_CONSUMABLE,
    CALLBACK_PLAYER,
    CALLBACK_RACES,
    CALLBACK_REVIVE_CONSUMABLE,
    CALLBACK_SPECIAL_DAMAGE,
    CALLBACK_STATS,
    CALLBACK_TROCADOPOUCH_CONSUMABLE,
    COMMANDS,
    SECTION_TEXT_HELP
)
from bot.constants.add_stats import COMMANDS as add_stats_commands
from bot.constants.bag import COMMANDS as bag_commands
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
from bot.constants.view_level import COMMANDS as view_level_commands
from bot.constants.view_player import COMMANDS as view_player_commands
from bot.constants.seller import COMMANDS as seller_commands, SELLER_NAME
from bot.constants.reset_char import COMMANDS as reset_char_commands
from bot.constants.skill_tree import COMMANDS as skill_commands
from bot.constants.filters import (
    BASIC_COMMAND_FILTER,
    PREFIX_COMMANDS
)
from bot.functions.chat import (
    MIN_AUTODELETE_TIME,
    call_telegram_message_function,
    get_close_button
)
from bot.decorators import print_basic_infos
from bot.decorators.player import alert_if_not_chat_owner
from bot.functions.general import get_attribute_group_or_player
from bot.functions.player import get_players_name_by_chat_id

from constant.text import (
    SECTION_HEAD,
    SECTION_HEAD_HELP_END,
    SECTION_HEAD_HELP_START,
    TEXT_SEPARATOR
)

from function.text import create_text_in_box, escape_basic_markdown_v2

from repository.mongo import ClasseModel, ItemModel, RaceModel
from rpgram.boosters import Equipment

from rpgram.conditions import ALL_BUFFS, ALL_DEBUFFS
from rpgram.conditions.heal import HEAL_STATUS
from rpgram.consumables import (
    CureConsumable,
    HealingConsumable,
    ReviveConsumable,
    GemstoneConsumable,
    TrocadoPouchConsumable
)
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
    RarityEnum,
    TrocadoEnum,
    CoinMaterialsEnum,
    KajiyaMaterialEnum,
    OmamoriMaterialEnum,
    SeishinWearbleMaterialEnum,
)
from rpgram.enums.damage import DamageEnum
from rpgram.skills.special_damage import SpecialDamage
from rpgram.stats.stats_combat import (
    EVASION_CHARISMA,
    EVASION_DEXTERITY,
    EVASION_INTELLIGENCE,
    EVASION_WISDOM,
    GENERAL_LEVEL,
    HIT_CHARISMA,
    HIT_DEXTERITY,
    HIT_INTELLIGENCE,
    HIT_POINTS_CONSTITUTION,
    HIT_POINTS_LEVEL,
    HIT_POINTS_STRENGTH,
    HIT_WISDOM,
    INITIATIVE_CHARISMA,
    INITIATIVE_DEXTERITY,
    INITIATIVE_INTELLIGENCE,
    INITIATIVE_WISDOM,
    MAGICAL_ATTACK_INTELLIGENCE,
    MAGICAL_ATTACK_WISDOM,
    MAGICAL_DEFENSE_CONSTITUTION,
    MAGICAL_DEFENSE_INTELLIGENCE,
    MAGICAL_DEFENSE_WISDOM,
    PHYSICAL_ATTACK_DEXTERITY,
    PHYSICAL_ATTACK_STRENGTH,
    PHYSICAL_DEFENSE_CONSTITUTION,
    PHYSICAL_DEFENSE_DEXTERITY,
    PRECISION_ATTACK_DEXTERITY,
    PRECISION_ATTACK_STRENGTH
)


@alert_if_not_chat_owner(alert_text=ACCESS_DENIED)
@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    option = None

    if query:
        data = eval(query.data)
        option = data['option']

    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    text = get_details_text(option)
    text = create_text_in_box(
        text=text,
        section_name=SECTION_TEXT_HELP,
        section_start=SECTION_HEAD_HELP_START,
        section_end=SECTION_HEAD_HELP_END
    )

    call_telegram_kwsargs = dict(
        text=text,
        reply_markup=get_help_reply_markup(update)
    )
    if query:
        call_telegram_kwsargs['function'] = query.edit_message_text
        call_telegram_kwsargs['parse_mode'] = ParseMode.MARKDOWN_V2
    else:
        call_telegram_kwsargs['function'] = (
            update.effective_message.reply_markdown_v2
        )
        call_telegram_kwsargs['disable_notification'] = silent

    await call_telegram_message_function(
        function_caller='HELP_START()',
        context=context,
        need_response=False,
        auto_delete_message=MIN_AUTODELETE_TIME,
        **call_telegram_kwsargs
    )


def get_details_text(option: str) -> str:
    text = ''
    if option == CALLBACK_GENERAL or option is None:
        add_stats_cmd = command_to_string(add_stats_commands)
        bag_cmd = command_to_string(bag_commands)
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
        view_level_cmd = command_to_string(view_level_commands)
        view_player_cmd = command_to_string(view_player_commands)
        seller_cmd = command_to_string(seller_commands)
        reset_char_cmd = command_to_string(reset_char_commands)
        skill_cmd = command_to_string(skill_commands)
        text = (
            f'{SECTION_HEAD.format("COMANDOS")}\n\n'

            f'{EmojiEnum.GROUP.value}'
            f'*CRIAR CONTA DO GRUPO*: /{sign_up_group_commands[0]}\n'
            'INFO: Cria uma conta para o grupo.\n'
            f'Atalhos: {sign_up_group_cmd}\n\n'

            f'{EmojiEnum.PLAYER.value}'
            f'*CRIAR CONTA DE JOGADOR*: /{sign_up_player_commands[0]}\n'
            'INFO: Cria uma conta para o jogador.\n'
            f'Atalhos: {sign_up_player_cmd}\n\n'

            f'{EmojiEnum.CHARACTER.value}'
            f'*CRIAR PERSONAGEM*: /{create_char_commands[0]}\n'
            'INFO: Cria um personagem para o jogador.\n'
            f'Atalhos: {create_char_cmd}\n\n'

            f'{EmojiEnum.GROUP.value}'
            f'*INFORMAÇÕES DO GRUPO*: /{view_group_commands[0]}\n'
            'INFO: Exibe as informações do grupo.\n'
            f'Atalhos: {view_group_cmd}\n\n'

            f'{EmojiEnum.PLAYER.value}'
            f'*INFORMAÇÕES DO JOGADOR*: /{view_player_commands[0]}\n'
            'INFO: Exibe as informações do jogador.\n'
            f'Atalhos: {view_player_cmd}\n\n'

            f'{EmojiEnum.CHARACTER.value}'
            f'*INFORMAÇÕES DO PERSONAGEM*: /{view_char_commands[0]}\n'
            'INFO: Exibe as informações do personagem.\n'
            f'Atalhos: {view_char_cmd}\n\n'

            f'{EmojiEnum.STATS.value}'
            f'*ADICIONAR/EXIBIR ESTATISTICAS*: /{add_stats_commands[0]}\n'
            'INFO: Exibe ou Adiciona estatisticas no personagem.\n'
            f'Atalhos: {add_stats_cmd}\n\n'

            f'{EmojiEnum.CONFIG.value}'
            f'*CONFIGURAÇÃO DO GRUPO*: /{config_group_commands[0]}\n'
            'INFO: Configura preferências do grupo.\n'
            f'Atalhos: {config_group_cmd}\n\n'

            f'{EmojiEnum.CONFIG.value}'
            f'*CONFIGURAÇÃO DO JOGADOR*: /{config_player_commands[0]}\n'
            'INFO: Configura preferências do jogador.\n'
            f'Atalhos: {config_player_cmd}\n\n'

            f'{EmojiEnum.REST.value}*INICIAR DESCANSO*: /{rest_commands[0]}\n'
            'INFO: Recupera HP do personagem a cada hora '
            '(mesmo se estiver 0).\n'
            f'Atalhos: {rest_cmd}\n\n'

            f'{EmojiEnum.CLASSE.value}*CLASSES*: /{classe_commands[0]}\n'
            'INFO: Exibe as classes existentes no jogo, tanto para os '
            'jogadores, quanto as classes exclusivas para os NPCs.\n'
            f'Atalhos: {classe_cmd}\n\n'

            f'{EmojiEnum.RACE.value}*RAÇAS*: /{race_commands[0]}\n'
            'INFO: Exibe as raças existentes no jogo, tanto para os '
            'jogadores, quanto as raças exclusivas para os NPCs.\n'
            f'Atalhos: {race_cmd}\n\n'

            f'{EmojiEnum.ITEMS.value}*BOLSA*: /{bag_commands[0]}\n'
            'INFO: Exibe o conteúdo da bolsa.\n'
            f'Atalhos: {bag_cmd}\n\n'

            f'{EmojiEnum.EQUIPS.value}*EQUIPAMENTOS*: /{equips_commands[0]}\n'
            'INFO: Exibe os itens equipados no personagem.\n'
            f'Atalhos: {equips_cmd}\n\n'

            f'{EmojiEnum.CHRYSUS_1.value}*LOJA*: /{seller_commands[0]}\n'
            f'INFO: Abre a loja do {SELLER_NAME}.\n'
            f'Atalhos: {seller_cmd}\n\n'

            f'{EmojiEnum.SKILL_POINTS.value}*HABILIDADES*: '
            f'/{skill_commands[0]}\n'
            'INFO: Abre o menu de gerenciamento de Habilidades.\n'
            f'Atalhos: {skill_cmd}\n\n'

            f'{EmojiEnum.SKILL_POINTS.value}*CHARS LEVELS*: '
            f'/{view_level_commands[0]}\n'
            'INFO: Exibe níveis dos personagens do grupo.\n'
            f'Atalhos: {view_level_cmd}'
        )
    elif option == CALLBACK_STATS:
        add_stats_cmd = command_to_string(add_stats_commands)
        reset_char_cmd = command_to_string(reset_char_commands)
        text = (
            f'*ADICIONAR/EXIBIR ESTATÍSTICAS*: /{add_stats_commands[0]}\n'
            'Argumentos: [<ATRIBUTO> <VALOR>]\n\n'

            f'Exemplo: "/{add_stats_commands[0]} FOR 10" '
            '(Adiciona 10 pontos em FORÇA).\n\n'

            'OBS: Pode ser usado sem argumentos para exibir as estatísticas '
            'do personagem. '
            'Use o argumento "verbose" ou "v" para exibir as estatísticas '
            'com mais detalhes.\n\n'

            f'Atalhos: {add_stats_cmd}\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'*RESETAR ATRIBUTOS BASE*: /{reset_char_commands[0]}\n'
            'INFO: Restitui todos os pontos usados nas estatísticas dos '
            '*Atributos Base*.\n\n'
            f'Atalhos: {reset_char_cmd}\n\n'
        )
    elif option == CALLBACK_GROUP:
        config_group_cmd = command_to_string(config_group_commands)
        sign_up_group_cmd = command_to_string(sign_up_group_commands)
        view_group_cmd = command_to_string(view_group_commands)
        text = (
            f'*CRIAR CONTA DO GRUPO*: /{sign_up_group_commands[0]}\n'
            'INFO: Cria uma conta para o grupo.\n\n'

            f'Atalhos: {sign_up_group_cmd}\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'*CONFIGURAÇÃO DO GRUPO*: /{config_group_commands[0]}\n'
            'Argumentos: [<CONFIGURAÇÃO> <VALOR>]\n\n'

            'Configurações:\n'
            '    "verbose": [true/false]. Configura se o bot vai falar muito.'
            '\n'
            '    "silent": [true/false]. Configura se as notificações do bot '
            'no '
            'grupo terão som.\n'
            '    "spawn_start_time": inteiro[0-24]. Hora de início do spawn.'
            '\n'
            '    "spawn_end_time": inteiro[0-24]. Hora de fim do spawn.\n'
            '    "multiplier_xp": decimal[0-5]. Multiplicador de XP.\n'
            '    "char_multiplier_xp": decimal[0-10]. Multiplicador do bônus '
            'de '
            'XP baseado no nível do personagem.\n\n'

            'Outros Argumentos:\n'
            '    "default": Retorna a configuração do grupo para o padrão.\n'
            '    "update": Atualiza as informações do grupo.\n\n'

            f'Atalhos: {config_group_cmd}\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'*INFORMAÇÕES DO GRUPO*: /{view_group_commands[0]}\n'
            'INFO: Exibe as informações do grupo.\n\n'

            f'Atalhos: {view_group_cmd}'
        )
    elif option == CALLBACK_PLAYER:
        config_player_cmd = command_to_string(config_player_commands)
        sign_up_player_cmd = command_to_string(sign_up_player_commands)
        view_player_cmd = command_to_string(view_player_commands)
        text = (
            f'*CRIAR CONTA DE JOGADOR*: /{sign_up_player_commands[0]}\n'
            'INFO: Cria uma conta para o jogador.\n\n'

            f'Atalhos: {sign_up_player_cmd}\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'*CONFIGURAÇÃO DO JOGADOR*: /{config_player_commands[0]}\n'
            'Argumentos: [<CONFIGURAÇÃO> <VALOR>]\n\n'

            'Configurações:\n'
            '    "verbose": [true/false]. Configura se o bot vai envia '
            'mensagens privadas para o jogador.\n'
            '    "silent": [true/false]. Configura se as notificações do bot '
            'no chat privado terão som.\n\n'

            'Outros Argumentos:\n'
            '    "default": Retorna a configuração do jogador para o padrão.\n'
            '    "update": Atualiza as informações do jogador.\n\n'

            f'Atalhos: {config_player_cmd}\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'*INFORMAÇÕES DO JOGADOR*: /{view_player_commands[0]}\n'
            'INFO: Exibe as informações do jogador.\n\n'

            f'Atalhos: {view_player_cmd}'
        )
    elif option == CALLBACK_EQUIPS:
        equips_cmd = command_to_string(equips_commands)
        text = (
            f'*EQUIPAMENTOS*: /{equips_commands[0]}\n'
            'INFO: Mostra os equipamentos do personagem.\n\n'

            'OBS: Use o argumento "verbose" ou "v" para exibir os '
            'equipamentos com mais detalhes.\n\n'

            f'Atalhos: {equips_cmd}\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'{EmojiEnum.EQUIPMENT_POWER.value}*PODER*\n\n'
            'O poder de um equipamento é calculado como a soma poderada de '
            'todos os atributos que o equipamento garante. Existem alguns '
            'fatores que influenciam no total de pontos de atributo que um '
            'equipamento vai possuir. Os principais fatores são: '
            '`Nível do Equipamento`, `Tipo do Equipamento`, '
            '`Raridade` e `Material`.\n\n'

            f'{EmojiEnum.EQUIPMENT_LEVEL.value}*NÍVEL DO EQUIPAMENTO*\n\n'

            'O `Nível do Equipamento` é o requisitos que todos os '
            'equipamentos possuem. Personagens com um `Nível` inferior ao '
            '`Nível do Equipamento` não poderão utilizar o equipamento.\n\n'
            'O `Nível do Equipamento` também é a base da distribuição dos '
            'atributos dos equipamentos. Ele será multiplicado pela valor do '
            '`Tipo do Equipamento`, `Raridade` e `Material` para definir '
            'o valor total de pontos que serão distribuídos entre os '
            '`Atributos de Combate` do equipamento.\n\n'

            f'{EmojiEnum.EQUIPS.value}*TIPO DE EQUIPAMENTO*\n\n'

            f'Os tipos de equipamentos são {len(EquipmentEnum)} ao todo. '
            'Cada tipo de equipamento possui um multiplicador diferente.\n'
            'Os tipos de equipamento são:\n'
            f'{EmojiEnum.HELMET.value}`{EquipmentEnum.HELMET.value}` (x0,5), '
            f'{EmojiEnum.ONE_HAND.value}`{EquipmentEnum.ONE_HAND.value}` (x1), '
            f'{EmojiEnum.TWO_HANDS.value}`{EquipmentEnum.TWO_HANDS.value}` (x2,5), '
            f'{EmojiEnum.ARMOR.value}`{EquipmentEnum.ARMOR.value}` (x2,5), '
            f'{EmojiEnum.BOOTS.value}`{EquipmentEnum.BOOTS.value}` (x0,5), '
            f'{EmojiEnum.RING.value}`{EquipmentEnum.RING.value}` (x0,25), '
            f'{EmojiEnum.AMULET.value}`{EquipmentEnum.AMULET.value}` (x0,25).\n\n'

            f'{EmojiEnum.EQUIPMENT_RARITY.value}*RARIDADE*\n\n'

            f'Os tipos de raridade são {len(RarityEnum)} ao todo. '
            'Cada raridade possui um multiplicador diferente. Além disso, '
            f'as raridades acima da `{list(RarityEnum)[1].value}` possuem a '
            'chance de ter `Atributos Ocultos` que precisam ser identificados '
            'para que o personagem possa garantir esses bônus. Esses '
            '`Atributos Ocultos` são pontos extras que podem ser '
            'distribuídos nos `Atributos de Combate` e também nos '
            '`Atributos Base`.\n'
            'As raridades são:\n'
            f'{help_enum(RarityEnum)}.\n\n'

            'Níveis de equipamentos que as raridades começam a aparecer:\n'
            f'Nível 1: {RarityEnum.COMMON.value} e {RarityEnum.UNCOMMON.value}\n'
            f'Nível 50: {RarityEnum.RARE.value}\n'
            f'Nível 500: {RarityEnum.EPIC.value}\n'
            f'Nível 1250: {RarityEnum.LEGENDARY.value}\n'
            f'Nível 2000: {RarityEnum.MYTHIC.value}\n\n'

            f'{EmojiEnum.EQUIPMENT_MATERIAL.value}*MATERIAIS*\n\n'

            'Os materias variam de acordo com o `Tipo do Equipamento` '
            'podendo variar entre equipamentos de um mesmo tipo. '
            'Os materias dos equipamentos são:\n'

            f'*Armas* : {help_enum(WeaponMaterialEnum)}.\n\n'
            f'*Penas* : {help_enum(MagicalQuillMaterialEnum)}.\n\n'
            f'*Grimórios* : {help_enum(MagicalGrimoireMaterialEnum)}.\n\n'
            f'*Pedras Mágicas* : {help_enum(MagicalStonesMaterialEnum)}.\n\n'
            f'*Armas Kajiya* : {help_enum(KajiyaMaterialEnum)}.\n\n'
            f'*Vestes* : {help_enum(WearableMaterialEnum)}.\n\n'
            f'*Vestes Mágicas* : {help_enum(MagicalWearableMaterialEnum)}.\n\n'
            f'*Vestes Seishin* : {help_enum(SeishinWearbleMaterialEnum)}.\n\n'
            f'*Máscaras* : {help_enum(MagicalMaskMaterialEnum)}.\n\n'
            f'*Capas* : {help_enum(TacticalWearableMaterialEnum)}.\n\n'
            f'*Acessórios* : {help_enum(AccessoryMaterialsEnum)}.\n\n'
            f'*Moedas* : {help_enum(CoinMaterialsEnum)}.\n\n'
            f'*Omamori* : {help_enum(OmamoriMaterialEnum)}.\n\n'

            'Níveis de aparição dos Materiais dos Equipamentos:\n'
            '1º: NV 1\n'
            '2º: NV 25\n'
            '3º: NV 100\n'
            '4º: NV 225\n'
            '5º: NV 400\n'
            '6º: NV 625\n'
            '7º: NV 900\n'
            '8º: NV 1225\n'
            '9º: NV 1600\n\n'

            'Níveis de aparição dos Materiais dos Acessórios:\n'
            '1º: NV 1\n'
            '2º: NV 50\n'
            '3º: NV 200\n'
            '4º: NV 450\n'
            '5º: NV 800\n'
            '6º: NV 1250\n\n'
        )
    elif option == CALLBACK_BASE_ATTRIBUTES:
        text = (
            f'{EmojiEnum.BASE_ATTRIBUTES.value}*ATRIBUTOS BASE*\n\n'

            'Os Atributos Base do personagem representam suas '
            'características que vão além do combate. Os seis Atributos Base '
            'são os seguintes:\n\n'

            f'{EmojiEnum.STRENGTH.value}'
            '*Força* (FOR): Representa a força física do personagem. '
            'A força influencia bastante no `Ataque Físico`, moderado nos '
            '`Pontos de Vida` e um pouco no `Ataque de Precisão`.\n\n'

            f'{EmojiEnum.DEXTERITY.value}'
            '*Destreza* (DES): Representa a habilidade e a ligeireza do '
            'personagem. A destreza influencia bastante no '
            '`Ataque de Precisão`, `Acerto` e `Evasão`, possui um pouco de '
            'influência na `Iniciativa`, no `Ataque Físico` e '
            'na `Defesa Física`.\n\n'

            f'{EmojiEnum.CONSTITUTION.value}'
            '*Constituição* (CON): Representa o vigor físico do '
            'personagem e a capacidade de resistir à ataques de qualquer '
            'origem. A contituição influencia bastante nos `Pontos de Vida` '
            'e na `Defesa Física` e na `Defesa Mágica`.\n\n'

            f'{EmojiEnum.INTELLIGENCE.value}'
            '*Inteligência* (INT): Representa a capacidade do personagem '
            'de pensar e aprender coisas por meio de estudo. '
            'A inteligência influencia consideravelmente no '
            '`Ataque Mágico` e na `Defesa Mágica` e um pouco na '
            '`Iniciativa`, no `Acerto` e na `Evasão`.\n\n'

            f'{EmojiEnum.WISDOM.value}'
            '*Sabedoria* (SAB): Representa a capacidade de raciocício '
            'inata e a habilidade de compreender o mundo do personagem. '
            'A sabedoria influencia bastante na `Defesa Mágica` e no '
            '`Ataque Mágico` e tem pouca influência na `Iniciativa`, no '
            '`Acerto` e na `Evasão`.\n\n'

            f'{EmojiEnum.CHARISMA.value}'
            '*Carisma* (CAR): Representa a capacidade do personagem de '
            'inspirar, persuadir, sugestionar ou manipular outras pessoas, '
            'seja de maneira positiva ou negativa. '
            'O carisma influencia bastante na `Iniciativa`, no `Acerto` '
            'e na `Evasão`.'
        )
    elif option == CALLBACK_COMBAT_ATTRIBUTES:
        text = (
            f'{EmojiEnum.COMBAT_ATTRIBUTES.value}*ATRIBUTOS DE COMBATE*\n\n'

            'Os Atributos de Combate do personagem representam suas '
            'habilidades ofensivas e defensivas em lutas. Esses atributos '
            'são diretamente influenciados pelos `Atributos Base` '
            'do personagem. Os nove Atributos de Combate '
            'são os seguintes:\n\n'

            f'{EmojiEnum.HIT_POINT_FULL.value}'
            '*Pontos de Vida (HP)*: Representam a '
            'vitalidade do personagem. Quando os `Pontos de Vida` chegam a '
            'zero o personagem ficará incapacidado até que recupere ao menos '
            'um `Ponto de Vida`.\n'
            'Os Atributos Base que compoem os `Pontos de Vida` são:\n'
            f'A `Constituição`(x{HIT_POINTS_CONSTITUTION}), '
            f'a `Força`(x{HIT_POINTS_STRENGTH}) e '
            f'o `Nível`(x{HIT_POINTS_LEVEL}).\n\n'

            f'{EmojiEnum.INITIATIVE.value}'
            '*Iniciativa*: Representa o quão rápido e sagaz um '
            'personagem é para agir em combate. Quanto maior o valor da '
            '`Iniciativa` em relação a dos demais lutadores, mais a frente o '
            'personagem estará na ordem de ataque.\n'
            'Os Atributos Base que compoem a `Iniciativa` são:\n'
            f'O `Carisma`(x{INITIATIVE_CHARISMA}), '
            f'a `Destreza`(x{INITIATIVE_DEXTERITY}), '
            f'a `Sabedoria`(x{INITIATIVE_WISDOM}), '
            f'a `Inteligência`(x{INITIATIVE_INTELLIGENCE}) e '
            f'o `Nível`(x{GENERAL_LEVEL}).\n\n'

            f'{EmojiEnum.PHYSICAL_ATTACK.value}'
            '*Ataque Físico*: Representa o poder dos '
            'golpes baseados na força física do personagem. Quanto maior o '
            'valor do `Ataque Físico` em relação ao da `Defesa Física` '
            'do alvo, maior será o dano causado aos `Pontos de Vida`.\n'
            'Os Atributos Base que compoem o `Ataque Físico` são:\n'
            f'A `Força`(x{PHYSICAL_ATTACK_STRENGTH}), '
            f'a `Destreza`(x{PHYSICAL_ATTACK_DEXTERITY}) e '
            f'o `Nível`(x{GENERAL_LEVEL}).\n\n'

            f'{EmojiEnum.PRECISION_ATTACK.value}'
            '*Ataque de Precisão*: Representa o '
            'poder dos golpes de visam atingir os pontos vitais do oponente '
            'para causar mais dano sem a necessidade de possuir uma grande '
            'força física. Quanto maior o valor do `Ataque de Precisão` em '
            'relação ao da `Defesa Física` do alvo, maior será o dano '
            'causado aos `Pontos de Vida` do oponente.\n'
            'Os Atributos Base que compoem o `Ataque de Precisão` são:\n'
            f'A `Destreza`(x{PRECISION_ATTACK_DEXTERITY}), '
            f'a `Força`(x{PRECISION_ATTACK_STRENGTH}) e '
            f'o `Nível`(x{GENERAL_LEVEL}).\n\n'

            f'{EmojiEnum.MAGICAL_ATTACK.value}'
            '*Ataque Mágico*: Representa o poder dos '
            'feitiços, magias e quaisquer outras habilidades sobrenaturais '
            'do personagem. Quanto maior o valor do `Ataque Mágico` em '
            'relação ao da `Defesa Mágica` do alvo, maior será o dano '
            'causado aos `Pontos de Vida` do inimigo.\n'
            'Os Atributos Base que compoem o `Ataque Mágico` são:\n'
            f'A `Inteligência`(x{MAGICAL_ATTACK_INTELLIGENCE}), '
            f'a `Sabedoria`(x{MAGICAL_ATTACK_WISDOM}) e '
            f'o `Nível`(x{GENERAL_LEVEL}).\n\n'

            f'{EmojiEnum.PHYSICAL_DEFENSE.value}'
            '*Defesa Física*: Representa a habilidade '
            'que o personagem possui para bloquear o dano de um '
            'golpe físico (aqueles baseados em `Ataque Físico` ou '
            '`Ataque de Precisão`).\n'
            'Os Atributos Base que compoem a `Defesa Física` são:\n'
            f'A `Constituição`(x{PHYSICAL_DEFENSE_CONSTITUTION}), '
            f'a `Destreza`(x{PHYSICAL_DEFENSE_DEXTERITY}) e '
            f'o `Nível`(x{GENERAL_LEVEL}).\n\n'

            f'{EmojiEnum.MAGICAL_DEFENSE.value}'
            '*Defesa Mágica*: Representa a capacidade '
            'que o personagem possui para bloquear o dano oriundo '
            'de ataques sobrenaturais (aqueles baseados em '
            '`Ataque Mágico`).\n'
            'Os Atributos Base que compoem a `Defesa Mágica` são:\n'
            f'A `Sabedoria`(x{MAGICAL_DEFENSE_WISDOM}), '
            f'a `Inteligência`(x{MAGICAL_DEFENSE_INTELLIGENCE}), '
            f'a `Constituição`(x{MAGICAL_DEFENSE_CONSTITUTION}) e '
            f'o `Nível`(x{GENERAL_LEVEL}).\n\n'

            f'{EmojiEnum.HIT.value}'
            '*Acerto*: Representa a perícia que o '
            'personagem possui para ter êxito em atingir um alvo com '
            'os seus ataques. Quanto maior o valor do `Acerto` em relação '
            'ao da `Evasão` do alvo, maior será a chance de acerto.\n'
            'Os Atributos Base que compoem o `Acerto` são:\n'
            f'O `Carisma`(x{HIT_CHARISMA}), '
            f'a `Destreza`(x{HIT_DEXTERITY}), '
            f'a `Inteligência`(x{HIT_INTELLIGENCE}), '
            f'a `Sabedoria`(x{HIT_WISDOM}) e '
            f'o `Nível`(x{GENERAL_LEVEL}).\n\n'

            f'{EmojiEnum.EVASION.value}'
            '*Evasão*: Representa a maestria que o '
            'personagem possui para evitar qualquer ataque. Quanto maior '
            'o valor da `Evasão` em relação ao do `Acerto` do atacante, '
            'maior será a chance de evitar o ataque.\n'
            'Os Atributos Base que compoem o `Evasão` são:\n'
            f'O `Carisma`(x{EVASION_CHARISMA}), '
            f'a `Destreza`(x{EVASION_DEXTERITY}), '
            f'a `Sabedoria`(x{EVASION_WISDOM}), '
            f'a `Inteligência`(x{EVASION_INTELLIGENCE}) e '
            f'o `Nível`(x{GENERAL_LEVEL}).'
        )
    elif option == CALLBACK_SPECIAL_DAMAGE:
        text = (
            f'{EmojiEnum.SPECIAL_DAMAGE.value}*DANO ESPECIAL*\n\n'

            'O `Dano Especial` é um dano adicional que armas e habilidades '
            'podem causar. Para armas, o valor do dano é baseado nos '
            'atributos de ataque da arma e no seu nível. '
            'Já para habilidades, o valor do dano é baseado no *Poder'
            f'{EmojiEnum.EQUIPMENT_POWER.value}*.\n'
            'Além do dano extra, o `Dano Especial` pode causar condições '
            'negativas (*Debuff*).\n\n`Danos Especiais` '
            f'com 100 de *Poder{EmojiEnum.EQUIPMENT_POWER.value}*:\n\n'
        )
        for damage in DamageEnum:
            special_damage = SpecialDamage(
                base_damage=100,
                damage_type=damage,
                equipment_level=100,
            )
            condition_ratio_list = special_damage.condition_ratio_list
            contition_text = '\n'.join([
                (
                    f'    *{condition_dict["condition"]().emoji_name}*: '
                    f'{condition_dict["ratio"]*100}%'
                )
                for condition_dict in condition_ratio_list
            ])
            text += (
                f'*{special_damage.damage_help_emoji_text}*\n'
                f'{contition_text}\n\n'
            )

    elif option == CALLBACK_ITEMS:
        bag_cmd = command_to_string(bag_commands)
        text = (

            f'*BAG (Items)*: /{bag_commands[0]}\n'
            'INFO: Mostra os itens na bolsa do jogador. Para usar itens '
            'consumíveis em outro jogador, passe o arroba dele como '
            'argumento do comando.\n'
            'Argumentos: [Arroba de algum jogador]\n\n'

            'OBS: Se o comando for acionado sem argumentos, os itens serão '
            'usados no próprio jogador. Somente consumíveis podem ser '
            'usados em outros jogadores, os equipamentos serão equipados '
            'no próprio jogador - independente do arroba passado como '
            'argumento.\n\n'

            f'Atalhos: {bag_cmd}\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'{EmojiEnum.ITEMS.value}*ITEMS*\n\n'

            'Os itens são divididos em duas categorias: `Consumíveis` e '
            '`Equipamentos`.\n'
            'Os itens `Consumíveis` são aqueles que o personagem pode usar '
            'somente uma vez, como beber uma poção de cura para recuperar os '
            '`Pontos de Vida`.\n'
            'Os `Equipamentos` são itens que o personagem pode usar para '
            'obter poderes enquanto estiver com ele equipado, como os '
            'pontos de `Ataque Físico` que uma espada pode fornecer ao '
            'personagem.'

        )
    elif option == CALLBACK_DEBUFFS:
        text = (
            f'{EmojiEnum.STATUS.value}*STATUS(DEBUFFS)*\n\n'

            'Debuffs são *Condições* que prejudicam o personagem de diversas '
            'maneiras - como causar dano ou reduzir as estatísticas.\n\n'

            'Os debuffs podem durar uma quantidade fixa de turnos ou por '
            'tempo indeterminado.\n\n'

            'Quando o personagem com um debuff de um tipo recebe novamente '
            'um debuff do mesmo tipo, o número de turnos para se curar '
            'retorna para o valor inicial e o '
            'nível do debuff é aumentado.\n\n'

            'O nível do debuff pode influenciar em quanto de prejuízo '
            'ele ira causar ao personagem ou somente dificultar na cura '
            'por meio de itens.\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            '*LISTA DE DEBUFFS*:\n\n'
        )
        for debuff in ALL_DEBUFFS:
            debuff_name = f'({debuff.enum_name.value})'
            text += f'*Nome*: {debuff.emoji_name} {debuff_name}\n'
            text += f'*Descrição*: {debuff.description}\n\n'
        text = text.strip()
    elif option == CALLBACK_BUFFS:
        text = (
            f'{EmojiEnum.STATUS.value}*STATUS(BUFFS)*\n\n'

            'Buffs são *Condições* que auxiliam o personagem de diversas '
            'maneiras - como curar dano ou aprimorar as estatísticas.\n\n'

            'Os buffs podem durar uma quantidade fixa de turnos ou por '
            'tempo indeterminado.\n\n'

            'Quando o personagem com um buff de um tipo recebe novamente '
            'um mesmo buff, o número de turnos para se perder o benefício '
            'retorna para o valor inicial e o '
            'nível do buff é aumentado.\n\n'

            'O nível do buff irá influenciar em quanto de auxílio '
            'ele ira conceder ao personagem.\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            '*LISTA ALEATÓRIA DE BUFFS (20)*:\n\n'
        )
        for buff in sorted(sample(list(ALL_BUFFS), 20)):
            buff_name = f'({buff.enum_name.value})'
            text += f'*Nome*: {buff.emoji_name} {buff_name}\n'
            text += f'*Descrição*: {buff.description}\n\n'
        text = text.strip()
    elif option == CALLBACK_HEALSTATUS:
        text = (
            f'{EmojiEnum.STATUS.value}*STATUS(CURA)*\n\n'

            '*Condições* de cura recuperam os Pontos de Vida (HP) do '
            'personagem a cada turno.\n\n'

            'Essas *Condições* geralmente são recebidas pelo uso de itens ou '
            'magias de cura durante a batalha, podendo durar alguns '
            'turnos ou por um número indefinido de turnos.\n\n'

            'Fora de batalha, essas *Condições* duram somente um turno, '
            'recebendo a cura de um turno multiplicada pelo total de turnos '
            'faltantes.\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            '*LISTA DE CONDIÇÕES DE CURA*:\n\n'
        )

        for heal_status in HEAL_STATUS:
            text += f'*Nome*: {heal_status.emoji}{heal_status.name}\n'
            text += f'*Descrição*: {heal_status.description}\n\n'
        text = text.strip()
    elif option == CALLBACK_CLASSES:
        classe_model = ClasseModel()
        query = {}
        all_classes = classe_model.get_all(query)
        text = (
            'A classe é a definição principal daquilo que o per­sonagem é '
            'capaz de realizar no cenário mágico e extraor­dinário. '
            'Uma classe é mais que uma profissão; ela é a vocação do seu '
            'personagem. A escolha de classe modelará todas as ações do '
            'herói durante suas aventuras através de um mun­do de fantasia '
            'repleto de magias, assolado por monstros e '
            'imerso em batalhas.\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'{EmojiEnum.CLASSE.value}*CLASSES*: /{classe_commands[0]}\n'
            'Use o argumento *"all"* ou *"a"* para exibir todas as classes.'
            '\n\n'
        )

        keys = attrgetter('name')
        sorted_all_classes = sorted(all_classes, key=keys)
        text += ', '.join([classe.name for classe in sorted_all_classes])
        text = text.strip() + '.'
    elif option == CALLBACK_RACES:
        race_model = RaceModel()
        query = {}
        all_races = race_model.get_all(query)
        text = (
            'Diversas culturas e sociedades povoam o mundo; algumas são '
            'formadas por humanos, mas existem outras que são compostas por '
            'raças fantásticas, como elfos e anões. '
            'Os aventureiros e heróis podem surgir dentre esses vários '
            'povos. A raça escolhida fornece ao personagem um conjunto '
            'básico de vantagens e habilidades especiais. '
            'Se optar por um guerreiro, seu personagem será um anão matador '
            'de monstros muito teimoso, uma graciosa elfa com domínio da '
            'esgrima ou um obstinado gladiador Orque? Caso escolha um mago, '
            'ele será um corajoso humano mercenário ou um astuto Halfling '
            'conjurador? A raça não afeta somente os valores de atributo e '
            'os poderes do personagem, mas também fornece as primeiras '
            'pistas para construir sua história.\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'{EmojiEnum.RACE.value}*RAÇAS*: /{race_commands[0]}\n'
            'Use o argumento *"all"* ou *"a"* para exibir todas as raças.\n\n'
        )

        keys = attrgetter('name')
        sorted_all_races = sorted(all_races, key=keys)
        text += ', '.join([race.name for race in sorted_all_races])
        text = text.strip() + '.'
    elif option == CALLBACK_HEALING_CONSUMABLE:
        item_model = ItemModel()
        query = {'_class': HealingConsumable.__name__}
        all_healing_consumables = item_model.get_all(query)
        text = (
            'Os itens que curam HP desempenham o papel vital de '
            'restaurar a saúde dos personagens. '
            'Esses itens são frequentemente consumíveis ou utilizáveis '
            'e são essenciais para a sobrevivência dos '
            'aventureiros em situações desafiadoras. '
            'Eles são projetados para fornecer uma solução rápida e eficaz '
            'para recuperar pontos de vida perdidos durante combates, '
            'explorações ou outros desafios.\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'{EmojiEnum.HEALING_CONSUMABLE.value}*ITENS DE CURA (HP)*\n\n'
        )

        for healing_consumable in all_healing_consumables:
            text += f'*Nome*: {healing_consumable.name}\n'
            text += f'*Descrição*: {healing_consumable.description}\n'
            text += f'*Raridade*: {healing_consumable.rarity.value}\n\n'
        text = text.strip()
    elif option == CALLBACK_CURE_CONSUMABLE:
        item_model = ItemModel()
        description_pattern = re.compile('^Cura 1 ')
        query = {
            '_class': CureConsumable.__name__,
            'description': description_pattern
        }
        all_cure_consumables = item_model.get_all(query)
        text = (
            'Os itens que curam Condições (Status) negativas atuam na '
            'retirada dos efeitos desfavoráveis que prejudicam o '
            'personagem ao longo do tempo. '
            'Geralmente, esses itens são representados por poções, elixires, '
            'ervas medicinais ou outros recursos mágicos ou alquímicos. '
            'Ao serem utilizados, esse itens diminuem o nível da condição '
            'que é retirada do personagem ao alcançar o nível zero.\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'{EmojiEnum.CURE_CONSUMABLE.value}*Itens de Cura (Status)*\n\n'
        )

        keys = attrgetter('name')
        for cure_consumable in sorted(all_cure_consumables, key=keys):
            text += f'*Nome*: {cure_consumable.name}\n'
            text += f'*Descrição*: {cure_consumable.description}\n'
            text += f'*Raridade*: {cure_consumable.rarity.value}\n\n'
        text = text.strip()
    elif option == CALLBACK_REVIVE_CONSUMABLE:
        item_model = ItemModel()
        query = {'_class': ReviveConsumable.__name__}
        all_revive_consumables = item_model.get_all(query)
        text = (
            'Os itens que revivem personagens exercem um papel crucial ao '
            'proporcionar uma nova chance aos aventureiros que enfrentaram '
            'a morte. Esses itens são frequentemente raros e preciosos, '
            'representando uma oportunidade de trazer de volta à vida um '
            'personagem que foi derrotado em combate ou por circunstâncias '
            'adversas. '
            'Ao serem utilizados, os itens de ressurreição têm o poder de '
            'restaurar um personagem à vida, superando lesões fatais ou '
            'mesmo mortes permanentes.\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'{EmojiEnum.REVIVE_CONSUMABLE.value}*ITENS DE REVIVER*\n\n'
        )

        keys = attrgetter('name')
        for revive_consumable in sorted(all_revive_consumables, key=keys):
            text += f'*Nome*: {revive_consumable.name}\n'
            text += f'*Descrição*: {revive_consumable.description}\n'
            text += f'*Raridade*: {revive_consumable.rarity.value}\n\n'
        text = text.strip()
    elif option == CALLBACK_OTHER_CONSUMABLE:
        item_model = ItemModel()
        query = {'_class': {'$nin': [
            CureConsumable.__name__,
            Equipment.__name__,
            HealingConsumable.__name__,
            ReviveConsumable.__name__,
            TrocadoPouchConsumable.__name__,
            GemstoneConsumable.__name__
        ]}}
        all_other_consumables = item_model.get_all(query)
        text = (
            f'{EmojiEnum.OTHER_CONSUMABLE.value}*OUTROS ITENS*\n\n'
        )

        def keys(x): return (x.__class__.__name__, x.name)
        for other_consumable in sorted(all_other_consumables, key=keys):
            text += f'*Nome*: {other_consumable.name}\n'
            text += f'*Descrição*: {other_consumable.description}\n'
            text += f'*Raridade*: {other_consumable.rarity.value}\n\n'
        text = text.strip()
    elif option == CALLBACK_TROCADOPOUCH_CONSUMABLE:
        item_model = ItemModel()
        query = {'_class': TrocadoPouchConsumable.__name__}
        all_other_consumables = item_model.get_all(query)
        text = (
            f'As {TrocadoEnum.TROCADO_POUCHES.value}'
            f'{EmojiEnum.TROCADO_POUCH.value} '
            'são bolsas especiais projetadas para '
            f'armazenar o {TrocadoEnum.TROCADO.value}'
            f'{EmojiEnum.TROCADO.value}, '
            'a moeda valiosa do jogo. '
            'Essas bolsas são distintas por sua capacidade de armazenar '
            f'diferentes quantidades de {TrocadoEnum.TROCADO.value}'
            f'{EmojiEnum.TROCADO.value}, '
            'dependendo do tipo e '
            'tamanho específicos. Elas podem ser obtidas de baús.\n\n'

            'Existem quatro tipos principais de '
            f'{TrocadoEnum.TROCADO_POUCHES.value}{EmojiEnum.TROCADO_POUCH.value}, '
            'cada um correspondendo a uma hierarquia diferente de valores '
            'monetários. O tipo Tax é a bolsa de menor valor, seguido por '
            'Monarch, Emperor e, no ápice, Overlord.\n\n'

            f'Além disso, as {TrocadoEnum.TROCADO_POUCHES.value}{EmojiEnum.TROCADO_POUCH.value} '
            'também variam em tamanho, '
            'apresentando seis categorias distintas: Tiny, Minor, Normal, '
            'Greater, Major e Superior. Cada tamanho representa a capacidade '
            f'da bolsa de armazenar {TrocadoEnum.TROCADO.value}'
            f'{EmojiEnum.TROCADO.value}, '
            'sendo Tiny a menor e Superior a maior.\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'{EmojiEnum.TROCADO_POUCH.value}*BOLSAS DE TROCADO*\n\n'
        )

        def keys(x): return x.price
        for other_consumable in sorted(all_other_consumables, key=keys):
            text += f'*Nome*: {other_consumable.name}\n'
            text += f'*Descrição*: {other_consumable.description}\n'
            text += f'*Raridade*: {other_consumable.rarity.value}\n\n'
        text = text.strip()
    elif option == CALLBACK_GEMSTONE_CONSUMABLE:
        item_model = ItemModel()
        query = {'_class': GemstoneConsumable.__name__}
        all_other_consumables = item_model.get_all(query)
        text = (
            'As Gemstones, ou Pedras Preciosas, são itens valiosos e '
            'cobiçados no vasto mundo, oferecendo aos aventureiros uma '
            f'fonte de {TrocadoEnum.TROCADOS.value}{EmojiEnum.TROCADO.value} '
            'substancial quando '
            'vendidas. Essas gemas são classificadas em três tamanhos '
            'distintos: Minor, Normal e Greater, representando a raridade '
            'e o valor relativo de cada pedra.\n\n'

            'Dentro de cada categoria de tamanho, as Gemstones são '
            'diferenciadas pelos tipos de pedras preciosas que incorporam. '
            'As variedades incluem Opal, Jadeite, Sapphire, Ruby, Emerald e '
            'Diamond. Cada tipo de pedra possui suas próprias '
            'características únicas, proporcionando uma variedade de '
            'opções aos jogadores que desejam maximizar seus ganhos ao '
            'vender esses itens valiosos.\n\n'

            f'{TEXT_SEPARATOR}\n\n'

            f'{EmojiEnum.GEMSTONE.value}*PEDRAS PRECIOSAS*\n\n'
        )

        def keys(x): return x.price
        for other_consumable in sorted(all_other_consumables, key=keys):
            text += f'*Nome*: {other_consumable.name}\n'
            text += f'*Descrição*: {other_consumable.description}\n'
            text += f'*Raridade*: {other_consumable.rarity.value}\n\n'
        text = text.strip()
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
    base_attributes_text = f'{EmojiEnum.BASE_ATTRIBUTES.value}Atrib. Base'
    combat_attributes_text = (
        f'Atrib. de Combate{EmojiEnum.COMBAT_ATTRIBUTES.value}'
    )
    if option == CALLBACK_BASE_ATTRIBUTES:
        combat_attributes_text = (
            f'{EmojiEnum.COMBAT_ATTRIBUTES.value}Atrib. de Combate'
        )
    special_damage_text = (
        f'Danos Especiais{EmojiEnum.SPECIAL_DAMAGE.value}'
    )
    items_text = f'{EmojiEnum.ITEMS.value}Itens'
    debuffs_text = f'{EmojiEnum.STATUS.value}Debuffs'
    buffs_text = f'Buffs{EmojiEnum.STATUS.value}'
    if option == CALLBACK_DEBUFFS:
        buffs_text = f'{EmojiEnum.STATUS.value}Buffs'
    heal_status_text = f'Cura{EmojiEnum.STATUS.value}'
    general_text = f'Geral{EmojiEnum.GENERAL.value}'
    classes_text = f'{EmojiEnum.CLASSE.value}Classes'
    races_text = f'Raças{EmojiEnum.RACE.value}'
    healing_consumable_text = (
        f'{EmojiEnum.HEALING_CONSUMABLE.value}Itens Cura(HP)'
    )
    cure_consumable_text = (
        f'Itens Cura(Status){EmojiEnum.CURE_CONSUMABLE.value}'
    )
    revive_consumable_text = (
        f'{EmojiEnum.REVIVE_CONSUMABLE.value}Itens Reviver'
    )
    other_consumable_text = (
        f'Outros Itens{EmojiEnum.OTHER_CONSUMABLE.value}'
    )
    trocadopouch_text = (
        f'{EmojiEnum.TROCADO_POUCH.value}Bolsas de Ouro'
    )
    gemstone_text = (
        f'Pedras Preciosas{EmojiEnum.GEMSTONE.value}'
    )

    (
        buttons1,
        buttons2,
        buttons3,
        buttons4,
        buttons5,
        buttons6,
        buttons7,
        buttons8,
        buttons9
    ) = [], [], [], [], [], [], [], [], []
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
    if option != CALLBACK_SPECIAL_DAMAGE:
        buttons3.append(
            InlineKeyboardButton(
                text=special_damage_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_SPECIAL_DAMAGE}",'
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
    if option != CALLBACK_BUFFS:
        buttons6.append(
            InlineKeyboardButton(
                text=buffs_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_BUFFS}","user_id":{user_id}}}'
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
    if option != CALLBACK_HEALING_CONSUMABLE:
        buttons7.append(
            InlineKeyboardButton(
                text=healing_consumable_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_HEALING_CONSUMABLE}",'
                    f'"user_id":{user_id}}}'
                )
            )
        )
    if option != CALLBACK_CURE_CONSUMABLE:
        buttons7.append(
            InlineKeyboardButton(
                text=cure_consumable_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_CURE_CONSUMABLE}",'
                    f'"user_id":{user_id}}}'
                )
            )
        )
    if option != CALLBACK_REVIVE_CONSUMABLE:
        buttons8.append(
            InlineKeyboardButton(
                text=revive_consumable_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_REVIVE_CONSUMABLE}",'
                    f'"user_id":{user_id}}}'
                )
            )
        )
    if option != CALLBACK_OTHER_CONSUMABLE:
        buttons8.append(
            InlineKeyboardButton(
                text=other_consumable_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_OTHER_CONSUMABLE}",'
                    f'"user_id":{user_id}}}'
                )
            )
        )
    if option != CALLBACK_TROCADOPOUCH_CONSUMABLE:
        buttons9.append(
            InlineKeyboardButton(
                text=trocadopouch_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_TROCADOPOUCH_CONSUMABLE}",'
                    f'"user_id":{user_id}}}'
                )
            )
        )
    if option != CALLBACK_GEMSTONE_CONSUMABLE:
        buttons9.append(
            InlineKeyboardButton(
                text=gemstone_text,
                callback_data=(
                    f'{{"option":"{CALLBACK_GEMSTONE_CONSUMABLE}",'
                    f'"user_id":{user_id}}}'
                )
            )
        )

    close_button = [get_close_button(user_id=user_id)]
    reply_markup = InlineKeyboardMarkup([
        buttons1, buttons2, buttons3,
        buttons4, buttons5, buttons6,
        buttons7, buttons8, buttons9,
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


async def job_info_deploy_bot(context: ContextTypes.DEFAULT_TYPE):
    '''Envia mensagem para o grupo informando o deploy e pedindo para usar o
    comando de descanso.
    '''
    print('JOB_INFO_DEPLOY_BOT()')
    job = context.job
    chat_id = job.chat_id
    player_name = get_players_name_by_chat_id(chat_id=chat_id)

    await call_telegram_message_function(
        function_caller='JOB_INFO_DEPLOY_BOT()',
        function=context.bot.send_message,
        context=context,
        need_response=False,
        chat_id=chat_id,
        text=(
            f'{SECTION_HEAD.format("DEPLOYANDO")}\n'
            'Viajantes destemidos, uma atualização mágica acaba de ser '
            'lançada em mim! '
            'Porém, como toda mudança encantada, aqueles que estavam '
            'desfrutando de um merecido descanso foram interrompidos, '
            'por isso todos que estiverem cansandos retomarão o descanso '
            'em breve para renovar suas energias.\n\n'
            f'{" ".join(player_name)}'
        ),
    )


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
