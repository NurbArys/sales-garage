import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# Этапы диалога для добавления товара
NAME, DESCRIPTION, CATEGORY, PRICE, IMAGE_URL = range(5)

# Начало процесса добавления товара
async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите наименование товара:")
    return NAME

# Шаг 1: Ввод наименования
async def name_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Введите описание товара:")
    return DESCRIPTION

# Шаг 2: Ввод описания
async def description_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['description'] = update.message.text
    await update.message.reply_text("Укажите категорию товара:")
    return CATEGORY

# Шаг 3: Ввод категории
async def category_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['category'] = update.message.text
    await update.message.reply_text("Введите цену товара:")
    return PRICE

# Шаг 4: Ввод цены
async def price_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['price'] = update.message.text
    await update.message.reply_text("Укажите ссылку на изображение товара:")
    return IMAGE_URL

# Шаг 5: Ввод ссылки на изображение и отправка данных на API
async def image_url_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['image_url'] = update.message.text

    # Формируем данные для отправки на сайт
    product_data = {
        "name": context.user_data['name'],
        "description": context.user_data['description'],
        "category": context.user_data['category'],
        "price": context.user_data['price'],
        "image_url": context.user_data['image_url']
    }

    # URL API для добавления товара (замените на ваш внешний IP)
    api_url = "104.198.147.29:8080/api/add_product"

    # Отправляем данные на сервер
    response = requests.post(api_url, json=product_data)

    if response.status_code == 200:
        await update.message.reply_text(f"Товар успешно добавлен:\n\n{product_data}")
    else:
        await update.message.reply_text("Произошла ошибка при добавлении товара на сайт.")

    # Конец диалога
    return ConversationHandler.END

# Функция отмены добавления товара
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добавление товара отменено.")
    return ConversationHandler.END

# Основной код для запуска бота
def main():
    # Токен вашего Telegram бота
    TOKEN = '7235348489:AAEeHyiYW6B8QB_VXbAGHXmtRAEnlWy-mqk'  # Замените на токен вашего бота

    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Создаем обработчик для добавления товара с шагами диалога
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add_product', add_product)],
        states={
            NAME: [MessageHandler(filters.TEXT, name_input)],
            DESCRIPTION: [MessageHandler(filters.TEXT, description_input)],
            CATEGORY: [MessageHandler(filters.TEXT, category_input)],
            PRICE: [MessageHandler(filters.TEXT, price_input)],
            IMAGE_URL: [MessageHandler(filters.TEXT, image_url_input)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Добавляем обработчики в приложение
    application.add_handler(conv_handler)

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
