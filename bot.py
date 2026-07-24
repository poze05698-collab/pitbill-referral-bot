import telebot

TOKEN = '8771309444:AAE522egqaCOPGaAZUqDCB-6zY6uK-y1lhg'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Funcionando!")

@bot.message_handler(commands=['teste'])
def teste(message):
    bot.reply_to(message, "Bot online!")

bot.infinity_polling()
