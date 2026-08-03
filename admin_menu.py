"""
==================================================
PITBULL REWARDS PLATFORM V3
MENU ADMIN
==================================================
"""

from telebot.types import (

    InlineKeyboardMarkup,

    InlineKeyboardButton

)

# ==================================================
# MENU PRINCIPAL
# ==================================================

def menu_admin_principal():

    menu = InlineKeyboardMarkup(row_width=2)

    menu.add(

        InlineKeyboardButton(
            "👥 Usuários",
            callback_data="admin_usuarios"
        ),

        InlineKeyboardButton(
            "💰 Saques",
            callback_data="admin_saques"

        )

    )

    menu.add(

        InlineKeyboardButton(
            "🎁 Indicações",
            callback_data="admin_indicacoes"
        ),

        InlineKeyboardButton(
            "🛡 Anti-Fraude",
            callback_data="admin_antifraude"
        )

    )

    menu.add(

        InlineKeyboardButton(
            "📊 Estatísticas",
            callback_data="admin_estatisticas"
        ),

        InlineKeyboardButton(
            "📢 Broadcast",
            callback_data="admin_broadcast"
        )

    )

    menu.add(

        InlineKeyboardButton(
            "👑 Cargos",
            callback_data="admin_cargos"
        ),

        InlineKeyboardButton(
            "⚙️ Configurações",
            callback_data="admin_config"
        )

    )

    menu.add(

        InlineKeyboardButton(
            "📄 Logs",
            callback_data="admin_logs"
        ),

        InlineKeyboardButton(
            "🔧 Sistema",
            callback_data="admin_sistema"
        )

    )

    return menu# ==================================================
# MENU USUÁRIOS
# ==================================================

def menu_admin_usuarios():

    menu = InlineKeyboardMarkup(row_width=2)

    menu.add(

        InlineKeyboardButton(
            "🔍 Buscar",
            callback_data="adm_buscar_usuario"
        ),

        InlineKeyboardButton(
            "📋 Lista",
            callback_data="adm_lista_usuarios"
        )

    )

    menu.add(

        InlineKeyboardButton(
            "🚫 Banidos",
            callback_data="adm_banidos"
        ),

        InlineKeyboardButton(
            "⭐ VIP",
            callback_data="adm_vips"
        )

    )

    menu.add(

        InlineKeyboardButton(
            "💎 Premium",
            callback_data="adm_premium"
        )

    )

    menu.add(

        InlineKeyboardButton(
            "⬅️ Voltar",
            callback_data="admin_menu"
        )

    )

    return menu


# ==================================================
# MENU SAQUES
# ==================================================

def menu_admin_saques():

    menu = InlineKeyboardMarkup(row_width=2)

    menu.add(

        InlineKeyboardButton(
            "⏳ Pendentes",
            callback_data="adm_saques_pendentes"
        ),

        InlineKeyboardButton(
            "✅ Aprovados",
            callback_data="adm_saques_aprovados"
        )

    )

    menu.add(

        InlineKeyboardButton(
            "💸 Pagos",
            callback_data="adm_saques_pagos"
        ),

        InlineKeyboardButton(
            "❌ Rejeitados",
            callback_data="adm_saques_rejeitados"
        )

    )

    menu.add(

        InlineKeyboardButton(
            "⬅️ Voltar",
            callback_data="admin_menu"
        )

    )

    return menu


# ==================================================
# MENU INDICAÇÕES
# ==================================================

def menu_admin_indicacoes():

    menu = InlineKeyboardMarkup(row_width=2)

    menu.add(

        InlineKeyboardButton(
            "⏳ Pendentes",
            callback_data="adm_indicacoes_pendentes"
        ),

        InlineKeyboardButton(
            "✅ Aprovadas",
            callback_data="adm_indicacoes_aprovadas"
        )

    )

    menu.add(

        InlineKeyboardButton(
            "❌ Rejeitadas",
            callback_data="adm_indicacoes_rejeitadas"
        )

    )

    menu.add(

        InlineKeyboardButton(
            "⬅️ Voltar",
            callback_data="admin_menu"
        )

    )

    return menu
