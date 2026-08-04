"""
=========================================
 PITBULL REWARDS PLATFORM V3
 Gerenciador de Estados
=========================================
"""

import teclado
import saques

# =========================================
# MEMÓRIA
# =========================================

_estados = {}


# =========================================
# DEFINIR
# =========================================

def definir_estado(usuario_id, estado):

    _estados[usuario_id] = estado


# =========================================
# OBTER
# =========================================

def obter_estado(usuario_id):

    return _estados.get(usuario_id)


# =========================================
# LIMPAR
# =========================================

def limpar_estado(usuario_id):

    _estados.pop(usuario_id, None)


# =========================================
# PROCESSADOR CENTRAL
# =========================================

def processar_estado(bot, message):

    estado = obter_estado(message.from_user.id)

    if estado is None:
        return False

    # =====================================
    # SAQUE
    # =====================================

    if estado == "AGUARDANDO_VALOR_SAQUE":

        limpar_estado(message.from_user.id)

        resposta = saques.solicitar_saque(

            usuario_id=message.from_user.id,

            valor=message.text

        )

        bot.send_message(

            message.chat.id,

            resposta,

            reply_markup=teclado.menu_saques()

        )

        return True

    return False

def processar_estado(bot, message):

    estado_atual = obter_estado(
        message.from_user.id
    )

    if estado_atual is None:
        return False

    # -----------------------------
    # CANCELAR
    # -----------------------------

    if message.text.lower() == "cancelar":

        limpar_estado(message.from_user.id)

        bot.send_message(

            message.chat.id,

            "✅ Operação cancelada.",

            reply_markup=teclado.menu_principal()

        )

        return True

    # -----------------------------
    # AGUARDANDO VALOR DO SAQUE
    # -----------------------------

    if estado_atual == "AGUARDANDO_VALOR_SAQUE":

        limpar_estado(message.from_user.id)

        resposta = saques.solicitar_saque(

            usuario_id=message.from_user.id,

            valor=message.text

        )

        bot.send_message(

            message.chat.id,

            resposta,

            reply_markup=teclado.menu_saques()

        )

        return True

    return False
