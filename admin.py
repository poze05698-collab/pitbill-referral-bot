"""
==================================================
 PITBULL REWARDS PLATFORM V3
 admin.py
==================================================
"""

from database import (
    conn,
    cursor,
    agora,
    get_config,
    set_config,
    modulo_ativo,
    alterar_modulo
)

from usuarios import (
    buscar_usuario,
    aprovar_usuario,
    bloquear_usuario,
    desbloquear_usuario,
    banir_usuario,
    desbanir_usuario,
    registrar_log_admin
)

# ==================================================
# VERIFICAR ADMIN
# ==================================================

def admin_existe(usuario_id):

    cursor.execute("""

    SELECT *

    FROM admins

    WHERE

        usuario_id=?

        AND ativo=1

    """, (

        usuario_id,

    ))

    return cursor.fetchone()

# ==================================================
# CARGO
# ==================================================

def cargo_admin(usuario_id):

    admin = admin_existe(usuario_id)

    if admin:

        return admin["cargo"]

    return None

# ==================================================
# PERMISSÃO
# ==================================================

def tem_permissao(

    usuario_id,

    permissao

):

    admin = admin_existe(usuario_id)

    if admin is None:

        return False

    if admin["cargo"] == "OWNER":

        return True

    cursor.execute("""

    SELECT *

    FROM permissoes

    WHERE

        admin_id=?

        AND permissao=?

        AND permitido=1

    """, (

        admin["id"],

        permissao

    ))

    return cursor.fetchone() is not None# ==================================================
# CRIAR ADMINISTRADOR
# ==================================================

def criar_admin(

    owner_id,

    usuario_id,

    cargo="ADMIN"

):

    if not tem_permissao(owner_id, "admins"):

        return False

    if admin_existe(usuario_id):

        return False

    cursor.execute("""

    INSERT INTO admins(

        usuario_id,

        cargo,

        ativo,

        criado_por,

        created_at,

        updated_at

    )

    VALUES(

        ?,?,?,?, ?,?

    )

    """, (

        usuario_id,

        cargo,

        1,

        owner_id,

        agora(),

        agora()

    ))

    conn.commit()

    registrar_log_admin(

        owner_id,

        "CRIAR_ADMIN",

        "ADMIN",

        usuario_id,

        detalhes=f"Cargo: {cargo}"

    )

    return True


# ==================================================
# REMOVER ADMINISTRADOR
# ==================================================

def remover_admin(

    owner_id,

    usuario_id

):

    if not tem_permissao(owner_id, "admins"):

        return False

    cursor.execute("""

    DELETE FROM admins

    WHERE usuario_id=?

    """, (

        usuario_id,

    ))

    conn.commit()

    registrar_log_admin(

        owner_id,

        "REMOVER_ADMIN",

        "ADMIN",

        usuario_id

    )

    return True


# ==================================================
# ALTERAR CARGO
# ==================================================

def alterar_cargo(

    owner_id,

    usuario_id,

    novo_cargo

):

    if not tem_permissao(owner_id, "admins"):

        return False

    cursor.execute("""

    UPDATE admins

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

    registrar_log_admin(

        owner_id,

        "ALTERAR_CARGO",

        "ADMIN",

        usuario_id,

        detalhes=f"Novo cargo: {novo_cargo}"

    )

    return True


# ==================================================
# ATIVAR ADMIN
# ==================================================

def ativar_admin(

    owner_id,

    usuario_id

):

    if not tem_permissao(owner_id, "admins"):

        return False

    cursor.execute("""

    UPDATE admins

    SET

        ativo=1,

        updated_at=?

    WHERE usuario_id=?

    """, (

        agora(),

        usuario_id

    ))

    conn.commit()

    return True


# ==================================================
# DESATIVAR ADMIN
# ==================================================

def desativar_admin(

    owner_id,

    usuario_id

):

    if not tem_permissao(owner_id, "admins"):

        return False

    cursor.execute("""

    UPDATE admins

    SET

        ativo=0,

        updated_at=?

    WHERE usuario_id=?

    """, (

        agora(),

        usuario_id

    ))

    conn.commit()

    return True# ==================================================
# ADICIONAR PERMISSÃO
# ==================================================

def adicionar_permissao(

    owner_id,

    usuario_id,

    permissao

):

    if not tem_permissao(owner_id, "admins"):

        return False

    admin = admin_existe(usuario_id)

    if admin is None:

        return False

    cursor.execute("""

    INSERT OR IGNORE INTO permissoes(

        admin_id,

        permissao,

        permitido,

        created_at

    )

    VALUES(

        ?,?,?,?

    )

    """, (

        admin["id"],

        permissao,

        1,

        agora()

    ))

    conn.commit()

    registrar_log_admin(

        owner_id,

        "ADICIONAR_PERMISSAO",

        "PERMISSOES",

        usuario_id,

        detalhes=permissao

    )

    return True


# ==================================================
# REMOVER PERMISSÃO
# ==================================================

def remover_permissao(

    owner_id,

    usuario_id,

    permissao

):

    if not tem_permissao(owner_id, "admins"):

        return False

    admin = admin_existe(usuario_id)

    if admin is None:

        return False

    cursor.execute("""

    DELETE FROM permissoes

    WHERE

        admin_id=?

        AND permissao=?

    """, (

        admin["id"],

        permissao

    ))

    conn.commit()

    registrar_log_admin(

        owner_id,

        "REMOVER_PERMISSAO",

        "PERMISSOES",

        usuario_id,

        detalhes=permissao

    )

    return True


# ==================================================
# LISTAR PERMISSÕES
# ==================================================

def listar_permissoes(

    usuario_id

):

    admin = admin_existe(usuario_id)

    if admin is None:

        return []

    cursor.execute("""

    SELECT permissao

    FROM permissoes

    WHERE

        admin_id=?

        AND permitido=1

    ORDER BY permissao

    """, (

        admin["id"],

    ))

    return cursor.fetchall()


# ==================================================
# LISTAR ADMINISTRADORES
# ==================================================

def listar_admins():

    cursor.execute("""

    SELECT *

    FROM admins

    ORDER BY cargo

    """)

    return cursor.fetchall()


# ==================================================
# TOTAL ADMINISTRADORES
# ==================================================

def total_admins():

    cursor.execute("""

    SELECT COUNT(*) AS total

    FROM admins

    WHERE ativo=1

    """)

    resultado = cursor.fetchone()

    return resultado["total"]


# ==================================================
# FINAL
# ==================================================

print("✅ admin.py carregado com sucesso.")
