"""
==================================================
PITBULL REWARDS PLATFORM V3
CARTEIRA
==================================================
"""

from database import (
    conn,
    cursor,
    agora
)

# ==================================================
# OBTER CARTEIRA
# ==================================================

def obter_carteira(usuario_id):

    cursor.execute("""
    SELECT *
    FROM carteira
    WHERE usuario_id=?
    """,(usuario_id,))

    return cursor.fetchone()


# ==================================================
# SALDO
# ==================================================

def saldo(usuario_id):

    carteira = obter_carteira(usuario_id)

    if carteira is None:
        return 0

    return float(carteira["saldo"])


# ==================================================
# SALDO PENDENTE
# ==================================================

def saldo_pendente(usuario_id):

    carteira = obter_carteira(usuario_id)

    if carteira is None:
        return 0

    return float(carteira["saldo_pendente"])


# ==================================================
# SALDO BLOQUEADO
# ==================================================

def saldo_bloqueado(usuario_id):

    carteira = obter_carteira(usuario_id)

    if carteira is None:
        return 0

    return float(carteira["saldo_bloqueado"])
    
# ==================================================
# ADICIONAR SALDO
# ==================================================

def adicionar_saldo(

    usuario_id,
    valor,
    categoria="GERAL",
    descricao="",
    admin_id=None

):

    if valor <= 0:
        return False

    carteira = obter_carteira(usuario_id)

    if carteira is None:
        return False

    saldo_anterior = float(carteira["saldo"])

    saldo_novo = saldo_anterior + valor

    cursor.execute("""

    UPDATE carteira

    SET

        saldo=?,

        total_recebido=total_recebido+?,

        updated_at=?,

        ultima_movimentacao=?

    WHERE usuario_id=?

    """,(

        saldo_novo,

        valor,

        agora(),

        agora(),

        usuario_id

    ))

    conn.commit()

    registrar_extrato(

        usuario_id=usuario_id,

        tipo="ENTRADA",

        categoria=categoria,

        valor=valor,

        saldo_anterior=saldo_anterior,

        saldo_atual=saldo_novo,

        descricao=descricao,

        admin_id=admin_id

    )

    return True


# ==================================================
# REMOVER SALDO
# ==================================================

def remover_saldo(

    usuario_id,
    valor,
    categoria="GERAL",
    descricao="",
    admin_id=None

):

    if valor <= 0:
        return False

    carteira = obter_carteira(usuario_id)

    if carteira is None:
        return False

    saldo_anterior = float(carteira["saldo"])

    if saldo_anterior < valor:
        return False

    saldo_novo = saldo_anterior - valor

    cursor.execute("""

    UPDATE carteira

    SET

        saldo=?,

        total_gasto=total_gasto+?,

        updated_at=?,

        ultima_movimentacao=?

    WHERE usuario_id=?

    """,(

        saldo_novo,

        valor,

        agora(),

        agora(),

        usuario_id

    ))

    conn.commit()

    registrar_extrato(

        usuario_id=usuario_id,

        tipo="SAIDA",

        categoria=categoria,

        valor=valor,

        saldo_anterior=saldo_anterior,

        saldo_atual=saldo_novo,

        descricao=descricao,

        admin_id=admin_id

    )

    return True# ==================================================
# REGISTRAR EXTRATO
# ==================================================

def registrar_extrato(

    usuario_id,
    tipo,
    categoria,
    valor,
    saldo_anterior,
    saldo_atual,
    descricao="",
    referencia_id=None,
    referencia_tabela=None,
    admin_id=None

):

    cursor.execute("""

    INSERT INTO extrato(

        usuario_id,

        tipo,

        categoria,

        valor,

        saldo_anterior,

        saldo_atual,

        descricao,

        referencia_id,

        referencia_tabela,

        admin_id,

        created_at

    )

    VALUES(?,?,?,?,?,?,?,?,?,?,?)

    """,(

        usuario_id,

        tipo,

        categoria,

        valor,

        saldo_anterior,

        saldo_atual,

        descricao,

        referencia_id,

        referencia_tabela,

        admin_id,

        agora()

    ))

    conn.commit()


# ==================================================
# BLOQUEAR SALDO
# ==================================================

def bloquear_saldo(usuario_id, valor):

    carteira = obter_carteira(usuario_id)

    if carteira is None:
        return False

    saldo = float(carteira["saldo"])

    if saldo < valor:
        return False

    cursor.execute("""

    UPDATE carteira

    SET

        saldo = saldo - ?,

        saldo_bloqueado = saldo_bloqueado + ?,

        updated_at = ?

    WHERE usuario_id=?

    """,(

        valor,

        valor,

        agora(),

        usuario_id

    ))

    conn.commit()

    return True


# ==================================================
# DESBLOQUEAR SALDO
# ==================================================

def desbloquear_saldo(usuario_id, valor):

    carteira = obter_carteira(usuario_id)

    if carteira is None:
        return False

    bloqueado = float(carteira["saldo_bloqueado"])

    if bloqueado < valor:
        return False

    cursor.execute("""

    UPDATE carteira

    SET

        saldo = saldo + ?,

        saldo_bloqueado = saldo_bloqueado - ?,

        updated_at = ?

    WHERE usuario_id=?

    """,(

        valor,

        valor,

        agora(),

        usuario_id

    ))

    conn.commit()

    return True


# ==================================================
# PENDENTE → SALDO
# ==================================================

def transferir_pendente_para_saldo(usuario_id):

    carteira = obter_carteira(usuario_id)

    if carteira is None:
        return False

    pendente = float(carteira["saldo_pendente"])

    if pendente <= 0:
        return False

    saldo_anterior = float(carteira["saldo"])

    saldo_novo = saldo_anterior + pendente

    cursor.execute("""

    UPDATE carteira

    SET

        saldo=?,

        saldo_pendente=0,

        updated_at=?,

        ultima_movimentacao=?

    WHERE usuario_id=?

    """,(

        saldo_novo,

        agora(),

        agora(),

        usuario_id

    ))

    conn.commit()

    registrar_extrato(

        usuario_id=usuario_id,

        tipo="ENTRADA",

        categoria="INDICACAO",

        valor=pendente,

        saldo_anterior=saldo_anterior,

        saldo_atual=saldo_novo,

        descricao="Saldo pendente aprovado"

    )

    return True# ==================================================
# TEXTO DA CARTEIRA
# ==================================================

def texto_carteira(usuario_id):

    carteira = obter_carteira(usuario_id)

    if carteira is None:

        return "❌ Carteira não encontrada."

    cursor.execute("""
    SELECT COUNT(*) total
    FROM extrato
    WHERE usuario_id=?
    """,(usuario_id,))

    total_mov = cursor.fetchone()["total"]

    texto = f"""
💰 <b>CARTEIRA</b>

━━━━━━━━━━━━━━━━━━

💵 Saldo Disponível

R$ {float(carteira["saldo"]):.2f}

━━━━━━━━━━━━━━━━━━

⏳ Saldo Pendente

R$ {float(carteira["saldo_pendente"]):.2f}

━━━━━━━━━━━━━━━━━━

🔒 Saldo Bloqueado

R$ {float(carteira["saldo_bloqueado"]):.2f}

━━━━━━━━━━━━━━━━━━

📥 Total Recebido

R$ {float(carteira["total_recebido"]):.2f}

📤 Total Gasto

R$ {float(carteira["total_gasto"]):.2f}

🎁 Total Indicações

R$ {float(carteira["total_indicacoes"]):.2f}

━━━━━━━━━━━━━━━━━━

📄 Movimentações

{total_mov}

━━━━━━━━━━━━━━━━━━

🕒 Última movimentação

{carteira["ultima_movimentacao"] or "Nenhuma"}

"""

    return texto


# ==================================================
# HISTÓRICO RESUMIDO
# ==================================================

def historico_resumido(usuario_id, limite=10):

    cursor.execute("""
    SELECT *

    FROM extrato

    WHERE usuario_id=?

    ORDER BY id DESC

    LIMIT ?

    """,(usuario_id, limite))

    return cursor.fetchall()


# ==================================================
# TEM SALDO?
# ==================================================

def possui_saldo(usuario_id, valor):

    return saldo(usuario_id) >= valor


# ==================================================
# TEM SALDO PENDENTE?
# ==================================================

def possui_pendente(usuario_id):

    return saldo_pendente(usuario_id) > 0


# ==================================================
# TEM SALDO BLOQUEADO?
# ==================================================

def possui_bloqueado(usuario_id):

    return saldo_bloqueado(usuario_id) > 0

# ==================================================
# CONFIRMAR SAQUE
# ==================================================

def confirmar_saldo_bloqueado(

    usuario_id,
    valor,
    categoria="SAQUE",
    descricao="",
    admin_id=None

):

    carteira = obter_carteira(usuario_id)

    if carteira is None:
        return False

    bloqueado = float(carteira["saldo_bloqueado"])

    if bloqueado < valor:
        return False

    cursor.execute("""

    UPDATE carteira

    SET

        saldo_bloqueado = saldo_bloqueado - ?,

        total_saques = total_saques + ?,

        updated_at = ?,

        ultima_movimentacao = ?

    WHERE usuario_id=?

    """,(

        valor,

        valor,

        agora(),

        agora(),

        usuario_id

    ))

    conn.commit()

    registrar_extrato(

        usuario_id=usuario_id,

        tipo="SAIDA",

        categoria=categoria,

        valor=valor,

        saldo_anterior=float(carteira["saldo"]),

        saldo_atual=float(carteira["saldo"]),

        descricao=descricao,

        admin_id=admin_id

    )

    return True

# ==================================================
# ADICIONAR SALDO PENDENTE
# ==================================================

def adicionar_saldo_pendente(

    usuario_id,
    valor,
    categoria="GERAL",
    descricao="",
    admin_id=None

):

    if valor <= 0:
        return False

    carteira = obter_carteira(usuario_id)

    if carteira is None:
        return False

    saldo_pendente_anterior = float(carteira["saldo_pendente"])

    saldo_pendente_novo = saldo_pendente_anterior + valor

    cursor.execute("""

    UPDATE carteira

    SET

        saldo_pendente=?,

        total_indicacoes=total_indicacoes+?,

        updated_at=?,

        ultima_movimentacao=?

    WHERE usuario_id=?

    """,(

        saldo_pendente_novo,

        valor,

        agora(),

        agora(),

        usuario_id

    ))

    conn.commit()

    registrar_extrato(

        usuario_id=usuario_id,

        tipo="ENTRADA",

        categoria=categoria,

        valor=valor,

        saldo_anterior=saldo_pendente_anterior,

        saldo_atual=saldo_pendente_novo,

        descricao=descricao,

        admin_id=admin_id

    )

    return True
