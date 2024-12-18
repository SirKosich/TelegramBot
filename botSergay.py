import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import random

# Инициализация бота
bot = telebot.TeleBot('8140993678:AAGwY7ConLogQAws0AdRJ2xJ2PX-Kw44euc')

# Секретные материалы
SECRETS = {
    "Кирилл": "https://www.youtube.com/channel/UCxNF7k50QNKxVcpEQYJMuDQ",
    "12419822": "https://via.placeholder.com/600x400.png?text=Ты+серьезно+поверил%3F"
}

SECRETS2 = [
    "https://sun9-19.userapi.com/impg/_qqhbi2YKDILvdDGRPbl3mejrNyZZjMTLlFNZw/2IdTxfvRz2s.jpg?size=476x682&quality=96&sign=8a38fd0babd13444ca58dd78969027b4&type=album",
    "https://sun9-54.userapi.com/impg/tkvIn6XrdfwLF4fK0BZRz-HC6w4xlu5UOa7Rdg/aPpqMBgpaNQ.jpg?size=189x202&quality=95&sign=b80bb4d4e5c80e47798306acaf13fcfc&type=album"
]

# Функция получения случайного изображения котика
def get_random_cat_image():
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    if response.status_code == 200:
        return response.json()[0]["url"]
    return None

# Главное меню
def get_main_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Список аниме", callback_data="anime_menu"))
    keyboard.add(InlineKeyboardButton(text="Развлечения", callback_data="fun_menu"))
    return keyboard

# Меню "Список аниме"
def get_anime_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Для мальчиков", callback_data="boys_list"))
    keyboard.add(InlineKeyboardButton(text="Для девочек", callback_data="girls_list"))
    keyboard.add(InlineKeyboardButton(text="Вернуться в главное меню", callback_data="back_to_main"))
    return keyboard

# Меню "Развлечения"
def get_fun_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Случайное фото котика", callback_data="random_cat"))
    keyboard.add(InlineKeyboardButton(text="Камень-ножницы-бумага", callback_data="game_kmn"))
    keyboard.add(InlineKeyboardButton(text="Секретные материалы", callback_data="secret_menu"))
    keyboard.add(InlineKeyboardButton(text="Вернуться в главное меню", callback_data="back_to_main"))
    return keyboard

# Клавиатура для возврата
def get_back_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Вернуться в главное меню", callback_data="back_to_main"))
    keyboard.add(InlineKeyboardButton(text="Вернуться назад", callback_data="fun_menu"))
    return keyboard

# Стартовая команда
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Выберите, что хотите сделать:",
        reply_markup=get_main_menu()
    )

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)

        if call.data == "back_to_main":
            bot.send_message(call.message.chat.id, "Вы вернулись в главное меню!", reply_markup=get_main_menu())

        elif call.data == "anime_menu":
            bot.send_message(call.message.chat.id, "Выберите категорию аниме:", reply_markup=get_anime_menu())

        elif call.data == "boys_list":
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text="Вернуться в главное меню", callback_data="back_to_main"))
            keyboard.add(InlineKeyboardButton(text="Вернуться назад", callback_data="anime_menu"))
            bot.send_message(
                call.message.chat.id,
                "Список аниме для мальчиков:\n1. Всегда вялый Танака-кун\n2. Полёт ведьмы\n3. Ох уж этот экстрасенс Сайки Кусуо!\n4. Сильнейший в истории ученик Кэнъити\n5. Selector Infected WIXOSS\n6. Horizon in the Middle of Nowhere\n7. Моя геройская академия\n8. Вторжение Кальмарки\n9. Баракамон\n10. Академия ведьмочек",
                reply_markup=keyboard
            )

        elif call.data == "girls_list":
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text="Вернуться в главное меню", callback_data="back_to_main"))
            keyboard.add(InlineKeyboardButton(text="Вернуться назад", callback_data="anime_menu"))
            bot.send_message(
                call.message.chat.id,
                "Список аниме для девочек:\n1. Красноволосая принцесса Белоснежка\n2. Деревенская глубинка\n3. Клетки за работой\n4. Алиса и Зороку\n5. Реальная девушка\n6. Как и ожидалось, моя школьная романтическая жизнь не удалась\n7. Не моя вина, что я не популярна!\n8. Притворная любовь\n9. Жизнь не в одиночку\n10. Золотая пора",
                reply_markup=keyboard
            )

        elif call.data == "fun_menu":
            bot.send_message(call.message.chat.id, "Выберите развлечение:", reply_markup=get_fun_menu())

        elif call.data == "random_cat":
            cat_image = get_random_cat_image()
            if cat_image:
                bot.send_photo(call.message.chat.id, cat_image, reply_markup=get_fun_menu())
            else:
                bot.send_message(call.message.chat.id, "Не удалось загрузить котика. Попробуйте снова!", reply_markup=get_fun_menu())

        elif call.data == "secret_menu":
            bot.send_message(call.message.chat.id, "Введите пароль:")

        elif call.data == "game_kmn":
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text="Камень", callback_data="kmn_rock"))
            keyboard.add(InlineKeyboardButton(text="Бумага", callback_data="kmn_paper"))
            keyboard.add(InlineKeyboardButton(text="Ножницы", callback_data="kmn_scissors"))
            keyboard.add(InlineKeyboardButton(text="Вернуться в меню развлечений", callback_data="fun_menu"))
            bot.send_message(call.message.chat.id, "Сыграем? Выберите:", reply_markup=keyboard)

        elif call.data.startswith("kmn_"):
            user_choice = call.data.split("_")[1]
            bot_choice = random.choice(["rock", "paper", "scissors"])
            choices = {"rock": "Камень", "paper": "Бумага", "scissors": "Ножницы"}

            if user_choice == bot_choice:
                result = "Ничья!"
            elif (user_choice == "rock" and bot_choice == "scissors") or \
                 (user_choice == "scissors" and bot_choice == "paper") or \
                 (user_choice == "paper" and bot_choice == "rock"):
                result = "Вы победили!"
            else:
                result = "Вы проиграли!"

            bot.send_message(
                call.message.chat.id,
                f"Вы выбрали: {choices[user_choice]}\nБот выбрал: {choices[bot_choice]}\n{result}",
                reply_markup=get_fun_menu()
            )

    except Exception as e:
        print(f"Ошибка: {e}")

# Обработка ввода пароля
@bot.message_handler(func=lambda message: True)
def handle_password(message):
    password = message.text
    if password in SECRETS:
        if password == "Кирилл":
            bot.send_message(message.chat.id, f"Секретный материал
