'''
Arquivo principal que executa o telegram-bot.
'''

from decouple import config

from telegram.ext import (
    Application,
)
from bot.conversation import (
    CREATE_CHAR_HANDLER,
    HELP_HANDLER,
    SIGNUP_GROUP_HANDLER,
    SIGNUP_PLAYER_HANDLER,
)

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CREATE_CHAR_HANDLER)
    application.add_handler(HELP_HANDLER)
    application.add_handler(SIGNUP_GROUP_HANDLER)
    application.add_handler(SIGNUP_PLAYER_HANDLER)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
