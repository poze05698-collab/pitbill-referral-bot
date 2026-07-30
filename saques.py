"""
==================================================
 PITBULL REWARDS PLATFORM V3
 saques.py
==================================================
"""

from database import (
    conn,
    cursor,
    agora,
    get_config
)

from usuarios import (
    buscar_usuario,
    adicionar_notificacao
)

from pix import (
    validar_pix_para_saque,
    dados_pix
)

from engine import (
    EngineFinanceira
)

# ==================================================
# CONFIGURAÇÕES
# ==================================================

def valor_minimo():

    valor = get_config("valor_minimo_saque")

    if valor is None:
        return 20.0

    return float(valor)


def valor_maximo():

    valor = get_config("valor_maximo_saque")

    if valor is None:
        return 1000.0

    return float(valor)

# ==================================================
# CONSULTAR SALDO
# ==================================================

def saldo_disponivel(usuario_id):

    usuario = buscar_usuario(usuario_id)

    if usuario is None:

        return 0

    return float(usuario["saldo"])# ==================================================
# SOLICITAR SAQUE
# ==================================================

def solicitar_saque(usuario_id, valor):

    # Validação do PIX
    if not validar_pix_para_saque(usuario_id):

        return False, "❌ Você precisa cadastrar uma chave PIX antes de solicitar um saque."

    # Validação do valor
    try:

        valor = float(valor)

    except (TypeError, ValueError):

        return False, "❌ Valor inválido."

    # Valor mínimo
    if valor < valor_minimo():

        return False, (
            f"❌ O valor mínimo para saque é R$ {valor_minimo():.2f}."
        )

    # Valor máximo
    if valor > valor_maximo():

        return False, (
            f"❌ O valor máximo para saque é R$ {valor_maximo():.2f}."
        )

    # Saldo
    saldo = saldo_disponivel(usuario_id)

    if saldo < valor:

        return False, "❌ Saldo insuficiente."

    # PIX
    pix = dados_pix(usuario_id)

    cursor.execute("""

    INSERT INTO saques(

        usuario,

        valor,

        pix,

        status,

        created_at

    )

    VALUES(

        ?,?,?,?,?

    )

    """, (

        usuario_id,

        valor,

        pix["chave"],

        "PENDENTE",

        agora()

    ))

    conn.commit()

    # Reserva o saldo
    EngineFinanceira.sacar(

        usuario_id,

        valor,

        descricao="Solicitação de saque"

    )

    adicionar_notificacao(

        usuario_id,

        "💸 Saque solicitado",

        (
            f"Sua solicitação de saque de "
            f"R$ {valor:.2f} foi registrada e está aguardando aprovação."
        )

    )

    return True, (
        f"✅ Solicitação enviada com sucesso!\n\n"
        f"Valor: R$ {valor:.2f}"
    )


# ==================================================
# HISTÓRICO
# ==================================================

def historico_saques(usuario_id):

    cursor.execute("""

    SELECT *

    FROM saques

    WHERE usuario=?

    ORDER BY id DESC

    """, (

        usuario_id,

    ))

    return cursor.fetchall()# ==================================================
# APROVAR SAQUE
# ==================================================

def aprovar_saque(admin_id, saque_id):

    cursor.execute("""

    SELECT *

    FROM saques

    WHERE id=?

    """, (

        saque_id,

    ))

    saque = cursor.fetchone()

    if saque is None:

        return False, "❌ Saque não encontrado."

    if saque["status"] != "PENDENTE":

        return False, "❌ Este saque já foi processado."

    cursor.execute("""

    UPDATE saques

    SET

        status=?,

        aprovado_por=?,

        updated_at=?

    WHERE id=?

    """, (

        "APROVADO",

        admin_id,

        agora(),

        saque_id

    ))

    conn.commit()

    adicionar_notificacao(

        saque["usuario"],

        "✅ Saque aprovado",

        "Seu saque foi aprovado e será processado em breve."

    )

    return True, "✅ Saque aprovado."


# ==================================================
# REJEITAR SAQUE
# ==================================================

def rejeitar_saque(admin_id, saque_id, motivo=""):

    cursor.execute("""

    SELECT *

    FROM saques

    WHERE id=?

    """, (

        saque_id,

    ))

    saque = cursor.fetchone()

    if saque is None:

        return False, "❌ Saque não encontrado."

    if saque["status"] != "PENDENTE":

        return False, "❌ Este saque já foi processado."

    cursor.execute("""

    UPDATE saques

    SET

        status=?,

        aprovado_por=?,

        observacao=?,

        updated_at=?

    WHERE id=?

    """, (

        "REJEITADO",

        admin_id,

        motivo,

        agora(),

        saque_id

    ))

    conn.commit()

    # Estorna o saldo
    from usuarios import adicionar_saldo

    adicionar_saldo(

        saque["usuario"],

        saque["valor"],

        categoria="ESTORNO",

        descricao="Estorno de saque rejeitado",

        admin_id=admin_id

    )

    adicionar_notificacao(

        saque["usuario"],

        "❌ Saque rejeitado",

        (
            "Seu saque foi rejeitado.\n\n"
            f"Motivo: {motivo if motivo else 'Não informado.'}"
        )

    )

    return True, "✅ Saque rejeitado e saldo devolvido."


# ==================================================
# LISTAR SAQUES PENDENTES
# ==================================================

def saques_pendentes():

    cursor.execute("""

    SELECT *

    FROM saques

    WHERE status='PENDENTE'

    ORDER BY id ASC

    """)

    return cursor.fetchall()


# ==================================================
# FINAL
# ==================================================

print("✅ saques.py carregado com sucesso.")
