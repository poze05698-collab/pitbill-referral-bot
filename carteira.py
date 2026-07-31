"""
==================================================
 PITBULL REWARDS PLATFORM V3
 carteira.py
==================================================
"""

from database import cursor
from usuarios import buscar_usuario

# ==================================================
# RESUMO DA CARTEIRA
# ==================================================

def resumo_carteira(usuario_id):

    usuario = buscar_usuario(usuario_id)

    if usuario is None:
        return None

    return {
        "saldo": float(usuario["saldo"]),
        "saldo_pendente": float(usuario["saldo_pendente"]),
        "saldo_bloqueado": float(usuario["saldo_bloqueado"]),
        "total_ganho": float(usuario["total_ganho"]),
        "total_sacado": float(usuario["total_sacado"])
    }

# ==================================================
# EXTRATO
# ==================================================

def extrato(usuario_id, limite=10):

    cursor.execute("""

    SELECT *

    FROM extrato

    WHERE usuario_id=?

    ORDER BY id DESC

    LIMIT ?

    """, (

        usuario_id,

        limite

    ))

    return cursor.fetchall()# ==================================================
# ÚLTIMAS MOVIMENTAÇÕES
# ==================================================

def ultimas_movimentacoes(usuario_id, limite=5):

    cursor.execute("""

    SELECT

        tipo,
        categoria,
        valor,
        descricao,
        created_at

    FROM extrato

    WHERE usuario_id=?

    ORDER BY id DESC

    LIMIT ?

    """, (

        usuario_id,
        limite

    ))

    return cursor.fetchall()


# ==================================================
# MENSAGEM DA CARTEIRA
# ==================================================

def texto_carteira(usuario_id):

    dados = resumo_carteira(usuario_id)

    if dados is None:

        return "❌ Carteira não encontrada."

    texto = f"""
💰 <b>MINHA CARTEIRA</b>

━━━━━━━━━━━━━━━━━━

💵 Saldo disponível:
R$ {dados['saldo']:.2f}

⏳ Saldo pendente:
R$ {dados['saldo_pendente']:.2f}

🔒 Saldo bloqueado:
R$ {dados['saldo_bloqueado']:.2f}

📈 Total ganho:
R$ {dados['total_ganho']:.2f}

📉 Total sacado:
R$ {dados['total_sacado']:.2f}

━━━━━━━━━━━━━━━━━━

📄 Últimas movimentações:

"""

    movimentacoes = ultimas_movimentacoes(usuario_id)

    if not movimentacoes:

        texto += "\nNenhuma movimentação encontrada."

    else:

        for mov in movimentacoes:

            texto += (
                f"\n• {mov['categoria']} | "
                f"R$ {mov['valor']:.2f}"
            )

    return texto
