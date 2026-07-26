from datetime import datetime, timedelta

from database import conn, cursor

# ==========================================
# AUTO INDICAÇÃO
# ==========================================

def verificar_auto_indicacao(user_id, indicador):

    if indicador is None:
        return True

    return user_id != indicador


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

    resultado = cursor.fetchone()

    if not resultado:
        return False

    return resultado[0] == 1


# ==========================================
# POSSUI INDICAÇÃO
# ==========================================

def possui_indicacao(user_id):

    cursor.execute(
        """
        SELECT id

        FROM indicacoes

        WHERE indicado=?
        """,
        (user_id,)
    )

    return cursor.fetchone() is not None


# ==========================================
# REGISTRAR FRAUDE
# ==========================================

def registrar_fraude(user_id, motivo):

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
            user_id,
            "FRAUDE",
            motivo,
            0,
            datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )
        )
    )

    conn.commit()


# ==========================================
# BLOQUEAR USUÁRIO
# ==========================================

def bloquear_usuario(user_id, motivo):

    cursor.execute(
        """
        UPDATE usuarios

        SET bloqueado=1

        WHERE id=?
        """,
        (user_id,)
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO usuarios_bloqueados(

            usuario,
            motivo,
            data

        )

        VALUES(

            ?,?,?

        )
        """,
        (
            user_id,
            motivo,
            datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )
        )
    )

    conn.commit()


# ==========================================
# LIMITE DE INDICAÇÕES
# ==========================================

def verificar_limite(indicador):

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM indicacoes

        WHERE indicador=?

        AND data LIKE ?
        """,
        (
            indicador,
            datetime.now().strftime("%d/%m/%Y") + "%"
        )
    )

    quantidade = cursor.fetchone()[0]

    # Máximo de 20 indicações por dia
    return quantidade < 20# ==========================================
# DETECTAR PADRÃO SUSPEITO
# ==========================================

def detectar_fraude(user_id, indicador):

    # Auto indicação
    if not verificar_auto_indicacao(
        user_id,
        indicador
    ):

        registrar_fraude(
            user_id,
            "Auto indicação"
        )

        bloquear_usuario(
            user_id,
            "Auto indicação"
        )

        return False

    # Já foi indicado
    if possui_indicacao(user_id):

        registrar_fraude(
            user_id,
            "Tentativa de dupla indicação"
        )

        return False

    # Limite diário
    if not verificar_limite(indicador):

        registrar_fraude(
            indicador,
            "Excesso de indicações"
        )

        return False

    return True


# ==========================================
# RELATÓRIO
# ==========================================

def relatorio_fraudes():

    cursor.execute(
        """
        SELECT

        usuario,
        descricao,
        data

        FROM historico

        WHERE tipo='FRAUDE'

        ORDER BY id DESC

        LIMIT 50
        """
    )

    return cursor.fetchall()


# ==========================================
# CONTAR FRAUDES
# ==========================================

def total_fraudes(user_id):

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM historico

        WHERE usuario=?

        AND tipo='FRAUDE'
        """,
        (user_id,)
    )

    return cursor.fetchone()[0]


# ==========================================
# BLOQUEIO AUTOMÁTICO
# ==========================================

def verificar_bloqueio_automatico(user_id):

    if total_fraudes(user_id) >= 3:

        bloquear_usuario(

            user_id,

            "Fraudes repetidas"

        )

        return True

    return False


# ==========================================
# VALIDAÇÃO GERAL
# ==========================================

def validar_usuario(user_id, indicador):

    if usuario_bloqueado(user_id):

        return False

    if not detectar_fraude(

        user_id,

        indicador

    ):

        return False

    if verificar_bloqueio_automatico(

        user_id

    ):

        return False

    return True
