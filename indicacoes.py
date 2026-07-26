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
# PROCESSAR LINK DE CONVITE
# ==========================================

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


    # ======================================
    # IMPEDIR AUTO INDICAÇÃO
    # ======================================

    if indicador == user_id:

        adicionar_log(

            user_id,

            "FRAUDE",

            "Tentativa de auto indicação."

        )

        return None


    # ======================================
    # VERIFICAR INDICADOR
    # ======================================

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



    # ======================================
    # VERIFICAR DUPLICADA
    # ======================================

    cursor.execute(

        """
        SELECT id

        FROM indicacoes

        WHERE indicado=?

        """,

        (user_id,)

    )


    if cursor.fetchone():

        return None



    # ======================================
    # CRIAR INDICAÇÃO
    # ======================================

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

        f"Indicado pelo usuário {indicador}"

    )


    return indicador



# ==========================================
# VERIFICAR ENTRADA NO GRUPO
# ==========================================

def verificar_grupo(bot, user_id):

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


    except:

        pass


    return False# ==========================================
# REGISTRAR MÓDULO
# ==========================================

def registrar_indicacoes(bot):


    # ======================================
    # CONFIRMAR ENTRADA NO GRUPO
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "✅ Já Entrei"
    )
    def confirmar_grupo(message):

        user_id = message.from_user.id


        # ==================================
        # VERIFICAR GRUPO
        # ==================================

        if not verificar_grupo(
            bot,
            user_id
        ):

            bot.send_message(

                message.chat.id,

                f"""
❌ Você ainda não entrou no grupo.

Entre primeiro:

{GRUPO_LINK}


Depois clique novamente:

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

            "GRUPO CONFIRMADO",

            "Usuário confirmou entrada no grupo."

        )



        bot.send_message(

            message.chat.id,

            """
✅ Grupo confirmado!


Agora cadastre sua chave Pix.

Quando o Pix for cadastrado,
a indicação será validada automaticamente.
"""

        )



    # ======================================
    # BOTÃO ENTRAR NO GRUPO
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "👥 Entrar no Grupo"
    )
    def enviar_grupo(message):


        bot.send_message(

            message.chat.id,

            f"""
👥 Entre no nosso grupo:

{GRUPO_LINK}


Depois volte e clique:

✅ Já Entrei
"""

        )# ==========================================
# FINALIZAR INDICAÇÃO APÓS PIX
# ==========================================

def finalizar_indicacao(bot, user_id):


    # ======================================
    # BUSCAR INDICAÇÃO
    # ======================================

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



    # ======================================
    # SÓ CONTINUA SE GRUPO OK
    # ======================================

    if status != "GRUPO_OK":

        return False



    # ======================================
    # VERIFICAR PIX
    # ======================================

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



    # ======================================
    # APROVAR INDICAÇÃO
    # ======================================

    cursor.execute(

        """
        UPDATE indicacoes

        SET status='APROVADA'

        WHERE id=?

        """,

        (indicacao_id,)

    )



    # ======================================
    # PAGAR INDICADOR
    # ======================================

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



    # ======================================
    # HISTÓRICO INDICADOR
    # ======================================

    adicionar_historico(

        indicador,

        "INDICAÇÃO",

        "Recompensa recebida por indicação",

        VALOR_INDICACAO

    )



    # ======================================
    # HISTÓRICO INDICADO
    # ======================================

    adicionar_historico(

        user_id,

        "INDICAÇÃO",

        "Cadastro validado",

        0

    )



    # ======================================
    # LOGS
    # ======================================

    adicionar_log(

        indicador,

        "RECOMPENSA",

        f"Recebeu R$ {VALOR_INDICACAO:.2f}"

    )


    adicionar_log(

        user_id,

        "INDICAÇÃO APROVADA",

        f"Indicação do usuário {indicador}"

    )



    # ======================================
    # AVISAR INDICADOR
    # ======================================

    try:

        bot.send_message(

            indicador,

            f"""
🎉 <b>INDICAÇÃO APROVADA!</b>

Você recebeu:

💰 <b>R$ {VALOR_INDICACAO:.2f}</b>

O valor já está no seu saldo.
""",

            parse_mode="HTML"

        )


    except:

        pass



    # ======================================
    # AVISAR INDICADO
    # ======================================

    try:

        bot.send_message(

            user_id,

            """
✅ Cadastro finalizado!

Sua participação foi validada com sucesso.
"""

        )


    except:

        pass



    return True# ==========================================
# GERAR LINK DE INDICAÇÃO
# ==========================================

def gerar_link_indicacao(bot, user_id):

    username_bot = bot.get_me().username

    link = (
        f"https://t.me/{username_bot}"
        f"?start=convite_{user_id}"
    )

    return link



# ==========================================
# ESTATÍSTICAS DE INDICAÇÃO
# ==========================================

def estatisticas_indicacao(user_id):


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


    resultado = {

        "PENDENTE": 0,

        "GRUPO_OK": 0,

        "APROVADA": 0

    }


    for status, quantidade in dados:

        if status in resultado:

            resultado[status] = quantidade


    return resultado



# ==========================================
# RANKING INDICAÇÕES
# ==========================================

def ranking_indicacoes():

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


    return cursor.fetchall()



# ==========================================
# VERIFICAR FRAUDE
# ==========================================

def verificar_fraude(indicador, indicado):


    # Mesmo usuário

    if indicador == indicado:


        adicionar_log(

            indicado,

            "FRAUDE",

            "Tentativa de auto indicação."

        )


        return True



    # Verifica se já foi indicado

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

            "Usuário já possui indicação."

        )


        return True



    return False



# ==========================================
# LISTAR INDICAÇÕES DO USUÁRIO
# ==========================================

def listar_indicacoes(user_id):


    cursor.execute(

        """
        SELECT

            indicado,

            status,

            data

        FROM indicacoes

        WHERE indicador=?

        ORDER BY id DESC

        """,

        (user_id,)

    )


    return cursor.fetchall()# ==========================================
# REGISTRAR FUNÇÕES DO BOT
# ==========================================

def registrar_indicacoes(bot):


    # ======================================
    # MEU LINK
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "🔗 Meu Link"
    )
    def meu_link(message):

        user_id = message.from_user.id


        link = gerar_link_indicacao(

            bot,

            user_id

        )


        bot.send_message(

            message.chat.id,

            f"""
🎁 <b>SEU LINK DE INDICAÇÃO</b>


Compartilhe este link:

🔗

<code>{link}</code>


💰 Você ganha:

<b>R$ {VALOR_INDICACAO:.2f}</b>

por cada indicação válida.


A indicação será validada quando o usuário:

✅ Entrar pelo seu link

✅ Entrar no grupo

✅ Cadastrar o Pix
""",

            parse_mode="HTML"

        )



    # ======================================
    # MINHAS INDICAÇÕES
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "👥 Indicados"
    )
    def meus_indicados(message):

        user_id = message.from_user.id


        dados = estatisticas_indicacao(

            user_id

        )


        texto = f"""
👥 <b>SUAS INDICAÇÕES</b>


⏳ Pendentes:

{dados['PENDENTE']}


👥 Grupo confirmado:

{dados['GRUPO_OK']}


✅ Aprovadas:

{dados['APROVADA']}


💰 Ganhos:

R$ {(dados['APROVADA'] * VALOR_INDICACAO):.2f}
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


        lista = ranking_indicacoes()


        texto = """
🏆 <b>RANKING DE INDICADORES</b>


"""


        posicao = 1


        for usuario in lista:


            texto += f"""
{posicao}º - {usuario[0]}

👥 Indicados:
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
    # ENTRAR NO GRUPO
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "👥 Entrar no Grupo"
    )
    def entrar_grupo(message):


        bot.send_message(

            message.chat.id,

            f"""
👥 Entre no grupo oficial:

{GRUPO_LINK}


Depois volte e clique:

✅ Já Entrei
"""

        )



# ==========================================
# FIM DO ARQUIVO
# ==========================================
