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

from config import TOKEN

from database import (
    cursor
)

import teclado

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
# MEMÓRIA
# ==================================================

estados = {}

cache = {}

# ==================================================
# CONTROLE DE ESTADOS
# ==================================================

def definir_estado(usuario_id, estado):

    estados[usuario_id] = estado


def obter_estado(usuario_id):

    return estados.get(usuario_id)


def limpar_estado(usuario_id):

    estados.pop(usuario_id, None)


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
# PROCESSAR ESTADOS
# ==================================================

@bot.message_handler(func=lambda message: True)
def processar_estados(message):

    estado = obter_estado(
        message.from_user.id
    )

    # ------------------------------------------
    # AGUARDANDO VALOR DO SAQUE
    # ------------------------------------------

    if estado == "AGUARDANDO_VALOR_SAQUE":

        limpar_estado(
            message.from_user.id
        )

        resposta = saques.solicitar_saque(

            usuario_id=message.from_user.id,

            valor=message.text

        )

        bot.send_message(

            message.chat.id,

            resposta,

            reply_markup=teclado.menu_saques()

        )

        return

# ==================================================
# INICIAR BOT
# ==================================================

def iniciar_bot():

    print()

    print("=" * 60)

    print("🐶 PITBULL REWARDS PLATFORM V3")

    print("🚀 Inicializando...")

    print("=" * 60)

    print("✅ Config carregada")

    print("✅ Banco conectado")

    print("✅ Módulos carregados")

    print()

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

    # ----------------------------------------------
    # CADASTRA O USUÁRIO
    # ----------------------------------------------

    usuarios.cadastrar_usuario(user)

    # ----------------------------------------------
    # ATUALIZA OS DADOS
    # ----------------------------------------------

    usuarios.atualizar_usuario(user)

    # ----------------------------------------------
    # LIMPA ESTADOS
    # ----------------------------------------------

    limpar_estado(user.id)

    # ----------------------------------------------
    # PROCESSA LINK DE CONVITE
    # ----------------------------------------------

    argumentos = message.text.split()

    if len(argumentos) > 1:

        parametro = argumentos[1]

        if parametro.startswith("convite_"):

            codigo = parametro.replace("convite_", "")

            try:

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

                    usuarios.registrar_indicacao(
                        indicador["id"],
                        user.id
                    )

            except Exception as erro:

                print(
                    f"Erro ao registrar indicação: {erro}"
                )

    # ----------------------------------------------
    # BUSCA O USUÁRIO
    # ----------------------------------------------

    usuario = usuarios.obter_usuario(user.id)

    # ----------------------------------------------
    # MENSAGEM
    # ----------------------------------------------

    texto = f"""
🐶 <b>{NOME_BOT}</b>

Olá,
<b>{usuario['nome']}</b>

Seja bem-vindo!

Escolha uma opção abaixo.
"""

    bot.send_message(

        message.chat.id,

        texto,

        reply_markup=teclado.menu_principal()

    )

# ==================================================
# MENU PRINCIPAL
# ==================================================

@bot.message_handler(func=lambda message: message.text == "👤 Perfil")
def menu_perfil(message):

    texto = usuarios.texto_perfil(
        message.from_user.id
    )

    bot.send_message(

        message.chat.id,

        texto,

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

        message.chat.id,

        texto,

        reply_markup=teclado.menu_carteira()

    )


# ==================================================
# CONVIDAR AMIGOS
# ==================================================

@bot.message_handler(func=lambda message: message.text == "👥 Convidar Amigos")
def menu_convites(message):

    link = usuarios.obter_link_convite(
        message.from_user.id
    )

    texto = f"""
👥 <b>CONVIDE SEUS AMIGOS</b>

Compartilhe seu link:

{link}
"""

    bot.send_message(

        message.chat.id,

        texto,

        reply_markup=teclado.menu_principal()

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

        message.chat.id,

        texto,

        reply_markup=teclado.menu_pix()

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

        message.chat.id,

        texto,

        reply_markup=teclado.menu_saques()

    )

# ==================================================
# NOVO SAQUE
# ==================================================

@bot.message_handler(func=lambda message: message.text == "💸 Novo Saque")
def novo_saque(message):

    definir_estado(
        message.from_user.id,
        "AGUARDANDO_VALOR_SAQUE"
    )

    bot.send_message(

        message.chat.id,

        """
💸 Informe o valor do saque.

Exemplo:

20
50
100
"""

    )


# ==================================================
# HISTÓRICO
# ==================================================

@bot.message_handler(func=lambda message: message.text == "📜 Histórico")
def historico_saques(message):

    lista = saques.listar_saques(
        message.from_user.id
    )

    if not lista:

        bot.send_message(

            message.chat.id,

            "Você ainda não possui saques."

        )

        return

    texto = "📜 <b>HISTÓRICO DE SAQUES</b>\n\n"

    for saque in lista[:10]:

        texto += saques.texto_saque(
            saque
        )

        texto += "\n"

    bot.send_message(

        message.chat.id,

        texto

    )


# ==================================================
# VOLTAR CARTEIRA
# ==================================================

@bot.message_handler(func=lambda message: message.text == "⬅️ Carteira")
def voltar_carteira(message):

    texto = carteira.texto_carteira(
        message.from_user.id
    )

    bot.send_message(

        message.chat.id,

        texto,

        reply_markup=teclado.menu_carteira()

    )

# ==================================================
# MENU PRINCIPAL
# ==================================================

@bot.message_handler(func=lambda message: message.text == "🏠 Menu Principal")
def voltar_menu(message):

    bot.send_message(

        message.chat.id,

        "🏠 Menu Principal",

        reply_markup=teclado.menu_principal()

    )

    
