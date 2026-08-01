"""
==================================================
PITBULL REWARDS PLATFORM V3
Admin Menu
==================================================
"""

from telebot.types import ReplyKeyboardMarkup, KeyboardButton


# ==================================================
# MENU ADMIN
# ==================================================

def menu_admin_principal():

    teclado = ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2
    )

    teclado.add(

        KeyboardButton("👥 Usuários"),

        KeyboardButton("👥 Indicações")

    )

    teclado.add(

        KeyboardButton("💸 Saques"),

        KeyboardButton("👨‍💼 Administradores")

    )

    teclado.add(

        KeyboardButton("⚙️ Configurações"),

        KeyboardButton("📊 Estatísticas")

    )

    teclado.add(

        KeyboardButton("📋 Logs"),

        KeyboardButton("📢 Broadcast")

    )

    teclado.add(

        KeyboardButton("🛡️ Anti-Fraude")

    )

    teclado.add(

        KeyboardButton("⬅️ Voltar")

    )

    return teclado
