from config import (
    ADMIN_ID,
    VALOR_MINIMO_SAQUE
)

from database import (
    conn,
    cursor
)

from teclado import (
    menu_principal,
    menu_confirmacao
)

from utils import (
    verificar_acesso,
    adicionar_historico,
    adicionar_log,
    agora
)

# ==========================================
# REGISTRAR MÓDULO
# ==========================================

def registrar_saques(bot):

    # ======================================
    # SOLICITAR SAQUE
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "💸 Solicitar Saque")
    def solicitar_saque(message):

        if not verificar_acesso(bot, message):
            return

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
                "Use /start primeiro."
            )

            return

        saldo = usuario[0]
        pix = usuario[1]

        # ==================================
        # PIX
        # ==================================

        if pix == "":

            bot.reply_to(

                message,

                """
❌ Você precisa cadastrar
uma chave Pix antes.

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
💸 <b>CONFIRMAR SAQUE</b>

Valor:

<b>R$ {saldo:.2f}</b>

Pix:

<code>{pix}</code>

Deseja continuar?
"""

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML",

            reply_markup=menu_confirmacao()

        )

        bot.register_next_step_handler(

            message,

            confirmar_saque,

            saldo,

            pix

        )    # ======================================
    # CONFIRMAR SAQUE
    # ======================================

    def confirmar_saque(message, valor, pix):

        if not verificar_acesso(bot, message):
            return

        resposta = message.text.lower()

        if resposta not in [

            "sim",

            "s",

            "confirmar",

            "✅ confirmar"

        ]:

            bot.send_message(

                message.chat.id,

                """
❌ Solicitação cancelada.
""",

                reply_markup=menu_principal()

            )

            return

        user_id = message.from_user.id

        # ==================================
        # REGISTRAR SAQUE
        # ==================================

        cursor.execute(
            """
            INSERT INTO saques(

                usuario,

                valor,

                pix,

                status,

                data,

                aprovado_por,

                data_aprovacao

            )

            VALUES(

                ?,?,?,?,?,?,?

            )
            """,
            (
                user_id,
                valor,
                pix,
                "PENDENTE",
                agora(),
                None,
                None
            )
        )

        saque_id = cursor.lastrowid

        conn.commit()

        # ==================================
        # HISTÓRICO
        # ==================================

        adicionar_historico(

            user_id,

            "SAQUE",

            "Solicitação de saque",

            valor

        )

        # ==================================
        # LOG
        # ==================================

        adicionar_log(

            user_id,

            "SAQUE",

            f"Solicitou saque de R$ {valor:.2f}"

        )

        # ==================================
        # MENSAGEM USUÁRIO
        # ==================================

        bot.send_message(

            message.chat.id,

            f"""
✅ <b>Solicitação enviada!</b>

🆔 ID do saque:

<code>{saque_id}</code>

💰 Valor:

<b>R$ {valor:.2f}</b>

Aguarde a análise do administrador.
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
🚨 <b>NOVO SAQUE</b>

🆔 ID:

<code>{saque_id}</code>

👤 Usuário:

<code>{user_id}</code>

💰 Valor:

<b>R$ {valor:.2f}</b>

💳 Pix:

<code>{pix}</code>

Comandos:

/aprovar {saque_id}

/rejeitar {saque_id}
""",

                parse_mode="HTML"

            )

        except Exception as erro:

            print(erro)    # ======================================
    # APROVAR SAQUE
    # ======================================

    @bot.message_handler(commands=["aprovar"])
    def aprovar_saque(message):

        if message.from_user.id != ADMIN_ID:
            return

        try:

            saque_id = int(message.text.split()[1])

        except:

            bot.reply_to(

                message,

                "Use:\n\n/aprovar ID"

            )

            return

        cursor.execute(
            """
            SELECT

                usuario,
                valor,
                status

            FROM saques

            WHERE id=?
            """,
            (saque_id,)
        )

        saque = cursor.fetchone()

        if saque is None:

            bot.reply_to(

                message,

                "❌ Saque não encontrado."

            )

            return

        usuario, valor, status = saque

        if status != "PENDENTE":

            bot.reply_to(

                message,

                "❌ Este saque já foi processado."

            )

            return

        # ==================================
        # DESCONTAR SALDO
        # ==================================

        cursor.execute(
            """
            UPDATE usuarios

            SET saldo = saldo - ?

            WHERE id=?
            """,
            (
                valor,
                usuario
            )
        )

        # ==================================
        # ATUALIZAR SAQUE
        # ==================================

        cursor.execute(
            """
            UPDATE saques

            SET

                status='APROVADO',

                aprovado_por=?,

                data_aprovacao=?

            WHERE id=?
            """,
            (
                ADMIN_ID,
                agora(),
                saque_id
            )
        )

        conn.commit()

        adicionar_historico(

            usuario,

            "SAQUE",

            "Saque aprovado",

            valor

        )

        adicionar_log(

            ADMIN_ID,

            "APROVAR SAQUE",

            f"Saque {saque_id} aprovado"

        )

        try:

            bot.send_message(

                usuario,

                f"""
🎉 Seu saque foi aprovado!

💰 Valor:

R$ {valor:.2f}

Em breve o pagamento será realizado.
"""

            )

        except:

            pass

        bot.reply_to(

            message,

            "✅ Saque aprovado com sucesso."

        )

    # ======================================
    # REJEITAR SAQUE
    # ======================================

    @bot.message_handler(commands=["rejeitar"])
    def rejeitar_saque(message):

        if message.from_user.id != ADMIN_ID:
            return

        try:

            saque_id = int(message.text.split()[1])

        except:

            bot.reply_to(

                message,

                "Use:\n\n/rejeitar ID"

            )

            return

        cursor.execute(
            """
            SELECT

                usuario,
                valor,
                status

            FROM saques

            WHERE id=?
            """,
            (saque_id,)
        )

        saque = cursor.fetchone()

        if saque is None:

            bot.reply_to(

                message,

                "❌ Saque não encontrado."

            )

            return

        usuario, valor, status = saque

        if status != "PENDENTE":

            bot.reply_to(

                message,

                "❌ Este saque já foi processado."

            )

            return

        cursor.execute(
            """
            UPDATE saques

            SET

                status='REJEITADO',

                aprovado_por=?,

                data_aprovacao=?

            WHERE id=?
            """,
            (
                ADMIN_ID,
                agora(),
                saque_id
            )
        )

        conn.commit()

        adicionar_historico(

            usuario,

            "SAQUE",

            "Saque rejeitado",

            valor

        )

        adicionar_log(

            ADMIN_ID,

            "REJEITAR SAQUE",

            f"Saque {saque_id} rejeitado"

        )

        try:

            bot.send_message(

                usuario,

                f"""
❌ Seu saque foi rejeitado.

Caso tenha dúvidas,
entre em contato com o suporte.
"""

            )

        except:

            pass

        bot.reply_to(

            message,

            "✅ Saque rejeitado."
        )
