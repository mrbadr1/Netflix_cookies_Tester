import logging
from telegram.ext import Updater, MessageHandler, Filters
TOKEN="5896144083:AAHrMeI6tOGk1Gij1Chsyx4uyQsjF9U-YVk"
BOTNAME="https://t.me/test_mrbadr1bot"
#---------------------------
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Define a function to handle incoming messages
def reply_to_message(update, context):
    # Get the message text
    message_text = update.message.text
    
    # Reply with "I'm alive"
    update.message.reply_text("I'm alive")

# Create an instance of the Updater class and pass your bot token
updater = Updater(TOKEN, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register the reply_to_message function as a handler for text messages
dispatcher.add_handler(MessageHandler(Filters.text, reply_to_message))

# Start the bot
updater.start_polling()

# Run the bot until you press Ctrl-C
updater.idle()
