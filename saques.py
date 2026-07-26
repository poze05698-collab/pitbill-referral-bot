from datetime import datetime

from database import conn, cursor
from config import VALOR_MINIMO_SAQUE
from teclado import menu_principal

# ==========================================
# REGISTRAR MÓDULO SAQUES
# ==========================================

def registrar_saques(bot):

    # ======================================
    # SOLICITAR SAQUE
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "💸 Solicitar Saque")
    def solicitar_saque(message):

        user_id = message.from_user.id

        cursor.execute(
            """
            SELECT saldo, pix
            FROM usuarios
            WHERE id=?
            """,
            (user_id,)
        )

        usuario = cursor.fetchone()

        if not usuario:

            bot.reply_to(
                message,
                "Use /start primeiro."
            )

            return

        saldo, pix = usuario

        # ==================================
        # PIX
        # ==================================

        if pix == "":

            bot.reply_to(

                message,

                """
❌ Cadastre sua chave Pix primeiro.

Clique em:

💳 Pix
"""

            )

            return

        # ==================================
        # VALOR MÍNIMO
        # ==================================

        if saldo < VALOR_MINIMO_SAQUE:

            falta = VALOR_MINIMO_SAQUE - saldo

            bot.reply_to(

                message,

                f"""
❌ Saldo insuficiente.

Faltam:

R$ {falta:.2f}
"""

            )

            return

        # ==================================
        # SAQUE DUPLICADO
        # ==================================

        cursor.execute(

            """
            SELECT id

            FROM saques

            WHERE usuario=?

            AND status='PENDENTE'
            """,

            (user_id,)

        )

        if cursor.fetchone():

            bot.reply_to(

                message,

                """
❌ Você já possui um saque pendente.
"""

            )

            return

        # ==================================
        # CONFIRMAÇÃO
        # ==================================

        texto = f"""
💸 Confirma a solicitação?

Valor:

R$ {saldo:.2f}

Pix:

<code>{pix}</code>
"""

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )

        bot.register_next_step_handler(

            message,

            confirmar_saque,

            saldo,

            pix

        )

    # ======================================
    # CONFIRMAR
    # ======================================

    def confirmar_saque(message, valor, pix):

        resposta = message.text.lower()

        if resposta not in [

            "sim",

            "s",

            "confirmar"

        ]:

            bot.reply_to(

                message,

                "❌ Saque cancelado."

            )

            return        # ==================================
        # REGISTRAR SAQUE
        # ==================================

        user_id = message.from_user.id

        cursor.execute(
            """
            INSERT INTO saques(

                usuario,
                valor,
                pix,
                status,
                data

            )

            VALUES(

                ?,?,?,?,?

            )
            """,
            (
                user_id,
                valor,
                pix,
                "PENDENTE",
                datetime.now().strftime(
                    "%d/%m/%Y %H:%M"
                )
            )
        )

        saque_id = cursor.lastrowid

        # ==================================
        # HISTÓRICO
        # ==================================

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
                "SAQUE",
                "Solicitação de saque",
                valor,
                datetime.now().strftime(
                    "%d/%m/%Y %H:%M"
                )
            )
        )

        conn.commit()

        # ==================================
        # CONFIRMAÇÃO USUÁRIO
        # ==================================

        bot.send_message(

            message.chat.id,

            f"""
✅ Solicitação enviada.

🆔 ID:
<code>{saque_id}</code>

💰 Valor:
R$ {valor:.2f}

Aguarde a aprovação do administrador.
""",

            parse_mode="HTML",

            reply_markup=menu_principal()

        )

        # ==================================
        # AVISAR ADMIN
        # ==================================

        try:

            from config import ADMIN_ID

            bot.send_message(

                ADMIN_ID,

                f"""
🚨 Novo saque solicitado

🆔 ID:
{saque_id}

👤 Usuário:
{user_id}

💰 Valor:
R$ {valor:.2f}

Use:

/aprovar {saque_id}

ou

/rejeitar {saque_id}
"""

            )

        except:

            pass
