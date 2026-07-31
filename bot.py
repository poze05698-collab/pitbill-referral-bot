"""
==================================================
PITBULL REWARDS PLATFORM V3
bot.py
==================================================
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
    saldo,
    adicionar_saldo
)

from carteira import (
    texto_carteira
)

from pix import (
    texto_pix,
    salvar_pix,
    validar_pix
)

from saques import (
    solicitar_saque
)

from indicacoes import (
    registrar_indicacao
)
from database import cursor
# ==================================================
# BOT
# ==================================================

bot = telebot.TeleBot(
    TOKEN,
    parse_mode="HTML"
)

# ==================================================
# ESTADOS TEMPORÁRIOS
# ==================================================

estados = {}

# ==================================================
# FUNÇÕES AUXILIARES
# ==================================================

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


def is_admin(usuario_id):

    return usuario_id == OWNER_ID


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
    )# ==================================================
# START
# ==================================================

@bot.message_handler(commands=["start"])
def start(message):

    usuario = verificar_cadastro(message)

    args = message.text.split()

    if len(args) > 1:

        parametro = args[1]

        if parametro.startswith("convite_"):

    codigo = parametro.replace(
        "convite_",
        ""
    )

    cursor.execute(
        """
        SELECT id
        FROM usuarios
        WHERE codigo=?
        """,
        (codigo,)
    )

    indicador = cursor.fetchone()

    if indicador:

        registrar_indicacao(
            indicador["id"],
            message.from_user.id
        )

enviar_menu(
    message.chat.id,
    usuario
)


# ==================================================
# MENU PRINCIPAL
# ==================================================

@bot.message_handler(func=lambda msg: msg.text == "🏠 Menu Principal")
def menu_handler(message):

    usuario = buscar_usuario(
        message.from_user.id
    )

    enviar_menu(
        message.chat.id,
        usuario
    )


# ==================================================
# ADMIN
# ==================================================

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

Bem-vindo ao painel administrativo.
""",
        reply_markup=menu_admin()
    )


# ==================================================
# ADICIONAR SALDO
# ==================================================

@bot.message_handler(commands=["addsaldo"])
def comando_addsaldo(message):

    if not is_admin(message.from_user.id):

        bot.reply_to(
            message,
            "❌ Você não tem permissão."
        )

        return

    try:

        args = message.text.split()

        if len(args) != 3:

            bot.reply_to(
                message,
                "Uso:\n/addsaldo ID VALOR\n\nExemplo:\n/addsaldo 123456789 100"
            )

            return

        usuario_id = int(args[1])

        valor = float(
            args[2].replace(",", ".")
        )

        sucesso = adicionar_saldo(
            usuario_id,
            valor,
            categoria="ADMIN",
            descricao="Saldo adicionado pelo administrador",
            admin_id=message.from_user.id
        )

        if sucesso:

            bot.reply_to(
                message,
                f"✅ Saldo de R$ {valor:.2f} adicionado com sucesso."
            )

        else:

            bot.reply_to(
                message,
                "❌ Não foi possível adicionar o saldo."
            )

    except Exception as erro:

        bot.reply_to(
            message,
            f"❌ Erro:\n{erro}"
        )# ==================================================
# PERFIL
# ==================================================

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


# ==================================================
# CARTEIRA
# ==================================================

@bot.message_handler(func=lambda msg: msg.text == "💰 Carteira")
def carteira(message):

    bot.send_message(
        message.chat.id,
        texto_carteira(message.from_user.id),
        reply_markup=menu_principal()
    )


# ==================================================
# PIX
# ==================================================

@bot.message_handler(func=lambda msg: msg.text == "💳 PIX")
def pix(message):

    estados[message.from_user.id] = "PIX"

    bot.send_message(
        message.chat.id,
        texto_pix(message.from_user.id)
    )

    bot.send_message(
        message.chat.id,
        """
✍️ Envie sua chave PIX.

Pode ser:

• CPF
• Telefone
• E-mail
• Chave Aleatória
"""
    )


# ==================================================
# SOLICITAR SAQUE
# ==================================================

@bot.message_handler(func=lambda msg: msg.text == "💸 Solicitar Saque")
def saque(message):

    estados[message.from_user.id] = "SAQUE"

    bot.send_message(
        message.chat.id,
        """
💸 Digite o valor do saque.

Exemplo:

20
"""
    )# ==================================================
# CONVIDAR AMIGOS
# ==================================================

@bot.message_handler(func=lambda msg: msg.text == "👥 Convidar Amigos")
def convidar_amigos(message):

    usuario = perfil(message.from_user.id)

    link = f"https://t.me/{bot.get_me().username}?start=convite_{usuario['codigo']}"

    texto = f"""
👥 <b>CONVIDAR AMIGOS</b>

━━━━━━━━━━━━━━━━━━

Seu link exclusivo:

<code>{link}</code>

━━━━━━━━━━━━━━━━━━

Convide seus amigos utilizando este link.

Você receberá recompensas por cada indicação válida.
"""

    bot.send_message(
        message.chat.id,
        texto,
        reply_markup=menu_principal()
    )


# ==================================================
# BÔNUS DIÁRIO
# ==================================================

@bot.message_handler(func=lambda msg: msg.text == "🎁 Bônus Diário")
def bonus_diario(message):

    bot.send_message(
        message.chat.id,
        "🎁 Sistema de bônus diário em desenvolvimento.",
        reply_markup=menu_principal()
    )


# ==================================================
# RANKING
# ==================================================

@bot.message_handler(func=lambda msg: msg.text == "🏆 Ranking")
def ranking(message):

    bot.send_message(
        message.chat.id,
        "🏆 Ranking em desenvolvimento.",
        reply_markup=menu_principal()
    )


# ==================================================
# ATENDIMENTO
# ==================================================

@bot.message_handler(func=lambda msg: msg.text == "🎫 Atendimento")
def atendimento(message):

    bot.send_message(
        message.chat.id,
        "🎫 Sistema de atendimento em desenvolvimento.",
        reply_markup=menu_principal()
    )


# ==================================================
# ROLETA
# ==================================================

@bot.message_handler(func=lambda msg: msg.text == "🎡 Roleta")
def roleta(message):

    bot.send_message(
        message.chat.id,
        "🎡 Sistema de roleta em desenvolvimento.",
        reply_markup=menu_principal()
    )


# ==================================================
# RASPADINHA
# ==================================================

@bot.message_handler(func=lambda msg: msg.text == "🎫 Raspadinha")
def raspadinha(message):

    bot.send_message(
        message.chat.id,
        "🎫 Sistema de raspadinha em desenvolvimento.",
        reply_markup=menu_principal()
    )


# ==================================================
# MISSÕES
# ==================================================

@bot.message_handler(func=lambda msg: msg.text == "🎯 Missões")
def missoes(message):

    bot.send_message(
        message.chat.id,
        "🎯 Sistema de missões em desenvolvimento.",
        reply_markup=menu_principal()
    )


# ==================================================
# INFORMAÇÕES
# ==================================================

@bot.message_handler(func=lambda msg: msg.text == "ℹ️ Informações")
def informacoes(message):

    texto = """
ℹ️ <b>PITBULL REWARDS PLATFORM V3</b>

━━━━━━━━━━━━━━━━━━

Versão: 3.0

Status:
✅ Sistema de usuários
✅ Carteira
✅ PIX
✅ Saques

🚧 Em desenvolvimento:

• Afiliados
• Ranking
• VIP
• Premium
• Tickets
• Eventos
• Loja
"""

    bot.send_message(
        message.chat.id,
        texto,
        reply_markup=menu_principal()
    )# ==================================================
# GERENCIADOR DE MENSAGENS
# ==================================================

@bot.message_handler(func=lambda message: True)
def gerenciador(message):

    usuario_id = message.from_user.id

    estado = estados.get(usuario_id)

    # ===============================================
    # CADASTRO DE PIX
    # ===============================================

    if estado == "PIX":

        chave = message.text.strip()

        if not validar_pix(chave):

            bot.send_message(
                message.chat.id,
                "❌ Chave PIX inválida.\n\nTente novamente."
            )
            return

        if salvar_pix(usuario_id, chave):

            estados.pop(usuario_id, None)

            bot.send_message(
                message.chat.id,
                "✅ Chave PIX cadastrada com sucesso!",
                reply_markup=menu_principal()
            )

        else:

            bot.send_message(
                message.chat.id,
                "❌ Não foi possível cadastrar sua chave PIX."
            )

        return

    # ===============================================
    # SOLICITAÇÃO DE SAQUE
    # ===============================================

    if estado == "SAQUE":

        try:

            valor = float(
                message.text.replace(",", ".")
            )

        except ValueError:

            bot.send_message(
                message.chat.id,
                "❌ Digite apenas o valor.\n\nExemplo:\n20"
            )
            return

        resposta = solicitar_saque(
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

    # ===============================================
    # MENSAGEM PADRÃO
    # ===============================================

    bot.send_message(
        message.chat.id,
        "⚠️ Utilize os botões do menu.",
        reply_markup=menu_principal()
    )# ==================================================
# INICIALIZAÇÃO DO BOT
# ==================================================

def iniciar_bot():

    print("=" * 50)
    print("🐶 PITBULL REWARDS PLATFORM V3")
    print("🚀 Bot iniciado com sucesso!")
    print("=" * 50)

    bot.infinity_polling(
        skip_pending=True,
        timeout=30,
        long_polling_timeout=30
    )


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    iniciar_bot()
