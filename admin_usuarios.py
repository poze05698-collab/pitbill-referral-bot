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
# ==================================================
# BUSCAR USUÁRIO
# ==================================================

from database import cursor

def buscar_usuario_admin(usuario_id):

    cursor.execute("""

        SELECT *

        FROM usuarios

        WHERE id=?

    """, (

        usuario_id,

    ))

    return cursor.fetchone()# ==================================================
# TEXTO DO USUÁRIO
# ==================================================

def texto_usuario_admin(usuario):

    if usuario is None:

        return "❌ Usuário não encontrado."

    return f"""
👤 <b>DADOS DO USUÁRIO</b>

━━━━━━━━━━━━━━━━━━

🆔 ID:
<code>{usuario['id']}</code>

👤 Nome:
{usuario['nome']}

🔖 Código:
<code>{usuario['codigo']}</code>

💰 Saldo:
R$ {usuario['saldo']:.2f}

👥 Indicados:
{usuario['indicados']}

⭐ Nível:
{usuario['nivel']}

🏆 XP:
{usuario['xp']}

👑 VIP:
{usuario['vip']}

💎 Premium:
{'Sim' if usuario['premium'] else 'Não'}

📢 Grupo:
{'✅ Sim' if usuario['grupo_verificado'] else '❌ Não'}

📣 Canal:
{'✅ Sim' if usuario['canal_verificado'] else '❌ Não'}

🚫 Banido:
{'✅ Sim' if usuario['banido'] else '❌ Não'}

━━━━━━━━━━━━━━━━━━
"""
