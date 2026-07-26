import time

from database import (
    conn,
    cursor
)

from utils import (
    adicionar_log,
    bloquear_usuario
)


# ==========================================
# CONTROLE DE TEMPO
# ==========================================

comandos_usuario = {}


tentativas_usuario = {}



# ==========================================
# REGISTRAR MÓDULO
# ==========================================

def registrar_antifraude(bot):


    pass



# ==========================================
# ANTI FLOOD
# ==========================================

def verificar_flood(user_id):

    agora = time.time()


    if user_id not in comandos_usuario:

        comandos_usuario[user_id] = agora

        return True



    intervalo = agora - comandos_usuario[user_id]


    comandos_usuario[user_id] = agora



    # menos de 2 segundos

    if intervalo < 2:


        adicionar_log(

            user_id,

            "ANTI FLOOD",

            "Muitas mensagens em pouco tempo."

        )


        return False



    return True



# ==========================================
# CONTROLE DE TENTATIVAS
# ==========================================

def registrar_tentativa(user_id):


    if user_id not in tentativas_usuario:

        tentativas_usuario[user_id] = 1


    else:

        tentativas_usuario[user_id] += 1



    if tentativas_usuario[user_id] >= 10:


        bloquear_usuario(user_id)


        adicionar_log(

            user_id,

            "BLOQUEIO ANTIFRAUDE",

            "Excesso de tentativas."

        )


        return False



    return True



# ==========================================
# RESETAR TENTATIVAS
# ==========================================

def resetar_tentativas(user_id):

    if user_id in tentativas_usuario:

        del tentativas_usuario[user_id]# ==========================================
# VERIFICAR PIX DUPLICADO
# ==========================================

def verificar_pix_existente(pix, user_id):


    cursor.execute(

        """
        SELECT id

        FROM usuarios

        WHERE pix=?

        AND id<>?

        """,

        (

            pix,

            user_id

        )

    )


    resultado = cursor.fetchone()



    if resultado:


        adicionar_log(

            user_id,

            "PIX DUPLICADO",

            f"Tentativa de usar Pix de outro usuário."

        )


        return True



    return False



# ==========================================
# VERIFICAR SAQUE DUPLICADO
# ==========================================

def verificar_saque_pendente(user_id):


    cursor.execute(

        """
        SELECT id

        FROM saques

        WHERE usuario=?

        AND status='PENDENTE'

        """,

        (user_id,)

    )


    saque = cursor.fetchone()



    if saque:


        adicionar_log(

            user_id,

            "SAQUE DUPLICADO",

            "Tentativa de criar novo saque pendente."

        )


        return True



    return False



# ==========================================
# VERIFICAR INDICAÇÃO FRAUDULENTA
# ==========================================

def verificar_indicacao_falsa(indicador, indicado):


    # mesmo usuário

    if indicador == indicado:


        adicionar_log(

            indicado,

            "AUTO INDICAÇÃO",

            "Tentativa de indicar a própria conta."

        )


        return True



    cursor.execute(

        """
        SELECT id

        FROM indicacoes

        WHERE indicado=?

        """,

        (indicado,)

    )


    existe = cursor.fetchone()



    if existe:


        adicionar_log(

            indicado,

            "INDICAÇÃO DUPLICADA",

            "Usuário já possui indicação."

        )


        return True



    return False



# ==========================================
# LIMPAR CONTROLES TEMPORÁRIOS
# ==========================================

def limpar_antifraude():


    comandos_usuario.clear()


    tentativas_usuario.clear()# ==========================================
# VERIFICAÇÃO PRINCIPAL
# ==========================================

def verificar_antifraude(user_id):


    # verificar flood

    if not verificar_flood(user_id):

        return False



    # registrar tentativa

    if not registrar_tentativa(user_id):

        return False



    return True



# ==========================================
# VERIFICAR USUÁRIO ANTES DE SAQUE
# ==========================================

def pode_sacar(user_id):


    if verificar_saque_pendente(user_id):

        return False


    return True



# ==========================================
# VERIFICAR PIX ANTES DE SALVAR
# ==========================================

def pode_cadastrar_pix(pix, user_id):


    if verificar_pix_existente(

        pix,

        user_id

    ):

        return False


    return True



# ==========================================
# VERIFICAR INDICAÇÃO
# ==========================================

def pode_indicar(indicador, indicado):


    if verificar_indicacao_falsa(

        indicador,

        indicado

    ):

        return False


    return True



# ==========================================
# REGISTRAR SUSPEITA
# ==========================================

def registrar_suspeita(

    user_id,

    motivo

):


    adicionar_log(

        user_id,

        "SUSPEITA",

        motivo

    )



# ==========================================
# FIM DO ANTIFRAUDE
# ==========================================
