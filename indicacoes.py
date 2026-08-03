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

    return cursor.fetchall()from carteira import (
    adicionar_saldo_pendente,
    transferir_pendente_para_saldo
)# ==================================================
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
