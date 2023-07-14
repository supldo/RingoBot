# Commands
from handlers_group.commands.command_start_button import start_button
from handlers_group.commands.command_help import help_button
from handlers_group.commands.command_quiz import quiz_1, quiz_2, quiz_id, handle_poll_answer
from handlers_group.commands.command_random import random
from handlers_group.commands.command_ruletka import ruletka
from handlers_group.commands.command_user_id import user_id

# Dispatcher
from aiogram import Dispatcher
def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])
    dp.register_message_handler(help_button, commands=['help'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, lambda call: call.data == "button_call_1")
    dp.register_poll_answer_handler(handle_poll_answer)
    dp.register_message_handler(random, commands=['random'])
    dp.register_message_handler(user_id, commands=['my_id'])
    dp.register_message_handler(ruletka, commands=['ruletka'])