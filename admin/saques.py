"""
==================================================
PITBULL REWARDS PLATFORM V3
ADMIN - SAQUES
==================================================
"""

from database import (
    conn,
    cursor,
    agora
)

from saques import (

    obter_saque,

    aprovar_saque,

    rejeitar_saque,

    pagar_saque

)

# ==================================================
# SAQUES PENDENTES
# ==================================================

def saques_pendentes():

    cursor.execute("""

    SELECT

        s.*,

        u.nome,

        u.username

    FROM saques s

    INNER JOIN usuarios u

        ON u.id=s.usuario_id

    WHERE s.status='PENDENTE'

    ORDER BY s.id ASC

    """)

    return cursor.fetchall()


# ==================================================
# SAQUES APROVADOS
# ==================================================

def saques_aprovados():

    cursor.execute("""

    SELECT

        s.*,

        u.nome,

        u.username

    FROM saques s

    INNER JOIN usuarios u

        ON u.id=s.usuario_id

    WHERE s.status='APROVADO'

    ORDER BY s.id DESC

    """)

    return cursor.fetchall()

# ==================================================
# SAQUES PAGOS
# ==================================================

def saques_pagos():

    cursor.execute("""

    SELECT

        s.*,

        u.nome,

        u.username

    FROM saques s

    INNER JOIN usuarios u

        ON u.id=s.usuario_id

    WHERE s.status='PAGO'

    ORDER BY s.id DESC

    """)

    return cursor.fetchall()


# ==================================================
# SAQUES REJEITADOS
# ==================================================

def saques_rejeitados():

    cursor.execute("""

    SELECT

        s.*,

        u.nome,

        u.username

    FROM saques s

    INNER JOIN usuarios u

        ON u.id=s.usuario_id

    WHERE s.status='REJEITADO'

    ORDER BY s.id DESC

    """)

    return cursor.fetchall()

# ==================================================
# BUSCAR SAQUE
# ==================================================

def buscar_saque_admin(saque_id):

    cursor.execute("""

    SELECT

        s.*,

        u.nome,

        u.username,

        p.tipo,

        p.chave

    FROM saques s

    INNER JOIN usuarios u

        ON u.id=s.usuario_id

    LEFT JOIN pix p

        ON p.id=s.pix_id

    WHERE s.id=?

    """,(saque_id,))

    return cursor.fetchone()


# ==================================================
# TEXTO DO SAQUE
# ==================================================

def texto_saque_admin(saque_id):

    saque = buscar_saque_admin(saque_id)

    if saque is None:

        return "❌ Saque não encontrado."

    texto = f"""
💸 <b>DETALHES DO SAQUE</b>

━━━━━━━━━━━━━━━━━━

🆔 ID

{saque['id']}

👤 Usuário

{saque['nome']}

🏷 Username

@{saque['username'] or "-"}

━━━━━━━━━━━━━━━━━━

💰 Valor

R$ {float(saque['valor']):.2f}

💵 Valor Líquido

R$ {float(saque['valor_liquido']):.2f}

━━━━━━━━━━━━━━━━━━

💳 PIX

{saque['tipo'] or "-"}

<code>{saque['chave'] or "-"}</code>

━━━━━━━━━━━━━━━━━━

📌 Status

{saque['status']}

━━━━━━━━━━━━━━━━━━

📅 Solicitado

{saque['data_solicitacao']}

"""

    return texto

  # ==================================================
# APROVAR
# ==================================================

def admin_aprovar_saque(

    saque_id,
    admin_id

):

    return aprovar_saque(

        saque_id,

        admin_id

    )


# ==================================================
# REJEITAR
# ==================================================

def admin_rejeitar_saque(

    saque_id,
    admin_id,
    motivo=""

):

    return rejeitar_saque(

        saque_id,

        admin_id,

        motivo

    )


# ==================================================
# PAGAR
# ==================================================

def admin_pagar_saque(

    saque_id,
    admin_id

):

    return pagar_saque(

        saque_id,

        admin_id

    )

  # ==================================================
# ESTATÍSTICAS
# ==================================================

def estatisticas_saques():

    cursor.execute("""

    SELECT COUNT(*)

    FROM saques

    """)

    total = cursor.fetchone()[0]

    cursor.execute("""

    SELECT COUNT(*)

    FROM saques

    WHERE status='PENDENTE'

    """)

    pendentes = cursor.fetchone()[0]

    cursor.execute("""

    SELECT COUNT(*)

    FROM saques

    WHERE status='PAGO'

    """)

    pagos = cursor.fetchone()[0]

    return {

        "total": total,

        "pendentes": pendentes,

        "pagos": pagos

    }
