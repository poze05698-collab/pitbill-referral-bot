from database import conn, cursor


from config import (
    NOME_BOT
)


from teclado import (
    menu_principal,
    menu_pix,
    menu_grupo
)


from utils import (
    verificar_acesso,
    adicionar_log,
    adicionar_historico,
    agora
)


from indicacoes import (
    processar_convite,
    finalizar_indicacao
)



# ==========================================
# REGISTRAR USUÁRIO
# ==========================================

def registrar_usuario(bot):


    # ======================================
    # START
    # ======================================

    @bot.message_handler(commands=["start"])
    def start(message):


        user_id = message.from_user.id

        nome = message.from_user.first_name


        username = (

            "@" + message.from_user.username

            if message.from_user.username

            else ""

        )


        if not verificar_acesso(
            bot,
            message
        ):

            return



        # Verifica usuário

        cursor.execute(

            """
            SELECT id

            FROM usuarios

            WHERE id=?

            """,

            (user_id,)

        )


        usuario = cursor.fetchone()



        if usuario is None:


            cursor.execute(

                """
                INSERT INTO usuarios(

                    id,

                    nome,

                    username,

                    saldo,

                    pix,

                    convidados,

                    bloqueado,

                    data_cadastro,

                    ultimo_acesso

                )

                VALUES(

                    ?,?,?,?,?,?,?,?,?

                )

                """,

                (

                    user_id,

                    nome,

                    username,

                    0,

                    "",

                    0,

                    0,

                    agora(),

                    agora()

                )

            )


            conn.commit()



            adicionar_log(

                user_id,

                "CADASTRO",

                "Novo usuário cadastrado"

            )


        else:


            cursor.execute(

                """
                UPDATE usuarios

                SET ultimo_acesso=?

                WHERE id=?

                """,

                (

                    agora(),

                    user_id

                )

            )


            conn.commit()



        # Processar convite

        indicador = processar_convite(

            user_id,

            message.text

        )



        if indicador:


            bot.send_message(

                message.chat.id,

                """
🎁 Você entrou através de um convite!


Agora faça:

👥 Entre no grupo

✅ Confirme sua entrada

💳 Cadastre seu Pix


Depois sua indicação será validada.
""",

                reply_markup=menu_grupo()

            )

            return



        bot.send_message(

            message.chat.id,

            f"""
🎉 Bem-vindo ao {NOME_BOT}

Use o menu abaixo.
""",

            reply_markup=menu_principal()

        )    # ======================================
    # PERFIL
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "👤 Perfil"
    )
    def perfil(message):


        if not verificar_acesso(bot, message):

            return


        user_id = message.from_user.id



        cursor.execute(

            """
            SELECT

                nome,

                username,

                saldo,

                convidados

            FROM usuarios

            WHERE id=?

            """,

            (user_id,)

        )


        usuario = cursor.fetchone()



        if usuario is None:

            return



        bot.send_message(

            message.chat.id,

            f"""
👤 <b>SEU PERFIL</b>


Nome:

{usuario[0]}


Usuário:

{usuario[1]}


💰 Saldo:

R$ {usuario[2]:.2f}


👥 Indicados:

{usuario[3]}
""",

            parse_mode="HTML"

        )



    # ======================================
    # SALDO
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "💰 Saldo"
    )
    def saldo(message):


        if not verificar_acesso(bot, message):

            return



        user_id = message.from_user.id



        cursor.execute(

            """
            SELECT saldo

            FROM usuarios

            WHERE id=?

            """,

            (user_id,)

        )


        resultado = cursor.fetchone()



        valor = 0


        if resultado:

            valor = resultado[0]



        bot.send_message(

            message.chat.id,

            f"""
💰 <b>SEU SALDO</b>


R$ {valor:.2f}
""",

            parse_mode="HTML"

        )



    # ======================================
    # MEU LINK
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "🔗 Meu Link"
    )
    def meu_link(message):


        if not verificar_acesso(bot, message):

            return



        user_id = message.from_user.id



        nome_bot = bot.get_me().username



        link = (

            f"https://t.me/{nome_bot}"

            f"?start=convite_{user_id}"

        )



        bot.send_message(

            message.chat.id,

            f"""
🔗 <b>SEU LINK DE CONVITE</b>


Compartilhe:

<code>{link}</code>


💰 Ganhe recompensa por cada indicação válida.
""",

            parse_mode="HTML"

        )



    # ======================================
    # INDICADOS
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "👥 Indicados"
    )
    def indicados(message):


        if not verificar_acesso(bot, message):

            return



        user_id = message.from_user.id



        cursor.execute(

            """
            SELECT

                status,

                COUNT(*)

            FROM indicacoes

            WHERE indicador=?

            GROUP BY status

            """,

            (user_id,)

        )


        dados = cursor.fetchall()



        pendentes = 0

        grupo_ok = 0

        aprovadas = 0



        for status, quantidade in dados:


            if status == "PENDENTE":

                pendentes = quantidade


            elif status == "GRUPO_OK":

                grupo_ok = quantidade


            elif status == "APROVADA":

                aprovadas = quantidade



        bot.send_message(

            message.chat.id,

            f"""
👥 <b>SUAS INDICAÇÕES</b>


⏳ Pendentes:

{pendentes}


👥 Grupo confirmado:

{grupo_ok}


✅ Aprovadas:

{aprovadas}
""",

            parse_mode="HTML"

        )    # ======================================
    # MENU PIX
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "💳 Pix"
    )
    def pix_menu(message):


        if not verificar_acesso(bot, message):

            return



        bot.send_message(

            message.chat.id,

            """
💳 <b>ÁREA PIX</b>


Escolha uma opção:

➕ Cadastrar Pix

✏️ Alterar Pix

👁 Ver Pix
""",

            parse_mode="HTML",

            reply_markup=menu_pix()

        )



    # ======================================
    # CADASTRAR PIX
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "➕ Cadastrar Pix"
    )
    def cadastrar_pix(message):


        if not verificar_acesso(bot, message):

            return



        bot.send_message(

            message.chat.id,

            """
💳 Envie sua chave Pix:

Pode ser:

CPF
E-mail
Telefone
Chave aleatória
"""

        )


        bot.register_next_step_handler(

            message,

            salvar_pix

        )



    # ======================================
    # SALVAR PIX
    # ======================================

    def salvar_pix(message):


        user_id = message.from_user.id


        pix = message.text.strip()



        if len(pix) < 3:


            bot.send_message(

                message.chat.id,

                "❌ Chave Pix inválida."

            )

            return



        cursor.execute(

            """
            UPDATE usuarios

            SET pix=?

            WHERE id=?

            """,

            (

                pix,

                user_id

            )

        )


        conn.commit()



        adicionar_log(

            user_id,

            "PIX",

            "Chave Pix cadastrada."

        )



        bot.send_message(

            message.chat.id,

            """
✅ Pix cadastrado!


Verificando indicação pendente...
"""

        )



        # ==================================
        # FINALIZAR INDICAÇÃO
        # ==================================

        aprovado = finalizar_indicacao(

            bot,

            user_id

        )



        if aprovado:


            bot.send_message(

                message.chat.id,

                """
🎉 Indicação validada!


A recompensa foi liberada.
"""

            )


        else:


            bot.send_message(

                message.chat.id,

                """
ℹ️ Pix salvo.

Nenhuma indicação pendente para validar.
"""

            )



    # ======================================
    # ALTERAR PIX
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "✏️ Alterar Pix"
    )
    def alterar_pix(message):


        if not verificar_acesso(bot, message):

            return



        bot.send_message(

            message.chat.id,

            """
✏️ Envie sua nova chave Pix.
"""

        )


        bot.register_next_step_handler(

            message,

            salvar_pix

        )



    # ======================================
    # VER PIX
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "👁 Ver Pix"
    )
    def ver_pix(message):


        if not verificar_acesso(bot, message):

            return



        user_id = message.from_user.id



        cursor.execute(

            """
            SELECT pix

            FROM usuarios

            WHERE id=?

            """,

            (user_id,)

        )


        resultado = cursor.fetchone()



        if not resultado or resultado[0] == "":


            texto = """
❌ Nenhuma chave Pix cadastrada.
"""


        else:


            texto = f"""
💳 Sua chave Pix:


<code>{resultado[0]}</code>
"""



        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )    # ======================================
    # HISTÓRICO
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "📜 Histórico"
    )
    def historico(message):


        if not verificar_acesso(bot, message):

            return



        user_id = message.from_user.id



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

            (user_id,)

        )


        registros = cursor.fetchall()



        if not registros:


            bot.send_message(

                message.chat.id,

                """
📜 Nenhum histórico encontrado.
"""

            )

            return



        texto = "📜 <b>SEU HISTÓRICO</b>\n\n"



        for item in registros:


            texto += f"""
📌 {item[0]}

{item[1]}

💰 R$ {item[2]:.2f}

📅 {item[3]}

────────────
"""



        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )



    # ======================================
    # REGRAS
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "📜 Regras"
    )
    def regras(message):


        bot.send_message(

            message.chat.id,

            """
📜 <b>REGRAS DO BOT</b>


✅ Não crie várias contas.

✅ Não faça auto indicação.

✅ Não use Pix de terceiros.

✅ Fraudes podem causar bloqueio.

✅ O pagamento depende da validação.
""",

            parse_mode="HTML"

        )



    # ======================================
    # INFORMAÇÕES
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "ℹ️ Informações"
    )
    def informacoes(message):


        bot.send_message(

            message.chat.id,

            f"""
ℹ️ <b>{NOME_BOT}</b>


🤖 Sistema automático de indicações.


🎁 Convide pessoas.

💰 Receba recompensas.

💳 Cadastre seu Pix.

👥 Participe do grupo oficial.
""",

            parse_mode="HTML"

        )



    # ======================================
    # VOLTAR MENU
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "🏠 Menu"
    )
    def voltar_menu(message):


        if not verificar_acesso(bot, message):

            return



        bot.send_message(

            message.chat.id,

            "🏠 Menu principal",

            reply_markup=menu_principal()

        )


# ==========================================
# FIM DO USUARIO.PY
# ==========================================
