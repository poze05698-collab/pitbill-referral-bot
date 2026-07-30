"""
=========================================
 PITBULL REWARDS PLATFORM V2
 bot.py
=========================================
"""

import telebot

from config import TOKEN

from usuarios import *

bot = telebot.TeleBot(
    TOKEN,
    parse_mode="HTML"
)

# ==========================================
# VERIFICAR CADASTRO
# ==========================================

def verificar_cadastro(message):

    user_id = message.from_user.id

    nome = message.from_user.first_name

    username = message.from_user.username

    if not usuario_existe(user_id):

        cadastrar_usuario(

            user_id,

            nome,

            username

        )

    else:

        atualizar_usuario(

            user_id,

            nome,

            username

        )

        atualizar_login(user_id)# ==========================================
# START
# ==========================================

@bot.message_handler(commands=["start"])
def start(message):

    verificar_cadastro(message)

    user = buscar_usuario(message.from_user.id)

    texto = f"""
🐶 <b>Bem-vindo ao {user['nome']}!</b>

🎉 Sua conta foi criada com sucesso.

━━━━━━━━━━━━━━━━━━

🆔 ID: <code>{user['id']}</code>

🔖 Código: <code>{user['codigo']}</code>

💰 Saldo: R$ {user['saldo']:.2f}

⭐ Nível: {user['nivel']}

👑 VIP: {user['vip']}

━━━━━━━━━━━━━━━━━━

👇 Escolha uma opção no menu abaixo.
"""

    bot.send_message(

        message.chat.id,

        texto

    )
