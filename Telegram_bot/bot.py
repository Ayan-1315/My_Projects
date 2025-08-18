import telebot
import config
import dotenv
import traceback
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from transformers import pipeline

# Load environment variables
dotenv.load_dotenv()

# MongoDB Client
try:
    client = MongoClient(config.MONGO_DB_URI, server_api=ServerApi('1'))
    client.admin.command('ping')
    print("Connected to MongoDB!")
except Exception as e:
    print("Error connecting to MongoDB:", e)
    client = None

# Load the text generation pipeline
try:
    print("Loading the model...")
    pipe = pipeline("text2text-generation", model="your_model") # choose a hugging face model based on text2text-generation
    print("Model loaded successfully!")
except Exception as e:
    print("Error loading the pipeline:", e)
    pipe = None

# Initialize the Telegram bot
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Hello! I’m Maya.\n" +
        "Use /help to contact the developer or use /hello to continue."
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Message the developer', url='your_telegram_url' # enter your telegram url
        )
    )
    bot.send_message(
        message.chat.id,
        "1) Use /hello to start a conversation.\n" +
        "2) If the request doesn't process, the update will come soon.\n" +
        "3) You can also ask me questions directly!",
        reply_markup=keyboard
    )

@bot.message_handler(commands=['hello'])
def hello_command(message):
    bot.send_message(
        message.chat.id,
        "Hello, I'm Maya. How can I help you?"
    )

@bot.message_handler(func=lambda message: True)
def respond_to_message(message):
    if pipe is None:
        bot.send_message(message.chat.id, "The AI model is not available right now.")
        return
    try:
        # Generate response
        response = pipe(
            message.text,
            max_new_tokens=50,  # Limit response length
            num_return_sequences=1  # Generate a single response
        )
        # Send the response back
        bot.send_message(message.chat.id, response[0]["generated_text"]) # type: ignore
    except Exception as e:
        bot.send_message(message.chat.id, "Sorry, I couldn't process your request.")
        traceback.print_exc()

# Start polling with error handling
try:
    print("Bot is running .....")
    bot.polling(none_stop=True)
except Exception as e:
    print("Error running the bot:", e)
    traceback.print_exc()
