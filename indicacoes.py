"""
==================================================
PITBULL REWARDS PLATFORM V3
INDICAÇÕES
==================================================
"""

from database import (
    conn,
    cursor,
    agora
)

from carteira import (
    registrar_extrato
)

# ==================================================
# BUSCAR INDICAÇÃO
# ==================================================

def obter_indicacao(indicado_id):

    cursor.execute("""

    SELECT *

    FROM indicacoes

    WHERE indicado_id=?

    """,(indicado_id,))

    return cursor.fetchone()


# ==================================================
# REGISTRAR INDICAÇÃO
# ==================================================

def registrar_indicacao(

    indicador_id,
    indicado_id,
    codigo_convite=""

):

    if indicador_id == indicado_id:
        return False

    if obter_indicacao(indicado_id):
        return False

    cursor.execute("""

    SELECT valor

    FROM configuracoes

    WHERE chave='valor_indicacao'

    """)

    config = cursor.fetchone()

    recompensa = 1.00

    if config:

        try:
            recompensa = float(config["valor"])
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

        codigo_convite,

        recompensa,

        "PENDENTE",

        data,

        data,

        data

    ))

    conn.commit()

    return True


# ==================================================
# LISTAR PENDENTES
# ==================================================

def listar_pendentes():

    cursor.execute("""

    SELECT *

    FROM indicacoes

    WHERE status='PENDENTE'

    ORDER BY id ASC

    """)

    from carteira import (
    adicionar_saldo_pendente,
    transferir_pendente_para_saldo
)
    
# ==================================================
# APROVAR INDICAÇÃO
# ==================================================

def aprovar_indicacao(indicado_id, admin_id):

    indicacao = obter_indicacao(indicado_id)

    if indicacao is None:

        return False, "❌ Indicação não encontrada."

    if indicacao["status"] != "PENDENTE":

        return False, "❌ Esta indicação já foi processada."

    # Credita o prêmio como saldo pendente

    adicionar_saldo_pendente(

        usuario_id=indicacao["indicador_id"],

        valor=indicacao["recompensa"],

        categoria="INDICACAO",

        descricao=f"Indicação aprovada #{indicacao['id']}",

        admin_id=admin_id

    )

    cursor.execute("""

    UPDATE indicacoes

    SET

        status='APROVADA',

        aprovado_por=?,

        data_aprovacao=?,

        updated_at=?

    WHERE id=?

    """,(

        admin_id,

        agora(),

        agora(),

        indicacao["id"]

    ))

    conn.commit()

    return True, "✅ Indicação aprovada com sucesso."


# ==================================================
# REJEITAR INDICAÇÃO
# ==================================================

def rejeitar_indicacao(indicado_id, admin_id, motivo=""):

    indicacao = obter_indicacao(indicado_id)

    if indicacao is None:

        return False, "❌ Indicação não encontrada."

    if indicacao["status"] != "PENDENTE":

        return False, "❌ Esta indicação já foi processada."

    cursor.execute("""

    UPDATE indicacoes

    SET

        status='REJEITADA',

        aprovado_por=?,

        motivo_rejeicao=?,

        data_rejeicao=?,

        updated_at=?

    WHERE id=?

    """,(

        admin_id,

        motivo,

        agora(),

        agora(),

        indicacao["id"]

    ))

    conn.commit()

    return True, "✅ Indicação rejeitada."

# ==================================================
# LISTAR INDICADOS
# ==================================================

def listar_indicados(indicador_id):

    cursor.execute("""

    SELECT

        u.id,

        u.nome,

        u.username,

        i.status,

        i.recompensa,

        i.data_cadastro,

        i.data_aprovacao

    FROM indicacoes i

    INNER JOIN usuarios u

        ON u.id=i.indicado_id

    WHERE i.indicador_id=?

    ORDER BY i.id DESC

    """,(indicador_id,))

    return cursor.fetchall()


# ==================================================
# TOTAL DE INDICAÇÕES
# ==================================================

def total_indicacoes(indicador_id):

    cursor.execute("""

    SELECT COUNT(*) total

    FROM indicacoes

    WHERE indicador_id=?

    """,(indicador_id,))

    return cursor.fetchone()["total"]


# ==================================================
# TOTAL APROVADAS
# ==================================================

def total_aprovadas(indicador_id):

    cursor.execute("""

    SELECT COUNT(*) total

    FROM indicacoes

    WHERE indicador_id=?

    AND status='APROVADA'

    """,(indicador_id,))

    return cursor.fetchone()["total"]


# ==================================================
# TOTAL PENDENTES
# ==================================================

def total_pendentes(indicador_id):

    cursor.execute("""

    SELECT COUNT(*) total

    FROM indicacoes

    WHERE indicador_id=?

    AND status='PENDENTE'

    """,(indicador_id,))

    return cursor.fetchone()["total"]


# ==================================================
# TOTAL REJEITADAS
# ==================================================

def total_rejeitadas(indicador_id):

    cursor.execute("""

    SELECT COUNT(*) total

    FROM indicacoes

    WHERE indicador_id=?

    AND status='REJEITADA'

    """,(indicador_id,))

    return cursor.fetchone()["total"]
    # ==================================================
# TEXTO DAS INDICAÇÕES
# ==================================================

def texto_indicacoes(usuario_id):

    total = total_indicacoes(usuario_id)

    aprovadas = total_aprovadas(usuario_id)

    pendentes = total_pendentes(usuario_id)

    rejeitadas = total_rejeitadas(usuario_id)

    texto = f"""
👥 <b>MINHAS INDICAÇÕES</b>

━━━━━━━━━━━━━━━━━━

👤 Total

{total}

✅ Aprovadas

{aprovadas}

⏳ Pendentes

{pendentes}

❌ Rejeitadas

{rejeitadas}

━━━━━━━━━━━━━━━━━━
"""

    return texto
