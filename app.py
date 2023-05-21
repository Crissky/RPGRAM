'''
Arquivo principal que executa o telegram-bot.
'''

from decouple import config

from telegram.ext import (
    Application,
)
from bot.conversation import (
    CREATE_CHAR_HANDLER,
    SIGNUP_GROUP_HANDLER,
    SIGNUP_PLAYER_HANDLER,
    CHAT_XP_HANDLER,
)
from bot.conversation import (
    HELP_HANDLERS,
    VIEW_GROUP_HANDLERS,
    VIEW_PLAYER_HANDLERS,
    VIEW_CHAR_HANDLERS,
    ADD_STATS_HANDLERS,
    CONFIG_GROUP_HANDLERS
)

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add Single Handler
    application.add_handler(CREATE_CHAR_HANDLER)
    application.add_handler(SIGNUP_GROUP_HANDLER)
    application.add_handler(SIGNUP_PLAYER_HANDLER)
    application.add_handler(CHAT_XP_HANDLER)

    # Add Multiple Handlers
    application.add_handlers(HELP_HANDLERS)
    application.add_handlers(VIEW_GROUP_HANDLERS)
    application.add_handlers(VIEW_PLAYER_HANDLERS)
    application.add_handlers(VIEW_CHAR_HANDLERS)
    application.add_handlers(ADD_STATS_HANDLERS)
    application.add_handlers(CONFIG_GROUP_HANDLERS)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
