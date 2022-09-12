from config import *
from extensions import *


def markup_button(base=None):
    values_buttons = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for value in keys.keys():
        if base != value:
            buttons.append(types.KeyboardButton(value.capitalize()))

    values_buttons.add(*buttons)
    return values_buttons


@bot.message_handler(commands=['start', ])
def start_command(message):
    text = f"Приветствую Вас, {message.chat.username}, в боте, который может конвертировать валюту по актуальному" \
           f" на сегодняшний день курсу!💸" \
           "\nЧто бы узнать, как пользоваться ботом, введите /help.❓" \
           "\nЧто бы начать конвертацию, введите /convert.🔁"

    bot.send_message(message.from_user.id, text)


@bot.message_handler(commands=['help', ])
def help_command(message):
    text = "Для конвертации выбирайте нужную валюту из списка.⬇" \
           "\nЧто бы начать конвертацию, введите /convert.🔁"

    bot.reply_to(message, text)


@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = "Выберите валюту, из которой Вы хотите конвертировать:➡"
    bot.send_message(message.from_user.id, text, reply_markup=markup_button())
    bot.register_next_step_handler(message, base_handler)


def base_handler(message: telebot.types.Message):
    base = message.text.strip().lower()
    text = "Выберите валюту, в которую Вы хотите конвертировать:⬅"
    bot.send_message(message.from_user.id, text, reply_markup=markup_button(base))
    bot.register_next_step_handler(message, quot_handler, base)


def quot_handler(message: telebot.types.Message, base):
    quot = message.text.strip()
    text = "Введите количество валюты, которую Вы хотите конвертировать:❓"
    bot.send_message(message.from_user.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quot)


def amount_handler(message: telebot.types.Message, base, quot):
    amount = message.text.strip()
    try:
        correct = Convertation.get_price(base, quot, amount)
    except APIExceptions as e:
        bot.send_message(message.from_user.id, f"Ошибка в конвертации:\n{e}")
    else:
        base_from = reply_from[base.lower()]
        quot_to = reply_to[quot.lower()]
        symbol_from = symbols[base.lower()]
        symbol_to = symbols[quot.lower()]
        text = f"Цена {amount} {base_from} {symbol_from} = {correct} {quot_to} {symbol_to}"
        bot.send_message(message.from_user.id, text)


bot.polling()
