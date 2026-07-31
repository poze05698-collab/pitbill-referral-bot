"""
==================================================
PITBULL REWARDS PLATFORM V3
indicacoes.py
==================================================
"""

from database import conn, cursor, agora
from usuarios import (
    buscar_usuario,
    adicionar_saldo,
    adicionar_indicado,
    limpar_cache
)

# ==================================================
# CONFIGURAÇÃO
# ==================================================

VALOR_INDICACAO = 1.00

# ==================================================
# BUSCAR INDICAÇÃO
# ==================================================

def buscar_indicacao(indicado_id):

    cursor.execute("""

    SELECT *

    FROM indicacoes

    WHERE indicado_id=?

    """, (

        indicado_id,

    ))

    return cursor.fetchone()


# ==================================================
# REGISTRAR INDICAÇÃO
# ==================================================

def registrar_indicacao(indicador_id, indicado_id):

    # Não permite indicar a si mesmo
    if indicador_id == indicado_id:
        return False

    # Verifica se já existe indicação
    if buscar_indicacao(indicado_id):
        return False

    cursor.execute("""

    INSERT INTO indicacoes(

        indicador_id,

        indicado_id,

        recompensa,

        status,

        created_at

    )

    VALUES(

        ?,?,?,?,?

    )

    """, (

        indicador_id,

        indicado_id,

        VALOR_INDICACAO,

        "PENDENTE",

        agora()

    ))

    conn.commit()

    return True


# ==================================================
# APROVAR INDICAÇÃO
# ==================================================

def aprovar_indicacao(indicado_id):

    cursor.execute("""

    SELECT *

    FROM indicacoes

    WHERE indicado_id=?

    """, (

        indicado_id,

    ))

    registro = cursor.fetchone()

    if registro is None:

        return False

    if registro["status"] == "APROVADA":

        return False

    indicador = registro["indicador_id"]

    valor = registro["recompensa"]

    adicionar_saldo(

        indicador,

        valor,

        categoria="INDICACAO",

        descricao="Recompensa por indicação"

    )

    adicionar_indicado(indicador)

    cursor.execute("""

    UPDATE indicacoes

    SET

        status='APROVADA',

        approved_at=?

    WHERE indicado_id=?

    """, (

        agora(),

        indicado_id

    ))

    conn.commit()

    limpar_cache(indicador)

    return True
