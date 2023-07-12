from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

help_button = KeyboardButton("/help")
quiz_button = KeyboardButton("/quiz")
my_id_button = KeyboardButton("/my_id")
random_button = KeyboardButton(f"/random 1 100")
ruletka_button = KeyboardButton("/ruletka")

start_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

start_markup.row(
    help_button,
    quiz_button,
    my_id_button,
    random_button,
    ruletka_button
)