from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Функция, обрабатывающая команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Приветственное сообщение пользователю
    await update.message.reply_text('Привет! Добро пожаловать в наш магазин!')

# Функция, отправляющая сообщение в канал
async def send_to_channel(context: ContextTypes.DEFAULT_TYPE):
    # ID вашего канала
    channel_id = '@sales_garage_atyrau'  # Имя вашего канала
    # Кнопка с ссылкой на витрину
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Посетить витрину", url='https://nurbarys.github.io/Sales-Garage/')]
    ])
    # Отправка сообщения в канал
    await context.bot.send_message(chat_id=channel_id, text="Посетите нашу витрину товаров!", reply_markup=keyboard)

def main():
    # Токен, который вы получили от BotFather
    TOKEN = '7235348489:AAEeHyiYW6B8QB_VXbAGHXmtRAEnlWy-mqk'
    application = Application.builder().token(TOKEN).build()

    # Добавление обработчиков команд
    application.add_handler(CommandHandler('start', start))

    # Задача для отправки сообщения в канал при запуске бота
    application.job_queue.run_once(send_to_channel, when=0)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
