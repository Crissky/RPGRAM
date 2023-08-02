from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)
from bot.constants.bag import COMMANDS

from bot.constants.filters import (
    BASIC_COMMAND_IN_GROUP_FILTER,
    PREFIX_COMMANDS
)
from bot.decorators import (
    need_not_in_battle,
    print_basic_infos,
    skip_if_no_have_char,
    skip_if_no_singup_player,
)
from bot.functions.general import get_attribute_group_or_player
from repository.mongo import BagModel
from rpgram import Bag


@skip_if_no_singup_player
@skip_if_no_have_char
@need_not_in_battle
@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bag_model = BagModel()
    chat_id = update.effective_chat.id
    player_id = update.effective_user.id
    query = update.callback_query
    silent = get_attribute_group_or_player(chat_id, 'silent')
    bag = bag_model.get(player_id)
    if bag:
        ...
    else:
        bag = Bag(
            items=[],
            player_id=player_id
        )
        bag_model.save(bag)


BAG_HANDLERS = [
    PrefixHandler(
        PREFIX_COMMANDS,
        COMMANDS,
        start,
        BASIC_COMMAND_IN_GROUP_FILTER
    ),
    CommandHandler(
        COMMANDS,
        start,
        BASIC_COMMAND_IN_GROUP_FILTER
    )
]
