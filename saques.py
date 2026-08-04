"""
==================================================
PITBULL REWARDS PLATFORM V3
SAQUES
==================================================
"""

from database import (
    conn,
    cursor,
    agora
)

from carteira import (

    saldo,

    bloquear_saldo,

    desbloquear_saldo,

    confirmar_saldo_bloqueado,

    registrar_extrato

)

from pix import (

    obter_pix,

    pix_valido_para_saque

)

from config import (

    VALOR_MINIMO_SAQUE,

    VALOR_MAXIMO_SAQUE

)

# ==================================================
# BUSCAR SAQUE
# ==================================================

def obter_saque(saque_id):

    cursor.execute("""

    SELECT *

    FROM saques

    WHERE id=?

    """,(saque_id,))

    return cursor.fetchone()


# ==================================================
# LISTAR SAQUES
# ==================================================

def listar_saques(usuario_id):

    cursor.execute("""

    SELECT *

    FROM saques

    WHERE usuario_id=?

    ORDER BY id DESC

    """,(usuario_id,))

    return cursor.fetchall()# ==================================================
# SOLICITAR SAQUE
# ==================================================

def solicitar_saque(usuario_id, valor):

    try:
        valor = float(valor)

    except:

        return "❌ Valor inválido."

    # Valor mínimo

    if valor < VALOR_MINIMO_SAQUE:

        return f"❌ O valor mínimo para saque é R$ {VALOR_MINIMO_SAQUE:.2f}"

    # Valor máximo

    if valor > VALOR_MAXIMO_SAQUE:

        return f"❌ O valor máximo por saque é R$ {VALOR_MAXIMO_SAQUE:.2f}"

    # PIX

    if not pix_valido_para_saque(usuario_id):

        return "❌ Cadastre uma chave PIX válida antes de solicitar um saque."

    # Saldo

    if saldo(usuario_id) < valor:

        return "❌ Saldo insuficiente."

    # Bloqueia o saldo

    if not bloquear_saldo(usuario_id, valor):

        return "❌ Não foi possível bloquear o saldo."

    pix = obter_pix(usuario_id)

    data = agora()

    cursor.execute("""

    INSERT INTO saques(

        usuario_id,

        pix_id,

        valor,

        valor_liquido,

        status,

        data_solicitacao,

        created_at,

        updated_at

    )

    VALUES(?,?,?,?,?,?,?,?)

    """,(

        usuario_id,

        pix["id"],

        valor,

        valor,

        "PENDENTE",

        data,

        data,

        data

    ))

    saque_id = cursor.lastrowid

    conn.commit()

    registrar_extrato(

        usuario_id=usuario_id,

        tipo="SAIDA",

        categoria="SAQUE_PENDENTE",

        valor=valor,

        saldo_anterior=saldo(usuario_id)+valor,

        saldo_atual=saldo(usuario_id),

        descricao=f"Solicitação de saque #{saque_id}",

        referencia_id=saque_id,

        referencia_tabela="saques"

    )

    return (
        "✅ Solicitação enviada com sucesso!\n\n"
        "Seu saque ficará aguardando aprovação do administrador."
    )# ==================================================
# APROVAR SAQUE
# ==================================================

def aprovar_saque(saque_id, admin_id):

    saque = obter_saque(saque_id)

    if saque is None:
        return False, "❌ Saque não encontrado."

    if saque["status"] != "PENDENTE":
        return False, "❌ Este saque já foi processado."

    cursor.execute("""

    UPDATE saques

    SET

        status='APROVADO',

        admin_id=?,

        data_aprovacao=?,

        updated_at=?

    WHERE id=?

    """,(

        admin_id,

        agora(),

        agora(),

        saque_id

    ))

    conn.commit()

    return True, "✅ Saque aprovado com sucesso."


# ==================================================
# REJEITAR SAQUE
# ==================================================

def rejeitar_saque(saque_id, admin_id, motivo=""):

    saque = obter_saque(saque_id)

    if saque is None:
        return False, "❌ Saque não encontrado."

    if saque["status"] != "PENDENTE":
        return False, "❌ Este saque já foi processado."

    desbloquear_saldo(

        saque["usuario_id"],

        saque["valor"]

    )

    cursor.execute("""

    UPDATE saques

    SET

        status='REJEITADO',

        admin_id=?,

        observacao_admin=?,

        updated_at=?

    WHERE id=?

    """,(

        admin_id,

        motivo,

        agora(),

        saque_id

    ))

    conn.commit()

    return True, "✅ Saque rejeitado."


# ==================================================
# PAGAR SAQUE
# ==================================================

def pagar_saque(saque_id, admin_id):

    saque = obter_saque(saque_id)

    if saque is None:
        return False, "❌ Saque não encontrado."

    if saque["status"] != "APROVADO":
        return False, "❌ O saque precisa estar aprovado."

    confirmar_saldo_bloqueado(

    usuario_id=saque["usuario_id"],

    valor=saque["valor"],

    categoria="SAQUE",

    descricao=f"Saque #{saque_id}",

    admin_id=admin_id

)

    cursor.execute("""

    UPDATE saques

    SET

        status='PAGO',

        data_pagamento=?,

        updated_at=?

    WHERE id=?

    """,(

        agora(),

        agora(),

        saque_id

    ))

    conn.commit()

    return True, "✅ Saque pago com sucesso."


# ==================================================
# SAQUES PENDENTES
# ==================================================

def listar_saques_pendentes():

    cursor.execute("""

    SELECT *

    FROM saques

    WHERE status='PENDENTE'

    ORDER BY id ASC

    """)

    return cursor.fetchall()


# ==================================================
# TEXTO DO SAQUE
# ==================================================

def texto_saque(saque):

    return f"""
💸 <b>SAQUE #{saque['id']}</b>

━━━━━━━━━━━━━━━━━━

👤 Usuário
{saque['usuario_id']}

💰 Valor
R$ {float(saque['valor']):.2f}

📋 Status
{saque['status']}

📅 Solicitação
{saque['data_solicitacao']}

━━━━━━━━━━━━━━━━━━
"""

# ==================================================
# TELA DE SAQUES
# ==================================================

def texto_saques(usuario_id):

    saques = listar_saques(usuario_id)

    pix = obter_pix(usuario_id)

    saldo_disponivel = saldo(usuario_id)

    chave = "-"

    if pix:
        chave = pix["chave"]

    texto = f"""
💸 <b>SAQUES</b>

━━━━━━━━━━━━━━━━━━

💰 Saldo disponível

R$ {saldo_disponivel:.2f}

━━━━━━━━━━━━━━━━━━

💳 PIX

<code>{chave}</code>

━━━━━━━━━━━━━━━━━━

📉 Valor mínimo

R$ {VALOR_MINIMO_SAQUE:.2f}

📈 Valor máximo

R$ {VALOR_MAXIMO_SAQUE:.2f}

━━━━━━━━━━━━━━━━━━

📄 Total de solicitações

{len(saques)}

━━━━━━━━━━━━━━━━━━

Escolha uma opção abaixo.
"""

    return texto
