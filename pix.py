"""
=========================================
 PITBULL REWARDS PLATFORM V3
 pix.py
=========================================
"""

from database import conn, cursor
from usuarios import buscar_usuario

# ==========================================
# CONSULTAR PIX
# ==========================================

def obter_pix(usuario_id):

    usuario = buscar_usuario(usuario_id)

    if usuario is None:
        return None

    return usuario["pix"]

# ==========================================
# SALVAR PIX
# ==========================================

def salvar_pix(usuario_id, chave):

    cursor.execute("""

    UPDATE usuarios

    SET pix=?

    WHERE id=?

    """, (

        chave,

        usuario_id

    ))

    conn.commit()

    return True

# ==========================================
# TEXTO DO PIX
# ==========================================

def texto_pix(usuario_id):

    chave = obter_pix(usuario_id)

    if not chave:

        chave = "Nenhuma chave cadastrada."

    return f"""
💳 <b>MINHA CHAVE PIX</b>

━━━━━━━━━━━━━━━━━━

Sua chave atual:

<code>{chave}</code>

━━━━━━━━━━━━━━━━━━

Envie uma nova chave PIX para cadastrá-la.
"""
