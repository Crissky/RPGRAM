'''Arquivo principal que executa o telegram-bot.
'''

from datetime import datetime, time, timedelta
from decouple import config

from telegram.ext import Application
from bot.constants.job import BASE_JOB_KWARGS
from bot.conversations import (
    CREATE_CHAR_HANDLER,
    SIGNUP_GROUP_HANDLER,
    SIGNUP_PLAYER_HANDLER,
    CHAT_XP_HANDLER,
    BAG_HANDLER,
    CLOSE_MSG_HANDLER,
    SELLER_HANDLER,
    ITEM_QUEST_HANDLER,
)
from bot.conversations import (
    HELP_HANDLERS,
    VIEW_GROUP_HANDLERS,
    VIEW_LEVEL_HANDLERS,
    VIEW_PLAYER_HANDLERS,
    VIEW_CHAR_HANDLERS,
    ADD_STATS_HANDLERS,
    CONFIG_GROUP_HANDLERS,
    CONFIG_PLAYER_HANDLERS,
    REST_HANDLERS,
    TREASURE_HANDLERS,
    VIEW_EQUIPS_HANDLERS,
    DROP_HANDLERS,
    DEBUG_HANDLERS,
    RACES_HANDLERS,
    CLASSES_HANDLERS,
    AMBUSH_HANDLERS,
    PUZZLE_HANDLERS,
    RESET_CHAR_HANDLERS,
    WORDGAME_HANDLERS,
    PICROSS_HANDLERS,
)
from bot.conversations import SEASON_JOBS_DEFINITIONS
from bot.conversations.event import job_add_event_points
from bot.conversations.help import job_info_deploy_bot
from bot.conversations.progress_year import show_percent_today
from bot.conversations.rest import autorest_midnight
from bot.conversations.seller import job_create_new_items
from bot.conversations.skill_tree import SKILL_TREE_HANDLERS
from bot.conversations.status import job_activate_conditions
from function.date_time import (
    adjust_season_datetime,
    brazil_to_utc_datetime,
    get_last_hour,
    get_midnight_hour
)


TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
MY_GROUP_ID = config('MY_GROUP_ID', cast=int)
(
    DEFAULT_GROUP,
    CHAT_XP_GROUP,
    WORDGAME_GROUP,
) = range(3)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add Single Handler
    application.add_handler(CREATE_CHAR_HANDLER)
    application.add_handler(SIGNUP_GROUP_HANDLER)
    application.add_handler(SIGNUP_PLAYER_HANDLER)
    application.add_handler(CHAT_XP_HANDLER, group=CHAT_XP_GROUP)
    application.add_handler(BAG_HANDLER)
    application.add_handler(CLOSE_MSG_HANDLER)
    application.add_handler(SELLER_HANDLER)
    application.add_handler(ITEM_QUEST_HANDLER)

    # Add Multiple Handlers
    application.add_handlers(HELP_HANDLERS)
    application.add_handlers(VIEW_GROUP_HANDLERS)
    application.add_handlers(VIEW_LEVEL_HANDLERS)
    application.add_handlers(VIEW_PLAYER_HANDLERS)
    application.add_handlers(VIEW_CHAR_HANDLERS)
    application.add_handlers(ADD_STATS_HANDLERS)
    application.add_handlers(CONFIG_GROUP_HANDLERS)
    application.add_handlers(CONFIG_PLAYER_HANDLERS)
    application.add_handlers(REST_HANDLERS)
    application.add_handlers(TREASURE_HANDLERS)
    application.add_handlers(VIEW_EQUIPS_HANDLERS)
    application.add_handlers(DROP_HANDLERS)
    application.add_handlers(DEBUG_HANDLERS)
    application.add_handlers(RACES_HANDLERS)
    application.add_handlers(CLASSES_HANDLERS)
    application.add_handlers(AMBUSH_HANDLERS)
    application.add_handlers(PUZZLE_HANDLERS)
    application.add_handlers(RESET_CHAR_HANDLERS)
    application.add_handlers(SKILL_TREE_HANDLERS)
    application.add_handlers(WORDGAME_HANDLERS)
    application.add_handlers(PICROSS_HANDLERS)

    # Add Jobs
    application.job_queue.run_repeating(
        callback=job_activate_conditions,
        interval=timedelta(minutes=20),
        first=get_last_hour(),
        chat_id=MY_GROUP_ID,
        name='JOB_ACTIVATE_CONDITIONS',
        job_kwargs=BASE_JOB_KWARGS,
    )
    application.job_queue.run_repeating(
        callback=autorest_midnight,
        interval=timedelta(hours=12),
        first=get_midnight_hour(get_yesterday=True),
        chat_id=MY_GROUP_ID,
        name='JOB_AUTOREST_MIDNIGHT',
        job_kwargs=BASE_JOB_KWARGS,
    )
    application.job_queue.run_once(
        callback=job_info_deploy_bot,
        when=timedelta(minutes=1),
        chat_id=MY_GROUP_ID,
        name='JOB_INFO_DEPLOY_BOT',
        job_kwargs=BASE_JOB_KWARGS,
    )
    application.job_queue.run_repeating(
        callback=job_create_new_items,
        interval=timedelta(hours=8),
        first=get_midnight_hour(get_yesterday=True),
        chat_id=MY_GROUP_ID,
        name='JOB_CREATE_NEW_ITEMS',
        job_kwargs=BASE_JOB_KWARGS,
    )
    application.job_queue.run_once(
        callback=autorest_midnight,
        when=timedelta(minutes=1),
        chat_id=MY_GROUP_ID,
        name='JOB_AUTOREST_MIDNIGHT_ON_START',
        job_kwargs=BASE_JOB_KWARGS,
    )
    application.job_queue.run_repeating(
        callback=job_add_event_points,
        interval=timedelta(minutes=20),
        first=get_last_hour(),
        chat_id=MY_GROUP_ID,
        name='JOB_ADD_EVENT_POINTS',
        job_kwargs=BASE_JOB_KWARGS,
    )
    application.job_queue.run_once(
        callback=job_add_event_points,
        when=timedelta(minutes=1),
        chat_id=MY_GROUP_ID,
        name='JOB_ADD_EVENT_POINTS_ON_START',
        job_kwargs=BASE_JOB_KWARGS,
    )
    application.job_queue.run_daily(
        callback=show_percent_today,
        time=time(8+3),
        name='SHOW_PERCENT_TODAY',
        chat_id=MY_GROUP_ID,
        job_kwargs=BASE_JOB_KWARGS,
    )

    print('APP().DATETIME.NOW()', datetime.now())
    for job_definition in SEASON_JOBS_DEFINITIONS:
        job_name = job_definition['callback'].__name__.upper()
        
        raw_when = job_definition['when']
        print(f'SEASON JOB BRAZIL TIME: {job_name} - "{raw_when}"')

        when = adjust_season_datetime(raw_when)
        print(f'SEASON JOB ADJUST TIME: {job_name} - "{when}"')

        when = brazil_to_utc_datetime(when)
        print(f'SEASON JOB UTC TIME: {job_name} - "{when}"')

        print(f'SEASON JOB: {job_name} - "{raw_when}" -> "{when}"')
        print()
        application.job_queue.run_once(
            callback=job_definition['callback'],
            when=when,
            chat_id=MY_GROUP_ID,
            name=job_name,
            job_kwargs=BASE_JOB_KWARGS
        )

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
