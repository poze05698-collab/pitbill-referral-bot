from telebot.types import ReplyKeyboardMarkup, KeyboardButton

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
        KeyboardButton("💰 Saldo")
    )

    menu.add(
        KeyboardButton("🔗 Meu Link"),
        KeyboardButton("👥 Indicados")
    )

    menu.add(
        KeyboardButton("💳 Pix"),
        KeyboardButton("💸 Solicitar Saque")
    )

    menu.add(
        KeyboardButton("📜 Histórico"),
        KeyboardButton("🏆 Ranking")
    )

    menu.add(
        KeyboardButton("📜 Regras"),
        KeyboardButton("ℹ️ Informações")
    )

    menu.add(
        KeyboardButton("📞 Suporte")
    )

    return menu


# ==========================================
# MENU ADMIN
# ==========================================

def menu_admin():

    menu = ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2
    )

    menu.add(
        KeyboardButton("📊 Estatísticas"),
        KeyboardButton("👥 Usuários")
    )

    menu.add(
        KeyboardButton("💸 Saques"),
        KeyboardButton("🏆 Ranking")
    )

    menu.add(
        KeyboardButton("➕ Adicionar Saldo"),
        KeyboardButton("➖ Remover Saldo")
    )

    menu.add(
        KeyboardButton("🚫 Banir"),
        KeyboardButton("✅ Desbanir")
    )

    menu.add(
        KeyboardButton("⚙️ Configurações")
    )

    menu.add(
        KeyboardButton("🏠 Menu")
    )

    return menu


# ==========================================
# MENU PIX
# ==========================================

def menu_pix():

    menu = ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2
    )

    menu.add(
        KeyboardButton("➕ Cadastrar Pix"),
        KeyboardButton("✏️ Alterar Pix")
    )

    menu.add(
        KeyboardButton("👁 Ver Pix")
    )

    menu.add(
        KeyboardButton("🏠 Menu")
    )

    return menu


# ==========================================
# MENU SAQUES
# ==========================================

def menu_saques():

    menu = ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2
    )

    menu.add(
        KeyboardButton("💸 Solicitar Saque")
    )

    menu.add(
        KeyboardButton("📜 Histórico")
    )

    menu.add(
        KeyboardButton("🏠 Menu")
    )

    return menu


# ==========================================
# MENU VOLTAR
# ==========================================

def menu_voltar():

    menu = ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    menu.add(
        KeyboardButton("🏠 Menu")
    )

    return menu
