"""
==================================================
 PITBULL REWARDS PLATFORM V3
 teclado.py
==================================================
"""

from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# ==================================================
# MENU DE ACESSO
# ==================================================

def menu_acesso():

    menu = ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    menu.row(

        KeyboardButton("📢 Entrar no Grupo")

    )

    menu.row(

        KeyboardButton("✅ Já Entrei")

    )

    return menu

# ==================================================
# MENU PRINCIPAL
# ==================================================

def menu_principal():

    menu = ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    menu.row(

        KeyboardButton("👤 Perfil"),

        KeyboardButton("💰 Carteira")

    )

    menu.row(

        KeyboardButton("👥 Convidar Amigos"),

        KeyboardButton("🏆 Ranking")

    )

    menu.row(

        KeyboardButton("🎁 Bônus Diário"),

        KeyboardButton("🎡 Roleta")

    )

    menu.row(

        KeyboardButton("🎫 Raspadinha"),

        KeyboardButton("🎯 Missões")

    )

    menu.row(

        KeyboardButton("🛒 Loja"),

        KeyboardButton("📦 Inventário")

    )

    menu.row(

        KeyboardButton("💳 PIX"),

        KeyboardButton("💸 Solicitar Saque")

    )

    menu.row(

        KeyboardButton("🎫 Atendimento"),

        KeyboardButton("🔔 Notificações")

    )

    menu.row(

        KeyboardButton("💎 Premium"),

        KeyboardButton("👑 VIP")

    )

    menu.row(

        KeyboardButton("ℹ️ Informações")

    )

    return menu# ==================================================
# MENU OWNER
# ==================================================

def menu_owner():

    menu = ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    menu.row(
        KeyboardButton("👥 Usuários"),
        KeyboardButton("👑 Administradores")
    )

    menu.row(
        KeyboardButton("💰 Financeiro"),
        KeyboardButton("📊 Estatísticas")
    )

    menu.row(
        KeyboardButton("⚙️ Configurações"),
        KeyboardButton("🧩 Módulos")
    )

    menu.row(
        KeyboardButton("🎟️ Cupons"),
        KeyboardButton("🎉 Eventos")
    )

    menu.row(
        KeyboardButton("💎 Premium"),
        KeyboardButton("👑 VIP")
    )

    menu.row(
        KeyboardButton("📢 Broadcast"),
        KeyboardButton("🎫 Tickets")
    )

    menu.row(
        KeyboardButton("💾 Backup"),
        KeyboardButton("📜 Logs")
    )

    menu.row(
        KeyboardButton("🏠 Menu Principal")
    )

    return menu

# ==================================================
# MENU ADMINISTRADOR
# ==================================================

def menu_admin():

    menu = ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    menu.row(
        KeyboardButton("👥 Usuários"),
        KeyboardButton("💸 Saques")
    )

    menu.row(
        KeyboardButton("👥 Indicações"),
        KeyboardButton("🎫 Tickets")
    )

    menu.row(
        KeyboardButton("📊 Estatísticas"),
        KeyboardButton("📢 Broadcast")
    )

    menu.row(
        KeyboardButton("🎉 Eventos"),
        KeyboardButton("🎟️ Cupons")
    )

    menu.row(
        KeyboardButton("⚙️ Configurações")
    )

    menu.row(
        KeyboardButton("🏠 Menu Principal")
    )

    return menu

# ==================================================
# MENU MODERADOR
# ==================================================

def menu_moderador():

    menu = ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    menu.row(
        KeyboardButton("👥 Aprovações"),
        KeyboardButton("🚫 Blacklist")
    )

    menu.row(
        KeyboardButton("🎫 Tickets"),
        KeyboardButton("👥 Usuários")
    )

    menu.row(
        KeyboardButton("🏠 Menu Principal")
    )

    return menu

# ==================================================
# MENU SUPORTE
# ==================================================

def menu_suporte():

    menu = ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    menu.row(
        KeyboardButton("🎫 Tickets")
    )

    menu.row(
        KeyboardButton("🏠 Menu Principal")
    )

    return menu# ==================================================
# MENU CONFIGURAÇÕES
# ==================================================

def menu_configuracoes():

    menu = ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    menu.row(
        KeyboardButton("📢 Grupo"),
        KeyboardButton("📣 Canal")
    )

    menu.row(
        KeyboardButton("💰 Indicações"),
        KeyboardButton("💸 Saques")
    )

    menu.row(
        KeyboardButton("💳 PIX"),
        KeyboardButton("💎 Premium")
    )

    menu.row(
        KeyboardButton("👑 VIP"),
        KeyboardButton("🎁 Bônus")
    )

    menu.row(
        KeyboardButton("🎡 Roleta"),
        KeyboardButton("🎫 Raspadinha")
    )

    menu.row(
        KeyboardButton("🎯 Missões"),
        KeyboardButton("🛒 Loja")
    )

    menu.row(
        KeyboardButton("🎉 Eventos"),
        KeyboardButton("🎟️ Cupons")
    )

    menu.row(
        KeyboardButton("🎁 Baús"),
        KeyboardButton("🎰 Jackpot")
    )

    menu.row(
        KeyboardButton("🎫 Tickets"),
        KeyboardButton("🔔 Notificações")
    )

    menu.row(
        KeyboardButton("🧩 Módulos"),
        KeyboardButton("🛡️ Segurança")
    )

    menu.row(
        KeyboardButton("⬅️ Painel Admin")
    )

    return menu# ==================================================
# MENU CARTEIRA
# ==================================================

def menu_carteira():

    menu = ReplyKeyboardMarkup(resize_keyboard=True)

    menu.row(
        KeyboardButton("📄 Extrato"),
        KeyboardButton("💸 Solicitar Saque")
    )

    menu.row(
        KeyboardButton("💳 PIX"),
        KeyboardButton("🏠 Menu Principal")
    )

    return menu


# ==================================================
# MENU PIX
# ==================================================

def menu_pix():

    menu = ReplyKeyboardMarkup(resize_keyboard=True)

    menu.row(
        KeyboardButton("➕ Cadastrar PIX"),
        KeyboardButton("✏️ Alterar PIX")
    )

    menu.row(
        KeyboardButton("👁️ Ver PIX"),
        KeyboardButton("⬅️ Carteira")
    )

    return menu


# ==================================================
# MENU SAQUES
# ==================================================

def menu_saques():

    menu = ReplyKeyboardMarkup(resize_keyboard=True)

    menu.row(
        KeyboardButton("💸 Novo Saque")
    )

    menu.row(
        KeyboardButton("📜 Histórico")
    )

    menu.row(
        KeyboardButton("⬅️ Carteira")
    )

    return menu


# ==================================================
# MENU PREMIUM
# ==================================================

def menu_premium():

    menu = ReplyKeyboardMarkup(resize_keyboard=True)

    menu.row(
        KeyboardButton("💎 Assinar Premium")
    )

    menu.row(
        KeyboardButton("🎁 Benefícios"),
        KeyboardButton("🎟️ Resgatar Cupom")
    )

    menu.row(
        KeyboardButton("📅 Minha Assinatura")
    )

    menu.row(
        KeyboardButton("🏠 Menu Principal")
    )

    return menu


# ==================================================
# MENU VIP
# ==================================================

def menu_vip():

    menu = ReplyKeyboardMarkup(resize_keyboard=True)

    menu.row(
        KeyboardButton("👑 Meu VIP")
    )

    menu.row(
        KeyboardButton("⭐ Benefícios"),
        KeyboardButton("🏆 Ranking VIP")
    )

    menu.row(
        KeyboardButton("🏠 Menu Principal")
    )

    return menu


# ==================================================
# MENU INVENTÁRIO
# ==================================================

def menu_inventario():

    menu = ReplyKeyboardMarkup(resize_keyboard=True)

    menu.row(
        KeyboardButton("🎁 Baús"),
        KeyboardButton("🎟️ Cupons")
    )

    menu.row(
        KeyboardButton("🎒 Meus Itens")
    )

    menu.row(
        KeyboardButton("🏠 Menu Principal")
    )

    return menu


# ==================================================
# MENU LOJA
# ==================================================

def menu_loja():

    menu = ReplyKeyboardMarkup(resize_keyboard=True)

    menu.row(
        KeyboardButton("🎡 Comprar Giros"),
        KeyboardButton("🎫 Comprar Raspadinhas")
    )

    menu.row(
        KeyboardButton("💎 Premium"),
        KeyboardButton("👑 VIP")
    )

    menu.row(
        KeyboardButton("🎁 Baús")
    )

    menu.row(
        KeyboardButton("🏠 Menu Principal")
    )

    return menu


# ==================================================
# MENU EVENTOS
# ==================================================

def menu_eventos():

    menu = ReplyKeyboardMarkup(resize_keyboard=True)

    menu.row(
        KeyboardButton("🎉 Eventos Ativos")
    )

    menu.row(
        KeyboardButton("🏆 Recompensas")
    )

    menu.row(
        KeyboardButton("🏠 Menu Principal")
    )

    return menu


# ==================================================
# MENU TICKETS
# ==================================================

def menu_tickets():

    menu = ReplyKeyboardMarkup(resize_keyboard=True)

    menu.row(
        KeyboardButton("➕ Abrir Ticket")
    )

    menu.row(
        KeyboardButton("📂 Meus Tickets")
    )

    menu.row(
        KeyboardButton("🏠 Menu Principal")
    )

    return menu
