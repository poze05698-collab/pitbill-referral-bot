from database import conn, cursor

from config import (
    ADMIN_ID
)

from teclado import (
    menu_admin,
    menu_principal
)

from utils import (
    adicionar_log,
    adicionar_saldo,
    remover_saldo,
    bloquear_usuario,
    desbloquear_usuario,
    total_usuarios,
    total_saldo,
    alterar_config,
    agora
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
    # ABRIR PAINEL
    # ======================================

    @bot.message_handler(commands=["admin"])
    def painel_admin(message):

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


💰 Saldo distribuído:

R$ {saldo:.2f}
""",

            parse_mode="HTML"

        )    # ======================================
    # LISTAR USUÁRIOS
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "👥 Usuários"
    )
    def usuarios(message):

        if not is_admin(message.from_user.id):

            return


        cursor.execute(

            """
            SELECT

                id,

                nome,

                bloqueado

            FROM usuarios

            ORDER BY id DESC

            LIMIT 20

            """

        )


        lista = cursor.fetchall()



        texto = "👥 <b>ÚLTIMOS USUÁRIOS</b>\n\n"



        for usuario in lista:


            status = (

                "🚫 Bloqueado"

                if usuario[2] == 1

                else

                "✅ Ativo"

            )


            texto += f"""

🆔 {usuario[0]}

👤 {usuario[1]}

{status}

────────────

"""



        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )



    # ======================================
    # BANIR USUÁRIO
    # ======================================

    @bot.message_handler(
        commands=["banir"]
    )
    def banir(message):

        if not is_admin(message.from_user.id):

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



        bloquear_usuario(usuario)



        adicionar_log(

            usuario,

            "BANIMENTO",

            "Usuário bloqueado pelo administrador."

        )



        bot.reply_to(

            message,

            f"🚫 Usuário {usuario} bloqueado."

        )



        try:

            bot.send_message(

                usuario,

                """
🚫 Sua conta foi bloqueada.

Você não poderá utilizar o bot.
"""

            )


        except:

            pass



    # ======================================
    # DESBANIR USUÁRIO
    # ======================================

    @bot.message_handler(
        commands=["desbanir"]
    )
    def desbanir(message):

        if not is_admin(message.from_user.id):

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



        desbloquear_usuario(usuario)



        adicionar_log(

            usuario,

            "DESBANIMENTO",

            "Usuário liberado pelo administrador."

        )



        bot.reply_to(

            message,

            f"✅ Usuário {usuario} desbloqueado."

        )



    # ======================================
    # ADICIONAR SALDO
    # ======================================

    @bot.message_handler(
        commands=["addsaldo"]
    )
    def add_saldo(message):

        if not is_admin(message.from_user.id):

            return



        try:

            dados = message.text.split()

            usuario = int(dados[1])

            valor = float(dados[2])


        except:


            bot.reply_to(

                message,

                "Use:\n/addsaldo ID VALOR"

            )

            return



        adicionar_saldo(

            usuario,

            valor

        )



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

    @bot.message_handler(
        commands=["removersaldo"]
    )
    def remover_saldo_admin(message):

        if not is_admin(message.from_user.id):

            return



        try:

            dados = message.text.split()

            usuario = int(dados[1])

            valor = float(dados[2])


        except:


            bot.reply_to(

                message,

                "Use:\n/removersaldo ID VALOR"

            )

            return



        remover_saldo(

            usuario,

            valor

        )



        adicionar_log(

            usuario,

            "SALDO",

            f"Removido R$ {valor:.2f}"

        )


        bot.reply_to(

            message,

            "✅ Saldo removido."

        )    # ======================================
    # AVISAR TODOS OS USUÁRIOS
    # ======================================

    @bot.message_handler(
        commands=["avisar"]
    )
    def avisar_todos(message):

        if not is_admin(message.from_user.id):

            return


        texto = message.text.replace(

            "/avisar",

            ""

        ).strip()



        if texto == "":


            bot.reply_to(

                message,

                "Use:\n/avisar mensagem"

            )

            return



        cursor.execute(

            """
            SELECT id

            FROM usuarios

            """

        )


        usuarios = cursor.fetchall()


        enviados = 0



        for usuario in usuarios:


            try:


                bot.send_message(

                    usuario[0],

                    texto

                )


                enviados += 1



            except:


                pass



        adicionar_log(

            ADMIN_ID,

            "AVISO GERAL",

            f"Enviado para {enviados} usuários."

        )



        bot.reply_to(

            message,

            f"📢 Aviso enviado para {enviados} usuários."

        )



    # ======================================
    # MANUTENÇÃO
    # ======================================

    @bot.message_handler(
        commands=["manutencao"]
    )
    def manutencao(message):

        if not is_admin(message.from_user.id):

            return



        partes = message.text.split()



        if len(partes) < 2:


            bot.reply_to(

                message,

                """
Use:

/manutencao ON

ou

/manutencao OFF
"""

            )

            return



        status = partes[1].upper()



        if status == "ON":


            alterar_config(

                "modo_manutencao",

                "SIM"

            )


            resposta = "🔧 Manutenção ativada."



        else:


            alterar_config(

                "modo_manutencao",

                "NAO"

            )


            resposta = "✅ Manutenção desativada."



        adicionar_log(

            ADMIN_ID,

            "MANUTENÇÃO",

            status

        )


        bot.reply_to(

            message,

            resposta

        )



    # ======================================
    # LOGS
    # ======================================

    @bot.message_handler(
        commands=["logs"]
    )
    def logs(message):

        if not is_admin(message.from_user.id):

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

            LIMIT 15

            """

        )


        registros = cursor.fetchall()



        texto = "📋 <b>ÚLTIMOS LOGS</b>\n\n"



        for log in registros:


            texto += f"""
👤 {log[0]}

⚙️ {log[1]}

📝 {log[2]}

📅 {log[3]}

────────────
"""



        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )



    # ======================================
    # BACKUP
    # ======================================

    @bot.message_handler(
        commands=["backup"]
    )
    def backup(message):

        if not is_admin(message.from_user.id):

            return



        try:


            arquivo = open(

                "database.db",

                "rb"

            )


            bot.send_document(

                message.chat.id,

                arquivo,

                caption="💾 Backup do banco."

            )


            arquivo.close()



        except Exception as erro:


            bot.reply_to(

                message,

                f"Erro: {erro}"

            )



    # ======================================
    # SAQUES PENDENTES
    # ======================================

    @bot.message_handler(
        commands=["pendentes"]
    )
    def saques_pendentes(message):

        if not is_admin(message.from_user.id):

            return



        cursor.execute(

            """
            SELECT

                id,

                usuario,

                valor,

                status

            FROM saques

            WHERE status='PENDENTE'

            """

        )


        lista = cursor.fetchall()



        if not lista:


            bot.send_message(

                message.chat.id,

                "✅ Nenhum saque pendente."

            )

            return



        texto = "💸 <b>SAQUES PENDENTES</b>\n\n"



        for saque in lista:


            texto += f"""
🆔 {saque[0]}

👤 Usuário:
{saque[1]}

💰 Valor:
R$ {saque[2]:.2f}

📌 Status:
{saque[3]}

────────────
"""



        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )    # ======================================
    # CRIAR CUPOM
    # ======================================

    @bot.message_handler(
        commands=["criarcupom"]
    )
    def criar_cupom(message):

        if not is_admin(message.from_user.id):

            return


        try:

            dados = message.text.split()


            codigo = dados[1].upper()

            valor = float(dados[2])

            limite = int(dados[3])


        except:


            bot.reply_to(

                message,

                """
Use:

/criarcupom CODIGO VALOR LIMITE
"""

            )

            return



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

                codigo,

                valor,

                limite

            )

        )


        conn.commit()



        adicionar_log(

            ADMIN_ID,

            "CUPOM",

            f"Criado {codigo}"

        )


        bot.reply_to(

            message,

            "🎁 Cupom criado."

        )



    # ======================================
    # REMOVER CUPOM
    # ======================================

    @bot.message_handler(
        commands=["removercupom"]
    )
    def remover_cupom(message):

        if not is_admin(message.from_user.id):

            return



        try:

            codigo = message.text.split()[1].upper()


        except:


            bot.reply_to(

                message,

                "Use:\n/removercupom CODIGO"

            )

            return



        cursor.execute(

            """
            DELETE FROM cupons

            WHERE codigo=?

            """,

            (codigo,)

        )


        conn.commit()



        adicionar_log(

            ADMIN_ID,

            "CUPOM REMOVIDO",

            codigo

        )


        bot.reply_to(

            message,

            "✅ Cupom removido."

        )



    # ======================================
    # RANKING ADMIN
    # ======================================

    @bot.message_handler(
        commands=["rankingadmin"]
    )
    def ranking_admin(message):

        if not is_admin(message.from_user.id):

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



        texto = "🏆 <b>RANKING ADMIN</b>\n\n"



        posicao = 1



        for usuario in ranking:


            texto += f"""
{posicao}º {usuario[0]}

👥 Convites:
{usuario[1]}

💰 Saldo:
R$ {usuario[2]:.2f}

────────────
"""


            posicao += 1



        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )



    # ======================================
    # CONFIGURAÇÕES
    # ======================================

    @bot.message_handler(
        commands=["config"]
    )
    def configuracoes(message):

        if not is_admin(message.from_user.id):

            return



        bot.send_message(

            message.chat.id,

            """
⚙️ <b>CONFIGURAÇÕES</b>


Comandos:


🔧 Manutenção:

/manutencao ON

/manutencao OFF


🎁 Criar cupom:

/criarcupom CODIGO VALOR LIMITE


💾 Backup:

/backup
""",

            parse_mode="HTML"

        )



# ==========================================
# FIM DO ADMIN.PY
# ==========================================
