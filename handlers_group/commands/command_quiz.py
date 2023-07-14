from config import bot
from aiogram import types
from database.sql_commands import Database
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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


async def quiz_2(call: types.PollAnswer):
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