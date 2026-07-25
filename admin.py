import telebot

from datetime import datetime

from config import *
from database import conn, cursor

# ==========================================
# REGISTRAR COMANDOS ADMIN
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

/usuarios
/estatisticas
/pedidos
/aprovar
/rejeitar
/addsaldo
/ranking
/banir
/desbanir
"""

        bot.send_message(
            message.chat.id,
            texto,
            parse_mode="HTML"
        )

    # ======================================
    # TOTAL USUÁRIOS
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
            f"👥 Total de usuários: {total}"
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

        usuarios = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM saques"
        )

        saques = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT IFNULL(SUM(valor),0)
            FROM saques
            WHERE status='APROVADO'
            """
        )

        total_pago = cursor.fetchone()[0]

        texto = f"""
📊 <b>ESTATÍSTICAS</b>

👥 Usuários:
{usuarios}

💸 Saques:
{saques}

💰 Total Pago:
R$ {total_pago:.2f}
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
            data
            FROM saques
            WHERE status='PENDENTE'
            ORDER BY id
            """
        )

        pedidos = cursor.fetchall()

        if not pedidos:

            bot.send_message(
                message.chat.id,
                "✅ Não existem saques pendentes."
            )

            return

        texto = "📋 <b>SAQUES PENDENTES</b>\n\n"

        for pedido in pedidos:

            texto += (
                f"🆔 ID: <code>{pedido[0]}</code>\n"
                f"👤 Usuário: <code>{pedido[1]}</code>\n"
                f"💰 Valor: R$ {pedido[2]:.2f}\n"
                f"📅 Data: {pedido[3]}\n\n"
            )

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

        if not saque:

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
✅ Seu saque foi aprovado.

💰 Valor:

R$ {valor:.2f}
"""

            )

        except:
            pass

        bot.reply_to(
            message,
            "✅ Saque aprovado."
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

        if not saque:

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
❌ Seu saque foi rejeitado.

💰 Valor:

R$ {valor:.2f}
"""

            )

        except:
            pass

        bot.reply_to(
            message,
            "❌ Saque rejeitado."
        )    # ======================================
    # ADICIONAR SALDO
    # ======================================

    @bot.message_handler(commands=["addsaldo"])
    def addsaldo(message):

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
🎁 Você recebeu um bônus!

💰 Valor:

R$ {valor:.2f}
"""

            )

        except:
            pass

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

            ORDER BY convidados DESC

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

        texto = "🏆 TOP 10 INDICAÇÕES\n\n"

        posicao = 1

        for usuario in ranking:

            texto += (
                f"{posicao}º - {usuario[0]}\n"
                f"👥 {usuario[1]} indicados\n"
                f"💰 R$ {usuario[2]:.2f}\n\n"
            )

            posicao += 1

        bot.send_message(
            message.chat.id,
            texto
        )

    # ======================================
    # BANIR USUÁRIO
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
🚫 Sua conta foi bloqueada.

Entre em contato com o suporte.
"""

            )

        except:
            pass

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

        configs = cursor.fetchall()

        texto = "⚙️ <b>CONFIGURAÇÕES</b>\n\n"

        for chave, valor in configs:

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
    def setconfig(message):

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
    # ATIVAR SAQUES
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
    # HISTÓRICO USUÁRIO
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

        registros = cursor.fetchall()

        if not registros:

            bot.send_message(
                message.chat.id,
                "Nenhum histórico encontrado."
            )

            return

        texto = f"📜 Histórico do usuário {usuario}\n\n"

        for tipo, descricao, valor, data in registros:

            texto += (
                f"📌 {tipo}\n"
                f"{descricao}\n"
                f"💰 R$ {valor:.2f}\n"
                f"📅 {data}\n\n"
            )

        bot.send_message(
            message.chat.id,
            texto
        )
