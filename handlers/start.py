from config import bot
from aiogram import types, Dispatcher
from database.sql_commands import Database
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup


async def start_button(message: types.Message):
    id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    Database().sql_insert_user(id=id,
                               username=username,
                               first_name=first_name,
                               last_name=last_name)

    await message.reply(text=f"Привет {message.from_user.first_name}!")

quiz_id = None

async def quiz_1(message: types.Message):
    global quiz_id
    quiz_id = 'quiz_1'

    question = "Ну тип это опрос 1"
    option = [
        "Вариант А",
        "Правильный вариант",
        "Вариант 3",
        "Что?"
    ]

    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton(
        "Следующая викторина",
        callback_data="button_call_1"
    )
    markup.add(button_call_1)

    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=option,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="Правильный ответ 2",
        explanation_parse_mode=types.ParseMode.MARKDOWN_V2,
        reply_markup=markup
    )

async def quiz_2(call: types.CallbackQuery):
    global quiz_id
    quiz_id = 'quiz_2'

    question = "А тип следующий опрос, верно же?"
    option = [
        "Вариант В",
        "Точно неправильный вариант",
        "А это точно правильный вариант",
        "Да-да, верхниый точно правильный вариант"
    ]

    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=option,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation="Правильный ответ 3",
        explanation_parse_mode=types.ParseMode.MARKDOWN_V2
    )

async def handle_poll_answer(poll_answer: types.PollAnswer):
    Database().sql_insert_answers_quiz(id_user=poll_answer.user.id,
                                       quiz=quiz_id,
                                       quiz_option=poll_answer.option_ids[0])

def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, lambda call: call.data == "button_call_1")
    dp.register_poll_answer_handler(handle_poll_answer)
