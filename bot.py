from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

# Function to handle the /start command
async def start(update: Update, context: CallbackContext):
    # Welcome message
    await update.message.reply_text('Welcome to our store!')

# Function to add a product
async def add_product(update: Update, context: CallbackContext):
    await update.message.reply_text("Let's add a product.\nPlease provide the following details:")

    # Ask for product name
    await update.message.reply_text("Enter product name:")

    # Store user's response in a variable (for future steps, you'll need to add logic to collect user inputs)
    context.user_data['product_name'] = update.message.text  # You would collect this after the user responds

# Main function to start the bot
def main():
    # Your Bot Token from BotFather
    TOKEN = '7235348489:AAEeK8eAs6TeRPrH-3sn_2f0_ohO54vB_oY'
    
    # Create the Application instance
    application = Application.builder().token(TOKEN).build()

    # Add handlers for commands
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('addproduct', add_product))

    # Start polling updates from Telegram (this avoids using webhooks)
    application.run_polling()

if __name__ == '__main__':
    main()
