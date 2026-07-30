"""
==================================================
 PITBULL REWARDS PLATFORM V3
 usuarios.py
==================================================
"""

from datetime import datetime
import random
import string

from database import (
    conn,
    cursor,
    agora
)

# ==================================================
# CACHE
# ==================================================

CACHE_USUARIOS = {}

# ==================================================
# TRANSAÇÕES
# ==================================================

def iniciar_transacao():

    conn.execute("BEGIN")


def confirmar_transacao():

    conn.commit()


def cancelar_transacao():

    conn.rollback()

# ==================================================
# DATA
# ==================================================

def data():

    return agora()

# ==================================================
# GERADOR DE CÓDIGO
# ==================================================

def gerar_codigo(tamanho=8):

    caracteres = string.ascii_uppercase + string.digits

    while True:

        codigo = "".join(

            random.choice(caracteres)

            for _ in range(tamanho)

        )

        cursor.execute(

            "SELECT id FROM usuarios WHERE codigo=?",

            (codigo,)

        )

        if cursor.fetchone() is None:

            return codigo

# ==================================================
# CACHE
# ==================================================

def limpar_cache(usuario_id=None):

    if usuario_id is None:

        CACHE_USUARIOS.clear()

    else:

        CACHE_USUARIOS.pop(

            usuario_id,

            None

        )

# ==================================================
# USUÁRIO EXISTE
# ==================================================

def usuario_existe(usuario_id):

    cursor.execute(

        """

        SELECT id

        FROM usuarios

        WHERE id=?

        """,

        (usuario_id,)

    )

    return cursor.fetchone() is not None

# ==================================================
# BUSCAR POR ID
# ==================================================

def buscar_usuario(usuario_id):

    if usuario_id in CACHE_USUARIOS:

        return CACHE_USUARIOS[usuario_id]

    cursor.execute(

        """

        SELECT *

        FROM usuarios

        WHERE id=?

        """,

        (usuario_id,)

    )

    usuario = cursor.fetchone()

    if usuario:

        CACHE_USUARIOS[usuario_id] = usuario

    return usuario

# ==================================================
# BUSCAR POR CÓDIGO
# ==================================================

def buscar_codigo(codigo):

    cursor.execute(

        """

        SELECT *

        FROM usuarios

        WHERE codigo=?

        """,

        (codigo,)

    )

    return cursor.fetchone()# ==================================================
# CADASTRAR USUÁRIO
# ==================================================

def cadastrar_usuario(user_id, nome, username):

    if usuario_existe(user_id):

        return buscar_usuario(user_id)

    codigo = gerar_codigo()

    cursor.execute("""

    INSERT INTO usuarios(

        id,

        codigo,

        nome,

        username,

        created_at,

        updated_at

    )

    VALUES(

        ?,?,?,?,?,?

    )

    """, (

        user_id,

        codigo,

        nome,

        username,

        data(),

        data()

    ))

    # Criar carteira automaticamente
    cursor.execute("""

    INSERT INTO carteira(

        usuario_id,

        updated_at

    )

    VALUES(

        ?,?

    )

    """, (

        user_id,

        data()

    ))

    conn.commit()

    limpar_cache(user_id)

    return buscar_usuario(user_id)


# ==================================================
# ATUALIZAR USUÁRIO
# ==================================================

def atualizar_usuario(user_id, nome, username):

    cursor.execute("""

    UPDATE usuarios

    SET

        nome=?,

        username=?,

        updated_at=?

    WHERE id=?

    """, (

        nome,

        username,

        data(),

        user_id

    ))

    conn.commit()

    limpar_cache(user_id)


# ==================================================
# ÚLTIMO LOGIN
# ==================================================

def atualizar_login(user_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        ultimo_login=?,

        updated_at=?

    WHERE id=?

    """, (

        data(),

        data(),

        user_id

    ))

    conn.commit()

    limpar_cache(user_id)


# ==================================================
# APROVAR USUÁRIO
# ==================================================

def aprovar_usuario(user_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        aprovado=1,

        updated_at=?

    WHERE id=?

    """, (

        data(),

        user_id

    ))

    conn.commit()

    limpar_cache(user_id)


# ==================================================
# REJEITAR USUÁRIO
# ==================================================

def rejeitar_usuario(user_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        aprovado=0,

        updated_at=?

    WHERE id=?

    """, (

        data(),

        user_id

    ))

    conn.commit()

    limpar_cache(user_id)


# ==================================================
# BLOQUEAR
# ==================================================

def bloquear_usuario(user_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        bloqueado=1,

        updated_at=?

    WHERE id=?

    """, (

        data(),

        user_id

    ))

    conn.commit()

    limpar_cache(user_id)


# ==================================================
# DESBLOQUEAR
# ==================================================

def desbloquear_usuario(user_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        bloqueado=0,

        updated_at=?

    WHERE id=?

    """, (

        data(),

        user_id

    ))

    conn.commit()

    limpar_cache(user_id)


# ==================================================
# BANIR
# ==================================================

def banir_usuario(user_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        banido=1,

        status='BANIDO',

        updated_at=?

    WHERE id=?

    """, (

        data(),

        user_id

    ))

    conn.commit()

    limpar_cache(user_id)


# ==================================================
# DESBANIR
# ==================================================

def desbanir_usuario(user_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        banido=0,

        status='ATIVO',

        updated_at=?

    WHERE id=?

    """, (

        data(),

        user_id

    ))

    conn.commit()

    limpar_cache(user_id)# ==================================================
# CARTEIRA
# ==================================================

def saldo(usuario_id):

    cursor.execute("""

    SELECT *

    FROM carteira

    WHERE usuario_id=?

    """, (

        usuario_id,

    ))

    return cursor.fetchone()


# ==================================================
# EXTRATO
# ==================================================

def registrar_extrato(

    usuario_id,

    tipo,

    categoria,

    valor,

    saldo_anterior,

    saldo_atual,

    descricao="",

    referencia="",

    admin_id=None

):

    cursor.execute("""

    INSERT INTO extrato(

        usuario_id,

        tipo,

        categoria,

        valor,

        saldo_anterior,

        saldo_atual,

        referencia,

        descricao,

        admin_id,

        created_at

    )

    VALUES(

        ?,?,?,?,?,?,?,?,?,?

    )

    """, (

        usuario_id,

        tipo,

        categoria,

        valor,

        saldo_anterior,

        saldo_atual,

        referencia,

        descricao,

        admin_id,

        data()

    ))


# ==================================================
# ADICIONAR SALDO
# ==================================================

def adicionar_saldo(

    usuario_id,

    valor,

    categoria="GERAL",

    descricao="",

    referencia="",

    admin_id=None

):

    iniciar_transacao()

    try:

        carteira = saldo(usuario_id)

        saldo_anterior = carteira["saldo"]

        saldo_atual = saldo_anterior + valor

        cursor.execute("""

        UPDATE carteira

        SET

            saldo=?,

            total_recebido=total_recebido+?,

            updated_at=?

        WHERE usuario_id=?

        """, (

            saldo_atual,

            valor,

            data(),

            usuario_id

        ))

        cursor.execute("""

        UPDATE usuarios

        SET

            saldo=?,

            total_ganho=total_ganho+?,

            updated_at=?

        WHERE id=?

        """, (

            saldo_atual,

            valor,

            data(),

            usuario_id

        ))

        registrar_extrato(

            usuario_id,

            "ENTRADA",

            categoria,

            valor,

            saldo_anterior,

            saldo_atual,

            descricao,

            referencia,

            admin_id

        )

        confirmar_transacao()

        limpar_cache(usuario_id)

        return True

    except:

        cancelar_transacao()

        return False


# ==================================================
# REMOVER SALDO
# ==================================================

def remover_saldo(

    usuario_id,

    valor,

    categoria="GERAL",

    descricao="",

    referencia="",

    admin_id=None

):

    iniciar_transacao()

    try:

        carteira = saldo(usuario_id)

        saldo_anterior = carteira["saldo"]

        if saldo_anterior < valor:

            cancelar_transacao()

            return False

        saldo_atual = saldo_anterior - valor

        cursor.execute("""

        UPDATE carteira

        SET

            saldo=?,

            updated_at=?

        WHERE usuario_id=?

        """, (

            saldo_atual,

            data(),

            usuario_id

        ))

        cursor.execute("""

        UPDATE usuarios

        SET

            saldo=?,

            updated_at=?

        WHERE id=?

        """, (

            saldo_atual,

            data(),

            usuario_id

        ))

        registrar_extrato(

            usuario_id,

            "SAIDA",

            categoria,

            valor,

            saldo_anterior,

            saldo_atual,

            descricao,

            referencia,

            admin_id

        )

        confirmar_transacao()

        limpar_cache(usuario_id)

        return True

    except:

        cancelar_transacao()

        return False# ==================================================
# XP
# ==================================================

def adicionar_xp(usuario_id, xp):

    cursor.execute("""

    UPDATE usuarios

    SET

        xp = xp + ?,

        experiencia_total = experiencia_total + ?,

        updated_at = ?

    WHERE id = ?

    """, (

        xp,

        xp,

        data(),

        usuario_id

    ))

    conn.commit()

    atualizar_nivel(usuario_id)

    limpar_cache(usuario_id)


# ==================================================
# REMOVER XP
# ==================================================

def remover_xp(usuario_id, xp):

    cursor.execute("""

    UPDATE usuarios

    SET

        xp = CASE
            WHEN xp >= ? THEN xp - ?
            ELSE 0
        END,

        updated_at = ?

    WHERE id = ?

    """, (

        xp,

        xp,

        data(),

        usuario_id

    ))

    conn.commit()

    limpar_cache(usuario_id)


# ==================================================
# NÍVEL
# ==================================================

def atualizar_nivel(usuario_id):

    usuario = buscar_usuario(usuario_id)

    xp = usuario["xp"]

    nivel = 1

    if xp >= 500:
        nivel = 2

    if xp >= 1500:
        nivel = 3

    if xp >= 3000:
        nivel = 4

    if xp >= 5000:
        nivel = 5

    if xp >= 10000:
        nivel = 6

    cursor.execute("""

    UPDATE usuarios

    SET

        nivel=?,

        updated_at=?

    WHERE id=?

    """, (

        nivel,

        data(),

        usuario_id

    ))

    conn.commit()

    atualizar_vip(usuario_id)

    limpar_cache(usuario_id)


# ==================================================
# VIP
# ==================================================

def atualizar_vip(usuario_id):

    usuario = buscar_usuario(usuario_id)

    xp = usuario["xp"]

    vip = "Bronze"

    if xp >= 500:
        vip = "Prata"

    if xp >= 1500:
        vip = "Ouro"

    if xp >= 5000:
        vip = "Diamante"

    cursor.execute("""

    UPDATE usuarios

    SET

        vip=?,

        updated_at=?

    WHERE id=?

    """, (

        vip,

        data(),

        usuario_id

    ))

    conn.commit()

    limpar_cache(usuario_id)


# ==================================================
# PREMIUM
# ==================================================

def premium_ativo(usuario_id):

    usuario = buscar_usuario(usuario_id)

    return usuario["premium"] == 1


def ativar_premium(usuario_id, dias=30):

    from datetime import timedelta

    inicio = datetime.now()

    fim = inicio + timedelta(days=dias)

    cursor.execute("""

    UPDATE usuarios

    SET

        premium=1,

        premium_expira=?,

        premium_multiplicador=2,

        updated_at=?

    WHERE id=?

    """, (

        fim.strftime("%d/%m/%Y %H:%M:%S"),

        data(),

        usuario_id

    ))

    conn.commit()

    limpar_cache(usuario_id)


def desativar_premium(usuario_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        premium=0,

        premium_expira=NULL,

        premium_multiplicador=1,

        updated_at=?

    WHERE id=?

    """, (

        data(),

        usuario_id

    ))

    conn.commit()

    limpar_cache(usuario_id)


# ==================================================
# STREAK
# ==================================================

def atualizar_streak(usuario_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        streak=streak+1,

        updated_at=?

    WHERE id=?

    """, (

        data(),

        usuario_id

    ))

    conn.commit()

    limpar_cache(usuario_id)


def resetar_streak(usuario_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        streak=0,

        updated_at=?

    WHERE id=?

    """, (

        data(),

        usuario_id

    ))

    conn.commit()

    limpar_cache(usuario_id)# ==================================================
# INDICAÇÕES
# ==================================================

def adicionar_indicado(indicador_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        indicados = indicados + 1,

        indicacoes_aprovadas = indicacoes_aprovadas + 1,

        updated_at = ?

    WHERE id = ?

    """, (

        data(),

        indicador_id

    ))

    conn.commit()

    limpar_cache(indicador_id)


# ==================================================
# GRUPO
# ==================================================

def verificar_grupo(usuario_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        grupo_verificado = 1,

        updated_at = ?

    WHERE id = ?

    """, (

        data(),

        usuario_id

    ))

    conn.commit()

    limpar_cache(usuario_id)


# ==================================================
# CANAL
# ==================================================

def verificar_canal(usuario_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        canal_verificado = 1,

        updated_at = ?

    WHERE id = ?

    """, (

        data(),

        usuario_id

    ))

    conn.commit()

    limpar_cache(usuario_id)


# ==================================================
# NOTIFICAÇÕES
# ==================================================

def adicionar_notificacao(

    usuario_id,

    titulo,

    mensagem,

    tipo="INFO"

):

    cursor.execute("""

    INSERT INTO notificacoes(

        usuario_id,

        titulo,

        mensagem,

        tipo,

        created_at

    )

    VALUES(

        ?,?,?,?,?

    )

    """, (

        usuario_id,

        titulo,

        mensagem,

        tipo,

        data()

    ))

    conn.commit()


# ==================================================
# INVENTÁRIO
# ==================================================

def adicionar_item(

    usuario_id,

    item,

    quantidade=1

):

    cursor.execute("""

    SELECT id, quantidade

    FROM inventario

    WHERE

        usuario_id=?

        AND item=?

    """, (

        usuario_id,

        item

    ))

    registro = cursor.fetchone()

    if registro:

        cursor.execute("""

        UPDATE inventario

        SET

            quantidade = quantidade + ?,

            updated_at = ?

        WHERE id = ?

        """, (

            quantidade,

            data(),

            registro["id"]

        ))

    else:

        cursor.execute("""

        INSERT INTO inventario(

            usuario_id,

            item,

            quantidade,

            created_at,

            updated_at

        )

        VALUES(

            ?,?,?,?,?

        )

        """, (

            usuario_id,

            item,

            quantidade,

            data(),

            data()

        ))

    conn.commit()


# ==================================================
# BAÚS
# ==================================================

def adicionar_bau(

    usuario_id,

    tipo

):

    cursor.execute("""

    INSERT INTO baus(

        usuario_id,

        tipo,

        created_at

    )

    VALUES(

        ?,?,?

    )

    """, (

        usuario_id,

        tipo,

        data()

    ))

    conn.commit()


# ==================================================
# CUPONS
# ==================================================

def registrar_cupom(

    usuario_id,

    cupom_id

):

    cursor.execute("""

    INSERT INTO usuario_cupons(

        usuario_id,

        cupom_id,

        created_at

    )

    VALUES(

        ?,?,?

    )

    """, (

        usuario_id,

        cupom_id,

        data()

    ))

    conn.commit()# ==================================================
# HISTÓRICO
# ==================================================

def registrar_historico(

    usuario_id,

    categoria,

    titulo,

    descricao="",

    referencia=""

):

    cursor.execute("""

    INSERT INTO historico(

        usuario,

        categoria,

        titulo,

        descricao,

        referencia,

        created_at

    )

    VALUES(

        ?,?,?,?,?,?

    )

    """, (

        usuario_id,

        categoria,

        titulo,

        descricao,

        referencia,

        data()

    ))

    conn.commit()


# ==================================================
# LOG ADMIN
# ==================================================

def registrar_log_admin(

    admin_id,

    acao,

    categoria,

    usuario_alvo=None,

    referencia="",

    detalhes=""

):

    cursor.execute("""

    INSERT INTO logs_admin(

        admin_id,

        acao,

        categoria,

        usuario_alvo,

        referencia,

        detalhes,

        created_at

    )

    VALUES(

        ?,?,?,?,?,?,?

    )

    """, (

        admin_id,

        acao,

        categoria,

        usuario_alvo,

        referencia,

        detalhes,

        data()

    ))

    conn.commit()


# ==================================================
# ESTATÍSTICAS
# ==================================================

def incrementar_estatistica(chave, valor=1):

    cursor.execute(

        "SELECT valor FROM estatisticas WHERE chave=?",

        (chave,)

    )

    registro = cursor.fetchone()

    if registro:

        cursor.execute("""

        UPDATE estatisticas

        SET

            valor=?,

            updated_at=?

        WHERE chave=?

        """, (

            str(int(registro["valor"]) + valor),

            data(),

            chave

        ))

    else:

        cursor.execute("""

        INSERT INTO estatisticas(

            chave,

            valor,

            updated_at

        )

        VALUES(

            ?,?,?

        )

        """, (

            chave,

            str(valor),

            data()

        ))

    conn.commit()


# ==================================================
# ENGINE DE RECOMPENSAS
# ==================================================

def recompensa(

    usuario_id,

    saldo=0,

    xp=0,

    item=None,

    quantidade_item=1,

    bau=None,

    notificacao=None,

    categoria="GERAL",

    descricao=""

):

    if saldo > 0:

        adicionar_saldo(

            usuario_id,

            saldo,

            categoria=categoria,

            descricao=descricao

        )

    if xp > 0:

        adicionar_xp(

            usuario_id,

            xp

        )

    if item:

        adicionar_item(

            usuario_id,

            item,

            quantidade_item

        )

    if bau:

        adicionar_bau(

            usuario_id,

            bau

        )

    if notificacao:

        adicionar_notificacao(

            usuario_id,

            "🎉 Recompensa",

            notificacao

        )

    registrar_historico(

        usuario_id,

        categoria,

        "Recompensa Recebida",

        descricao

    )

    incrementar_estatistica(

        "recompensas"

    )

    return True


# ==================================================
# PERFIL
# ==================================================

def perfil(usuario_id):

    return buscar_usuario(usuario_id)# ==================================================
# LISTAR USUÁRIOS
# ==================================================

def listar_usuarios():

    cursor.execute("""

    SELECT *

    FROM usuarios

    ORDER BY created_at DESC

    """)

    return cursor.fetchall()


# ==================================================
# TOTAL DE USUÁRIOS
# ==================================================

def total_usuarios():

    cursor.execute("""

    SELECT COUNT(*) AS total

    FROM usuarios

    """)

    resultado = cursor.fetchone()

    return resultado["total"]


# ==================================================
# USUÁRIOS APROVADOS
# ==================================================

def total_aprovados():

    cursor.execute("""

    SELECT COUNT(*) AS total

    FROM usuarios

    WHERE aprovado=1

    """)

    return cursor.fetchone()["total"]


# ==================================================
# USUÁRIOS PENDENTES
# ==================================================

def total_pendentes():

    cursor.execute("""

    SELECT COUNT(*) AS total

    FROM usuarios

    WHERE aprovado=0

    """)

    return cursor.fetchone()["total"]


# ==================================================
# USUÁRIOS PREMIUM
# ==================================================

def total_premium():

    cursor.execute("""

    SELECT COUNT(*) AS total

    FROM usuarios

    WHERE premium=1

    """)

    return cursor.fetchone()["total"]


# ==================================================
# USUÁRIOS VIP
# ==================================================

def total_vip(vip):

    cursor.execute("""

    SELECT COUNT(*) AS total

    FROM usuarios

    WHERE vip=?

    """, (

        vip,

    ))

    return cursor.fetchone()["total"]


# ==================================================
# TOP INDICADORES
# ==================================================

def ranking_indicacoes(limite=10):

    cursor.execute("""

    SELECT *

    FROM usuarios

    ORDER BY indicados DESC

    LIMIT ?

    """, (

        limite,

    ))

    return cursor.fetchall()


# ==================================================
# TOP XP
# ==================================================

def ranking_xp(limite=10):

    cursor.execute("""

    SELECT *

    FROM usuarios

    ORDER BY xp DESC

    LIMIT ?

    """, (

        limite,

    ))

    return cursor.fetchall()


# ==================================================
# TOP SALDO
# ==================================================

def ranking_saldo(limite=10):

    cursor.execute("""

    SELECT *

    FROM usuarios

    ORDER BY saldo DESC

    LIMIT ?

    """, (

        limite,

    ))

    return cursor.fetchall()


# ==================================================
# FECHAR CACHE
# ==================================================

def reiniciar_cache():

    CACHE_USUARIOS.clear()


# ==================================================
# FINAL
# ==================================================

print("✅ usuarios.py carregado com sucesso.")
