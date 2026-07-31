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

from saques import solicitar_saque

# ==========================================
# BOT
# ==========================================

bot = telebot.TeleBot(
    TOKEN,
    parse_mode="HTML"
)

# ==========================================
# ESTADOS TEMPORÁRIOS
# ==========================================

# Guarda o que cada usuário está fazendo.
# Exemplos:
# estados[id] = "PIX"
# estados[id] = "SAQUE"

estados = {}

# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def dados_usuario(message):

    return {
        "id": message.from_user.id,
        "nome": message.from_user.first_name or "",
        "username": message.from_user.username or ""
    }


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


def is_admin(user_id):

    return user_id == OWNER_ID


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

    args = message.text.split()

    if len(args) > 1:

        parametro = args[1]

        if parametro.startswith("convite_"):

            codigo = parametro.replace("convite_", "")

            # Sistema de indicação
            # Será implementado depois
            pass

    enviar_menu(
        message.chat.id,
        usuario
    )


# ==========================================
# MENU PRINCIPAL
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "🏠 Menu Principal")
def menu_principal_handler(message):

    usuario = buscar_usuario(
        message.from_user.id
    )

    enviar_menu(
        message.chat.id,
        usuario
    )


# ==========================================
# ADMIN
# ==========================================

@bot.message_handler(commands=["admin"])
def admin(message):

    if not is_admin(message.from_user.id):

        bot.reply_to(
            message,
            "❌ Apenas administradores podem utilizar este comando."
        )

        return

    bot.send_message(
        message.chat.id,
        """
🛡️ <b>PAINEL ADMINISTRATIVO</b>

Bem-vindo!
""",
        reply_markup=menu_admin()
    )# ==========================================
# PERFIL
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "👤 Perfil")
def meu_perfil(message):

    usuario = perfil(message.from_user.id)

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
    )


# ==========================================
# PIX
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "💳 PIX")
def pix(message):

    estados[message.from_user.id] = "PIX"

    bot.send_message(
        message.chat.id,
        texto_pix(message.from_user.id)
    )

    bot.send_message(
        message.chat.id,
        "✍️ Agora envie sua chave PIX."
    )


# ==========================================
# SOLICITAR SAQUE
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "💸 Solicitar Saque")
def saque(message):

    estados[message.from_user.id] = "SAQUE"

    bot.send_message(
        message.chat.id,
        "💸 Digite o valor que deseja sacar.\n\nExemplo:\n20"
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

Compartilhe seu link e ganhe recompensas por cada indicação válida.
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
        "🎁 Sistema de bônus diário em desenvolvimento.",
        reply_markup=menu_principal()
    )


# ==========================================
# RANKING
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "🏆 Ranking")
def ranking(message):

    bot.send_message(
        message.chat.id,
        "🏆 Ranking em desenvolvimento.",
        reply_markup=menu_principal()
    )


# ==========================================
# ATENDIMENTO
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "🎫 Atendimento")
def atendimento(message):

    bot.send_message(
        message.chat.id,
        "🎫 Sistema de atendimento em desenvolvimento.",
        reply_markup=menu_principal()
    )


# ==========================================
# ROLETA
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "🎡 Roleta")
def roleta(message):

    bot.send_message(
        message.chat.id,
        "🎡 Roleta em desenvolvimento.",
        reply_markup=menu_principal()
    )


# ==========================================
# RASPADINHA
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "🎫 Raspadinha")
def raspadinha(message):

    bot.send_message(
        message.chat.id,
        "🎫 Raspadinha em desenvolvimento.",
        reply_markup=menu_principal()
    )


# ==========================================
# MISSÕES
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "🎯 Missões")
def missoes(message):

    bot.send_message(
        message.chat.id,
        "🎯 Sistema de missões em desenvolvimento.",
        reply_markup=menu_principal()
    )


# ==========================================
# INFORMAÇÕES
# ==========================================

@bot.message_handler(func=lambda msg: msg.text == "ℹ️ Informações")
def informacoes(message):

    texto = """
ℹ️ <b>PITBULL REWARDS PLATFORM</b>

Versão 3.0

🚧 Plataforma em desenvolvimento.

Em breve:

✅ Sistema VIP
✅ Jogos
✅ Missões
✅ Eventos
✅ Tickets
✅ Ranking
"""

    bot.send_message(
        message.chat.id,
        texto,
        reply_markup=menu_principal()
    )# ==========================================
# GERENCIADOR DE MENSAGENS
# ==========================================

@bot.message_handler(func=lambda msg: True)
def gerenciador(message):

    usuario_id = message.from_user.id
    texto = message.text.strip()

    # -------------------------
    # CADASTRAR PIX
    # -------------------------

    if estados.get(usuario_id) == "PIX":

        if not validar_pix(texto):

            bot.send_message(
                message.chat.id,
                "❌ Chave PIX inválida.\n\nTente novamente."
            )
            return

        salvar_pix(usuario_id, texto)

        estados.pop(usuario_id, None)

        bot.send_message(
            message.chat.id,
            "✅ Chave PIX cadastrada com sucesso!",
            reply_markup=menu_principal()
        )
        return

    # -------------------------
    # SOLICITAR SAQUE
    # -------------------------

    if estados.get(usuario_id) == "SAQUE":

        try:

            valor = float(texto.replace(",", "."))

        except ValueError:

            bot.send_message(
                message.chat.id,
                "❌ Digite apenas um número.\n\nExemplo:\n20"
            )
            return

        sucesso, resposta = solicitar_saque(
            usuario_id,
            valor
        )

        estados.pop(usuario_id, None)

        bot.send_message(
            message.chat.id,
            resposta,
            reply_markup=menu_principal()
        )
        return

    # -------------------------
    # DESCONHECIDO
    # -------------------------

    bot.send_message(
        message.chat.id,
        "⚠️ Utilize os botões do menu.",
        reply_markup=menu_principal()
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
