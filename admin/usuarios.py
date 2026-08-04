"""
==================================================
PITBULL REWARDS PLATFORM V3
ADMIN - USUÁRIOS
==================================================
"""

from database import (
    conn,
    cursor,
    agora
)

from carteira import (
    adicionar_saldo,
    remover_saldo,
    texto_carteira
)

from pix import (
    texto_pix
)

from indicacoes import (
    texto_indicacoes
)

# ==================================================
# BUSCAR POR ID
# ==================================================

def buscar_usuario_admin(usuario_id):

    cursor.execute("""

    SELECT *

    FROM usuarios

    WHERE id=?

    """,(usuario_id,))

    return cursor.fetchone()


# ==================================================
# BUSCAR POR USERNAME
# ==================================================

def buscar_username(username):

    username = username.replace("@","")

    cursor.execute("""

    SELECT *

    FROM usuarios

    WHERE username=?

    """,(username,))

    return cursor.fetchone()


# ==================================================
# USUÁRIO EXISTE?
# ==================================================

def usuario_existe(usuario_id):

   return buscar_usuario_admin(usuario_id) is not None


# ==================================================
# PERFIL ADMIN
# ==================================================
def texto_usuario_admin(usuario_id):

    usuario = buscar_usuario_admin(usuario_id)

    if usuario is None:

        return "❌ Usuário não encontrado."

    cursor.execute("""

    SELECT *

    FROM carteira

    WHERE usuario_id=?

    """,(usuario_id,))

    carteira = cursor.fetchone()

    saldo = 0

    pendente = 0

    bloqueado = 0

    if carteira:

        saldo = carteira["saldo"]

        pendente = carteira["saldo_pendente"]

        bloqueado = carteira["saldo_bloqueado"]

    texto = f"""
👤 <b>PERFIL DO USUÁRIO</b>

━━━━━━━━━━━━━━━━━━

🆔 ID

<code>{usuario["id"]}</code>

👤 Nome

{usuario["nome"]}

🏷 Username

@{usuario["username"] or "-"}

━━━━━━━━━━━━━━━━━━

📌 Status

{usuario["status"]}

🚫 Banido

{"SIM" if usuario["banido"] else "NÃO"}

━━━━━━━━━━━━━━━━━━

💰 Saldo

R$ {saldo:.2f}

⏳ Pendente

R$ {pendente:.2f}

🔒 Bloqueado

R$ {bloqueado:.2f}

━━━━━━━━━━━━━━━━━━

⭐ XP

{usuario["xp"]}

🏆 Nível

{usuario["nivel"]}

━━━━━━━━━━━━━━━━━━
"""

    return texto# ==================================================
# ADICIONAR SALDO
# ==================================================

def admin_adicionar_saldo(

    usuario_id,
    valor,
    admin_id,
    motivo="Adição manual"

):

    usuario = buscar_usuario_admin(usuario_id)

    if usuario is None:

        return False, "❌ Usuário não encontrado."

    adicionar_saldo(

        usuario_id=usuario_id,

        valor=valor,

        categoria="ADMIN",

        descricao=motivo,

        admin_id=admin_id

    )

    return True, "✅ Saldo adicionado com sucesso."


# ==================================================
# REMOVER SALDO
# ==================================================

def admin_remover_saldo(

    usuario_id,
    valor,
    admin_id,
    motivo="Remoção manual"

):

    usuario = buscar_usuario_admin(usuario_id)

    if usuario is None:

        return False, "❌ Usuário não encontrado."

    resultado = remover_saldo(

        usuario_id=usuario_id,

        valor=valor,

        categoria="ADMIN",

        descricao=motivo,

        admin_id=admin_id

    )

    if not resultado:

        return False, "❌ Saldo insuficiente."

    return True, "✅ Saldo removido com sucesso."# ==================================================
# BANIR
# ==================================================

def banir_usuario(

    usuario_id,
    admin_id

):

    cursor.execute("""

    UPDATE usuarios

    SET

        banido=1,

        status='BANIDO',

        updated_at=?

    WHERE id=?

    """,(

        agora(),

        usuario_id

    ))

    conn.commit()

    return True


# ==================================================
# DESBANIR
# ==================================================

def desbanir_usuario(

    usuario_id,
    admin_id

):

    cursor.execute("""

    UPDATE usuarios

    SET

        banido=0,

        status='ATIVO',

        updated_at=?

    WHERE id=?

    """,(

        agora(),

        usuario_id

    ))

    conn.commit()

    return True# ==================================================
# BLOQUEAR
# ==================================================

def bloquear_usuario(usuario_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        bloqueado=1,

        updated_at=?

    WHERE id=?

    """,(

        agora(),

        usuario_id

    ))

    conn.commit()


# ==================================================
# DESBLOQUEAR
# ==================================================

def desbloquear_usuario(usuario_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        bloqueado=0,

        updated_at=?

    WHERE id=?

    """,(

        agora(),

        usuario_id

    ))

    conn.commit()
    # ==================================================
# TORNAR VIP
# ==================================================

def tornar_vip(

    usuario_id,
    plano,
    dias,
    admin_id

):

    data = agora()

    cursor.execute("""

    SELECT usuario_id

    FROM vip

    WHERE usuario_id=?

    """,(usuario_id,))

    vip = cursor.fetchone()

    if vip:

        cursor.execute("""

        UPDATE vip

        SET

            plano=?,

            ativo=1,

            expira_em=?,

            updated_at=?

        WHERE usuario_id=?

        """,(

            plano,

            dias,

            data,

            usuario_id

        ))

    else:

        cursor.execute("""

        INSERT INTO vip(

            usuario_id,

            plano,

            ativo,

            expira_em,

            created_at,

            updated_at

        )

        VALUES(?,?,?,?,?,?)

        """,(

            usuario_id,

            plano,

            1,

            dias,

            data,

            data

        ))

    conn.commit()

    return True
    # ==================================================
# TORNAR PREMIUM
# ==================================================

def tornar_premium(

    usuario_id,
    plano,
    dias,
    admin_id

):

    data = agora()

    cursor.execute("""

    SELECT usuario_id

    FROM premium

    WHERE usuario_id=?

    """,(usuario_id,))

    premium = cursor.fetchone()

    if premium:

        cursor.execute("""

        UPDATE premium

        SET

            plano=?,

            ativo=1,

            expira_em=?,

            updated_at=?

        WHERE usuario_id=?

        """,(

            plano,

            dias,

            data,

            usuario_id

        ))

    else:

        cursor.execute("""

        INSERT INTO premium(

            usuario_id,

            plano,

            ativo,

            expira_em,

            created_at,

            updated_at

        )

        VALUES(?,?,?,?,?,?)

        """,(

            usuario_id,

            plano,

            1,

            dias,

            data,

            data

        ))

    conn.commit()

    return True
    # ==================================================
# DADOS COMPLETOS
# ==================================================

def dados_completos(usuario_id):

    return {

        "perfil": texto_usuario_admin(usuario_id),

        "carteira": texto_carteira(usuario_id),

        "pix": texto_pix(usuario_id),

        "indicacoes": texto_indicacoes(usuario_id)

    }

