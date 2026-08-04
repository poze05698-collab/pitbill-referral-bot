"""
==================================================
PITBULL REWARDS PLATFORM V3
BOT PRINCIPAL
==================================================
"""

import telebot

from config import TOKEN

import usuarios
import carteira
import pix
import saques
import indicacoes

import grupo
import estado
import teclado
import utils

from admin import menu as admin_menu
from admin import usuarios as admin_usuarios
from admin import saques as admin_saques
from admin import indicacoes as admin_indicacoes
from admin import estatisticas as admin_estatisticas
from admin import broadcast as admin_broadcast

# =====================================================
# BOT
# =====================================================

bot = telebot.TeleBot(
    TOKEN,
    parse_mode="HTML"
)

# =====================================================
# MEMÓRIA
# =====================================================

estados = {}

cache = {}

# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================

def limpar_estado(usuario_id):

    estados.pop(usuario_id, None)


def definir_estado(usuario_id, estado):

    estados[usuario_id] = estado


def obter_estado(usuario_id):

    return estados.get(usuario_id)


# =====================================================
# INICIALIZAÇÃO
# =====================================================

def iniciar_bot():

    print("=" * 60)
    print("🐶 PITBULL REWARDS PLATFORM V3")
    print("🚀 Inicializando Bot...")
    print("=" * 60)

    print("✅ Banco conectado")
    print("✅ Módulos carregados")
    print("✅ Bot iniciado")

    bot.infinity_polling(
        skip_pending=True,
        timeout=30,
        long_polling_timeout=30
    )

# =====================================================
# /START
# =====================================================

@bot.message_handler(commands=["start"])
def comando_start(message):

    user = message.from_user
    usuario_id = user.id

    # Cadastra o usuário caso ainda não exista
    usuarios.cadastrar_usuario(user)

    # Atualiza nome, username e último acesso
    usuarios.atualizar_usuario(user)

    # Limpa qualquer estado pendente
    limpar_estado(usuario_id)

    # Processa link de indicação
    parametros = message.text.split()

    if len(parametros) > 1:

        argumento = parametros[1]

        if argumento.startswith("convite_"):

            codigo = argumento.replace("convite_", "")

            try:
                indicacoes.registrar_indicacao(
                    usuario_id,
                    codigo
                )

            except Exception as erro:
                print(f"Erro ao registrar indicação: {erro}")

    texto = f"""
🐶 <b>Bem-vindo ao PITBULL REWARDS PLATFORM</b>

Olá, <b>{user.first_name}</b>!

Sua conta foi carregada com sucesso.

Escolha uma opção no menu abaixo.
"""

    bot.send_message(

        chat_id=message.chat.id,

        text=texto,

        reply_markup=teclado.menu_principal()

    )

    
