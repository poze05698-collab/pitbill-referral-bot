"""
=========================================
 PITBULL REWARDS PLATFORM V3
 bot.py
=========================================
"""

import telebot

from config import (
    TOKEN,
    OWNER_ID
)

from teclado import (
    menu_principal,
    menu_admin
)

from usuarios import (
    usuario_existe,
    cadastrar_usuario,
    atualizar_usuario,
    atualizar_login,
    buscar_usuario,
    perfil,
    saldo
)
from carteira import texto_carteira
from pix import (
    texto_pix,
    salvar_pix,
    validar_pix
)
# ==========================================
# BOT
# ==========================================

bot = telebot.TeleBot(

    TOKEN,

    parse_mode="HTML"

)

# ==========================================
# DATA DO USUÁRIO
# ==========================================

def dados_usuario(message):

    return {

        "id": message.from_user.id,

        "nome": message.from_user.first_name or "",

        "username": message.from_user.username or ""

    }

# ==========================================
# ADMIN
# ==========================================

def is_admin(user_id):

    return user_id == OWNER_ID

# ==========================================
# CADASTRO
# ==========================================

def verificar_cadastro(message):

    dados = dados_usuario(message)

    if not usuario_existe(dados["id"]):

        cadastrar_usuario(

            user_id=dados["id"],

            nome=dados["nome"],

            username=dados["username"]

        )

    else:

        atualizar_usuario(

            user_id=dados["id"],

            nome=dados["nome"],

            username=dados["username"]

        )

        atualizar_login(

            dados["id"]

        )

    return buscar_usuario(

        dados["id"]

    )

# ==========================================
# ENVIAR MENU
# ==========================================

def enviar_menu(chat_id, usuario):

    texto = f"""
🐶 <b>PITBULL REWARDS PLATFORM</b>

Olá <b>{usuario['nome']}</b>

━━━━━━━━━━━━━━━━━━

💰 Saldo:
R$ {usuario['saldo']:.2f}

⭐ Nível:
{usuario['nivel']}

👑 VIP:
{usuario['vip']}

━━━━━━━━━━━━━━━━━━

Escolha uma opção abaixo.
"""

    bot.send_message(

        chat_id,

        texto,

        reply_markup=menu_principal()

    )# ==========================================
# START
# ==========================================

@bot.message_handler(commands=["start"])
def start(message):

    usuario = verificar_cadastro(message)

    # Parâmetros do /start
    args = message.text.split()

    if len(args) > 1:

        parametro = args[1]

        # Exemplo:
        # /start convite_ABC123

        if parametro.startswith("convite_"):

            codigo = parametro.replace("convite_", "")

            # Sistema de indicação
            # Será implementado no afiliados.py
            pass

    enviar_menu(

        message.chat.id,

        usuario

    )

# ==========================================
# MENU PRINCIPAL
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "🏠 Menu Principal")
def menu(message):

    usuario = buscar_usuario(

        message.from_user.id

    )

    enviar_menu(

        message.chat.id,

        usuario

    )

# ==========================================
# PAINEL ADMIN
# ==========================================

@bot.message_handler(commands=["admin"])
def admin(message):

    if not is_admin(message.from_user.id):

        bot.reply_to(

            message,

            "❌ Apenas administradores podem utilizar este comando."

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
# PERFIL
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "👤 Perfil")
def meu_perfil(message):

    usuario = perfil(

        message.from_user.id

    )

    texto = f"""
👤 <b>MEU PERFIL</b>

━━━━━━━━━━━━━━━━━━

🆔 ID

<code>{usuario['id']}</code>

👤 Nome

{usuario['nome']}

🔖 Código

<code>{usuario['codigo']}</code>

💰 Saldo

R$ {usuario['saldo']:.2f}

⭐ Nível

{usuario['nivel']}

👑 VIP

{usuario['vip']}

🏆 XP

{usuario['xp']}

👥 Indicados

{usuario['indicados']}

🔥 Sequência

{usuario['streak']}

━━━━━━━━━━━━━━━━━━
"""

    bot.send_message(

        message.chat.id,

        texto,

        reply_markup=menu_principal()

    )

# ==========================================
# CARTEIRA
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "💰 Carteira")
def carteira(message):

    bot.send_message(

        message.chat.id,

        texto_carteira(message.from_user.id),

        reply_markup=menu_principal()

    )# ==========================================
# CONVIDAR AMIGOS
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "👥 Convidar Amigos")
def convidar_amigos(message):

    usuario = perfil(message.from_user.id)

    link = f"https://t.me/{bot.get_me().username}?start=convite_{usuario['codigo']}"

    texto = f"""
👥 <b>CONVIDAR AMIGOS</b>

Seu link exclusivo:

<code>{link}</code>

━━━━━━━━━━━━━━━━━━

🔹 Compartilhe o seu link.

🔹 Quando um amigo entrar usando o seu link e for aprovado pelo administrador, a recompensa será creditada automaticamente.

Boa sorte!
"""

    bot.send_message(
        message.chat.id,
        texto,
        reply_markup=menu_principal()
    )

# ==========================================
# BÔNUS DIÁRIO
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "🎁 Bônus Diário")
def bonus_diario(message):

    bot.send_message(
        message.chat.id,
        "🎁 O sistema de bônus diário será implementado na próxima etapa.",
        reply_markup=menu_principal()
    )

# ==========================================
# RANKING
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "🏆 Ranking")
def ranking(message):

    bot.send_message(
        message.chat.id,
        "🏆 O sistema de ranking será implementado na próxima etapa.",
        reply_markup=menu_principal()
    )

# ==========================================
# INFORMAÇÕES
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "ℹ️ Informações")
def informacoes(message):

    texto = """
ℹ️ <b>PITBULL REWARDS PLATFORM</b>

Versão: 2.1

Em desenvolvimento.

Em breve:

✅ Sistema VIP
✅ Missões
✅ Raspadinha
✅ Roleta
✅ Eventos
✅ Tickets
"""

    bot.send_message(
        message.chat.id,
        texto,
        reply_markup=menu_principal()
    )

# ==========================================
# ATENDIMENTO
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "🎫 Atendimento")
def atendimento(message):

    bot.send_message(
        message.chat.id,
        "🎫 O sistema de tickets será implementado na próxima etapa.",
        reply_markup=menu_principal()
    )# ==========================================
# PIX
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "💳 PIX")
def pix(message):

    bot.send_message(

        message.chat.id,

        texto_pix(message.from_user.id),

        reply_markup=menu_principal()

    )

# ==========================================
# SOLICITAR SAQUE
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "💸 Solicitar Saque")
def saque(message):

    bot.send_message(

        message.chat.id,

        "💸 O sistema de saques será implementado na próxima etapa.",

        reply_markup=menu_principal()

    )

# ==========================================
# ROLETA
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "🎡 Roleta")
def roleta(message):

    bot.send_message(

        message.chat.id,

        "🎡 A roleta diária será implementada na próxima etapa.",

        reply_markup=menu_principal()

    )

# ==========================================
# RASPADINHA
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "🎫 Raspadinha")
def raspadinha(message):

    bot.send_message(

        message.chat.id,

        "🎫 A raspadinha diária será implementada na próxima etapa.",

        reply_markup=menu_principal()

    )

# ==========================================
# MISSÕES
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "🎯 Missões")
def missoes(message):

    bot.send_message(

        message.chat.id,

        "🎯 O sistema de missões será implementado na próxima etapa.",

        reply_markup=menu_principal()

    )
# ==========================================
# CADASTRAR PIX
# ==========================================

@bot.message_handler(func=lambda msg: msg.text and not msg.text.startswith("/"))
def cadastrar_pix(message):

    texto = message.text.strip()

    # Ignora os botões do menu
    botoes = [
        "🏠 Menu Principal",
        "👤 Perfil",
        "💰 Carteira",
        "💳 PIX",
        "💸 Solicitar Saque",
        "👥 Convidar Amigos",
        "🎁 Bônus Diário",
        "🏆 Ranking",
        "🎫 Atendimento",
        "🎡 Roleta",
        "🎫 Raspadinha",
        "🎯 Missões",
        "ℹ️ Informações",
    ]

    if texto in botoes:
        return

    if not validar_pix(texto):
        return

    salvar_pix(
        message.from_user.id,
        texto
    )

    bot.send_message(
        message.chat.id,
        "✅ Sua chave PIX foi cadastrada com sucesso!",
        reply_markup=menu_principal()
    )
# ==========================================
# MENSAGENS DESCONHECIDAS
# ==========================================

@bot.message_handler(func=lambda msg: True)
def mensagens(message):

    bot.reply_to(

        message,

        "⚠️ Utilize os botões do menu para navegar."

    )

# ==========================================
# INICIAR BOT
# ==========================================

def iniciar_bot():

    print("=" * 50)

    print("🐶 PITBULL REWARDS PLATFORM V3")

    print("🤖 Bot iniciado com sucesso!")

    print("=" * 50)

    bot.infinity_polling(

        skip_pending=True,

        timeout=60,

        long_polling_timeout=60

    )
