"""
==================================================
 PITBULL REWARDS PLATFORM V3
 BOT PRINCIPAL
==================================================
"""

# ==================================================
# IMPORTS
# ==================================================

import telebot

from config import (
    TOKEN,
    NOME_BOT
)

from database import (
    conn,
    cursor,
    agora
)

import estado
import teclado

from config import ADMIN_IDS

from admin import menu as admin_menu

import usuarios
import carteira
import pix
import saques
import indicacoes

# ==================================================
# BOT
# ==================================================

bot = telebot.TeleBot(
    TOKEN,
    parse_mode="HTML"
)

# ==================================================
# CACHE TEMPORÁRIO
# ==================================================

cache = {}

# ==================================================
# CACHE
# ==================================================

def salvar_cache(chave, valor):
    cache[chave] = valor


def obter_cache(chave):
    return cache.get(chave)


def limpar_cache(chave):
    cache.pop(chave, None)

# ==================================================
# PERFIL
# ==================================================

@bot.message_handler(func=lambda message: message.text == "👤 Perfil")
def menu_perfil(message):

    texto = usuarios.texto_perfil(
        message.from_user.id
    )

    bot.send_message(

        chat_id=message.chat.id,

        text=texto,

        reply_markup=teclado.menu_principal()

    )


# ==================================================
# CARTEIRA
# ==================================================

@bot.message_handler(func=lambda message: message.text == "💰 Carteira")
def menu_carteira(message):

    texto = carteira.texto_carteira(
        message.from_user.id
    )

    bot.send_message(

        chat_id=message.chat.id,

        text=texto,

        reply_markup=teclado.menu_carteira()

    )


# ==================================================
# PIX
# ==================================================

@bot.message_handler(func=lambda message: message.text == "💳 PIX")
def menu_pix(message):

    texto = pix.texto_pix(
        message.from_user.id
    )

    bot.send_message(

        chat_id=message.chat.id,

        text=texto,

        reply_markup=teclado.menu_pix()

    )


# ==================================================
# CONVIDAR AMIGOS
# ==================================================

@bot.message_handler(func=lambda message: message.text == "👥 Convidar Amigos")
def menu_indicacoes(message):

    link = usuarios.obter_link_convite(
        message.from_user.id
    )

    total = usuarios.total_indicacoes(
        message.from_user.id
    )

    pendentes = usuarios.indicacoes_pendentes(
        message.from_user.id
    )

    aprovadas = usuarios.indicacoes_aprovadas(
        message.from_user.id
    )

    texto = f"""
👥 <b>INDICAÇÕES</b>

━━━━━━━━━━━━━━━━━━

🔗 Seu link

<code>{link}</code>

━━━━━━━━━━━━━━━━━━

👥 Total

{total}

⏳ Pendentes

{pendentes}

✅ Aprovadas

{aprovadas}

━━━━━━━━━━━━━━━━━━

Compartilhe seu link e ganhe recompensas.
"""

    bot.send_message(

        chat_id=message.chat.id,

        text=texto,

        reply_markup=teclado.menu_principal()

    )


# ==================================================
# SAQUES
# ==================================================

@bot.message_handler(func=lambda message: message.text == "💸 Solicitar Saque")
def menu_saque(message):

    texto = saques.texto_saques(
        message.from_user.id
    )

    bot.send_message(

        chat_id=message.chat.id,

        text=texto,

        reply_markup=teclado.menu_saques()

    )


# ==================================================
# MENU PRINCIPAL
# ==================================================

@bot.message_handler(func=lambda message: message.text == "🏠 Menu Principal")
def voltar_menu(message):

    usuario = usuarios.obter_usuario(
        message.from_user.id
    )

    bot.send_message(

        chat_id=message.chat.id,

        text=f"🏠 Bem-vindo novamente, <b>{usuario['nome']}</b>!",

        reply_markup=teclado.menu_principal()

    )

# ==================================================
# NOVO SAQUE
# ==================================================

@bot.message_handler(func=lambda message: message.text == "💸 Novo Saque")
def novo_saque(message):

    estado.definir_estado(

        message.from_user.id,

        "AGUARDANDO_VALOR_SAQUE"

    )

    bot.send_message(

        message.chat.id,

        """
💸 <b>NOVO SAQUE</b>

━━━━━━━━━━━━━━━━━━

Digite o valor que deseja sacar.

Exemplo:

20
50
100

Para cancelar basta enviar:

cancelar
""",

        reply_markup=teclado.menu_saques()

    )


# ==================================================
# HISTÓRICO DE SAQUES
# ==================================================

@bot.message_handler(func=lambda message: message.text == "📜 Histórico")
def historico_saques(message):

    lista = saques.listar_saques(
        message.from_user.id
    )

    if not lista:

        bot.send_message(

            message.chat.id,

            "Você ainda não possui saques.",

            reply_markup=teclado.menu_saques()

        )

        return

    texto = "📜 <b>HISTÓRICO DE SAQUES</b>\n\n"

    for saque in lista[:10]:

        texto += saques.texto_saque(saque)
        texto += "\n"

    bot.send_message(

        message.chat.id,

        texto,

        reply_markup=teclado.menu_saques()

    )


# ==================================================
# CADASTRAR PIX
# ==================================================

@bot.message_handler(func=lambda message: message.text == "➕ Cadastrar PIX")
def cadastrar_pix(message):

    estado.definir_estado(

        message.from_user.id,

        "AGUARDANDO_PIX"

    )

    bot.send_message(

        message.chat.id,

        """
💳 <b>CADASTRAR PIX</b>

━━━━━━━━━━━━━━━━━━

Envie sua chave PIX.

Pode ser:

• CPF

• E-mail

• Telefone

• Chave Aleatória
""",

        reply_markup=teclado.menu_pix()

    )


# ==================================================
# REMOVER PIX
# ==================================================

@bot.message_handler(func=lambda message: message.text == "🗑 Remover PIX")
def remover_pix(message):

    if pix.remover_pix(message.from_user.id):

        bot.send_message(

            message.chat.id,

            "✅ PIX removido com sucesso.",

            reply_markup=teclado.menu_pix()

        )

    else:

        bot.send_message(

            message.chat.id,

            "❌ Você não possui PIX cadastrado.",

            reply_markup=teclado.menu_pix()

        )


# ==================================================
# HISTÓRICO DA CARTEIRA
# ==================================================

@bot.message_handler(func=lambda message: message.text == "📄 Extrato")
def extrato(message):

    historico = carteira.historico_resumido(
        message.from_user.id
    )

    if not historico:

        bot.send_message(

            message.chat.id,

            "Nenhuma movimentação encontrada.",

            reply_markup=teclado.menu_carteira()

        )

        return

    texto = "📄 <b>ÚLTIMAS MOVIMENTAÇÕES</b>\n\n"

    for item in historico:

        texto += (
            f"{item['tipo']} | "
            f"R$ {float(item['valor']):.2f}\n"
        )

    bot.send_message(

        message.chat.id,

        texto,

        reply_markup=teclado.menu_carteira()

    )

# ==================================================
# PROCESSADOR DE ESTADOS
# ==================================================

@bot.message_handler(func=lambda message: True)
def mensagens(message):

    # Processa estados temporários
    if estado.processar_estado(bot, message):
        return

    # Caso a mensagem não pertença a nenhum estado,
    # ela simplesmente será ignorada por enquanto.
    return
 

# ==================================================
# INICIAR BOT
# ==================================================

def iniciar_bot():

    print("=" * 60)
    print(f"🐶 {NOME_BOT}")
    print("🚀 Inicializando...")
    print("=" * 60)

    print("✅ Config carregada")
    print("✅ Banco conectado")
    print("✅ Módulos carregados")
    print("✅ Bot iniciado")

    bot.infinity_polling(
        skip_pending=True,
        timeout=30,
        long_polling_timeout=30
    )

# ==================================================
# /START
# ==================================================

@bot.message_handler(commands=["start"])
def comando_start(message):

    user = message.from_user

    # =============================================
    # CADASTRA O USUÁRIO
    # =============================================

    usuarios.cadastrar_usuario(user)

    # =============================================
    # ATUALIZA DADOS
    # =============================================

    usuarios.atualizar_usuario(user)

    # =============================================
    # LIMPA QUALQUER ESTADO
    # =============================================

    estado.limpar_estado(user.id)

    # =============================================
    # PROCESSA LINK DE INDICAÇÃO
    # =============================================

    argumentos = message.text.split()

    if len(argumentos) > 1:

        parametro = argumentos[1]

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

                try:

                    usuarios.registrar_indicacao(

                        indicador["id"],

                        user.id

                    )

                except Exception as erro:

                    print(
                        "Erro na indicação:",
                        erro
                    )

    # =============================================
    # BUSCA O USUÁRIO
    # =============================================

    usuario = usuarios.obter_usuario(
        user.id
    )

    # =============================================
    # MENSAGEM
    # =============================================

    texto = f"""
🐶 <b>{NOME_BOT}</b>

Olá,
<b>{usuario['nome']}</b>!

Seja bem-vindo à plataforma.

Escolha uma opção abaixo.
"""

    bot.send_message(

        chat_id=message.chat.id,

        text=texto,

        reply_markup=teclado.menu_principal()

    )

# ==================================================
# /ADMIN
# ==================================================

@bot.message_handler(commands=["admin"])
def comando_admin(message):

    if message.from_user.id not in ADMIN_IDS:

        bot.send_message(

            message.chat.id,

            "❌ Você não possui permissão."

        )

        return

    bot.send_message(

        message.chat.id,

        "👑 Painel Administrativo",

        reply_markup=admin_menu.menu_admin()

    )
