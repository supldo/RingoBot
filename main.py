from aiogram.utils import executor
from config import dp
from handlers_group import start, echo_ban
from handlers_group.commands import command_fsm_form
from handlers_admin.commands import command_list_user_survey
from handlers_admin import chat_actions, callback
from database import sql_commands


start.register_handlers_start(dp=dp)
command_fsm_form.register_handler_fsm_form(dp=dp)
chat_actions.register_handlers_chat_actions(dp=dp)
command_list_user_survey.register_handler_load_survey(dp=dp)
callback.register_handlers_callback(dp=dp)
echo_ban.register_handlers_echo_ban(dp=dp)

async def on_startup(_):
    db = sql_commands.Database()
    db.sql_create_db()
    print("Bot is ready!")


if __name__ == "__main__":
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup
                           )
