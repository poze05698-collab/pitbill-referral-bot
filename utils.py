from database import cursor

# ==========================================
# VERIFICAR SE O USUÁRIO ESTÁ BLOQUEADO
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
# VERIFICAR ACESSO AO BOT
# ==========================================

def verificar_acesso(bot, message):

    if usuario_bloqueado(message.from_user.id):

        bot.send_message(

            message.chat.id,

            """
🚫 <b>CONTA BLOQUEADA</b>

Sua conta foi bloqueada pelo administrador.

Você não pode utilizar o bot enquanto estiver bloqueado.

Entre em contato com o suporte caso ache que isso foi um erro.
""",

            parse_mode="HTML"

        )

        return False

    return True


# ==========================================
# VERIFICAR SE É ADMIN
# ==========================================

def eh_admin(user_id, admin_id):

    return user_id == admin_id
