from aiogram import Dispatcher

from handlers_admin.commands.command_list_of_users import list_of_users
from handlers_admin.commands.command_list_potential_user_ban import list_potential_user_ban
from handlers_admin.commands.command_list_user_survey import list_user_survey
from handlers_admin.commands.command_nothing import nothing

def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(list_of_users, lambda call: call.data == "list_of_users")
    dp.register_callback_query_handler(list_potential_user_ban, lambda call: call.data == "list_potential_user_ban")
    dp.register_callback_query_handler(list_user_survey, lambda call: call.data == "list_user_survey")
    dp.register_callback_query_handler(nothing, lambda call: call.data == "nothing")