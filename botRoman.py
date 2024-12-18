import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

bot = telebot.TeleBot('8010183493:AAF0H8AMCSYIwKjaNVP9DFtynJU5vZcL8HQ')


# Главное меню
def get_main_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Собачки", callback_data="sob"))
    keyboard.add(InlineKeyboardButton(text="Котики", callback_data="kot"))
    keyboard.add(InlineKeyboardButton(text="Хомяки", callback_data="ham"))
    keyboard.add(InlineKeyboardButton(text="Обо мне", callback_data="about"))
    keyboard.add(InlineKeyboardButton(text="О Wisp", callback_data="wisp"))
    keyboard.add(InlineKeyboardButton(text="Предметы", callback_data="items"))
    return keyboard


# Клавиатуры для разделов
def get_items_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Даэдалус", callback_data="daedalus"))
    keyboard.add(InlineKeyboardButton(text="Сатаник", callback_data="satanic"))
    keyboard.add(InlineKeyboardButton(text="Тараска", callback_data="tarrasque"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_main"))
    return keyboard


def get_wisp_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Лор Wisp", callback_data="lor_wisp"))
    keyboard.add(InlineKeyboardButton(text="Кто такие Предвечные", callback_data="predv"))
    keyboard.add(InlineKeyboardButton(text="Кто такой Puck", callback_data="puck"))
    keyboard.add(InlineKeyboardButton(text="Кто такой Elder Titan", callback_data="elder"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_main"))
    return keyboard


def get_animal_menu(animal_type):
    keyboard = InlineKeyboardMarkup()
    if animal_type == "ham":
        keyboard.add(InlineKeyboardButton(text="Хомяк", callback_data="hamst"))
    elif animal_type == "sob":
        keyboard.add(InlineKeyboardButton(text="Собачка", callback_data="sobachka"))
        keyboard.add(InlineKeyboardButton(text="Случайная собачка", callback_data="sobaka"))
    elif animal_type == "kot":
        keyboard.add(InlineKeyboardButton(text="Котик", callback_data="kotek"))
        keyboard.add(InlineKeyboardButton(text="Случайный котик", callback_data="kotik"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_main"))
    return keyboard


# Хэндлеры
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Выберите, что хотите сделать:",
        reply_markup=get_main_menu()
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)

        if call.data == "back_to_main":
            bot.send_message(call.message.chat.id, "Вы вернулись в главное меню!", reply_markup=get_main_menu())

        elif call.data == "about":
            bot.send_message(call.message.chat.id, "Привет! Меня зовут Роман, мне 14 лет. Моя любимая игра — Dota 2, и я обожаю Wisp!")

        elif call.data in ["sob", "kot", "ham"]:
            bot.send_message(call.message.chat.id, f"Выберите {call.data}:", reply_markup=get_animal_menu(call.data))

        elif call.data == "kotik":
            response = requests.get("https://api.thecatapi.com/v1/images/search")
            if response.status_code == 200:
                data = response.json()
                bot.send_photo(call.message.chat.id, data[0]["url"])
            else:
                bot.send_message(call.message.chat.id, "Не удалось получить котика 🐱")

        elif call.data == "sobaka":
            response = requests.get("https://dog.ceo/api/breeds/image/random")
            if response.status_code == 200:
                data = response.json()
                bot.send_photo(call.message.chat.id, data["message"])
            else:
                bot.send_message(call.message.chat.id, "Не удалось получить собачку 🐶")

        elif call.data == "hamst":
            bot.send_animation(
                call.message.chat.id,
                "https://media.tenor.com/9RCIDZjkhBsAAAAM/hamster-meme.gif"
            )

        elif call.data == "items":
            bot.send_message(call.message.chat.id, "Выберите предмет:", reply_markup=get_items_menu())

        elif call.data == "wisp":
            bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=get_wisp_menu())

        # Лор, предметы, и другие описания
        elif call.data in ["daedalus", "satanic", "tarrasque", "lor_wisp", "predv", "puck", "elder"]:
            descriptions = {
                "daedalus": "Даэдалус — легендарный артефакт...",
                "satanic": "Сатаник — воплощение тёмной магии...",
                "tarrasque": "Тараска — символ стойкости...",
                "lor_wisp": "Wisp — это сущность вселенной...",
                "predv": "Предвечные — изначальные сущности...",
                "puck": "Puck — волшебный дракончик...",
                "elder": "Elder Titan — создатель вселенной..."
            }
            bot.send_message(call.message.chat.id, descriptions[call.data])

    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(call.message.chat.id, "Произошла ошибка, попробуйте снова.")

bot.polling(none_stop=True)
