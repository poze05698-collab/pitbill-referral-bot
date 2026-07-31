"""
=========================================
 PITBULL REWARDS PLATFORM V3
 pix.py
=========================================
"""

from database import conn, cursor
from usuarios import (
    buscar_usuario,
    limpar_cache
)

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

limpar_cache(usuario_id)

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
# ==========================================
# VALIDAÇÃO DA CHAVE PIX
# ==========================================

def validar_pix(chave):

    chave = chave.strip()

    if len(chave) < 5:
        return False

    if len(chave) > 120:
        return False

    return True
