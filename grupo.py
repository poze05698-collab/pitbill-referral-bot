"""
==================================================
 PITBULL REWARDS PLATFORM V3
 grupo.py
==================================================
"""

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import (
    cursor,
    conn,
    get_config
)

from usuarios import (

    buscar_usuario,

    verificar_grupo,

    aprovar_usuario,

    adicionar_notificacao

)

# ==================================================
# BOTÃO ENTRAR NO GRUPO
# ==================================================

def teclado_grupo():

    menu = InlineKeyboardMarkup()

    menu.add(

        InlineKeyboardButton(

            "📢 Entrar no Grupo",

            url=get_config("grupo_link")

        )

    )

    menu.add(

        InlineKeyboardButton(

            "✅ Já Entrei",

            callback_data="verificar_grupo"

        )

    )

    return menu

# ==================================================
# USUÁRIO APROVADO
# ==================================================

def usuario_aprovado(usuario_id):

    usuario = buscar_usuario(usuario_id)

    if usuario is None:

        return False

    return usuario["aprovado"] == 1

# ==================================================
# GRUPO VERIFICADO
# ==================================================

def grupo_verificado(usuario_id):

    usuario = buscar_usuario(usuario_id)

    if usuario is None:

        return False

    return usuario["grupo_verificado"] == 1

# ==================================================
# LIBERAR USUÁRIO
# ==================================================

def liberar_usuario(usuario_id):

    verificar_grupo(usuario_id)

    aprovar_usuario(usuario_id)

    adicionar_notificacao(

        usuario_id,

        "✅ Conta Liberada",

        "Sua conta foi aprovada com sucesso."

    )

    return True# ==================================================
# VERIFICAR MEMBRO DO GRUPO
# ==================================================

def verificar_membro_grupo(bot, usuario_id):

    grupo_id = get_config("grupo_id")

    if not grupo_id:
        return False

    try:

        membro = bot.get_chat_member(

            grupo_id,

            usuario_id

        )

        return membro.status in (

            "creator",

            "administrator",

            "member"

        )

    except Exception:

        return False


# ==================================================
# PROCESSAR VERIFICAÇÃO
# ==================================================

def processar_verificacao(bot, usuario_id):

    if not verificar_membro_grupo(bot, usuario_id):

        return False, (
            "❌ Você ainda não entrou no grupo oficial.\n\n"
            "Entre no grupo e tente novamente."
        )

    verificar_grupo(usuario_id)

    if get_config("aprovacao_manual") == "1":

        adicionar_notificacao(

            usuario_id,

            "⏳ Aprovação Pendente",

            "Sua conta está aguardando aprovação da equipe."

        )

        return True, (
            "⏳ Seu cadastro foi enviado para aprovação.\n"
            "Aguarde um administrador liberar sua conta."
        )

    liberar_usuario(usuario_id)

    return True, (
        "✅ Sua conta foi liberada com sucesso!\n"
        "Agora você já pode utilizar a plataforma."
    )


# ==================================================
# ACESSO AO MENU
# ==================================================

def pode_acessar(usuario_id):

    usuario = buscar_usuario(usuario_id)

    if usuario is None:
        return False

    if usuario["banido"] == 1:
        return False

    if usuario["bloqueado"] == 1:
        return False

    if usuario["aprovado"] == 0:
        return False

    return True# ==================================================
# REVALIDAR ACESSO
# ==================================================

def validar_acesso(bot, usuario_id):

    # Grupo obrigatório desativado
    if get_config("grupo_obrigatorio") != "1":

        return True

    # Usuário ainda não aprovado
    if not usuario_aprovado(usuario_id):

        return False

    # Continua no grupo?
    if not verificar_membro_grupo(bot, usuario_id):

        cursor.execute("""

        UPDATE usuarios

        SET

            grupo_verificado = 0,

            aprovado = 0,

            updated_at = ?

        WHERE id = ?

        """, (

            agora(),

            usuario_id

        ))

        conn.commit()

        adicionar_notificacao(

            usuario_id,

            "⚠️ Acesso Suspenso",

            "Você saiu do grupo oficial. Entre novamente para recuperar o acesso."

        )

        return False

    return True


# ==================================================
# STATUS DO USUÁRIO
# ==================================================

def status_usuario(usuario_id):

    usuario = buscar_usuario(usuario_id)

    if usuario is None:

        return "NAO_CADASTRADO"

    if usuario["banido"]:

        return "BANIDO"

    if usuario["bloqueado"]:

        return "BLOQUEADO"

    if not usuario["grupo_verificado"]:

        return "GRUPO"

    if not usuario["aprovado"]:

        return "APROVACAO"

    return "LIBERADO"


# ==================================================
# MENSAGEM DE ACESSO
# ==================================================

def mensagem_status(status):

    mensagens = {

        "NAO_CADASTRADO":
        "❌ Usuário não encontrado.",

        "BANIDO":
        "🚫 Sua conta foi banida da plataforma.",

        "BLOQUEADO":
        "⛔ Sua conta está temporariamente bloqueada.",

        "GRUPO":
        "📢 Entre no grupo oficial para continuar.",

        "APROVACAO":
        "⏳ Aguarde a aprovação da equipe.",

        "LIBERADO":
        "✅ Acesso liberado."

    }

    return mensagens.get(

        status,

        "Erro desconhecido."

    )


# ==================================================
# FINAL
# ==================================================

print("✅ grupo.py carregado com sucesso.")
