import logging
from telegram.ext import Updater, CommandHandler

TOKEN="5896144083:AAHrMeI6tOGk1Gij1Chsyx4uyQsjF9U-YVk"
BOTNAME="https://t.me/test_mrbadr1bot"
#---------------------------

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Define a function to handle the /start command
def start(update, context):
    # Reply with "I'm alive"
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm alive")

# Create an instance of the Updater class and pass your bot token
updater = Updater(TOKEN, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register the start function as a handler for the /start command
dispatcher.add_handler(CommandHandler("start", start))

# Start the bot
updater.start_polling()

# Run the bot until you press Ctrl-C
updater.idle()
