"""
==================================================
PITBULL REWARDS PLATFORM V3
Admin Usuários
==================================================
"""

from telebot.types import ReplyKeyboardMarkup, KeyboardButton


# ==================================================
# MENU USUÁRIOS
# ==================================================

def menu_admin_usuarios():

    teclado = ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2
    )

    teclado.add(

        KeyboardButton("🔍 Buscar Usuário"),

        KeyboardButton("📋 Listar Usuários")

    )

    teclado.add(

        KeyboardButton("➕ Adicionar Saldo"),

        KeyboardButton("➖ Remover Saldo")

    )

    teclado.add(

        KeyboardButton("🚫 Banir"),

        KeyboardButton("✅ Desbanir")

    )

    teclado.add(

        KeyboardButton("📄 Histórico")

    )

    teclado.add(

        KeyboardButton("⬅️ Painel Admin")

    )

    return teclado
