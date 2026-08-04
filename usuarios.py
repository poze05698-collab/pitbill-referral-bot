from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database import (
    conn,
    cursor,
    agora
)

from config import *

import random
import string
# =====================================================
# GERAR CÓDIGO
# =====================================================

def gerar_codigo():

    while True:

        codigo = "".join(
            random.choice(
                string.ascii_uppercase +
                string.digits
            )
            for _ in range(8)
        )

        cursor.execute(
            """
            SELECT id
            FROM usuarios
            WHERE codigo=?
            """,
            (codigo,)
        )

        if cursor.fetchone() is None:
            return codigo
         # =====================================================
# CADASTRAR USUÁRIO
# =====================================================

def cadastrar_usuario(user):

    cursor.execute(
        """
        SELECT *
        FROM usuarios
        WHERE id=?
        """,
        (user.id,)
    )

    if cursor.fetchone():
        return False

    codigo = gerar_codigo()

    data = agora()

    cursor.execute(
        """
        INSERT INTO usuarios(

            id,

            codigo,

            nome,

            username,

            status,

            created_at,

            updated_at

        )

        VALUES(?,?,?,?,?,?,?)

        """,

        (

            user.id,

            codigo,

            user.first_name,

            user.username,

            "ATIVO",

            data,

            data

        )

       )

    conn.commit()

    criar_estrutura_usuario(user.id)

    return True
# =====================================================
# ATUALIZAR USUÁRIO
# =====================================================

def atualizar_usuario(user):

    data = agora()

    cursor.execute(
        """
        UPDATE usuarios
        SET
            nome=?,
            username=?,
            ultimo_login=?,
            updated_at=?
        WHERE id=?
        """,
        (
            user.first_name,
            user.username,
            data,
            data,
            user.id
        )
    )

    conn.commit()

    return True
 # =====================================================
# BUSCAR USUÁRIO
# =====================================================

def obter_usuario(usuario_id):

    cursor.execute(

        """
        SELECT *

        FROM usuarios

        WHERE id=?

        """,

        (usuario_id,)

    )

    return cursor.fetchone()
 # =====================================================
# CRIAR ESTRUTURA DO USUÁRIO
# =====================================================

def criar_estrutura_usuario(usuario_id):

    data = agora()

    # Carteira
    cursor.execute("""
    INSERT OR IGNORE INTO carteira(
        usuario_id,
        created_at,
        updated_at
    )
    VALUES(?,?,?)
    """,(
        usuario_id,
        data,
        data
    ))

    # PIX
    cursor.execute("""
    INSERT OR IGNORE INTO pix(
        usuario_id,
        tipo,
        chave,
        status,
        created_at,
        updated_at
    )
    VALUES(?,?,?,?,?,?)
    """,(
        usuario_id,
        "",
        "",
        "SEM_CHAVE",
        data,
        data
    ))

    # Grupo
    cursor.execute("""
    INSERT OR IGNORE INTO grupo(
        usuario_id
    )
    VALUES(?)
    """,(
        usuario_id,
    ))

    # Canal
    cursor.execute("""
    INSERT OR IGNORE INTO canal(
        usuario_id
    )
    VALUES(?)
    """,(
        usuario_id,
    ))

    # Anti Fraude
    cursor.execute("""
    INSERT OR IGNORE INTO antifraude(
        usuario_id,
        score,
        created_at,
        updated_at
    )
    VALUES(?,?,?,?)
    """,(
        usuario_id,
        100,
        data,
        data
    ))

    conn.commit()

    return True
 # =====================================================
# PERFIL
# =====================================================

def texto_perfil(usuario_id):

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE id=?
    """, (usuario_id,))

    usuario = cursor.fetchone()

    cursor.execute("""
        SELECT *
        FROM carteira
        WHERE usuario_id=?
    """, (usuario_id,))

    carteira = cursor.fetchone()

    if usuario is None:
        return "❌ Usuário não encontrado."

    if carteira is None:
        return "❌ Carteira não encontrada."

    texto = f"""
👤 <b>MEU PERFIL</b>

━━━━━━━━━━━━━━

🆔 <b>ID:</b>
<code>{usuario['id']}</code>

👤 <b>Nome:</b>
{usuario['nome']}

🏷 <b>Usuário:</b>
@{usuario['username'] if usuario['username'] else "-"}

🎁 <b>Código:</b>
<code>{usuario['codigo']}</code>

━━━━━━━━━━━━━━

⭐ XP: {usuario['xp']}

🏆 Nível: {usuario['nivel']}

━━━━━━━━━━━━━━

💰 Saldo:
R$ {carteira['saldo']:.2f}

⏳ Pendente:
R$ {carteira['saldo_pendente']:.2f}

━━━━━━━━━━━━━━
"""

    return texto
 # =====================================================
# REGISTRAR INDICAÇÃO
# =====================================================

def registrar_indicacao(indicador_id, indicado_id):

    if indicador_id == indicado_id:
        return False

    cursor.execute("""
    SELECT id
    FROM indicacoes
    WHERE indicado_id=?
    """,(indicado_id,))

    if cursor.fetchone():
        return False

    cursor.execute("""
    SELECT valor
    FROM configuracoes
    WHERE chave='valor_indicacao'
    """)

    recompensa = cursor.fetchone()

    valor = 1.00

    if recompensa:
        try:
            valor = float(recompensa["valor"])
        except:
            pass

    data = agora()

    cursor.execute("""

    INSERT INTO indicacoes(

        indicador_id,

        indicado_id,

        codigo_convite,

        recompensa,

        status,

        data_cadastro,

        created_at,

        updated_at

    )

    VALUES(?,?,?,?,?,?,?,?)

    """,(

        indicador_id,

        indicado_id,

        "",

        valor,

        "PENDENTE",

        data,

        data,

        data

    ))

    conn.commit()

    return True
    # =====================================================
# LINK DE CONVITE
# =====================================================

def obter_link_convite(usuario_id):

    cursor.execute("""

    SELECT codigo

    FROM usuarios

    WHERE id=?

    """,(usuario_id,))

    usuario = cursor.fetchone()

    if usuario is None:
        return None

    return f"https://t.me/{BOT_USERNAME}?start=convite_{usuario['codigo']}"
 # =====================================================
# CONTAR INDICAÇÕES
# =====================================================

def total_indicacoes(usuario_id):

    cursor.execute("""

    SELECT COUNT(*) total

    FROM indicacoes

    WHERE indicador_id=?

    """,(usuario_id,))

    return cursor.fetchone()["total"]
 # =====================================================
# PENDENTES
# =====================================================

def indicacoes_pendentes(usuario_id):

    cursor.execute("""

    SELECT COUNT(*) total

    FROM indicacoes

    WHERE indicador_id=?

    AND status='PENDENTE'

    """,(usuario_id,))

    return cursor.fetchone()["total"]
 # =====================================================
# APROVADAS
# =====================================================

def indicacoes_aprovadas(usuario_id):

    cursor.execute("""

    SELECT COUNT(*) total

    FROM indicacoes

    WHERE indicador_id=?

    AND status='APROVADA'

    """,(usuario_id,))

    return cursor.fetchone()["total"]
    # =====================================================
# MENU PRINCIPAL
# =====================================================

def menu_principal():

    menu = InlineKeyboardMarkup(row_width=2)

    menu.add(

        InlineKeyboardButton(
            "👤 Perfil",
            callback_data="perfil"
        ),

        InlineKeyboardButton(
            "💰 Carteira",
            callback_data="carteira"
        )

    )

    menu.add(

        InlineKeyboardButton(
            "👥 Indicados",
            callback_data="indicados"
        ),

        InlineKeyboardButton(
            "🔗 Meu Link",
            callback_data="meulink"
        )

    )

    menu.add(

        InlineKeyboardButton(
            "💳 PIX",
            callback_data="pix"
        ),

        InlineKeyboardButton(
            "💸 Solicitar Saque",
            callback_data="saque"
        )

    )

    menu.add(

        InlineKeyboardButton(
            "📜 Histórico",
            callback_data="historico"
        )

    )

    return menu
    # =====================================================
# ENVIAR MENU
# =====================================================

def enviar_menu(bot, chat_id, usuario):

    texto = f"""
🐶 <b>{NOME_BOT}</b>

Olá, <b>{usuario['nome']}</b>!

Bem-vindo à plataforma.

Escolha uma opção abaixo.
"""

    bot.send_message(

        chat_id,

        texto,

        parse_mode="HTML",

        reply_markup=menu_principal()

    )
