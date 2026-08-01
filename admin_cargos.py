"""
==================================================
PITBULL REWARDS PLATFORM V3
Sistema de Cargos
==================================================
"""

from database import cursor

# ==========================================
# CARGOS
# ==========================================

OWNER = "OWNER"
ADMIN = "ADMIN"
MODERADOR = "MODERADOR"
SUPORTE = "SUPORTE"

# ==========================================
# BUSCAR CARGO
# ==========================================

def obter_cargo(usuario_id):

    cursor.execute("""

        SELECT cargo

        FROM usuarios

        WHERE id=?

    """, (usuario_id,))

    usuario = cursor.fetchone()

    if usuario is None:

        return None

    cargo = usuario["cargo"]

    if cargo is None:

        return None

    return cargo

# ==========================================
# VERIFICAR CARGO
# ==========================================

def is_owner(usuario_id):

    return obter_cargo(usuario_id) == OWNER


def is_admin(usuario_id):

    cargo = obter_cargo(usuario_id)

    return cargo in [

        OWNER,

        ADMIN

    ]


def is_moderador(usuario_id):

    cargo = obter_cargo(usuario_id)

    return cargo in [

        OWNER,

        ADMIN,

        MODERADOR

    ]


def is_suporte(usuario_id):

    cargo = obter_cargo(usuario_id)

    return cargo in [

        OWNER,

        ADMIN,

        MODERADOR,

        SUPORTE

    ]
