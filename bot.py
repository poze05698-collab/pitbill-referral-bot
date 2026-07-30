"""
=========================================
 PITBULL REWARDS PLATFORM V2
 bot.py
=========================================
"""

import telebot

from config import TOKEN, ADMIN_ID

from teclado import (
    menu_principal,
    menu_admin
)

from usuarios import (
    usuario_existe,
    cadastrar_usuario,
    atualizar_usuario,
    atualizar_login,
    buscar_usuario
)

# ==========================================
# BOT
# ==========================================

bot = telebot.TeleBot(
    TOKEN,
    parse_mode="HTML"
)# ==========================================
# VERIFICAR CADASTRO
# ==========================================

def verificar_cadastro(message):

    user_id = message.from_user.id

    nome = message.from_user.first_name or ""

    username = message.from_user.username or ""

    if not usuario_existe(user_id):

        cadastrar_usuario(

            user_id=user_id,

            nome=nome,

            username=username

        )

    else:

        atualizar_usuario(

            user_id=user_id,

            nome=nome,

            username=username

        )

        atualizar_login(user_id)

    return buscar_usuario(user_id)


# ==========================================
# VERIFICAR ADMIN
# ==========================================

def is_admin(user_id):

    return user_id == ADMIN_ID# ==========================================
# COMANDO START
# ==========================================

@bot.message_handler(commands=["start"])
def start(message):

    # Verifica cadastro
    usuario = verificar_cadastro(message)

    # Verifica se veio por convite
    args = message.text.split()

    if len(args) > 1:

        convite = args[1]

        # Exemplo:
        # /start convite_123456

        if convite.startswith("convite_"):

            indicador = convite.replace("convite_", "")

            # Aqui vamos implementar o sistema
            # de indicações no afiliados.py
            pass

    texto = f"""
🐶 <b>Bem-vindo ao Pitbull Rewards Platform!</b>

Olá <b>{usuario['nome']}</b> 👋

━━━━━━━━━━━━━━━━━━

🆔 <b>ID:</b> <code>{usuario['id']}</code>

🔖 <b>Código:</b>
<code>{usuario['codigo']}</code>

💰 <b>Saldo:</b>
R$ {usuario['saldo']:.2f}

⭐ <b>Nível:</b>
{usuario['nivel']}

👑 <b>VIP:</b>
{usuario['vip']}

━━━━━━━━━━━━━━━━━━

🎁 Convide amigos.

🎡 Ganhe giros.

🎫 Use raspadinhas.

🏆 Complete missões.

👇 Escolha uma opção abaixo.
"""

    bot.send_message(

        message.chat.id,

        texto,

        reply_markup=menu_principal()

    )# ==========================================
# PAINEL ADMIN
# ==========================================

@bot.message_handler(commands=["admin"])
def painel_admin(message):

    if not is_admin(message.from_user.id):

        bot.reply_to(

            message,

            "❌ Você não tem permissão para acessar o painel."

        )

        return

    texto = """
🛡️ <b>PAINEL ADMINISTRATIVO</b>

Bem-vindo!

Escolha uma opção abaixo.
"""

    bot.send_message(

        message.chat.id,

        texto,

        reply_markup=menu_admin()

    )


# ==========================================
# MENU PRINCIPAL
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "🏠 Menu Principal")
def voltar_menu(message):

    usuario = buscar_usuario(message.from_user.id)

    texto = f"""
🏠 <b>MENU PRINCIPAL</b>

Olá <b>{usuario['nome']}</b>

💰 Saldo: R$ {usuario['saldo']:.2f}

⭐ Nível: {usuario['nivel']}

👑 VIP: {usuario['vip']}

Escolha uma opção abaixo.
"""

    bot.send_message(

        message.chat.id,

        texto,

        reply_markup=menu_principal()

    )


# ==========================================
# MENSAGENS DESCONHECIDAS
# ==========================================

@bot.message_handler(func=lambda msg: True)
def mensagens(message):

    bot.reply_to(

        message,

        "⚠️ Utilize os botões do menu para navegar pelo bot."

    )


# ==========================================
# INICIAR BOT
# ==========================================

def iniciar_bot():

    print("=" * 50)
    print("🐶 PITBULL REWARDS PLATFORM")
    print("🤖 Bot iniciado com sucesso!")
    print("=" * 50)

    bot.infinity_polling(
        timeout=60,
        long_polling_timeout=60,
        skip_pending=True
    )
