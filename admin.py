from config import ADMIN_ID

from database import (
    conn,
    cursor
)

from teclado import (
    menu_admin,
    menu_principal
)

from utils import (
    adicionar_log,
    adicionar_historico,
    alterar_config,
    agora
)

# ==========================================
# REGISTRAR MÓDULO
# ==========================================

def registrar_admin(bot):

    # ======================================
    # /ADMIN
    # ======================================

    @bot.message_handler(commands=["admin"])
    def painel_admin(message):

        if message.from_user.id != ADMIN_ID:

            bot.reply_to(

                message,

                "❌ Você não é administrador."

            )

            return

        texto = """
👑 <b>PAINEL ADMINISTRATIVO</b>

Bem-vindo.

Escolha uma opção abaixo.
"""

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML",

            reply_markup=menu_admin()

        )

    # ======================================
    # ESTATÍSTICAS
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "📊 Estatísticas")
    def estatisticas(message):

        if message.from_user.id != ADMIN_ID:
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
            "SELECT COUNT(*) FROM indicacoes"
        )

        indicacoes = cursor.fetchone()[0]

        cursor.execute(
            "SELECT SUM(saldo) FROM usuarios"
        )

        saldo = cursor.fetchone()[0]

        if saldo is None:
            saldo = 0

        texto = f"""
📊 <b>ESTATÍSTICAS</b>

👥 Usuários:

<b>{usuarios}</b>

👤 Indicações:

<b>{indicacoes}</b>

💸 Saques:

<b>{saques}</b>

💰 Saldo total:

<b>R$ {saldo:.2f}</b>
"""

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

        if message.from_user.id != ADMIN_ID:
            return

        try:

            usuario = int(

                message.text.split()[1]

            )

        except:

            bot.reply_to(

                message,

                "Use:\n\n/banir ID"

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

        adicionar_log(

            ADMIN_ID,

            "BANIMENTO",

            f"Usuário {usuario} banido."

        )

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

        if message.from_user.id != ADMIN_ID:
            return

        try:

            usuario = int(

                message.text.split()[1]

            )

        except:

            bot.reply_to(

                message,

                "Use:\n\n/desbanir ID"

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

        adicionar_log(

            ADMIN_ID,

            "DESBANIMENTO",

            f"Usuário {usuario} desbanido."

        )

        try:

            bot.send_message(

                usuario,

                """
✅ Sua conta foi desbloqueada.

Bem-vindo novamente.
"""

            )

        except:

            pass

        bot.reply_to(

            message,

            "✅ Usuário desbloqueado."
        )    # ======================================
    # ADICIONAR SALDO
    # ======================================

    @bot.message_handler(commands=["addsaldo"])
    def adicionar_saldo_admin(message):

        if message.from_user.id != ADMIN_ID:
            return

        try:

            _, usuario, valor = message.text.split()

            usuario = int(usuario)

            valor = float(valor.replace(",", "."))

        except:

            bot.reply_to(

                message,

                "Use:\n\n/addsaldo ID VALOR"

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

        conn.commit()

        adicionar_historico(

            usuario,

            "ADMIN",

            "Saldo adicionado pelo administrador",

            valor

        )

        adicionar_log(

            ADMIN_ID,

            "ADD SALDO",

            f"Usuário {usuario} recebeu R$ {valor:.2f}"

        )

        try:

            bot.send_message(

                usuario,

                f"""
💰 Você recebeu um bônus.

Valor:

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
    # REMOVER SALDO
    # ======================================

    @bot.message_handler(commands=["removersaldo"])
    def remover_saldo_admin(message):

        if message.from_user.id != ADMIN_ID:
            return

        try:

            _, usuario, valor = message.text.split()

            usuario = int(usuario)

            valor = float(valor.replace(",", "."))

        except:

            bot.reply_to(

                message,

                "Use:\n\n/removersaldo ID VALOR"

            )

            return

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

        conn.commit()

        adicionar_historico(

            usuario,

            "ADMIN",

            "Saldo removido pelo administrador",

            valor

        )

        adicionar_log(

            ADMIN_ID,

            "REMOVER SALDO",

            f"Usuário {usuario} perdeu R$ {valor:.2f}"

        )

        try:

            bot.send_message(

                usuario,

                f"""
⚠️ O administrador removeu:

R$ {valor:.2f}

do seu saldo.
"""

            )

        except:

            pass

        bot.reply_to(

            message,

            "✅ Saldo removido."

        )

    # ======================================
    # RANKING
    # ======================================

    @bot.message_handler(commands=["ranking"])
    def ranking(message):

        if message.from_user.id != ADMIN_ID:
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

        texto = "🏆 <b>TOP 10 INDICADORES</b>\n\n"

        posicao = 1

        for nome, convidados, saldo in ranking:

            texto += (
                f"{posicao}º - {nome}\n"
                f"👥 {convidados} | 💰 R$ {saldo:.2f}\n\n"
            )

            posicao += 1

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )

    # ======================================
    # TOTAL DE USUÁRIOS
    # ======================================

    @bot.message_handler(commands=["usuarios"])
    def total_usuarios(message):

        if message.from_user.id != ADMIN_ID:
            return

        cursor.execute(
            "SELECT COUNT(*) FROM usuarios"
        )

        total = cursor.fetchone()[0]

        bot.send_message(

            message.chat.id,

            f"""
👥 Usuários cadastrados:

<b>{total}</b>
""",

            parse_mode="HTML"

        )    # ======================================
    # MANUTENÇÃO
    # ======================================

    @bot.message_handler(commands=["manutencao"])
    def manutencao(message):

        if message.from_user.id != ADMIN_ID:
            return

        try:

            opcao = message.text.split()[1].lower()

        except:

            bot.reply_to(

                message,

                "Use:\n\n/manutencao on\n/manutencao off"

            )

            return

        if opcao == "on":

            alterar_config(

                "modo_manutencao",

                "SIM"

            )

            adicionar_log(

                ADMIN_ID,

                "MANUTENÇÃO",

                "Modo manutenção ativado."

            )

            bot.reply_to(

                message,

                "✅ Manutenção ativada."

            )

            return

        if opcao == "off":

            alterar_config(

                "modo_manutencao",

                "NAO"

            )

            adicionar_log(

                ADMIN_ID,

                "MANUTENÇÃO",

                "Modo manutenção desativado."

            )

            bot.reply_to(

                message,

                "✅ Manutenção desativada."

            )

            return

        bot.reply_to(

            message,

            "Use apenas on ou off."

        )

    # ======================================
    # LOGS
    # ======================================

    @bot.message_handler(commands=["logs"])
    def logs(message):

        if message.from_user.id != ADMIN_ID:
            return

        cursor.execute(
            """
            SELECT

                usuario,

                acao,

                detalhes,

                data

            FROM logs

            ORDER BY id DESC

            LIMIT 20
            """
        )

        registros = cursor.fetchall()

        if len(registros) == 0:

            bot.reply_to(

                message,

                "Nenhum log encontrado."

            )

            return

        texto = "📋 <b>ÚLTIMOS LOGS</b>\n\n"

        for usuario, acao, detalhes, data in registros:

            texto += f"""
👤 {usuario}

📌 {acao}

📝 {detalhes}

📅 {data}

──────────────

"""

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )

    # ======================================
    # AVISAR
    # ======================================

    @bot.message_handler(commands=["avisar"])
    def avisar(message):

        if message.from_user.id != ADMIN_ID:
            return

        texto = message.text.replace(

            "/avisar",

            ""

        ).strip()

        if texto == "":

            bot.reply_to(

                message,

                "Use:\n\n/avisar sua mensagem"

            )

            return

        cursor.execute(

            "SELECT id FROM usuarios"

        )

        usuarios = cursor.fetchall()

        enviados = 0

        for usuario in usuarios:

            try:

                bot.send_message(

                    usuario[0],

                    f"📢 {texto}"

                )

                enviados += 1

            except:

                pass

        adicionar_log(

            ADMIN_ID,

            "AVISO",

            texto

        )

        bot.reply_to(

            message,

            f"✅ Aviso enviado para {enviados} usuários."

        )    # ======================================
    # BACKUP DO BANCO
    # ======================================

    @bot.message_handler(commands=["backup"])
    def backup(message):

        if message.from_user.id != ADMIN_ID:
            return

        try:

            with open("database.db", "rb") as banco:

                bot.send_document(

                    message.chat.id,

                    banco,

                    caption="💾 Backup do banco de dados."

                )

            adicionar_log(

                ADMIN_ID,

                "BACKUP",

                "Backup realizado."

            )

        except Exception as erro:

            bot.reply_to(

                message,

                f"Erro:\n{erro}"

            )

    # ======================================
    # CRIAR CUPOM
    # ======================================

    @bot.message_handler(commands=["criarcupom"])
    def criar_cupom(message):

        if message.from_user.id != ADMIN_ID:
            return

        try:

            _, codigo, valor, limite = message.text.split()

            valor = float(valor.replace(",", "."))

            limite = int(limite)

        except:

            bot.reply_to(

                message,

                "Use:\n\n/criarcupom CODIGO VALOR LIMITE"

            )

            return

        try:

            cursor.execute(

                """
                INSERT INTO cupons(

                    codigo,

                    valor,

                    limite,

                    usados,

                    ativo

                )

                VALUES(

                    ?,?,?,0,1

                )
                """,

                (

                    codigo.upper(),

                    valor,

                    limite

                )

            )

            conn.commit()

            adicionar_log(

                ADMIN_ID,

                "CUPOM",

                f"Cupom {codigo} criado."

            )

            bot.reply_to(

                message,

                "✅ Cupom criado."

            )

        except:

            bot.reply_to(

                message,

                "❌ Este cupom já existe."

            )

    # ======================================
    # REMOVER CUPOM
    # ======================================

    @bot.message_handler(commands=["removercupom"])
    def remover_cupom(message):

        if message.from_user.id != ADMIN_ID:
            return

        try:

            codigo = message.text.split()[1]

        except:

            bot.reply_to(

                message,

                "Use:\n\n/removercupom CODIGO"

            )

            return

        cursor.execute(

            """
            DELETE FROM cupons

            WHERE codigo=?
            """,

            (

                codigo.upper(),

            )

        )

        conn.commit()

        adicionar_log(

            ADMIN_ID,

            "REMOVER CUPOM",

            codigo.upper()

        )

        bot.reply_to(

            message,

            "✅ Cupom removido."

        )

    # ======================================
    # SAQUES PENDENTES
    # ======================================

    @bot.message_handler(commands=["pendentes"])
    def pendentes(message):

        if message.from_user.id != ADMIN_ID:
            return

        cursor.execute(

            """
            SELECT

                id,

                usuario,

                valor

            FROM saques

            WHERE status='PENDENTE'

            ORDER BY id
            """

        )

        saques = cursor.fetchall()

        if len(saques) == 0:

            bot.reply_to(

                message,

                "Nenhum saque pendente."

            )

            return

        texto = "💸 <b>SAQUES PENDENTES</b>\n\n"

        for saque in saques:

            texto += f"""
🆔 {saque[0]}

👤 {saque[1]}

💰 R$ {saque[2]:.2f}

──────────────

"""

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )

    # ======================================
    # FIM DO MÓDULO
    # ======================================
