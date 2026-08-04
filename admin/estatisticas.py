"""
==================================================
PITBULL REWARDS PLATFORM V3
ADMIN - ESTATÍSTICAS
==================================================
"""

from database import (
    cursor
)

# ==================================================
# ESTATÍSTICAS DOS USUÁRIOS
# ==================================================

def estatisticas_usuarios():

    cursor.execute("""
    SELECT COUNT(*)
    FROM usuarios
    """)
    total = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM usuarios
    WHERE status='ATIVO'
    """)
    ativos = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM usuarios
    WHERE banido=1
    """)
    banidos = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM vip
    WHERE ativo=1
    """)
    vip = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM premium
    WHERE ativo=1
    """)
    premium = cursor.fetchone()[0]

    return {
        "total": total,
        "ativos": ativos,
        "banidos": banidos,
        "vip": vip,
        "premium": premium
    }


# ==================================================
# ESTATÍSTICAS DA CARTEIRA
# ==================================================

def estatisticas_carteira():

    cursor.execute("""
    SELECT
        COALESCE(SUM(saldo),0),
        COALESCE(SUM(saldo_pendente),0),
        COALESCE(SUM(saldo_bloqueado),0)
    FROM carteira
    """)

    resultado = cursor.fetchone()

    return {
        "saldo": float(resultado[0]),
        "pendente": float(resultado[1]),
        "bloqueado": float(resultado[2])
    }

  # ==================================================
# ESTATÍSTICAS DOS SAQUES
# ==================================================

def estatisticas_saques():

    cursor.execute("""
    SELECT COUNT(*)
    FROM saques
    """)
    total = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM saques
    WHERE status='PENDENTE'
    """)
    pendentes = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM saques
    WHERE status='APROVADO'
    """)
    aprovados = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM saques
    WHERE status='PAGO'
    """)
    pagos = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM saques
    WHERE status='REJEITADO'
    """)
    rejeitados = cursor.fetchone()[0]

    return {
        "total": total,
        "pendentes": pendentes,
        "aprovados": aprovados,
        "pagos": pagos,
        "rejeitados": rejeitados
    }


# ==================================================
# ESTATÍSTICAS DAS INDICAÇÕES
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

  # ==================================================
# TEXTO DAS ESTATÍSTICAS
# ==================================================

def texto_estatisticas():

    usuarios = estatisticas_usuarios()
    carteira = estatisticas_carteira()
    saques = estatisticas_saques()
    indicacoes = estatisticas_indicacoes()

    texto = f"""
📊 <b>ESTATÍSTICAS DO SISTEMA</b>

━━━━━━━━━━━━━━━━━━
👥 <b>USUÁRIOS</b>

• Total: <b>{usuarios['total']}</b>
• Ativos: <b>{usuarios['ativos']}</b>
• Banidos: <b>{usuarios['banidos']}</b>
• VIP: <b>{usuarios['vip']}</b>
• Premium: <b>{usuarios['premium']}</b>

━━━━━━━━━━━━━━━━━━
💰 <b>CARTEIRA</b>

• Saldo: <b>R$ {carteira['saldo']:.2f}</b>
• Pendente: <b>R$ {carteira['pendente']:.2f}</b>
• Bloqueado: <b>R$ {carteira['bloqueado']:.2f}</b>

━━━━━━━━━━━━━━━━━━
💸 <b>SAQUES</b>

• Total: <b>{saques['total']}</b>
• Pendentes: <b>{saques['pendentes']}</b>
• Aprovados: <b>{saques['aprovados']}</b>
• Pagos: <b>{saques['pagos']}</b>
• Rejeitados: <b>{saques['rejeitados']}</b>

━━━━━━━━━━━━━━━━━━
🎁 <b>INDICAÇÕES</b>

• Total: <b>{indicacoes['total']}</b>
• Pendentes: <b>{indicacoes['pendentes']}</b>
• Aprovadas: <b>{indicacoes['aprovadas']}</b>
• Rejeitadas: <b>{indicacoes['rejeitadas']}</b>

━━━━━━━━━━━━━━━━━━
"""

    return texto
