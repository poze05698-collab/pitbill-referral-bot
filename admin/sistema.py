"""
==================================================
PITBULL REWARDS PLATFORM V3
Admin Sistema
==================================================
"""
from config import OWNER_ID
from database import conn, cursor, agora


# ==================================================
# CRIAR OWNER
# ==================================================

def criar_owner():

    cursor.execute("""

        SELECT *

        FROM administradores

        WHERE cargo='OWNER'

    """)

    owner = cursor.fetchone()

    if owner:

        return

    cursor.execute("""

        INSERT INTO administradores(

            usuario_id,

            cargo,

            status,

            criado_por,

            created_at,

            updated_at

        )

        VALUES(

            ?,?,?,?,?,?

        )

    """, (

        OWNER_ID,

        "OWNER",

        "ATIVO",

        OWNER_ID,

        agora(),

        agora()

    ))

    conn.commit()

    print("✅ OWNER criado automaticamente.")
