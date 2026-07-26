from database import conn, cursor

from config import VALOR_INDICACAO

from utils import (
    adicionar_saldo,
    adicionar_historico,
    adicionar_log,
    agora
)

# ==========================================
# REGISTRAR MÓDULO
# ==========================================

def registrar_indicacoes(bot):

    pass


# ==========================================
# VALIDAR INDICAÇÃO
# ==========================================

def validar_indicacao(bot, usuario_id):

    # ======================================
    # PROCURA INDICAÇÃO PENDENTE
    # ======================================

    cursor.execute(
        """
        SELECT

            id,
            indicador

        FROM indicacoes

        WHERE indicado=?

        AND status='PENDENTE'
        """,
        (usuario_id,)
    )

    indicacao = cursor.fetchone()

    if indicacao is None:

        return False

    indicacao_id = indicacao[0]

    indicador = indicacao[1]

    # ======================================
    # EVITA AUTO INDICAÇÃO
    # ======================================

    if indicador == usuario_id:

        return False

    # ======================================
    # VERIFICA PIX
    # ======================================

    cursor.execute(
        """
        SELECT pix

        FROM usuarios

        WHERE id=?
        """,
        (usuario_id,)
    )

    usuario = cursor.fetchone()

    if usuario is None:

        return False

    if usuario[0] == "":

        return False    # ======================================
    # VERIFICA SE JÁ FOI APROVADA
    # ======================================

    cursor.execute(
        """
        SELECT status

        FROM indicacoes

        WHERE id=?
        """,
        (indicacao_id,)
    )

    status = cursor.fetchone()

    if status is None:

        return False

    if status[0] == "APROVADA":

        return False

    # ======================================
    # APROVAR INDICAÇÃO
    # ======================================

    cursor.execute(
        """
        UPDATE indicacoes

        SET

            status='APROVADA',

            recompensa=?

        WHERE id=?
        """,
        (
            VALOR_INDICACAO,
            indicacao_id
        )
    )

    # ======================================
    # PAGAR RECOMPENSA
    # ======================================

    adicionar_saldo(

        indicador,

        VALOR_INDICACAO

    )

    # ======================================
    # ATUALIZAR CONTADOR
    # ======================================

    cursor.execute(
        """
        UPDATE usuarios

        SET convidados = convidados + 1

        WHERE id=?
        """,
        (indicador,)
    )

    conn.commit()

    # ======================================
    # HISTÓRICO INDICADOR
    # ======================================

    adicionar_historico(

        indicador,

        "INDICAÇÃO",

        "Recompensa por indicação aprovada",

        VALOR_INDICACAO

    )

    # ======================================
    # HISTÓRICO INDICADO
    # ======================================

    adicionar_historico(

        usuario_id,

        "CADASTRO",

        "Cadastro validado",

        0

    )

    # ======================================
    # LOGS
    # ======================================

    adicionar_log(

        indicador,

        "INDICAÇÃO",

        f"Recebeu recompensa do usuário {usuario_id}"

    )

    adicionar_log(

        usuario_id,

        "INDICAÇÃO",

        f"Cadastro validado pelo indicador {indicador}"

    )    # ======================================
    # ENVIAR MENSAGEM AO INDICADOR
    # ======================================

    try:

        bot.send_message(

            indicador,

            f"""
🎉 <b>PARABÉNS!</b>

Sua indicação foi aprovada.

💰 Você recebeu:

<b>R$ {VALOR_INDICACAO:.2f}</b>

O valor já foi adicionado ao seu saldo.
""",

            parse_mode="HTML"

        )

    except Exception as erro:

        print(erro)

    # ======================================
    # ENVIAR MENSAGEM AO INDICADO
    # ======================================

    try:

        bot.send_message(

            usuario_id,

            """
✅ Seu cadastro foi validado com sucesso.

Agora você já pode utilizar todas as funções do bot.

Convide seus amigos e ganhe dinheiro também!
"""

        )

    except Exception as erro:

        print(erro)

    # ======================================
    # LOG FINAL
    # ======================================

    adicionar_log(

        indicador,

        "RECOMPENSA",

        f"Recebeu R$ {VALOR_INDICACAO:.2f}"

    )

    conn.commit()

    return True


# ==========================================
# CONSULTAR INDICAÇÕES
# ==========================================

def listar_indicacoes(user_id):

    cursor.execute(
        """
        SELECT

            indicado,
            recompensa,
            status,
            data

        FROM indicacoes

        WHERE indicador=?

        ORDER BY id DESC
        """,
        (user_id,)
    )

    return cursor.fetchall()


# ==========================================
# TOTAL DE INDICAÇÕES
# ==========================================

def total_indicacoes(user_id):

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM indicacoes

        WHERE indicador=?
        """,
        (user_id,)
    )

    return cursor.fetchone()[0]


# ==========================================
# TOTAL APROVADAS
# ==========================================

def total_aprovadas(user_id):

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM indicacoes

        WHERE indicador=?

        AND status='APROVADA'
        """,
        (user_id,)
    )

    return cursor.fetchone()[0]


# ==========================================
# TOTAL PENDENTES
# ==========================================

def total_pendentes(user_id):

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM indicacoes

        WHERE indicador=?

        AND status='PENDENTE'
        """,
        (user_id,)
    )

    return cursor.fetchone()[0]
