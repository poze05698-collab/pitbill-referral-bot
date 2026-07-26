from datetime import datetime

from database import (
    conn,
    cursor
)

from config import (
    ADMIN_ID
)



# ==========================================
# DATA ATUAL
# ==========================================

def agora():

    return datetime.now().strftime(

        "%d/%m/%Y %H:%M:%S"

    )



# ==========================================
# VERIFICAR USUÁRIO BLOQUEADO
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


    resultado = cursor.fetchone()


    if resultado is None:

        return False


    return resultado[0] == 1



# ==========================================
# VERIFICAR MANUTENÇÃO
# ==========================================

def em_manutencao():


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
# ALTERAR CONFIGURAÇÃO
# ==========================================

def alterar_config(chave, valor):


    cursor.execute(

        """
        INSERT OR REPLACE INTO configuracoes(

            chave,

            valor

        )

        VALUES(

            ?,?

        )

        """,

        (

            chave,

            valor

        )

    )


    conn.commit()# ==========================================
# VERIFICAR ACESSO COMPLETO
# ==========================================

def verificar_acesso(bot, message):

    user_id = message.from_user.id


    # ADMIN SEMPRE ENTRA

    if user_id == ADMIN_ID:

        return True



    # VERIFICAR BANIMENTO

    if usuario_bloqueado(user_id):

        bot.send_message(

            message.chat.id,

            """
🚫 Sua conta está bloqueada.

Entre em contato com o suporte.
"""

        )

        return False



    # VERIFICAR MANUTENÇÃO

    if em_manutencao():


        bot.send_message(

            message.chat.id,

            """
🔧 Bot em manutenção.

Tente novamente mais tarde.
"""

        )

        return False



    return True



# ==========================================
# ADICIONAR LOG
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
# ADICIONAR HISTÓRICO
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
# ADICIONAR SALDO
# ==========================================

def adicionar_saldo(

    usuario,

    valor

):


    cursor.execute(

        """
        UPDATE usuarios

        SET saldo = saldo + ?

        WHERE id=?

        """,

        (

            valor,

            usuario

        )

    )


    conn.commit()



# ==========================================
# REMOVER SALDO
# ==========================================

def remover_saldo(

    usuario,

    valor

):


    cursor.execute(

        """
        UPDATE usuarios

        SET saldo = saldo - ?

        WHERE id=?

        """,

        (

            valor,

            usuario

        )

    )


    conn.commit()# ==========================================
# BUSCAR USUÁRIO
# ==========================================

def buscar_usuario(user_id):

    cursor.execute(

        """
        SELECT *

        FROM usuarios

        WHERE id=?

        """,

        (user_id,)

    )


    return cursor.fetchone()



# ==========================================
# VERIFICAR EXISTÊNCIA DO USUÁRIO
# ==========================================

def usuario_existe(user_id):

    cursor.execute(

        """
        SELECT id

        FROM usuarios

        WHERE id=?

        """,

        (user_id,)

    )


    resultado = cursor.fetchone()


    return resultado is not None



# ==========================================
# ATUALIZAR ÚLTIMO ACESSO
# ==========================================

def atualizar_acesso(user_id):

    cursor.execute(

        """
        UPDATE usuarios

        SET ultimo_acesso=?

        WHERE id=?

        """,

        (

            agora(),

            user_id

        )

    )


    conn.commit()



# ==========================================
# BLOQUEAR USUÁRIO
# ==========================================

def bloquear_usuario(user_id):

    cursor.execute(

        """
        UPDATE usuarios

        SET bloqueado=1

        WHERE id=?

        """,

        (user_id,)

    )


    conn.commit()



# ==========================================
# DESBLOQUEAR USUÁRIO
# ==========================================

def desbloquear_usuario(user_id):

    cursor.execute(

        """
        UPDATE usuarios

        SET bloqueado=0

        WHERE id=?

        """,

        (user_id,)

    )


    conn.commit()



# ==========================================
# CONTAR USUÁRIOS
# ==========================================

def total_usuarios():

    cursor.execute(

        """
        SELECT COUNT(*)

        FROM usuarios

        """

    )


    return cursor.fetchone()[0]



# ==========================================
# TOTAL DE SALDO
# ==========================================

def total_saldo():

    cursor.execute(

        """
        SELECT SUM(saldo)

        FROM usuarios

        """

    )


    resultado = cursor.fetchone()[0]


    if resultado is None:

        return 0


    return resultado



# ==========================================
# LIMPAR CACHE (RESERVADO)
# ==========================================

def limpar_cache():

    pass



# ==========================================
# FIM DO UTILS
# ==========================================
