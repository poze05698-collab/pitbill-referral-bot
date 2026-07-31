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

WHERE usuario_id=?

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
# ==========================================
# SOLICITAR SAQUE
# ==========================================

def solicitar_saque(usuario_id, valor):

    usuario = buscar_usuario(usuario_id)

    if usuario is None:
        return "❌ Usuário não encontrado."
     
    # Verifica se possui PIX
    if not usuario["pix"]:
        return "❌ Você precisa cadastrar uma chave PIX primeiro."

    # Verifica saldo
    if float(usuario["saldo"]) < valor:
        return "❌ Saldo insuficiente."

    # Valor mínimo
    if valor < VALOR_MINIMO:
        return f"❌ O saque mínimo é R$ {VALOR_MINIMO:.2f}."

    cursor.execute("""

    INSERT INTO saques (

        usuario_id,

        valor,

        taxa,

        valor_liquido,

        chave_pix,

        status

    )

    VALUES (?, ?, ?, ?, ?, ?)

    """, (

        usuario_id,

        valor,

        0,

        valor,

        usuario["pix"],

        "PENDENTE"

    ))

    conn.commit()

    return "✅ Solicitação enviada com sucesso!"
