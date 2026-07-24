import telebot

TOKEN = '8771309444:AAE522egqaCOPGaAZUqDCB-6zY6uK-y1lhg'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    nome = message.from_user.first_name
    bot.reply_to(message, f"Ola {nome}! Bot funcionando!\n\n/teste - Testar\n/meusdados - Dados\n/saque - Sacar\n/regras - Regras")

@bot.message_handler(commands=['teste'])
def teste(message):
    bot.reply_to(message, "Bot online e funcionando!")

@bot.message_handler(commands=['meusdados'])
def meusdados(message):
    bot.reply_to(message, "Comando /meusdados funcionando!")

@bot.message_handler(commands=['saque'])
def saque(message):
    bot.reply_to(message, "Comando /saque funcionando!")

@bot.message_handler(commands=['regras'])
def regras(message):
    bot.reply_to(message, "Comando /regras funcionando!")

print("Bot ligado!")
bot.infinity_polling()
