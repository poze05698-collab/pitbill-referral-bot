"""
==================================================
PITBULL REWARDS PLATFORM V3
ADMIN - LOGS
==================================================
"""

from database import (
    conn,
    cursor,
    agora
)

# ==================================================
# REGISTRAR LOG
# ==================================================

def registrar_log(

    admin_id,
    categoria,
    descricao,
    usuario_id=None

):

    data = agora()

    cursor.execute("""

    INSERT INTO logs(

        admin_id,

        usuario_id,

        categoria,

        descricao,

        created_at

    )

    VALUES(?,?,?,?,?)

    """,(

        admin_id,

        usuario_id,

        categoria,

        descricao,

        data

    ))

    conn.commit()

    return True


# ==================================================
# BUSCAR LOG
# ==================================================

def obter_log(log_id):

    cursor.execute("""

    SELECT *

    FROM logs

    WHERE id=?

    """,(log_id,))

    return cursor.fetchone()

  
