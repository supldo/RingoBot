from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

help_button = KeyboardButton("Помощь")
wallet_button = KeyboardButton("Кошелёк")
referrals_button = KeyboardButton("Список рефералов")
reference_button = KeyboardButton("Реферальная ссылка")
random_button = KeyboardButton("Случайное число от 1 до 100")
quiz_button = KeyboardButton("QUIZ")
ruletka_button = KeyboardButton("Русская рулетка")

start_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_markup.row(help_button, wallet_button, referrals_button, reference_button)
start_markup.add(random_button, quiz_button, ruletka_button)
