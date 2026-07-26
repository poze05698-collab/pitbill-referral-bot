from database import cursor

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

    if usuario_bloqueado(message.from_user.id):

        bot.send_message(

            message.chat.id,

            """
🚫 <b>CONTA BLOQUEADA</b>

Seu acesso ao bot foi bloqueado pelo administrador.

Entre em contato com o suporte para mais informações.
""",

            parse_mode="HTML"

        )

        return False

    return True
