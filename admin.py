from database import conn, cursor

from config import ADMIN_ID

from teclado import menu_admin

from utils import (
    adicionar_log,
    total_usuarios,
    total_saldo,
    alterar_config
)



# ==========================================
# VERIFICAR ADMIN
# ==========================================

def is_admin(user_id):

    return user_id == ADMIN_ID



# ==========================================
# REGISTRAR ADMIN
# ==========================================

def registrar_admin(bot):


    # ======================================
    # PAINEL
    # ======================================

    @bot.message_handler(commands=["admin"])
    def painel(message):


        if not is_admin(message.from_user.id):

            return



        bot.send_message(

            message.chat.id,

            """
👑 <b>PAINEL ADMINISTRATIVO</b>

Escolha uma opção:
""",

            parse_mode="HTML",

            reply_markup=menu_admin()

        )



    # ======================================
    # ESTATÍSTICAS
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "📊 Estatísticas"
    )
    def estatisticas(message):


        if not is_admin(message.from_user.id):

            return



        usuarios = total_usuarios()

        saldo = total_saldo()



        bot.send_message(

            message.chat.id,

            f"""
📊 <b>ESTATÍSTICAS</b>


👥 Usuários:

{usuarios}


💰 Saldo:

R$ {saldo:.2f}
""",

            parse_mode="HTML"

        )    # ======================================
    # USUÁRIOS
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "👥 Usuários"
    )
    def listar_usuarios(message):

        if not is_admin(message.from_user.id):
            return

        cursor.execute("""
            SELECT id, nome, saldo, bloqueado
            FROM usuarios
            ORDER BY id DESC
            LIMIT 20
        """)

        usuarios = cursor.fetchall()

        if not usuarios:
            bot.send_message(
                message.chat.id,
                "Nenhum usuário encontrado."
            )
            return

        texto = "👥 <b>ÚLTIMOS USUÁRIOS</b>\n\n"

        for usuario in usuarios:

            status = "🚫 Bloqueado" if usuario[3] else "✅ Ativo"

            texto += (
                f"🆔 {usuario[0]}\n"
                f"👤 {usuario[1]}\n"
                f"💰 R$ {usuario[2]:.2f}\n"
                f"{status}\n"
                "────────────\n"
            )

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

        if not is_admin(message.from_user.id):
            return

        try:
            user = int(message.text.split()[1])
        except:
            bot.reply_to(
                message,
                "Use:\n/banir ID"
            )
            return

        cursor.execute(
            "UPDATE usuarios SET bloqueado=1 WHERE id=?",
            (user,)
        )

        conn.commit()

        adicionar_log(
            user,
            "BANIMENTO",
            "Conta bloqueada pelo administrador."
        )

        bot.reply_to(
            message,
            "✅ Usuário bloqueado."
        )


    # ======================================
    # DESBANIR
    # ======================================

    @bot.message_handler(commands=["desbanir"])
    def desbanir(message):

        if not is_admin(message.from_user.id):
            return

        try:
            user = int(message.text.split()[1])
        except:
            bot.reply_to(
                message,
                "Use:\n/desbanir ID"
            )
            return

        cursor.execute(
            "UPDATE usuarios SET bloqueado=0 WHERE id=?",
            (user,)
        )

        conn.commit()

        adicionar_log(
            user,
            "DESBANIMENTO",
            "Conta desbloqueada."
        )

        bot.reply_to(
            message,
            "✅ Usuário desbloqueado."
        )


    # ======================================
    # ADICIONAR SALDO
    # ======================================

    @bot.message_handler(commands=["addsaldo"])
    def adicionar_saldo(message):

        if not is_admin(message.from_user.id):
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
            (valor, usuario)
        )

        conn.commit()

        adicionar_log(
            usuario,
            "SALDO",
            f"Adicionado R$ {valor:.2f}"
        )

        bot.reply_to(
            message,
            "✅ Saldo adicionado."
        )


    # ======================================
    # REMOVER SALDO
    # ======================================

    @bot.message_handler(commands=["removersaldo"])
    def remover_saldo(message):

        if not is_admin(message.from_user.id):
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
                "Use:\n/removersaldo ID VALOR"
            )
            return

        cursor.execute(
            """
            UPDATE usuarios
            SET saldo = saldo - ?
            WHERE id=?
            """,
            (valor, usuario)
        )

        conn.commit()

        adicionar_log(
            usuario,
            "SALDO",
            f"Removido R$ {valor:.2f}"
        )

        bot.reply_to(
            message,
            "✅ Saldo removido."
        )    # ======================================
    # BOTÃO AVISAR
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "📢 Avisar")
    def aviso_menu(message):

        if not is_admin(message.from_user.id):
            return

        bot.send_message(
            message.chat.id,
            """
📢 Envie a mensagem que deseja enviar para todos os usuários.

Exemplo:

Promoção liberada!

Cancelar: /cancelar
"""
        )

        bot.register_next_step_handler(
            message,
            enviar_aviso
        )


    def enviar_aviso(message):

        if message.text == "/cancelar":

            bot.send_message(
                message.chat.id,
                "❌ Operação cancelada."
            )

            return

        cursor.execute("SELECT id FROM usuarios")

        usuarios = cursor.fetchall()

        enviados = 0

        for usuario in usuarios:

            try:

                bot.send_message(
                    usuario[0],
                    f"📢 {message.text}"
                )

                enviados += 1

            except:
                pass

        adicionar_log(
            ADMIN_ID,
            "AVISO",
            f"Mensagem enviada para {enviados} usuários."
        )

        bot.send_message(
            message.chat.id,
            f"✅ Aviso enviado para {enviados} usuários."
        )


    # ======================================
    # BOTÃO MANUTENÇÃO
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "🔧 Manutenção")
    def manutencao_menu(message):

        if not is_admin(message.from_user.id):
            return

        bot.send_message(
            message.chat.id,
            """
🔧 Escolha:

Digite:

ON

ou

OFF
"""
        )

        bot.register_next_step_handler(
            message,
            alterar_manutencao
        )


    def alterar_manutencao(message):

        resposta = message.text.upper()

        if resposta == "ON":

            alterar_config(
                "modo_manutencao",
                "SIM"
            )

            bot.send_message(
                message.chat.id,
                "✅ Manutenção ativada."
            )

        elif resposta == "OFF":

            alterar_config(
                "modo_manutencao",
                "NAO"
            )

            bot.send_message(
                message.chat.id,
                "✅ Manutenção desativada."
            )

        else:

            bot.send_message(
                message.chat.id,
                "Digite apenas ON ou OFF."
            )


    # ======================================
    # BOTÃO LOGS
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "📋 Logs")
    def mostrar_logs(message):

        if not is_admin(message.from_user.id):
            return

        cursor.execute("""
            SELECT usuario, acao, detalhes, data
            FROM logs
            ORDER BY id DESC
            LIMIT 20
        """)

        logs = cursor.fetchall()

        if not logs:

            bot.send_message(
                message.chat.id,
                "Nenhum log encontrado."
            )

            return

        texto = "📋 <b>ÚLTIMOS LOGS</b>\n\n"

        for log in logs:

            texto += (
                f"👤 {log[0]}\n"
                f"⚙ {log[1]}\n"
                f"📝 {log[2]}\n"
                f"📅 {log[3]}\n"
                "────────────\n"
            )

        bot.send_message(
            message.chat.id,
            texto,
            parse_mode="HTML"
        )


    # ======================================
    # BOTÃO BACKUP
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "💾 Backup")
    def backup(message):

        if not is_admin(message.from_user.id):
            return

        try:

            with open("database.db", "rb") as banco:

                bot.send_document(
                    message.chat.id,
                    banco,
                    caption="💾 Backup do banco de dados."
                )

        except Exception as erro:

            bot.send_message(
                message.chat.id,
                f"Erro ao gerar backup:\n{erro}"
            )    # ======================================
    # BOTÃO CRIAR CUPOM
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "🎁 Criar Cupom")
    def criar_cupom_menu(message):

        if not is_admin(message.from_user.id):
            return

        bot.send_message(
            message.chat.id,
            """
🎁 Informe os dados do cupom:

Formato:

CODIGO VALOR LIMITE

Exemplo:

BEMVINDO 10 100
"""
        )

        bot.register_next_step_handler(
            message,
            salvar_cupom
        )


    def salvar_cupom(message):

        try:

            dados = message.text.split()

            codigo = dados[0].upper()

            valor = float(dados[1].replace(",", "."))

            limite = int(dados[2])

        except:

            bot.send_message(
                message.chat.id,
                "❌ Formato inválido."
            )

            return


        cursor.execute("""
            INSERT INTO cupons
            (
                codigo,
                valor,
                limite,
                usados,
                ativo
            )
            VALUES
            (
                ?,?,?,0,1
            )
        """,
        (
            codigo,
            valor,
            limite
        ))

        conn.commit()

        adicionar_log(
            ADMIN_ID,
            "CUPOM",
            f"Cupom {codigo} criado."
        )

        bot.send_message(
            message.chat.id,
            "✅ Cupom criado com sucesso."
        )


    # ======================================
    # BOTÃO CONFIGURAÇÕES
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "⚙️ Configurações")
    def configuracoes(message):

        if not is_admin(message.from_user.id):
            return

        cursor.execute("""
            SELECT chave, valor
            FROM configuracoes
            ORDER BY chave
        """)

        configuracoes = cursor.fetchall()

        texto = "⚙️ <b>CONFIGURAÇÕES DO BOT</b>\n\n"

        if not configuracoes:

            texto += "Nenhuma configuração cadastrada."

        else:

            for chave, valor in configuracoes:

                texto += (
                    f"• <b>{chave}</b>: {valor}\n"
                )

        bot.send_message(
            message.chat.id,
            texto,
            parse_mode="HTML"
        )


    # ======================================
    # RANKING ADMIN
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "🏆 Ranking")
    def ranking_admin(message):

        if not is_admin(message.from_user.id):
            return

        cursor.execute("""
            SELECT
                nome,
                convidados,
                saldo
            FROM usuarios
            ORDER BY convidados DESC
            LIMIT 10
        """)

        ranking = cursor.fetchall()

        texto = "🏆 <b>RANKING GERAL</b>\n\n"

        posicao = 1

        for usuario in ranking:

            texto += (
                f"{posicao}º {usuario[0]}\n"
                f"👥 {usuario[1]} indicações\n"
                f"💰 R$ {usuario[2]:.2f}\n"
                "────────────\n"
            )

            posicao += 1

        if posicao == 1:

            texto += "Nenhum usuário encontrado."

        bot.send_message(
            message.chat.id,
            texto,
            parse_mode="HTML"
        )


# ==========================================
# FIM DO ADMIN.PY
# ==========================================
