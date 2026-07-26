from datetime import datetime

from database import conn, cursor

from config import (
    VALOR_MINIMO_SAQUE,
    ADMIN_ID
)

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
            SELECT
                saldo,
                pix

            FROM usuarios

            WHERE id=?
            """,
            (user_id,)
        )

        usuario = cursor.fetchone()

        if usuario is None:

            bot.reply_to(
                message,
                "❌ Use /start primeiro."
            )

            return

        saldo, pix = usuario

        # ==================================
        # PIX
        # ==================================

        if not pix:

            bot.reply_to(
                message,
                """
❌ Você precisa cadastrar sua chave Pix primeiro.

Clique em:

💳 Pix
"""
            )

            return

        # ==================================
        # SALDO
        # ==================================

        if saldo < VALOR_MINIMO_SAQUE:

            falta = VALOR_MINIMO_SAQUE - saldo

            bot.reply_to(
                message,
                f"""
❌ Você ainda não pode sacar.

Faltam:

R$ {falta:.2f}
"""
            )

            return

        # ==================================
        # SAQUE PENDENTE
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
💸 <b>CONFIRMAR SAQUE</b>

💰 Valor:

R$ {saldo:.2f}

💳 Pix:

<code>{pix}</code>

Digite:

<b>SIM</b>

para confirmar.
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
    # CONFIRMAR SAQUE
    # ======================================

    def confirmar_saque(message, valor, pix):

        resposta = message.text.strip().lower()

        if resposta not in [

            "sim",

            "s",

            "confirmar"

        ]:

            bot.reply_to(
                message,
                "❌ Solicitação cancelada."
            )

            return

        user_id = message.from_user.id

        # Verifica novamente o saldo

        cursor.execute(
            """
            SELECT saldo

            FROM usuarios

            WHERE id=?
            """,
            (user_id,)
        )

        saldo_atual = cursor.fetchone()

        if saldo_atual is None:

            bot.reply_to(
                message,
                "❌ Usuário não encontrado."
            )

            return

        if saldo_atual[0] < valor:

            bot.reply_to(
                message,
                "❌ Seu saldo mudou. Solicite novamente."
            )

            return        # ==================================
        # REGISTRAR SAQUE
        # ==================================

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
        # CONFIRMAÇÃO PARA O USUÁRIO
        # ==================================

        bot.send_message(

            message.chat.id,

            f"""
✅ <b>Solicitação enviada com sucesso!</b>

🆔 ID do saque:
<code>{saque_id}</code>

💰 Valor:
<b>R$ {valor:.2f}</b>

⏳ Aguarde a análise do administrador.
""",

            parse_mode="HTML",

            reply_markup=menu_principal()

        )

        # ==================================
        # AVISAR ADMINISTRADOR
        # ==================================

        try:

            bot.send_message(

                ADMIN_ID,

                f"""
🚨 <b>NOVO PEDIDO DE SAQUE</b>

🆔 ID:
<code>{saque_id}</code>

👤 Usuário:
<code>{user_id}</code>

💰 Valor:
<b>R$ {valor:.2f}</b>

Para aprovar:

<code>/aprovar {saque_id}</code>

Para rejeitar:

<code>/rejeitar {saque_id}</code>
""",

                parse_mode="HTML"

            )

        except Exception as erro:

            print(
                f"Erro ao avisar administrador: {erro}"
            )
