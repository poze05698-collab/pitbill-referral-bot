from database import conn, cursor

from config import (
    VALOR_INDICACAO,
    GRUPO_ID,
    GRUPO_LINK
)

from utils import (
    adicionar_log,
    adicionar_historico,
    agora
)


# ==========================================
# REGISTRAR MÓDULO
# ==========================================

def registrar_indicacoes(bot):


    # ======================================
    # PROCESSAR LINK DE CONVITE
    # ======================================

    def processar_convite(user_id, texto):

        if not texto:
            return None


        partes = texto.split()


        if len(partes) < 2:
            return None


        codigo = partes[1]


        if not codigo.startswith("convite_"):

            return None


        try:

            indicador = int(

                codigo.replace(
                    "convite_",
                    ""
                )

            )

        except:

            return None


        # ==================================
        # IMPEDIR AUTO INDICAÇÃO
        # ==================================

        if indicador == user_id:

            adicionar_log(

                user_id,

                "AUTO INDICAÇÃO",

                "Tentativa de indicar a própria conta."

            )

            return None


        # ==================================
        # VERIFICAR INDICADOR EXISTE
        # ==================================

        cursor.execute(

            """
            SELECT id

            FROM usuarios

            WHERE id=?

            """,

            (indicador,)

        )


        existe = cursor.fetchone()


        if existe is None:

            return None


        # ==================================
        # VERIFICAR DUPLICADA
        # ==================================

        cursor.execute(

            """
            SELECT id

            FROM indicacoes

            WHERE indicado=?

            """,

            (user_id,)

        )


        duplicada = cursor.fetchone()


        if duplicada:

            return None


        # ==================================
        # CRIAR INDICAÇÃO PENDENTE
        # ==================================

        cursor.execute(

            """
            INSERT INTO indicacoes(

                indicador,

                indicado,

                recompensa,

                status,

                data

            )

            VALUES(

                ?,?,?,?,?

            )

            """,

            (

                indicador,

                user_id,

                VALOR_INDICACAO,

                "PENDENTE",

                agora()

            )

        )


        conn.commit()


        adicionar_log(

            user_id,

            "INDICAÇÃO",

            f"Entrou pelo link do usuário {indicador}"

        )


        return indicador



    # ======================================
    # VERIFICAR ENTRADA NO GRUPO
    # ======================================

    def verificar_grupo(user_id):

        try:

            membro = bot.get_chat_member(

                GRUPO_ID,

                user_id

            )


            if membro.status in [

                "member",

                "administrator",

                "creator"

            ]:

                return True


        except Exception:

            pass


        return False    # ======================================
    # BOTÃO JÁ ENTREI NO GRUPO
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "✅ Já Entrei"
    )
    def ja_entrei_grupo(message):

        user_id = message.from_user.id


        # ==================================
        # VERIFICAR GRUPO
        # ==================================

        if not verificar_grupo(user_id):

            bot.send_message(

                message.chat.id,

                f"""
❌ Você ainda não entrou no grupo.

Entre pelo link:

{GRUPO_LINK}

Depois clique novamente em:

✅ Já Entrei
"""

            )

            return


        # ==================================
        # BUSCAR INDICAÇÃO
        # ==================================

        cursor.execute(

            """
            SELECT

                id,
                indicador

            FROM indicacoes

            WHERE indicado=?

            AND status='PENDENTE'

            """,

            (user_id,)

        )


        indicacao = cursor.fetchone()


        if indicacao is None:


            bot.send_message(

                message.chat.id,

                """
⚠️ Nenhuma indicação pendente encontrada.
"""

            )

            return


        indicacao_id = indicacao[0]


        # ==================================
        # ATUALIZAR STATUS
        # ==================================

        cursor.execute(

            """
            UPDATE indicacoes

            SET status='GRUPO_OK'

            WHERE id=?

            """,

            (indicacao_id,)

        )


        conn.commit()


        adicionar_log(

            user_id,

            "GRUPO VALIDADO",

            "Usuário confirmou entrada no grupo."

        )


        bot.send_message(

            message.chat.id,

            """
✅ Grupo confirmado!

Agora cadastre sua chave Pix para finalizar o cadastro da indicação.
""",

        )    # ======================================
    # FINALIZAR INDICAÇÃO APÓS PIX
    # ======================================

    def finalizar_indicacao(user_id):


        # ==================================
        # BUSCAR INDICAÇÃO
        # ==================================

        cursor.execute(

            """
            SELECT

                id,

                indicador,

                status

            FROM indicacoes

            WHERE indicado=?

            """,

            (user_id,)

        )


        indicacao = cursor.fetchone()


        if indicacao is None:

            return False


        indicacao_id = indicacao[0]

        indicador = indicacao[1]

        status = indicacao[2]


        # ==================================
        # VERIFICAR STATUS
        # ==================================

        if status != "GRUPO_OK":

            return False


        # ==================================
        # VERIFICAR PIX
        # ==================================

        cursor.execute(

            """
            SELECT pix

            FROM usuarios

            WHERE id=?

            """,

            (user_id,)

        )


        usuario = cursor.fetchone()


        if usuario is None:

            return False


        if usuario[0] == "":

            return False


        # ==================================
        # APROVAR INDICAÇÃO
        # ==================================

        cursor.execute(

            """
            UPDATE indicacoes

            SET

                status='APROVADA'

            WHERE id=?

            """,

            (indicacao_id,)

        )


        # ==================================
        # PAGAR RECOMPENSA
        # ==================================

        cursor.execute(

            """
            UPDATE usuarios

            SET

                saldo = saldo + ?,

                convidados = convidados + 1

            WHERE id=?

            """,

            (

                VALOR_INDICACAO,

                indicador

            )

        )


        conn.commit()


        # ==================================
        # HISTÓRICO INDICADOR
        # ==================================

        adicionar_historico(

            indicador,

            "INDICAÇÃO",

            "Recompensa por indicação aprovada",

            VALOR_INDICACAO

        )


        # ==================================
        # HISTÓRICO INDICADO
        # ==================================

        adicionar_historico(

            user_id,

            "CADASTRO",

            "Indicação validada",

            0

        )


        # ==================================
        # LOGS
        # ==================================

        adicionar_log(

            indicador,

            "RECOMPENSA",

            f"Recebeu R$ {VALOR_INDICACAO:.2f} pela indicação {user_id}"

        )


        adicionar_log(

            user_id,

            "INDICAÇÃO APROVADA",

            f"Indicação do usuário {indicador}"

        )


        # ==================================
        # AVISAR INDICADOR
        # ==================================

        try:

            bot.send_message(

                indicador,

                f"""
🎉 <b>INDICAÇÃO APROVADA!</b>

Você recebeu:

💰 R$ {VALOR_INDICACAO:.2f}

O valor já está no seu saldo.
""",

                parse_mode="HTML"

            )


        except:

            pass


        # ==================================
        # AVISAR INDICADO
        # ==================================

        try:

            bot.send_message(

                user_id,

                """
✅ Cadastro finalizado!

Sua indicação foi validada.
Agora você já pode utilizar o bot.
"""

            )


        except:

            pass


        return True    # ======================================
    # MEU LINK DE INDICAÇÃO
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "🔗 Meu Link"
    )
    def gerar_link(message):

        user_id = message.from_user.id

        username_bot = bot.get_me().username

        link = (
            f"https://t.me/{username_bot}"
            f"?start=convite_{user_id}"
        )


        texto = f"""
🎁 <b>SEU LINK DE INDICAÇÃO</b>

Compartilhe com seus amigos:

🔗

<code>{link}</code>


💰 Cada pessoa que:

✅ Entrar pelo seu link

✅ Entrar no grupo

✅ Cadastrar o Pix


gera uma recompensa de:

<b>R$ {VALOR_INDICACAO:.2f}</b>

Boa sorte! 🚀
"""


        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )


    # ======================================
    # BOTÃO ENTRAR NO GRUPO
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "👥 Entrar no Grupo"
    )
    def entrar_grupo(message):

        bot.send_message(

            message.chat.id,

            f"""
👥 Entre no nosso grupo:

{GRUPO_LINK}


Depois clique:

✅ Já Entrei
"""

        )


    # ======================================
    # MINHAS INDICAÇÕES
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "👥 Indicados"
    )
    def minhas_indicacoes(message):

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



        texto = f"""
👥 <b>SUAS INDICAÇÕES</b>


⏳ Pendentes:

{pendentes}


👥 Grupo confirmado:

{grupo_ok}


✅ Aprovadas:

{aprovadas}


💰 Ganhos:

R$ {(aprovadas * VALOR_INDICACAO):.2f}
"""


        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )


    # ======================================
    # RANKING
    # ======================================

    @bot.message_handler(
        commands=["ranking"]
    )
    def ranking(message):


        cursor.execute(

            """
            SELECT

                nome,

                convidados

            FROM usuarios

            ORDER BY convidados DESC

            LIMIT 10

            """

        )


        lista = cursor.fetchall()


        texto = """
🏆 <b>RANKING DE INDICADORES</b>


"""


        posicao = 1


        for usuario in lista:


            texto += (
                f"{posicao}º "
                f"{usuario[0]} "
                f"- 👥 {usuario[1]}\n"
            )


            posicao += 1



        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )    # ======================================
    # REGISTRAR INDICAÇÃO PELO START
    # ======================================

    @bot.message_handler(commands=["start"])
    def registrar_start_indicacao(message):

        user_id = message.from_user.id

        texto = message.text

        indicador = processar_convite(

            user_id,

            texto

        )


        if indicador:

            bot.send_message(

                message.chat.id,

                """
🎁 Você entrou através de um link de indicação!

Para validar sua participação:

1️⃣ Entre no grupo.

2️⃣ Confirme sua entrada.

3️⃣ Cadastre sua chave Pix.

Depois disso a indicação será aprovada.
"""

            )


    # ======================================
    # VERIFICAR STATUS DA INDICAÇÃO
    # ======================================

    def status_indicacao(user_id):

        cursor.execute(

            """
            SELECT

                status

            FROM indicacoes

            WHERE indicado=?

            """,

            (user_id,)

        )


        resultado = cursor.fetchone()


        if resultado:

            return resultado[0]


        return None



    # ======================================
    # VALIDAR APÓS CADASTRAR PIX
    # ======================================

    def validar_apos_pix(user_id):

        resultado = finalizar_indicacao(

            user_id

        )


        if resultado:

            adicionar_log(

                user_id,

                "VALIDAÇÃO FINAL",

                "Indicação concluída após Pix."

            )


        return resultado



    # ======================================
    # VERIFICAR INDICAÇÕES FRAUDULENTAS
    # ======================================

    def verificar_fraude_indicacao(

        indicador,

        indicado

    ):


        # Mesmo usuário

        if indicador == indicado:


            adicionar_log(

                indicado,

                "FRAUDE",

                "Tentativa de auto indicação."

            )


            return True



        # Indicação já existe

        cursor.execute(

            """
            SELECT id

            FROM indicacoes

            WHERE indicado=?

            """,

            (indicado,)

        )


        existe = cursor.fetchone()


        if existe:


            adicionar_log(

                indicado,

                "FRAUDE",

                "Indicação duplicada."

            )


            return True



        return False



    # ======================================
    # FIM DO MÓDULO
    # ======================================
