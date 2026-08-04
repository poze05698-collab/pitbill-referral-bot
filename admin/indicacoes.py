"""
==================================================
PITBULL REWARDS PLATFORM V3
ADMIN - INDICAÇÕES
==================================================
"""

from database import (
    conn,
    cursor,
    agora
)

from indicacoes import (

    aprovar_indicacao,

    rejeitar_indicacao

)

# ==================================================
# INDICAÇÕES PENDENTES
# ==================================================

def indicacoes_pendentes():

    cursor.execute("""

    SELECT

        i.*,

        indicador.nome AS nome_indicador,

        indicador.username AS username_indicador,

        indicado.nome AS nome_indicado,

        indicado.username AS username_indicado

    FROM indicacoes i

    INNER JOIN usuarios indicador

        ON indicador.id=i.indicador_id

    INNER JOIN usuarios indicado

        ON indicado.id=i.indicado_id

    WHERE i.status='PENDENTE'

    ORDER BY i.id ASC

    """)

    return cursor.fetchall()


# ==================================================
# INDICAÇÕES APROVADAS
# ==================================================

def indicacoes_aprovadas():

    cursor.execute("""

    SELECT

        i.*,

        indicador.nome AS nome_indicador,

        indicado.nome AS nome_indicado

    FROM indicacoes i

    INNER JOIN usuarios indicador

        ON indicador.id=i.indicador_id

    INNER JOIN usuarios indicado

        ON indicado.id=i.indicado_id

    WHERE i.status='APROVADA'

    ORDER BY i.id DESC

    """)

    return cursor.fetchall()


# ==================================================
# INDICAÇÕES REJEITADAS
# ==================================================

def indicacoes_rejeitadas():

    cursor.execute("""

    SELECT

        i.*,

        indicador.nome AS nome_indicador,

        indicado.nome AS nome_indicado

    FROM indicacoes i

    INNER JOIN usuarios indicador

        ON indicador.id=i.indicador_id

    INNER JOIN usuarios indicado

        ON indicado.id=i.indicado_id

    WHERE i.status='REJEITADA'

    ORDER BY i.id DESC

    """)

    return cursor.fetchall()

  # ==================================================
# BUSCAR INDICAÇÃO
# ==================================================

def buscar_indicacao_admin(indicacao_id):

    cursor.execute("""

    SELECT

        i.*,

        indicador.nome AS nome_indicador,

        indicador.username AS username_indicador,

        indicado.nome AS nome_indicado,

        indicado.username AS username_indicado

    FROM indicacoes i

    INNER JOIN usuarios indicador

        ON indicador.id=i.indicador_id

    INNER JOIN usuarios indicado

        ON indicado.id=i.indicado_id

    WHERE i.id=?

    """,(indicacao_id,))

    return cursor.fetchone()

# ==================================================
# TEXTO DA INDICAÇÃO
# ==================================================

def texto_indicacao_admin(indicacao_id):

    indicacao = buscar_indicacao_admin(indicacao_id)

    if indicacao is None:

        return "❌ Indicação não encontrada."

    cursor.execute("""

    SELECT *

    FROM grupo

    WHERE usuario_id=?

    """,(indicacao["indicado_id"],))

    grupo = cursor.fetchone()

    cursor.execute("""

    SELECT *

    FROM canal

    WHERE usuario_id=?

    """,(indicacao["indicado_id"],))

    canal = cursor.fetchone()

    cursor.execute("""

    SELECT *

    FROM antifraude

    WHERE usuario_id=?

    """,(indicacao["indicado_id"],))

    antifraude = cursor.fetchone()

    grupo_ok = "✅ Sim" if grupo and grupo["verificado"] else "❌ Não"

    canal_ok = "✅ Sim" if canal and canal["verificado"] else "❌ Não"

    score = 100

    if antifraude:

        score = antifraude["score"]

    texto = f"""
👥 <b>INDICAÇÃO #{indicacao['id']}</b>

━━━━━━━━━━━━━━━━━━

👤 Indicador

{indicacao['nome_indicador']}

━━━━━━━━━━━━━━━━━━

👤 Indicado

{indicacao['nome_indicado']}

━━━━━━━━━━━━━━━━━━

💰 Recompensa

R$ {float(indicacao['recompensa']):.2f}

━━━━━━━━━━━━━━━━━━

👥 Grupo

{grupo_ok}

📢 Canal

{canal_ok}

🛡 Score

{score}

━━━━━━━━━━━━━━━━━━

📋 Status

{indicacao['status']}

"""

    return texto

  # ==================================================
# APROVAR
# ==================================================

def admin_aprovar_indicacao(

    indicado_id,

    admin_id

):

    return aprovar_indicacao(

        indicado_id,

        admin_id

    )


# ==================================================
# REJEITAR
# ==================================================

def admin_rejeitar_indicacao(

    indicado_id,

    admin_id,

    motivo=""

):

    return rejeitar_indicacao(

        indicado_id,

        admin_id,

        motivo

    )

 # ==================================================
# ESTATÍSTICAS
# ==================================================

def estatisticas_indicacoes():

    cursor.execute("""

    SELECT COUNT(*)

    FROM indicacoes

    """)

    total = cursor.fetchone()[0]

    cursor.execute("""

    SELECT COUNT(*)

    FROM indicacoes

    WHERE status='PENDENTE'

    """)

    pendentes = cursor.fetchone()[0]

    cursor.execute("""

    SELECT COUNT(*)

    FROM indicacoes

    WHERE status='APROVADA'

    """)

    aprovadas = cursor.fetchone()[0]

    cursor.execute("""

    SELECT COUNT(*)

    FROM indicacoes

    WHERE status='REJEITADA'

    """)

    rejeitadas = cursor.fetchone()[0]

    return {

        "total": total,

        "pendentes": pendentes,

        "aprovadas": aprovadas,

        "rejeitadas": rejeitadas

    } 
