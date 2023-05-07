from decouple import config

from telegram.ext import (
    Application,
)
from bot.conversation import (
    SIGNUP_PLAYER_HANDLER,
    SIGNUP_GROUP_HANDLER
)

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(SIGNUP_PLAYER_HANDLER)
    application.add_handler(SIGNUP_GROUP_HANDLER)
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
