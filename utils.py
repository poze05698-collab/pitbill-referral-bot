from datetime import datetime

from database import conn, cursor

from config import (
    ADMIN_ID,
    FORMATO_DATA,
    MODO_MANUTENCAO,
    MENSAGEM_MANUTENCAO,
    MENSAGEM_BANIMENTO
)

# ==========================================
# DATA E HORA
# ==========================================

def agora():

    return datetime.now().strftime(
        FORMATO_DATA
    )


# ==========================================
# ADMIN
# ==========================================

def eh_admin(user_id):

    return user_id == ADMIN_ID


# ==========================================
# MANUTENÇÃO
# ==========================================

def em_manutencao():

    if MODO_MANUTENCAO:

        return True

    cursor.execute(
        """
        SELECT valor

        FROM configuracoes

        WHERE chave='modo_manutencao'
        """
    )

    resultado = cursor.fetchone()

    if resultado is None:

        return False

    return resultado[0] == "SIM"


# ==========================================
# USUÁRIO BLOQUEADO
# ==========================================

def usuario_bloqueado(user_id):

    cursor.execute(
        """
        SELECT bloqueado

        FROM usuarios

        WHERE id=?
        """,
        (user_id,)
    )

    usuario = cursor.fetchone()

    if usuario is None:

        return False

    return usuario[0] == 1


# ==========================================
# VERIFICAR ACESSO
# ==========================================

def verificar_acesso(bot, message):

    user_id = message.from_user.id

    # Admin nunca é bloqueado

    if eh_admin(user_id):

        return True

    # Manutenção

    if em_manutencao():

        bot.send_message(

            message.chat.id,

            MENSAGEM_MANUTENCAO

        )

        return False

    # Banimento

    if usuario_bloqueado(user_id):

        bot.send_message(

            message.chat.id,

            MENSAGEM_BANIMENTO,

            parse_mode="HTML"

        )

        return False

    return True


# ==========================================
# SALDO
# ==========================================

def adicionar_saldo(user_id, valor):

    cursor.execute(
        """
        UPDATE usuarios

        SET saldo = saldo + ?

        WHERE id=?
        """,
        (
            valor,
            user_id
        )
    )

    conn.commit()


def remover_saldo(user_id, valor):

    cursor.execute(
        """
        UPDATE usuarios

        SET saldo = saldo - ?

        WHERE id=?
        """,
        (
            valor,
            user_id
        )
    )

    conn.commit()


# ==========================================
# HISTÓRICO
# ==========================================

def adicionar_historico(

    usuario,

    tipo,

    descricao,

    valor

):

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
            usuario,
            tipo,
            descricao,
            valor,
            agora()
        )
    )

    conn.commit()


# ==========================================
# LOGS
# ==========================================

def adicionar_log(

    usuario,

    acao,

    detalhes

):

    cursor.execute(
        """
        INSERT INTO logs(

            usuario,

            acao,

            detalhes,

            data

        )

        VALUES(

            ?,?,?,?

        )
        """,
        (
            usuario,
            acao,
            detalhes,
            agora()
        )
    )

    conn.commit()


# ==========================================
# CONFIGURAÇÕES
# ==========================================

def obter_config(chave):

    cursor.execute(
        """
        SELECT valor

        FROM configuracoes

        WHERE chave=?
        """,
        (chave,)
    )

    valor = cursor.fetchone()

    if valor:

        return valor[0]

    return None


def alterar_config(chave, valor):

    cursor.execute(
        """
        UPDATE configuracoes

        SET valor=?

        WHERE chave=?
        """,
        (
            valor,
            chave
        )
    )

    conn.commit()
