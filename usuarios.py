"""
=========================================
 PITBULL REWARDS PLATFORM V2
 usuarios.py
=========================================
"""

import random
import string

from datetime import datetime

from database import (
    conn,
    cursor,
    fetchone,
    fetchall,
    execute
)

# ==========================================
# DATA / HORA
# ==========================================

def agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# ==========================================
# GERAR CÓDIGO DE REFERÊNCIA
# ==========================================

def gerar_codigo():

    while True:

        codigo = "PIT" + "".join(

            random.choices(

                string.ascii_uppercase + string.digits,

                k=6

            )

        )

        cursor.execute(

            "SELECT id FROM usuarios WHERE codigo=?",

            (codigo,)

        )

        if cursor.fetchone() is None:

            return codigo


# ==========================================
# VERIFICAR SE O USUÁRIO EXISTE
# ==========================================

def usuario_existe(user_id):

    cursor.execute(

        "SELECT id FROM usuarios WHERE id=?",

        (user_id,)

    )

    return cursor.fetchone() is not None


# ==========================================
# BUSCAR USUÁRIO
# ==========================================

def buscar_usuario(user_id):

    cursor.execute(

        "SELECT * FROM usuarios WHERE id=?",

        (user_id,)

    )

    return cursor.fetchone()


# ==========================================
# CADASTRAR USUÁRIO
# ==========================================

def cadastrar_usuario(

    user_id,

    nome,

    username=None,

    convidado_por=None

):

    if usuario_existe(user_id):

        return False

    codigo = gerar_codigo()

    data = agora()

    cursor.execute("""

    INSERT INTO usuarios(

        id,

        codigo,

        nome,

        username,

        convidado_por,

        created_at,

        updated_at,

        ultimo_login,

        ultima_atividade

    )

    VALUES(?,?,?,?,?,?,?,?,?)

    """,(

        user_id,

        codigo,

        nome,

        username,

        convidado_por,

        data,

        data,

        data,

        data

    ))

    # Criar estatísticas do usuário

    cursor.execute("""

    INSERT INTO estatisticas(

        usuario

    )

    VALUES(?)

    """,(user_id,))

    # Criar ranking

    cursor.execute("""

    INSERT INTO ranking(

        usuario,

        updated_at

    )

    VALUES(?,?)

    """,(user_id,data))

    conn.commit()

    return True


# ==========================================
# ATUALIZAR DADOS DO USUÁRIO
# ==========================================

def atualizar_usuario(

    user_id,

    nome,

    username

):

    cursor.execute("""

    UPDATE usuarios

    SET

        nome=?,

        username=?,

        updated_at=?,

        ultima_atividade=?

    WHERE id=?

    """,(

        nome,

        username,

        agora(),

        agora(),

        user_id

    ))

    conn.commit()


# ==========================================
# ATUALIZAR ÚLTIMO LOGIN
# ==========================================

def atualizar_login(user_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        ultimo_login=?,

        ultima_atividade=?

    WHERE id=?

    """,(

        agora(),

        agora(),

        user_id

    ))

    conn.commit()# ==========================================
# PERFIL
# ==========================================

def perfil(user_id):

    cursor.execute("""

    SELECT *

    FROM usuarios

    WHERE id=?

    """,(user_id,))

    return cursor.fetchone()


# ==========================================
# SALDO
# ==========================================

def saldo(user_id):

    cursor.execute("""

    SELECT saldo

    FROM usuarios

    WHERE id=?

    """,(user_id,))

    resultado = cursor.fetchone()

    if resultado:

        return resultado["saldo"]

    return 0


# ==========================================
# ADICIONAR XP
# ==========================================

def adicionar_xp(user_id, xp):

    cursor.execute("""

    UPDATE usuarios

    SET

        xp = xp + ?,

        updated_at=?

    WHERE id=?

    """,(

        xp,

        agora(),

        user_id

    ))

    conn.commit()

    verificar_nivel(user_id)


# ==========================================
# VERIFICAR NÍVEL
# ==========================================

def verificar_nivel(user_id):

    cursor.execute("""

    SELECT

        xp,

        nivel

    FROM usuarios

    WHERE id=?

    """,(user_id,))

    usuario = cursor.fetchone()

    if usuario is None:

        return

    xp = usuario["xp"]

    nivel = usuario["nivel"]

    novo_nivel = (xp // 100) + 1

    if novo_nivel > nivel:

        cursor.execute("""

        UPDATE usuarios

        SET

            nivel=?,

            updated_at=?

        WHERE id=?

        """,(

            novo_nivel,

            agora(),

            user_id

        ))

        conn.commit()


# ==========================================
# ALTERAR STREAK
# ==========================================

def atualizar_streak(user_id, streak):

    cursor.execute("""

    UPDATE usuarios

    SET

        streak=?,

        updated_at=?

    WHERE id=?

    """,(

        streak,

        agora(),

        user_id

    ))

    conn.commit()


# ==========================================
# BUSCAR INVENTÁRIO
# ==========================================

def inventario(user_id):

    cursor.execute("""

    SELECT *

    FROM inventario

    WHERE usuario=?

    """,(user_id,))

    return cursor.fetchall()


# ==========================================
# ADICIONAR ITEM
# ==========================================

def adicionar_item(user_id, item, quantidade=1):

    cursor.execute("""

    SELECT quantidade

    FROM inventario

    WHERE usuario=? AND item=?

    """,(

        user_id,

        item

    ))

    resultado = cursor.fetchone()

    if resultado:

        cursor.execute("""

        UPDATE inventario

        SET

            quantidade = quantidade + ?,

            updated_at=?

        WHERE usuario=? AND item=?

        """,(

            quantidade,

            agora(),

            user_id,

            item

        ))

    else:

        cursor.execute("""

        INSERT INTO inventario(

            usuario,

            item,

            quantidade,

            created_at,

            updated_at

        )

        VALUES(?,?,?,?,?)

        """,(

            user_id,

            item,

            quantidade,

            agora(),

            agora()

        ))

    conn.commit()


# ==========================================
# REMOVER ITEM
# ==========================================

def remover_item(user_id, item, quantidade=1):

    cursor.execute("""

    SELECT quantidade

    FROM inventario

    WHERE usuario=? AND item=?

    """,(

        user_id,

        item

    ))

    resultado = cursor.fetchone()

    if resultado is None:

        return False

    if resultado["quantidade"] < quantidade:

        return False

    cursor.execute("""

    UPDATE inventario

    SET

        quantidade = quantidade - ?,

        updated_at=?

    WHERE usuario=? AND item=?

    """,(

        quantidade,

        agora(),

        user_id,

        item

    ))

    conn.commit()

    return True# ==========================================
# ALTERAR SALDO
# ==========================================

def alterar_saldo(user_id, valor):

    cursor.execute("""

    UPDATE usuarios

    SET

        saldo = ?,

        updated_at = ?

    WHERE id = ?

    """,(

        valor,

        agora(),

        user_id

    ))

    conn.commit()


# ==========================================
# ADICIONAR SALDO
# ==========================================

def adicionar_saldo(user_id, valor):

    cursor.execute("""

    UPDATE usuarios

    SET

        saldo = saldo + ?,

        total_ganho = total_ganho + ?,

        updated_at = ?

    WHERE id = ?

    """,(

        valor,

        valor,

        agora(),

        user_id

    ))

    conn.commit()


# ==========================================
# DESCONTAR SALDO
# ==========================================

def remover_saldo(user_id, valor):

    cursor.execute("""

    SELECT saldo

    FROM usuarios

    WHERE id=?

    """,(user_id,))

    usuario = cursor.fetchone()

    if usuario is None:

        return False

    if usuario["saldo"] < valor:

        return False

    cursor.execute("""

    UPDATE usuarios

    SET

        saldo = saldo - ?,

        updated_at = ?

    WHERE id = ?

    """,(

        valor,

        agora(),

        user_id

    ))

    conn.commit()

    return True


# ==========================================
# ALTERAR VIP
# ==========================================

def alterar_vip(user_id, vip):

    cursor.execute("""

    UPDATE usuarios

    SET

        vip = ?,

        updated_at = ?

    WHERE id = ?

    """,(

        vip,

        agora(),

        user_id

    ))

    conn.commit()


# ==========================================
# BANIR USUÁRIO
# ==========================================

def banir_usuario(user_id, motivo):

    cursor.execute("""

    UPDATE usuarios

    SET

        banido = 1,

        motivo_ban = ?,

        updated_at = ?

    WHERE id = ?

    """,(

        motivo,

        agora(),

        user_id

    ))

    conn.commit()


# ==========================================
# DESBANIR USUÁRIO
# ==========================================

def desbanir_usuario(user_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        banido = 0,

        motivo_ban = NULL,

        updated_at = ?

    WHERE id = ?

    """,(

        agora(),

        user_id

    ))

    conn.commit()


# ==========================================
# USUÁRIO BANIDO
# ==========================================

def usuario_banido(user_id):

    cursor.execute("""

    SELECT banido

    FROM usuarios

    WHERE id=?

    """,(user_id,))

    usuario = cursor.fetchone()

    if usuario is None:

        return False

    return usuario["banido"] == 1


# ==========================================
# BUSCAR POR CÓDIGO
# ==========================================

def buscar_por_codigo(codigo):

    cursor.execute("""

    SELECT *

    FROM usuarios

    WHERE codigo=?

    """,(codigo,))

    return cursor.fetchone()


# ==========================================
# TOTAL DE USUÁRIOS
# ==========================================

def total_usuarios():

    cursor.execute("""

    SELECT COUNT(*)

    FROM usuarios

    """)

    return cursor.fetchone()[0]


# ==========================================
# TOP 10 RANKING
# ==========================================

def top_ranking():

    cursor.execute("""

    SELECT

        nome,

        xp,

        nivel

    FROM usuarios

    ORDER BY xp DESC

    LIMIT 10

    """)

    return cursor.fetchall()
