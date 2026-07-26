import telebot

from config import TOKEN

# Banco
from database import conn, cursor

# Módulos
from usuario import registrar_usuario
from saques import registrar_saques
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
registrar_saques(bot)
registrar_admin(bot)

# ==========================================
# COMANDOS GERAIS
# ==========================================

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

Utilize os botões para navegar.

Caso tenha dúvidas,
entre em contato com o suporte.
"""

    bot.send_message(
        message.chat.id,
        texto
    )


# ==========================================
# BLOQUEAR MENSAGENS DESCONHECIDAS
# ==========================================

@bot.message_handler(func=lambda m: True)
def desconhecido(message):

    bot.reply_to(

        message,

        """
❌ Comando não reconhecido.

Utilize os botões do menu.
"""

    )


# ==========================================
# INICIAR
# ==========================================

print("=" * 40)
print("BOT ONLINE")
print("=" * 40)

bot.infinity_polling(
    timeout=30,
    long_polling_timeout=30
)
