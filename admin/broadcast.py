"""
==================================================
PITBULL REWARDS PLATFORM V3
ADMIN - BROADCAST
==================================================
"""

from database import (
    cursor
)

# ==================================================
# TODOS OS USUÁRIOS
# ==================================================

def usuarios_broadcast():

    cursor.execute("""
    SELECT id
    FROM usuarios
    WHERE banido=0
    ORDER BY id
    """)

    return [usuario["id"] for usuario in cursor.fetchall()]


# ==================================================
# USUÁRIOS ATIVOS
# ==================================================

def usuarios_ativos():

    cursor.execute("""
    SELECT id
    FROM usuarios
    WHERE status='ATIVO'
    AND banido=0
    ORDER BY id
    """)

    return [usuario["id"] for usuario in cursor.fetchall()]


# ==================================================
# USUÁRIOS VIP
# ==================================================

def usuarios_vip():

    cursor.execute("""
    SELECT u.id

    FROM usuarios u

    INNER JOIN vip v
        ON v.usuario_id=u.id

    WHERE
        u.banido=0
        AND v.ativo=1

    ORDER BY u.id
    """)

    return [usuario["id"] for usuario in cursor.fetchall()]

  # ==================================================
# USUÁRIOS PREMIUM
# ==================================================

def usuarios_premium():

    cursor.execute("""
    SELECT u.id

    FROM usuarios u

    INNER JOIN premium p
        ON p.usuario_id=u.id

    WHERE
        u.banido=0
        AND p.ativo=1

    ORDER BY u.id
    """)

    return [usuario["id"] for usuario in cursor.fetchall()]


# ==================================================
# USUÁRIOS BANIDOS
# ==================================================

def usuarios_banidos():

    cursor.execute("""
    SELECT id

    FROM usuarios

    WHERE banido=1

    ORDER BY id
    """)

    return [usuario["id"] for usuario in cursor.fetchall()]


# ==================================================
# ESTATÍSTICAS DO BROADCAST
# ==================================================

def estatisticas_broadcast():

    return {

        "todos": len(usuarios_broadcast()),

        "ativos": len(usuarios_ativos()),

        "vip": len(usuarios_vip()),

        "premium": len(usuarios_premium()),

        "banidos": len(usuarios_banidos())

    }

  # ==================================================
# TEXTO DO BROADCAST
# ==================================================

def texto_broadcast():

    dados = estatisticas_broadcast()

    texto = f"""
📢 <b>BROADCAST</b>

━━━━━━━━━━━━━━━━━━

👥 Total de usuários

<b>{dados['todos']}</b>

🟢 Usuários ativos

<b>{dados['ativos']}</b>

⭐ Usuários VIP

<b>{dados['vip']}</b>

💎 Usuários Premium

<b>{dados['premium']}</b>

🚫 Usuários banidos

<b>{dados['banidos']}</b>

━━━━━━━━━━━━━━━━━━

Escolha o público que receberá a mensagem.
"""

    return texto


# ==================================================
# DESTINATÁRIOS
# ==================================================

def obter_destinatarios(tipo):

    tipo = tipo.upper()

    if tipo == "TODOS":
        return usuarios_broadcast()

    elif tipo == "ATIVOS":
        return usuarios_ativos()

    elif tipo == "VIP":
        return usuarios_vip()

    elif tipo == "PREMIUM":
        return usuarios_premium()

    elif tipo == "BANIDOS":
        return usuarios_banidos()

    return []
