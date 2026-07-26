import telebot

from config import TOKEN

from database import *

from usuario import registrar_usuario

from admin import registrar_admin

# ==========================================
# BOT
# ==========================================

bot = telebot.TeleBot(
    TOKEN,
    parse_mode="HTML"
)

# ==========================================
# REGISTRAR MÓDULOS
# ==========================================

registrar_usuario(bot)

registrar_admin(bot)

# ==========================================
# COMANDO STARTUP
# ==========================================

print("=" * 40)
print("Bot iniciado com sucesso!")
print("=" * 40)

# ==========================================
# POLLING
# ==========================================

bot.infinity_polling(
    timeout=30,
    long_polling_timeout=30
)
