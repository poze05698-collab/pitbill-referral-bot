from datetime import datetime

from database import conn, cursor


# ==========================================
# DATA E HORA
# ==========================================

def agora():

    return datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )


# ==========================================
# FORMATA VALOR
# ==========================================

def dinheiro(valor):

    return f"R$ {valor:.2f}"


# ==========================================
# VERIFICA USUÁRIO
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

    return cursor.fetchone() is not None


# ==========================================
# VERIFICA BLOQUEIO
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

    if not resultado:

        return False

    return resultado[0] == 1


# ==========================================
# PEGAR SALDO
# ==========================================

def saldo(user_id):

    cursor.execute(

        """
        SELECT saldo

        FROM usuarios

        WHERE id=?
        """,

        (user_id,)

    )

    resultado = cursor.fetchone()

    if not resultado:

        return 0

    return resultado[0]


# ==========================================
# SOMAR SALDO
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


# ==========================================
# DESCONTAR SALDO
# ==========================================

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
# CONFIGURAÇÃO
# ==========================================

def configuracao(chave):

    cursor.execute(

        """
        SELECT valor

        FROM configuracoes

        WHERE chave=?
        """,

        (chave,)

    )

    resultado = cursor.fetchone()

    if resultado:

        return resultado[0]

    return None


# ==========================================
# ALTERAR CONFIG
# ==========================================

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


# ==========================================
# LOG
# ==========================================

def log(texto):

    print(

        f"[{agora()}] {texto}"

    )
