import telebot

from config import TOKEN
from database import conn, cursor

from usuario import registrar_usuario
from admin import registrar_admin

# ==========================================
# INICIAR BOT
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
# COMANDO PING
# ==========================================

@bot.message_handler(commands=["ping"])
def ping(message):

    bot.reply_to(
        message,
        "🏓 Pong!"
    )

# ==========================================
# AJUDA
# ==========================================

@bot.message_handler(commands=["help"])
def ajuda(message):

    texto = """
🤖 Bot de Indicações

Comandos:

/start
/help

Caso tenha dúvidas,
entre em contato com o suporte.
"""

    bot.send_message(
        message.chat.id,
        texto
    )

# ==========================================
# BLOQUEIO
# ==========================================

@bot.message_handler(func=lambda m: True)
def verificar_bloqueio(message):

    cursor.execute(
        """
        SELECT bloqueado
        FROM usuarios
        WHERE id=?
        """,
        (message.from_user.id,)
    )

    usuario = cursor.fetchone()

    if usuario:

        if usuario[0] == 1:

            bot.reply_to(
                message,
                """
🚫 Sua conta está bloqueada.

Entre em contato com o suporte.
"""
            )

            return

# ==========================================
# ERROS
# ==========================================

def iniciar():

    while True:

        try:

            print("Bot iniciado.")

            bot.infinity_polling(
                timeout=30,
                long_polling_timeout=30
            )

        except Exception as erro:

            print(
                f"Erro: {erro}"
            )

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    iniciar()
