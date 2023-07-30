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
    skip_if_no_have_char,
    skip_if_no_singup_player,
    print_basic_infos,
)
from repository.mongo import BagModel
from rpgram import Bag


@skip_if_no_singup_player
@skip_if_no_have_char
@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bag_model = BagModel()
    player_id = update.effective_user.id
    bag = bag_model.get(player_id)
    if not bag:
        bag = Bag(
            items=[],
            player_id=player_id
        )

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
