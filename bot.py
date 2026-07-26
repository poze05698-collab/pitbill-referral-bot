import telebot

from config import TOKEN

from database import *

from usuario import registrar_usuario
from saques import registrar_saques
from admin import registrar_admin

bot = telebot.TeleBot(
    TOKEN,
    parse_mode="HTML"
)

# Registrar módulos
registrar_usuario(bot)
registrar_saques(bot)
registrar_admin(bot)

print("✅ Bot iniciado!")

bot.infinity_polling(
    timeout=30,
    long_polling_timeout=30
)
