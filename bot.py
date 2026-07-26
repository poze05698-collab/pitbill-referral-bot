import telebot

from config import TOKEN

from database import conn, cursor

from usuario import registrar_usuario
from saques import registrar_saques
from admin import registrar_admin

bot = telebot.TeleBot(
    TOKEN,
    parse_mode="HTML"
)

registrar_usuario(bot)
registrar_saques(bot)
registrar_admin(bot)

@bot.message_handler(commands=["ping"])
def ping(message):

    bot.reply_to(
        message,
        "🏓 Online!"
    )

@bot.message_handler(commands=["id"])
def meu_id(message):

    bot.reply_to(
        message,
        f"Seu ID é:\n\n{message.from_user.id}"
    )

@bot.message_handler(commands=["ajuda"])
def ajuda(message):

    texto = """
🤖 BOT DE INDICAÇÕES

Comandos disponíveis:

/start
/id
/ping
"""

    bot.send_message(
        message.chat.id,
        texto
    )

print("=" * 40)
print("BOT ONLINE")
print("=" * 40)

bot.infinity_polling(
    timeout=30,
    long_polling_timeout=30
)
