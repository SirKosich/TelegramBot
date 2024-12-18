import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import random

# Создание бота
bot = telebot.TeleBot('7344785563:AAGzxBgrcWgSwYKtLfEVHHU')

# Секретные материалы
SECRETS = {
    "Катя": "https://cdn.monetnik.ru/storage/market-lot/48/63/155048/498535_mainViewLot_2x.jpg",
    "15112009": "https://vk.com/photo739573592_457239294",
    "hippo": "https://vk.com/photo739573592_457239293",
    "Дура": "https://vk.com/photo739573592_457239297",
    "Казань": "https://vk.com/photo739573592_457239295",
    "Сбодуненко": "https://vk.com/photo739573592_457239296",
    "Капибара": "https://vk.com/photo739573592_457239300",
    "Томми гёрл": "https://vk.com/photo739573592_457239298",
    "wait": "https://vk.com/photo739573592_457239299"
}

SECRETS2 = [
    "https://assets.pinterest.com/ext/embed.html?id=581245895693413521",
    "https://assets.pinterest.com/ext/embed.html?id=303711568638752672"
]

PHOTO_LINKS = [
    "https://sun9-9.userapi.com/impg/2gbzzAePztBauEJemm9jia-SKQE6O1-OE6ICUg/wV5alygIPt0.jpg?size=656x928&quality=96&sign=800c9593ac8084f3649a872d939e548d&type=album",
    "https://sun4-21.userapi.com/impg/NlfyFJy5LxoSefrC1q46gLBIPhJ-ATCn0eK4Aw/FEHP2_16U-A.jpg?size=810x1080&quality=95&sign=944bbbda3fc622e873c025024a398ce9&type=album",
    "https://sun4-22.userapi.com/impg/-XVpzjeGAZ8TzMEvcfih-1QzIcsOAeJSm6ZYFA/WssY2uBXSWk.jpg?size=1120x940&quality=95&sign=7e4a1dfe41bb87d93f7965ea44c04c29&type=album",
    "https://sun9-45.userapi.com/impg/iS-Fk7Y72vP7adfXhP-cIHfTZeLmxAGkFQfyGg/hRz_jVg1yrE.jpg?size=1280x960&quality=95&sign=1399b5b45bacdb58537ca747747cadeb&type=album",
    "https://sun4-22.userapi.com/impg/AaWDVh8G2a-McisB3MNHN1sm-aKlllQo2wVldw/wUS4-AMDx94.jpg?size=809x1080&quality=95&sign=b2969fb5afbc87562ebaf67cac6a42db&type=album"
]

# Функция для получения случайной картинки кота
def get_random_cat_image():
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    if response.status_code == 200:
        return response.json()[0]["url"]
    return None

# Главное меню
def get_main_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Истории про моих друзей", callback_data="stories_about_friends_menu"))
    keyboard.add(InlineKeyboardButton(text="Обо мне", callback_data="about_me_menu"))
    keyboard.add(InlineKeyboardButton(text="Я не знал куда поместить эти фотографии!", callback_data="photo_gallery"))
    return keyboard

# Меню "Обо мне"
def get_about_me_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Случайная фотка кота", callback_data="random_cat"))
    keyboard.add(InlineKeyboardButton(text="Информация обо мне", callback_data="Katya_menu"))
    keyboard.add(InlineKeyboardButton(text="Секретные материалы", callback_data="secret_menu"))
    keyboard.add(InlineKeyboardButton(text="Вернуться в главное меню", callback_data="back_to_main"))
    return keyboard

# Меню "Истории про моих друзей"
def get_stories_about_friends_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Маша", callback_data="Masha_storie"))
    keyboard.add(InlineKeyboardButton(text="Даша Клеймёнова", callback_data="DashaKleimenova_storie"))
    keyboard.add(InlineKeyboardButton(text="Даша Казанцева", callback_data="DashaKazanceva_storie"))
    keyboard.add(InlineKeyboardButton(text="Аня", callback_data="Anya_storie"))
    keyboard.add(InlineKeyboardButton(text="Стёпа", callback_data="Stepa_storie"))
    keyboard.add(InlineKeyboardButton(text="Радик", callback_data="Radik_storie"))
    keyboard.add(InlineKeyboardButton(text="Вернуться в главное меню", callback_data="back_to_main"))
    return keyboard

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Хай. Выберите, что хотите сделать:", reply_markup=get_main_menu())

# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "back_to_main":
        bot.send_message(call.message.chat.id, "Вы вернулись в главное меню!", reply_markup=get_main_menu())

    elif call.data == "stories_about_friends_menu":
        bot.send_message(call.message.chat.id, "Выберите историю, которую хотите прочитать:", reply_markup=get_stories_about_friends_menu())

    elif call.data == "about_me_menu":
        bot.send_message(call.message.chat.id, "Выберите, что хотите узнать:", reply_markup=get_about_me_menu())

    elif call.data == "random_cat":
        cat_image = get_random_cat_image()
        if cat_image:
            bot.send_photo(call.message.chat.id, cat_image, reply_markup=get_about_me_menu())
        else:
            bot.send_message(call.message.chat.id, "Не удалось загрузить мем. Попробуйте снова!", reply_markup=get_about_me_menu())

    elif call.data == "Katya_menu":
        bot.send_message(
            call.message.chat.id,
            "История обо мне:\nЯ 15-летняя школьница. По знаку зодиака скорпион. Я увлекаюсь программированием и мечтаю жить у моря!",
            reply_markup=get_about_me_menu()
        )

    elif call.data == "photo_gallery":
        for photo in PHOTO_LINKS:
            bot.send_photo(call.message.chat.id, photo, reply_markup=get_main_menu())

    elif call.data == "secret_menu":
        bot.send_message(call.message.chat.id, "Введите пароль:")

# Обработчик текстовых сообщений (пароли)
@bot.message_handler(func=lambda message: True)
def handle_password(message):
    password = message.text
    if password in SECRETS:
        bot.send_photo(message.chat.id, SECRETS[password], reply_markup=get_main_menu())
    else:
        bot.send_message(message.chat.id, "Неверный пароль! Попробуйте снова.")

# Запуск бота
bot.polling(none_stop=True)
