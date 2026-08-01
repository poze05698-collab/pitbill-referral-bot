"""
==================================================
PITBULL REWARDS PLATFORM V3
Admin Cargos
==================================================
"""
from database import conn, cursor, agora

# ==========================================
# ADICIONAR ADMINISTRADOR
# ==========================================

def adicionar_administrador(usuario_id, cargo, criado_por):

    cursor.execute("""

        SELECT id

        FROM administradores

        WHERE usuario_id=?

    """, (usuario_id,))

    if cursor.fetchone():

        return False, "Este usuário já é administrador."

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

        usuario_id,

        cargo,

        "ATIVO",

        criado_por,

        agora(),

        agora()

    ))

    conn.commit()

    return True, "Administrador adicionado com sucesso."


# ==========================================
# LISTAR ADMINISTRADORES
# ==========================================

def listar_administradores():

    cursor.execute("""

        SELECT *

        FROM administradores

        ORDER BY cargo, usuario_id

    """)

    return cursor.fetchall()


# ==========================================
# BUSCAR ADMINISTRADOR
# ==========================================

def buscar_administrador(usuario_id):

    cursor.execute("""

        SELECT *

        FROM administradores

        WHERE usuario_id=?

    """, (usuario_id,))

    return cursor.fetchone()


# ==========================================
# REMOVER ADMINISTRADOR
# ==========================================

def remover_administrador(usuario_id):

    cursor.execute("""

        DELETE FROM administradores

        WHERE usuario_id=?

    """, (usuario_id,))

    conn.commit()

    return True


# ==========================================
# ALTERAR CARGO
# ==========================================

def alterar_cargo(usuario_id, novo_cargo):

    cursor.execute("""

        UPDATE administradores

        SET

            cargo=?,

            updated_at=?

        WHERE usuario_id=?

    """, (

        novo_cargo,

        agora(),

        usuario_id

    ))

    conn.commit()

    return True


# ==========================================
# ATIVAR ADMINISTRADOR
# ==========================================

def ativar_administrador(usuario_id):

    cursor.execute("""

        UPDATE administradores

        SET

            status='ATIVO',

            updated_at=?

        WHERE usuario_id=?

    """, (

        agora(),

        usuario_id

    ))

    conn.commit()

    return True


# ==========================================
# DESATIVAR ADMINISTRADOR
# ==========================================

def desativar_administrador(usuario_id):

    cursor.execute("""

        UPDATE administradores

        SET

            status='INATIVO',

            updated_at=?

        WHERE usuario_id=?

    """, (

        agora(),

        usuario_id

    ))

    conn.commit()

    return True
