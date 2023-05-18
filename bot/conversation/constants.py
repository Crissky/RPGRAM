from telegram import MessageEntity
from telegram.ext import filters

PREFIX_COMMANDS = ['!']
BASIC_COMMAND_FILTER = (
    ~filters.FORWARDED &
    ~filters.UpdateType.EDITED &
    ~filters.Entity(MessageEntity.URL) &
    ~filters.Entity(MessageEntity.TEXT_LINK)
)
ALLOW_WRITE_TEXT_IN_GROUP_FILTER = (
    filters.TEXT &
    filters.ChatType.GROUPS &
    ~filters.COMMAND &
    ~filters.FORWARDED &
    ~filters.UpdateType.EDITED &
    ~filters.Regex('^!')
)