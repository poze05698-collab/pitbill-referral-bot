"""
=========================================
 PITBULL REWARDS PLATFORM V2
 teclado.py
=========================================
"""

from telebot.types import ReplyKeyboardMarkup
from telebot.types import KeyboardButton

# ==========================================
# MENU PRINCIPAL
# ==========================================

def menu_principal():

    menu = ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2
    )

    menu.add(

        KeyboardButton("👤 Perfil"),
        KeyboardButton("💰 Carteira")

    )

    menu.add(

        KeyboardButton("👥 Convidar Amigos"),
        KeyboardButton("🎁 Bônus Diário")

    )

    menu.add(

        KeyboardButton("🎡 Roleta"),
        KeyboardButton("🎫 Raspadinha")

    )

    menu.add(

        KeyboardButton("🎯 Missões"),
        KeyboardButton("🏆 Ranking")

    )

    menu.add(

        KeyboardButton("💳 PIX"),
        KeyboardButton("💸 Solicitar Saque")

    )

    menu.add(

        KeyboardButton("🎫 Atendimento"),
        KeyboardButton("ℹ️ Informações")

    )

    return menu# ==========================================
# MENU ADMIN
# ==========================================

def menu_admin():

    menu = ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2
    )

    menu.add(

        KeyboardButton("👥 Usuários"),
        KeyboardButton("💸 Saques")

    )

    menu.add(

        KeyboardButton("🎫 Tickets"),
        KeyboardButton("📊 Estatísticas")

    )

    menu.add(

        KeyboardButton("🎯 Missões"),
        KeyboardButton("🎉 Eventos")

    )

    menu.add(

        KeyboardButton("🎡 Roleta"),
        KeyboardButton("🎫 Raspadinha")

    )

    menu.add(

        KeyboardButton("🏆 Ranking"),
        KeyboardButton("👑 VIP")

    )

    menu.add(

        KeyboardButton("💰 Carteira"),
        KeyboardButton("📢 Broadcast")

    )

    menu.add(

        KeyboardButton("⚙️ Configurações"),
        KeyboardButton("📜 Logs")

    )

    menu.add(

        KeyboardButton("🔄 Backup"),
        KeyboardButton("🛠️ Manutenção")

    )

    menu.add(

        KeyboardButton("🏠 Menu Principal")

    )

    return menu
