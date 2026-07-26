import time

from database import cursor

from utils import (
    adicionar_log,
    usuario_bloqueado
)

# ==========================================
# CONTROLE DE TEMPO
# ==========================================

ultimo_comando = {}

# ==========================================
# REGISTRAR MÓDULO
# ==========================================

def registrar_antifraude(bot):

    pass

# ==========================================
# ANTI FLOOD
# ==========================================

def anti_flood(user_id):

    agora = time.time()

    if user_id not in ultimo_comando:

        ultimo_comando[user_id] = agora

        return True

    diferenca = agora - ultimo_comando[user_id]

    ultimo_comando[user_id] = agora

    if diferenca < 2:

        adicionar_log(

            user_id,

            "ANTI FLOOD",

            "Comandos enviados muito rápido."

        )

        return False

    return True

# ==========================================
# AUTO INDICAÇÃO
# ==========================================

def auto_indicacao(indicador, indicado):

    if indicador == indicado:

        adicionar_log(

            indicador,

            "AUTO INDICAÇÃO",

            "Tentativa bloqueada."

        )

        return False

    return True

# ==========================================
# CADASTRO DUPLICADO
# ==========================================

def cadastro_existente(user_id):

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
# USUÁRIO BLOQUEADO
# ==========================================

def acesso_permitido(user_id):

    return not usuario_bloqueado(user_id)# ==========================================
# SAQUE DUPLICADO
# ==========================================

def saque_pendente(user_id):

    cursor.execute(
        """
        SELECT id

        FROM saques

        WHERE usuario=?

        AND status='PENDENTE'
        """,
        (user_id,)
    )

    return cursor.fetchone() is not None


# ==========================================
# LIMITE DE TENTATIVAS
# ==========================================

tentativas = {}

def verificar_tentativas(user_id):

    if user_id not in tentativas:

        tentativas[user_id] = 1

        return True

    tentativas[user_id] += 1

    if tentativas[user_id] >= 10:

        adicionar_log(

            user_id,

            "MUITAS TENTATIVAS",

            "Usuário excedeu o limite de tentativas."

        )

        return False

    return True


# ==========================================
# RESETAR TENTATIVAS
# ==========================================

def resetar_tentativas(user_id):

    tentativas[user_id] = 0


# ==========================================
# VERIFICAR PIX DUPLICADO
# ==========================================

def pix_duplicado(chave_pix, user_id):

    cursor.execute(
        """
        SELECT id

        FROM usuarios

        WHERE pix=?

        AND id<>?
        """,
        (
            chave_pix,
            user_id
        )
    )

    usuario = cursor.fetchone()

    if usuario:

        adicionar_log(

            user_id,

            "PIX DUPLICADO",

            f"Tentou cadastrar um Pix já utilizado."

        )

        return True

    return False


# ==========================================
# VERIFICAR INDICAÇÃO DUPLICADA
# ==========================================

def indicacao_duplicada(indicador, indicado):

    cursor.execute(
        """
        SELECT id

        FROM indicacoes

        WHERE indicador=?

        AND indicado=?
        """,
        (
            indicador,
            indicado
        )
    )

    if cursor.fetchone():

        adicionar_log(

            indicador,

            "INDICAÇÃO DUPLICADA",

            f"Usuário {indicado}"

        )

        return True

    return False


# ==========================================
# REGISTRAR SUSPEITA
# ==========================================

def registrar_suspeita(user_id, motivo):

    adicionar_log(

        user_id,

        "ATIVIDADE SUSPEITA",

        motivo

    )


# ==========================================
# VERIFICAR ACESSO COMPLETO
# ==========================================

def verificar_antifraude(user_id):

    if not acesso_permitido(user_id):

        return False

    if not verificar_tentativas(user_id):

        return False

    if not anti_flood(user_id):

        return False

    return True


# ==========================================
# LIMPAR DADOS TEMPORÁRIOS
# ==========================================

def limpar_cache():

    ultimo_comando.clear()

    tentativas.clear()


# ==========================================
# FIM DO MÓDULO
# ==========================================
