"""
==================================================
PITBULL REWARDS PLATFORM V3
PIX
==================================================
"""

import re

from database import (
    conn,
    cursor,
    agora
)

# ==================================================
# OBTER PIX
# ==================================================

def obter_pix(usuario_id):

    cursor.execute("""

    SELECT *

    FROM pix

    WHERE usuario_id=?

    AND principal=1

    LIMIT 1

    """,(usuario_id,))

    return cursor.fetchone()


# ==================================================
# POSSUI PIX?
# ==================================================

def possui_pix(usuario_id):

    return obter_pix(usuario_id) is not None


# ==================================================
# CHAVE PIX
# ==================================================

def chave_pix(usuario_id):

    pix = obter_pix(usuario_id)

    if pix is None:
        return None

    return pix["chave"]


# ==================================================
# VALIDAR PIX
# ==================================================

def validar_pix(chave):

    chave = chave.strip()

    # CPF
    if chave.isdigit() and len(chave) == 11:
        return True

    # Telefone
    if chave.startswith("+") and len(chave) >= 12:
        return True

    # Email
    if re.match(
        r"^[^@]+@[^@]+\.[^@]+$",
        chave
    ):
        return True

    # Aleatória
    if len(chave) >= 32:
        return True

    return False# ==================================================
# CHAVE JÁ EXISTE?
# ==================================================

def chave_existente(chave, usuario_id=None):

    if usuario_id:

        cursor.execute("""

        SELECT usuario_id

        FROM pix

        WHERE chave=?

        AND usuario_id<>?

        AND status='ATIVO'

        """,(

            chave,

            usuario_id

        ))

    else:

        cursor.execute("""

        SELECT usuario_id

        FROM pix

        WHERE chave=?

        AND status='ATIVO'

        """,(

            chave,

        ))

    return cursor.fetchone() is not None


# ==================================================
# SALVAR PIX
# ==================================================

def salvar_pix(usuario_id, chave):

    chave = chave.strip()

    if not validar_pix(chave):
        return False

    if chave_existente(chave, usuario_id):
        return False

    # Descobre o tipo da chave

    if chave.isdigit() and len(chave) == 11:

        tipo = "CPF"

    elif chave.startswith("+"):

        tipo = "TELEFONE"

    elif "@" in chave:

        tipo = "EMAIL"

    else:

        tipo = "ALEATORIA"

    cursor.execute("""

    SELECT id

    FROM pix

    WHERE usuario_id=?

    AND principal=1

    """,(usuario_id,))

    registro = cursor.fetchone()

    if registro:

        cursor.execute("""

        UPDATE pix

        SET

            tipo=?,

            chave=?,

            status='ATIVO',

            updated_at=?

        WHERE usuario_id=?

        AND principal=1

        """,(

            tipo,

            chave,

            agora(),

            usuario_id

        ))

    else:

        cursor.execute("""

        INSERT INTO pix(

            usuario_id,

            tipo,

            chave,

            principal,

            status,

            created_at,

            updated_at

        )

        VALUES(?,?,?,?,?,?,?)

        """,(

            usuario_id,

            tipo,

            chave,

            1,

            "ATIVO",

            agora(),

            agora()

        ))

    conn.commit()

    return True# ==================================================
# REMOVER PIX
# ==================================================

def remover_pix(usuario_id):

    cursor.execute("""

    UPDATE pix

    SET

        status='REMOVIDO',

        principal=0,

        updated_at=?

    WHERE usuario_id=?

    AND principal=1

    """,(

        agora(),

        usuario_id

    ))

    conn.commit()

    return cursor.rowcount > 0


# ==================================================
# ALTERAR STATUS PIX
# ==================================================

def alterar_status_pix(usuario_id, status):

    cursor.execute("""

    UPDATE pix

    SET

        status=?,

        updated_at=?

    WHERE usuario_id=?

    AND principal=1

    """,(

        status,

        agora(),

        usuario_id

    ))

    conn.commit()

    return True


# ==================================================
# LISTAR CHAVES PIX
# ==================================================

def listar_chaves_pix(usuario_id):

    cursor.execute("""

    SELECT *

    FROM pix

    WHERE usuario_id=?

    ORDER BY principal DESC,id DESC

    """,(usuario_id,))

    return cursor.fetchall()


# ==================================================
# TEXTO PIX
# ==================================================

def texto_pix(usuario_id):

    pix = obter_pix(usuario_id)

    if pix is None:

        return """
💳 <b>PIX</b>

━━━━━━━━━━━━━━━━━━

Você ainda não cadastrou
uma chave PIX.

Envie sua chave para cadastrar.
"""

    texto = f"""
💳 <b>PIX CADASTRADO</b>

━━━━━━━━━━━━━━━━━━

📌 Tipo

{pix['tipo']}

━━━━━━━━━━━━━━━━━━

🔑 Chave

<code>{pix['chave']}</code>

━━━━━━━━━━━━━━━━━━

📋 Status

{pix['status']}

━━━━━━━━━━━━━━━━━━

🗓 Atualizado

{pix['updated_at'] or "-"}
"""

    return texto


# ==================================================
# PIX APTO PARA SAQUE
# ==================================================

def pix_valido_para_saque(usuario_id):

    pix = obter_pix(usuario_id)

    if pix is None:
        return False

    if pix["status"] != "ATIVO":
        return False

    if not pix["chave"]:
        return False

    return True
