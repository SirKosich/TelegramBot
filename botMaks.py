import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

bot = telebot.TeleBot('Ваш_Токен_Бота')

# Секретные материалы
SECRETS = {
    "Кирилл": "https://www.youtube.com/channel/UCxNF7k50QNKxVcpEQYJMuDQ",
    "12419822": "https://via.placeholder.com/600x400.png?text=Ты+серьезно+поверил%3F"
}

SECRETS2 = [
    "https://sun9-19.userapi.com/impg/_qqhbi2YKDILvdDGRPbl3mejrNyZZjMTLlFNZw/2IdTxfvRz2s.jpg?size=476x682&quality=96&sign=8a38fd0babd13444ca58dd78969027b4&type=album",
    "https://sun9-54.userapi.com/impg/tkvIn6XrdfwLF4fK0BZRz-HC6w4xlu5UOa7Rdg/aPpqMBgpaNQ.jpg?size=189x202&quality=95&sign=b80bb4d4e5c80e47798306acaf13fcfc&type=album"
]

# Получение случайного изображения котика
def get_random_cat_image():
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    if response.status_code == 200:
        return response.json()[0]["url"]
    return None

# Главное меню
def get_main_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Лор Subnautica", callback_data="subnautica_menu"))
    keyboard.add(InlineKeyboardButton(text="Существа Subnautica", callback_data="fun_menu"))
    return keyboard

# Меню "Существа Subnautica"
def get_fun_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Ghost Leviathan", callback_data="ghost_leviathan"))
    keyboard.add(InlineKeyboardButton(text="Reaper Leviathan", callback_data="reaper_leviathan"))
    keyboard.add(InlineKeyboardButton(text="Sea Dragon", callback_data="sea_dragon"))
    keyboard.add(InlineKeyboardButton(text="Вернуться в главное меню", callback_data="back_to_main"))
    return keyboard

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Добро пожаловать в мир Subnautica. Выберите, что хотите узнать:",
        reply_markup=get_main_menu()
    )

# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)

        if call.data == "back_to_main":
            bot.send_message(call.message.chat.id, "Вы вернулись в главное меню!", reply_markup=get_main_menu())

        elif call.data == "subnautica_menu":
            bot.send_message(
                call.message.chat.id,
                "Лор Subnautica: события игры происходят на планете 4546B. Трансгосударство Alterra отправило корабль Aurora на исследование планеты, но он терпит крушение. "
                "На планете присутствуют биомы, такие как Безопасные отмели, Лес водорослей, Поле утёсов, Зона кровавых водорослей, Мёртвая зона и другие. "
                "Дальнейшая судьба — в руках игрока.",
                reply_markup=get_main_menu()
            )

        elif call.data == "fun_menu":
            bot.send_message(call.message.chat.id, "Выберите существо:", reply_markup=get_fun_menu())

        elif call.data == "ghost_leviathan":
            bot.send_message(
                call.message.chat.id,
                "Ghost Leviathan — одно из самых опасных существ в Subnautica. Он обитает в Дюнах, Тропе морских топтунов и Мёртвой зоне. Огромный и агрессивный.",
                reply_markup=get_fun_menu()
            )

        elif call.data == "reaper_leviathan":
            bot.send_message(
                call.message.chat.id,
                "Reaper Leviathan — агрессивное существо, которое можно встретить в Зоне кровавых водорослей и на границах биомов. Его рык слышен издалека.",
                reply_markup=get_fun_menu()
            )

        elif call.data == "sea_dragon":
            bot.send_message(
                call.message.chat.id,
                "Sea Dragon Leviathan — огромное существо, встречающееся в Лавовом замке. Оно может дышать огнём и атаковать игрока с большого расстояния.",
                reply_markup=get_fun_menu()
            )

    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка: {str(e)}")

# Запуск бота
bot.polling(none_stop=True)
