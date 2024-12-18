import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Конфигурация для Telethon
API_ID = "ВАШ_API_ID"  # Замените на ваш API ID
API_HASH = "ВАШ_API_HASH"  # Замените на ваш API Hash
CHANNEL_USERNAME = "myfavoritejumoreski"  # Юзернейм канала
telethon_client = TelegramClient("anon", API_ID, API_HASH)

# Словарь с каталогом
catalog = {
    'item1': 'Тайлер Дерден — это только начало!',
    'item2': 'Сигма статус: плохо, но красиво.',
    'item3': 'Деды в деле: дедлайн близок.',
}

# Подключение к Telethon
async def fetch_random_post():
    """Получает случайный пост из указанного Telegram-канала."""
    try:
        await telethon_client.start()
        history = await telethon_client(GetHistoryRequest(
            peer=CHANNEL_USERNAME,
            limit=100,  # Получить 100 последних сообщений
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))
        messages = history.messages
        if messages:
            random_message = random.choice(messages)
            if random_message.message:  # Если текстовое сообщение
                return random_message.message
            elif random_message.media:  # Если есть медиа (фото/видео)
                return random_message
        return "Не удалось найти сообщения в канале."
    except Exception as e:
        logging.error(f"Ошибка при получении сообщения из канала: {e}")
        return "Произошла ошибка при получении поста из канала."

# Стартовое меню
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Каталог", callback_data="catalog")],
        [InlineKeyboardButton("Случайный пост", callback_data="random_post")],
        [InlineKeyboardButton("Вернуться в главное меню", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Привет! Выберите действие:", reply_markup=reply_markup)

def catalog_command(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton(item, callback_data=item) for item in catalog.keys()]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите лакомку:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data in catalog:
        description = catalog.get(query.data, "Описание недоступно.")
        query.edit_message_text(text=f"{query.data}: {description}")
    
    elif query.data == "random_post":
        post = context.bot_data.get("last_post", "Попробуйте ещё раз!")
        keyboard = [
            [InlineKeyboardButton("Следующий пост", callback_data="next_post")],
            [InlineKeyboardButton("Вернуться в главное меню", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text=f"Случайный пост:\n\n{post}", reply_markup=reply_markup)

    elif query.data == "next_post":
        post = context.bot_data.get("next_post", "Попробуйте ещё раз!")
        keyboard = [
            [InlineKeyboardButton("Следующий пост", callback_data="next_post")],
            [InlineKeyboardButton("Вернуться в главное меню", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text=f"Следующий пост:\n\n{post}", reply_markup=reply_markup)

    elif query.data == "main_menu":
        start(query.message, context)

    else:
        query.edit_message_text(text="Я не понял вашего запроса. Попробуйте ещё раз.")

async def update_posts(context: CallbackContext):
    """Обновляет случайные посты из канала."""
    post = await fetch_random_post()
    context.bot_data["last_post"] = post
    context.bot_data["next_post"] = await fetch_random_post()

def main() -> None:
    """Запуск бота."""
    updater = Updater("ВАШ_ТОКЕН")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("catalog", catalog_command))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Запуск асинхронного обновления постов
    updater.job_queue.run_repeating(update_posts, interval=30, first=0)

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    with telethon_client:
        main()
