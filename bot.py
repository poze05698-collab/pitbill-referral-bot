import telebot
import time

from config import TOKEN

# ==========================================
# BANCO
# ==========================================

from database import conn, cursor

# ==========================================
# MÓDULOS
# ==========================================

from usuario import registrar_usuario
from admin import registrar_admin
from saques import registrar_saques
from indicacoes import registrar_indicacoes
from antifraude import registrar_antifraude

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

registrar_saques(bot)

registrar_indicacoes(bot)

registrar_antifraude(bot)

# ==========================================
# COMANDOS GERAIS
# ==========================================

@bot.message_handler(commands=["ping"])
def ping(message):

    bot.reply_to(

        message,

        "🏓 Bot Online!"

    )


@bot.message_handler(commands=["id"])
def meu_id(message):

    bot.reply_to(

        message,

        f"""
🆔 Seu ID

<code>{message.from_user.id}</code>
""",

        parse_mode="HTML"

    )


@bot.message_handler(commands=["versao"])
def versao(message):

    from config import VERSAO

    bot.reply_to(

        message,

        f"""
🤖 Pitbull Referral Bot

Versão:

<b>{VERSAO}</b>
""",

        parse_mode="HTML"

    )


@bot.message_handler(commands=["ajuda"])
def ajuda(message):

    texto = """
🤖 <b>AJUDA</b>

Comandos disponíveis:

/start

/ping

/id

/versao

/admin (Administrador)

Utilize os botões para navegar.
"""

    bot.send_message(

        message.chat.id,

        texto,

        parse_mode="HTML"

    )


# ==========================================
# MENSAGEM DESCONHECIDA
# ==========================================

@bot.message_handler(func=lambda m: True)
def desconhecido(message):

    bot.reply_to(

        message,

        """
❌ Opção inválida.

Utilize os botões do menu.
"""

    )


# ==========================================
# INICIAR BOT
# ==========================================

print("=" * 50)

print("🚀 PITBULL REFERRAL BOT")

print("=" * 50)

print("Banco de dados conectado.")

print("Módulos carregados.")

print("Bot iniciado com sucesso.")

print("=" * 50)

# ==========================================
# LOOP PRINCIPAL
# ==========================================

while True:

    try:

        bot.infinity_polling(

            timeout=30,

            long_polling_timeout=30,

            skip_pending=True

        )

    except Exception as erro:

        print("=" * 50)

        print("ERRO ENCONTRADO")

        print(erro)

        print("Reiniciando em 10 segundos...")

        print("=" * 50)

        time.sleep(10)
