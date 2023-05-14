from telegram import MessageEntity
from telegram.ext import filters

PREFIX_COMMANDS = ['!']
BASIC_COMMAND_FILTER = (
    ~filters.FORWARDED &
    ~filters.UpdateType.EDITED &
    ~filters.Entity(MessageEntity.URL) &
    ~filters.Entity(MessageEntity.TEXT_LINK)
)
