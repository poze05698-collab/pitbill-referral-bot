from datetime import datetime

from database import conn, cursor

from config import *

# ==========================================
# VALIDAR INDICAÇÃO
# ==========================================

def validar_indicacao(bot, user_id):

    cursor.execute(
        """
        SELECT
        convidado_por,
        pix

        FROM usuarios

        WHERE id=?
        """,
        (user_id,)
    )

    usuario = cursor.fetchone()

    if not usuario:
        return

    indicador, pix = usuario

    # Não foi indicado
    if indicador is None:
        return

    # Pix obrigatório
    if PIX_OBRIGATORIO:

        if pix == "":
            return

    # Já validou

    cursor.execute(

        """
        SELECT status

        FROM indicacoes

        WHERE indicado=?
        """,

        (user_id,)

    )

    indicacao = cursor.fetchone()

    if not indicacao:
        return

    if indicacao[0] == "APROVADA":
        return    # ======================================
    # GRUPO OBRIGATÓRIO
    # ======================================

    if GRUPO_OBRIGATORIO:

        try:

            membro = bot.get_chat_member(
                GRUPO_ID,
                user_id
            )

            if membro.status not in [

                "member",

                "administrator",

                "creator"

            ]:

                return

        except:

            return

    # ======================================
    # VALOR DA INDICAÇÃO
    # ======================================

    cursor.execute(
        """
        SELECT valor

        FROM configuracoes

        WHERE chave='valor_indicacao'
        """
    )

    resultado = cursor.fetchone()

    if resultado:

        recompensa = float(resultado[0])

    else:

        recompensa = VALOR_INDICACAO

    # ======================================
    # APROVAR INDICAÇÃO
    # ======================================

    cursor.execute(
        """
        UPDATE indicacoes

        SET

        recompensa=?,
        status='APROVADA'

        WHERE indicado=?
        """,
        (
            recompensa,
            user_id
        )
    )

    # ======================================
    # SOMAR SALDO
    # ======================================

    cursor.execute(
        """
        UPDATE usuarios

        SET

        saldo = saldo + ?,
        convidados = convidados + 1

        WHERE id=?
        """,
        (
            recompensa,
            indicador
        )
    )

    # ======================================
    # HISTÓRICO
    # ======================================

    cursor.execute(
        """
        INSERT INTO historico(

            usuario,
            tipo,
            descricao,
            valor,
            data

        )

        VALUES(

            ?,?,?,?,?

        )
        """,
        (
            indicador,
            "INDICACAO",
            "Bônus por indicação",
            recompensa,
            datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )
        )
    )

    conn.commit()

    # ======================================
    # AVISAR INDICADOR
    # ======================================

    try:

        bot.send_message(

            indicador,

            f"""
🎉 Sua indicação foi validada!

💰 Você recebeu:

R$ {recompensa:.2f}

O valor já foi adicionado ao seu saldo.
"""

        )

    except:

        pass
