'''
Arquivo principal que executa o telegram-bot.
'''

from datetime import timedelta
from decouple import config

from telegram.ext import Application
from bot.conversations import (
    CREATE_CHAR_HANDLER,
    SIGNUP_GROUP_HANDLER,
    SIGNUP_PLAYER_HANDLER,
    CHAT_XP_HANDLER,
    BATTLE_HANDLER
)
from bot.conversations import (
    HELP_HANDLERS,
    VIEW_GROUP_HANDLERS,
    VIEW_PLAYER_HANDLERS,
    VIEW_CHAR_HANDLERS,
    ADD_STATS_HANDLERS,
    CONFIG_GROUP_HANDLERS,
    CONFIG_PLAYER_HANDLERS,
    REST_HANDLERS,
    TREASURE_HANDLERS
)
from bot.conversations.item import job_create_find_treasure
from function.datetime import get_last_hour

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
MY_GROUP_ID = config('MY_GROUP_ID')


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add Single Handler
    application.add_handler(CREATE_CHAR_HANDLER)
    application.add_handler(SIGNUP_GROUP_HANDLER)
    application.add_handler(SIGNUP_PLAYER_HANDLER)
    application.add_handler(CHAT_XP_HANDLER)
    application.add_handler(BATTLE_HANDLER)

    # Add Multiple Handlers
    application.add_handlers(HELP_HANDLERS)
    application.add_handlers(VIEW_GROUP_HANDLERS)
    application.add_handlers(VIEW_PLAYER_HANDLERS)
    application.add_handlers(VIEW_CHAR_HANDLERS)
    application.add_handlers(ADD_STATS_HANDLERS)
    application.add_handlers(CONFIG_GROUP_HANDLERS)
    application.add_handlers(CONFIG_PLAYER_HANDLERS)
    application.add_handlers(REST_HANDLERS)
    application.add_handlers(TREASURE_HANDLERS)

    # Add Jobs
    application.job_queue.run_repeating(
        callback=job_create_find_treasure,
        interval=timedelta(minutes=30),
        first=get_last_hour(),
        chat_id=MY_GROUP_ID,
        name='JOB_EVENT_TREASURE',
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
