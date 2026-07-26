import telebot

from datetime import datetime

from config import ADMIN_ID
from database import conn, cursor

# ==========================================
# REGISTRAR MÓDULO ADMIN
# ==========================================

def registrar_admin(bot):

    # ======================================
    # VERIFICAR ADMIN
    # ======================================

    def eh_admin(user_id):

        return user_id == ADMIN_ID

    # ======================================
    # PAINEL ADMIN
    # ======================================

    @bot.message_handler(commands=["admin"])
    def painel_admin(message):

        if not eh_admin(message.from_user.id):

            return

        texto = """
👑 <b>PAINEL ADMINISTRATIVO</b>

Comandos disponíveis:

📊 /estatisticas
👥 /usuarios

💸 /pedidos
✅ /aprovar ID
❌ /rejeitar ID

💰 /addsaldo ID VALOR

🏆 /ranking

🚫 /banir ID
✅ /desbanir ID

⚙️ /config
📜 /historico ID
"""

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )

    # ======================================
    # TOTAL DE USUÁRIOS
    # ======================================

    @bot.message_handler(commands=["usuarios"])
    def usuarios(message):

        if not eh_admin(message.from_user.id):

            return

        cursor.execute(
            "SELECT COUNT(*) FROM usuarios"
        )

        total = cursor.fetchone()[0]

        bot.send_message(

            message.chat.id,

            f"""
👥 <b>USUÁRIOS CADASTRADOS</b>

Total:

<b>{total}</b>
""",

            parse_mode="HTML"

        )

    # ======================================
    # ESTATÍSTICAS
    # ======================================

    @bot.message_handler(commands=["estatisticas"])
    def estatisticas(message):

        if not eh_admin(message.from_user.id):

            return

        cursor.execute(
            "SELECT COUNT(*) FROM usuarios"
        )

        total_usuarios = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM saques"
        )

        total_saques = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT IFNULL(SUM(valor),0)

            FROM saques

            WHERE status='APROVADO'
            """
        )

        total_pago = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)

            FROM indicacoes

            WHERE status='APROVADA'
            """
        )

        indicacoes = cursor.fetchone()[0]

        texto = f"""
📊 <b>ESTATÍSTICAS DO BOT</b>

👥 Usuários:
<b>{total_usuarios}</b>

👤 Indicações aprovadas:
<b>{indicacoes}</b>

💸 Total de saques:
<b>{total_saques}</b>

💰 Total pago:

<b>R$ {total_pago:.2f}</b>
"""

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )    # ======================================
    # PEDIDOS DE SAQUE
    # ======================================

    @bot.message_handler(commands=["pedidos"])
    def pedidos(message):

        if not eh_admin(message.from_user.id):
            return

        cursor.execute(
            """
            SELECT

                id,
                usuario,
                valor,
                pix,
                data

            FROM saques

            WHERE status='PENDENTE'

            ORDER BY id ASC
            """
        )

        saques = cursor.fetchall()

        if len(saques) == 0:

            bot.send_message(

                message.chat.id,

                "✅ Não existem saques pendentes."

            )

            return

        texto = "📋 <b>SAQUES PENDENTES</b>\n\n"

        for saque in saques:

            texto += f"""
🆔 ID: <code>{saque[0]}</code>

👤 Usuário:
<code>{saque[1]}</code>

💰 Valor:
<b>R$ {saque[2]:.2f}</b>

💳 Pix:
<code>{saque[3]}</code>

📅 Data:
{saque[4]}

──────────────

"""

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )

    # ======================================
    # APROVAR SAQUE
    # ======================================

    @bot.message_handler(commands=["aprovar"])
    def aprovar(message):

        if not eh_admin(message.from_user.id):
            return

        try:

            saque_id = int(
                message.text.split()[1]
            )

        except:

            bot.reply_to(
                message,
                "Use:\n/aprovar ID"
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
                "❌ Esse saque já foi processado."
            )

            return

        cursor.execute(
            """
            UPDATE saques

            SET status='APROVADO'

            WHERE id=?
            """,
            (saque_id,)
        )

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
                usuario,
                "SAQUE",
                "Saque aprovado",
                valor,
                datetime.now().strftime(
                    "%d/%m/%Y %H:%M"
                )
            )
        )

        conn.commit()

        try:

            bot.send_message(

                usuario,

                f"""
✅ <b>Seu saque foi aprovado!</b>

💰 Valor:

<b>R$ {valor:.2f}</b>

Em breve o pagamento será realizado.
""",

                parse_mode="HTML"

            )

        except Exception as erro:

            print(erro)

        bot.reply_to(

            message,

            "✅ Saque aprovado com sucesso."

        )

    # ======================================
    # REJEITAR SAQUE
    # ======================================

    @bot.message_handler(commands=["rejeitar"])
    def rejeitar(message):

        if not eh_admin(message.from_user.id):
            return

        try:

            saque_id = int(
                message.text.split()[1]
            )

        except:

            bot.reply_to(
                message,
                "Use:\n/rejeitar ID"
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
                "❌ Esse saque já foi processado."
            )

            return

        cursor.execute(
            """
            UPDATE saques

            SET status='REJEITADO'

            WHERE id=?
            """,
            (saque_id,)
        )

        conn.commit()

        try:

            bot.send_message(

                usuario,

                f"""
❌ <b>Seu saque foi rejeitado.</b>

💰 Valor:

<b>R$ {valor:.2f}</b>

Entre em contato com o suporte caso tenha dúvidas.
""",

                parse_mode="HTML"

            )

        except Exception as erro:

            print(erro)

        bot.reply_to(

            message,

            "❌ Saque rejeitado."

        )    # ======================================
    # ADICIONAR SALDO
    # ======================================

    @bot.message_handler(commands=["addsaldo"])
    def adicionar_saldo(message):

        if not eh_admin(message.from_user.id):
            return

        try:

            dados = message.text.split()

            usuario = int(dados[1])

            valor = float(
                dados[2].replace(",", ".")
            )

        except:

            bot.reply_to(
                message,
                "Use:\n/addsaldo ID VALOR"
            )

            return

        cursor.execute(
            """
            SELECT id

            FROM usuarios

            WHERE id=?
            """,
            (usuario,)
        )

        if cursor.fetchone() is None:

            bot.reply_to(
                message,
                "❌ Usuário não encontrado."
            )

            return

        cursor.execute(
            """
            UPDATE usuarios

            SET saldo = saldo + ?

            WHERE id=?
            """,
            (
                valor,
                usuario
            )
        )

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
                usuario,
                "BONUS",
                "Saldo adicionado pelo administrador",
                valor,
                datetime.now().strftime("%d/%m/%Y %H:%M")
            )
        )

        conn.commit()

        try:

            bot.send_message(

                usuario,

                f"""
🎁 <b>Você recebeu um bônus!</b>

💰 Valor:

<b>R$ {valor:.2f}</b>
""",

                parse_mode="HTML"

            )

        except Exception as erro:

            print(erro)

        bot.reply_to(
            message,
            "✅ Saldo adicionado."
        )

    # ======================================
    # RANKING
    # ======================================

    @bot.message_handler(commands=["ranking"])
    def ranking(message):

        if not eh_admin(message.from_user.id):
            return

        cursor.execute(
            """
            SELECT

                nome,
                convidados,
                saldo

            FROM usuarios

            ORDER BY convidados DESC,
                     saldo DESC

            LIMIT 10
            """
        )

        ranking = cursor.fetchall()

        if not ranking:

            bot.send_message(
                message.chat.id,
                "Nenhum usuário encontrado."
            )

            return

        texto = "🏆 <b>TOP 10 INDICAÇÕES</b>\n\n"

        posicao = 1

        for usuario in ranking:

            texto += (
                f"{posicao}º - <b>{usuario[0]}</b>\n"
                f"👥 {usuario[1]} indicados\n"
                f"💰 R$ {usuario[2]:.2f}\n\n"
            )

            posicao += 1

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )

    # ======================================
    # BANIR
    # ======================================

    @bot.message_handler(commands=["banir"])
    def banir(message):

        if not eh_admin(message.from_user.id):
            return

        try:

            usuario = int(
                message.text.split()[1]
            )

        except:

            bot.reply_to(
                message,
                "Use:\n/banir ID"
            )

            return

        cursor.execute(
            """
            UPDATE usuarios

            SET bloqueado=1

            WHERE id=?
            """,
            (usuario,)
        )

        conn.commit()

        try:

            bot.send_message(

                usuario,

                """
🚫 <b>Sua conta foi bloqueada.</b>

Entre em contato com o suporte.
""",

                parse_mode="HTML"

            )

        except Exception as erro:

            print(erro)

        bot.reply_to(
            message,
            "✅ Usuário bloqueado."
        )

    # ======================================
    # DESBANIR
    # ======================================

    @bot.message_handler(commands=["desbanir"])
    def desbanir(message):

        if not eh_admin(message.from_user.id):
            return

        try:

            usuario = int(
                message.text.split()[1]
            )

        except:

            bot.reply_to(
                message,
                "Use:\n/desbanir ID"
            )

            return

        cursor.execute(
            """
            UPDATE usuarios

            SET bloqueado=0

            WHERE id=?
            """,
            (usuario,)
        )

        conn.commit()

        try:

            bot.send_message(

                usuario,

                """
✅ <b>Sua conta foi desbloqueada.</b>

Agora você pode utilizar o bot normalmente.
""",

                parse_mode="HTML"

            )

        except Exception as erro:

            print(erro)

        bot.reply_to(
            message,
            "✅ Usuário desbloqueado."
        )    # ======================================
    # CONFIGURAÇÕES
    # ======================================

    @bot.message_handler(commands=["config"])
    def configuracoes(message):

        if not eh_admin(message.from_user.id):
            return

        cursor.execute(
            """
            SELECT chave, valor

            FROM configuracoes

            ORDER BY chave
            """
        )

        configuracoes = cursor.fetchall()

        texto = "⚙️ <b>CONFIGURAÇÕES DO BOT</b>\n\n"

        for chave, valor in configuracoes:

            texto += f"• <b>{chave}</b>: {valor}\n"

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )

    # ======================================
    # ALTERAR CONFIGURAÇÃO
    # ======================================

    @bot.message_handler(commands=["setconfig"])
    def alterar_config(message):

        if not eh_admin(message.from_user.id):
            return

        try:

            dados = message.text.split(maxsplit=2)

            chave = dados[1]

            valor = dados[2]

        except:

            bot.reply_to(

                message,

                "Use:\n/setconfig chave valor"

            )

            return

        cursor.execute(
            """
            UPDATE configuracoes

            SET valor=?

            WHERE chave=?
            """,
            (
                valor,
                chave
            )
        )

        conn.commit()

        bot.reply_to(

            message,

            "✅ Configuração atualizada."

        )

    # ======================================
    # LIBERAR SAQUES
    # ======================================

    @bot.message_handler(commands=["liberarsaque"])
    def liberar_saque(message):

        if not eh_admin(message.from_user.id):
            return

        cursor.execute(
            """
            UPDATE configuracoes

            SET valor='SIM'

            WHERE chave='saque_liberado'
            """
        )

        conn.commit()

        bot.reply_to(

            message,

            "✅ Saques liberados."

        )

    # ======================================
    # BLOQUEAR SAQUES
    # ======================================

    @bot.message_handler(commands=["bloquearsaque"])
    def bloquear_saque(message):

        if not eh_admin(message.from_user.id):
            return

        cursor.execute(
            """
            UPDATE configuracoes

            SET valor='NAO'

            WHERE chave='saque_liberado'
            """
        )

        conn.commit()

        bot.reply_to(

            message,

            "⛔ Saques bloqueados."

        )

    # ======================================
    # HISTÓRICO
    # ======================================

    @bot.message_handler(commands=["historico"])
    def historico(message):

        if not eh_admin(message.from_user.id):
            return

        try:

            usuario = int(
                message.text.split()[1]
            )

        except:

            bot.reply_to(

                message,

                "Use:\n/historico ID"

            )

            return

        cursor.execute(
            """
            SELECT

                tipo,
                descricao,
                valor,
                data

            FROM historico

            WHERE usuario=?

            ORDER BY id DESC

            LIMIT 20
            """,
            (usuario,)
        )

        historico = cursor.fetchall()

        if len(historico) == 0:

            bot.send_message(

                message.chat.id,

                "Nenhum histórico encontrado."

            )

            return

        texto = f"📜 <b>HISTÓRICO DO USUÁRIO {usuario}</b>\n\n"

        for registro in historico:

            texto += (
                f"📌 <b>{registro[0]}</b>\n"
                f"{registro[1]}\n"
                f"💰 R$ {registro[2]:.2f}\n"
                f"📅 {registro[3]}\n\n"
            )

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )
