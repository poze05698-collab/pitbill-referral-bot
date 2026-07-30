"""
==================================================
 PITBULL REWARDS PLATFORM V3
 pix.py
==================================================
"""

import re

from database import conn, cursor, agora
from usuarios import (
    buscar_usuario,
    limpar_cache,
    adicionar_notificacao
)

# ==================================================
# VALIDADORES
# ==================================================

def validar_email(chave):

    padrao = r"^[^@]+@[^@]+\.[^@]+$"
    return re.match(padrao, chave) is not None


def validar_cpf(chave):

    numeros = "".join(filter(str.isdigit, chave))
    return len(numeros) == 11


def validar_telefone(chave):

    numeros = "".join(filter(str.isdigit, chave))
    return len(numeros) in (10, 11, 13)


def validar_aleatoria(chave):

    return len(chave.strip()) >= 20

# ==================================================
# IDENTIFICAR TIPO
# ==================================================

def identificar_tipo_pix(chave):

    chave = chave.strip()

    if validar_email(chave):
        return "EMAIL"

    if validar_cpf(chave):
        return "CPF"

    if validar_telefone(chave):
        return "TELEFONE"

    if validar_aleatoria(chave):
        return "ALEATORIA"

    return None

# ==================================================
# CONSULTAR PIX
# ==================================================

def obter_pix(usuario_id):

    usuario = buscar_usuario(usuario_id)

    if usuario:

        return usuario["pix"]

    return ""# ==================================================
# CADASTRAR / ALTERAR PIX
# ==================================================

def salvar_pix(usuario_id, chave):

    chave = chave.strip()

    tipo = identificar_tipo_pix(chave)

    if tipo is None:

        return False, "❌ Chave PIX inválida."

    cursor.execute("""

    UPDATE usuarios

    SET

        pix = ?,

        pix_tipo = ?,

        updated_at = ?

    WHERE id = ?

    """, (

        chave,

        tipo,

        agora(),

        usuario_id

    ))

    conn.commit()

    limpar_cache(usuario_id)

    adicionar_notificacao(

        usuario_id,

        "💳 PIX Atualizado",

        f"Sua chave PIX do tipo {tipo} foi salva com sucesso."

    )

    return True, "✅ Chave PIX salva com sucesso."

# ==================================================
# REMOVER PIX
# ==================================================

def remover_pix(usuario_id):

    cursor.execute("""

    UPDATE usuarios

    SET

        pix = '',

        pix_tipo = '',

        updated_at = ?

    WHERE id = ?

    """, (

        agora(),

        usuario_id

    ))

    conn.commit()

    limpar_cache(usuario_id)

    adicionar_notificacao(

        usuario_id,

        "🗑️ PIX Removido",

        "Sua chave PIX foi removida."

    )

    return True

# ==================================================
# VERIFICAR PIX
# ==================================================

def possui_pix(usuario_id):

    usuario = buscar_usuario(usuario_id)

    if usuario is None:

        return False

    return bool(usuario["pix"])

# ==================================================
# DADOS DO PIX
# ==================================================

def dados_pix(usuario_id):

    usuario = buscar_usuario(usuario_id)

    if usuario is None:

        return None

    return {

        "chave": usuario["pix"],

        "tipo": usuario["pix_tipo"]

    }

# ==================================================
# MENSAGEM DO PIX
# ==================================================

def texto_pix(usuario_id):

    dados = dados_pix(usuario_id)

    if dados is None or not dados["chave"]:

        return (
            "💳 <b>PIX</b>\n\n"
            "Você ainda não possui uma chave PIX cadastrada."
        )

    return (
        "💳 <b>PIX CADASTRADO</b>\n\n"
        f"Tipo: <b>{dados['tipo']}</b>\n"
        f"Chave:\n<code>{dados['chave']}</code>"
    )# ==================================================
# MENSAGEM DE CADASTRO
# ==================================================

def mensagem_cadastro():

    return (
        "💳 <b>CADASTRO DE PIX</b>\n\n"
        "Envie sua chave PIX.\n\n"
        "Tipos aceitos:\n"
        "• CPF\n"
        "• E-mail\n"
        "• Telefone\n"
        "• Chave Aleatória"
    )


# ==================================================
# VALIDAR CADASTRO
# ==================================================

def cadastrar_pix(usuario_id, chave):

    sucesso, mensagem = salvar_pix(

        usuario_id,

        chave

    )

    return sucesso, mensagem


# ==================================================
# FORMATAR PIX
# ==================================================

def pix_formatado(usuario_id):

    dados = dados_pix(usuario_id)

    if dados is None:

        return "Nenhuma chave cadastrada."

    if dados["chave"] == "":

        return "Nenhuma chave cadastrada."

    return (

        f"💳 <b>PIX CADASTRADO</b>\n\n"

        f"Tipo:\n"

        f"<b>{dados['tipo']}</b>\n\n"

        f"Chave:\n"

        f"<code>{dados['chave']}</code>"

    )


# ==================================================
# PIX OBRIGATÓRIO
# ==================================================

def validar_pix_para_saque(usuario_id):

    if possui_pix(usuario_id):

        return True

    return False


# ==================================================
# FINAL
# ==================================================

print("✅ pix.py carregado com sucesso.")
