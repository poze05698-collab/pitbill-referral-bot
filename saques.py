"""
=========================================
 PITBULL REWARDS PLATFORM V3
 saques.py
=========================================
"""

from database import conn, cursor
from usuarios import buscar_usuario

# ==========================================
# CONFIGURAÇÕES
# ==========================================

VALOR_MINIMO = 20.00

# ==========================================
# CONSULTAR SAQUES
# ==========================================

def listar_saques(usuario_id):

    cursor.execute("""

    SELECT *

    FROM saques

    WHERE usuario=?

    ORDER BY id DESC

    """, (

        usuario_id,

    ))

    return cursor.fetchall()

# ==========================================
# VERIFICAR SALDO
# ==========================================

def saldo_disponivel(usuario_id):

    usuario = buscar_usuario(usuario_id)

    if usuario is None:
        return 0

    return float(usuario["saldo"])
