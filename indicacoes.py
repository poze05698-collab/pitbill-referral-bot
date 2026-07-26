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
# CHAMADO PELO usuario.py
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
    # BLOQUEAR AUTO INDICAÇÃO
    # ======================================

    if indicador == user_id:


        adicionar_log(

            user_id,

            "FRAUDE",

            "Tentativa de auto indicação"

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
    # VERIFICAR SE JÁ FOI INDICADO
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


    except Exception:

        pass



    return False# ==========================================
# REGISTRAR HANDLERS DE INDICAÇÃO
# ==========================================

def registrar_indicacoes(bot):


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
👥 <b>ENTRE NO GRUPO OFICIAL</b>


Clique no link abaixo:

{GRUPO_LINK}


Depois volte e clique:

✅ Já Entrei
""",

            parse_mode="HTML"

        )



    # ======================================
    # CONFIRMAR ENTRADA NO GRUPO
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "✅ Já Entrei"
    )
    def ja_entrei(message):

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
❌ Não encontramos sua entrada no grupo.

Entre primeiro:

{GRUPO_LINK}

Depois clique novamente:

✅ Já Entrei
"""

            )


            return



        # ==================================
        # BUSCAR INDICAÇÃO PENDENTE
        # ==================================

        cursor.execute(

            """
            SELECT

                id

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
✅ <b>Grupo confirmado!</b>


Agora cadastre sua chave Pix.

Quando o Pix for salvo,
a indicação será finalizada.
""",

            parse_mode="HTML"

        )# ==========================================
# FINALIZAR INDICAÇÃO APÓS PIX
# CHAMADO PELO usuario.py
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
    # PRECISA TER CONFIRMADO O GRUPO
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
    # PAGAR RECOMPENSA
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
    # HISTÓRICO DO INDICADOR
    # ======================================

    adicionar_historico(

        indicador,

        "INDICAÇÃO",

        "Recompensa por indicação aprovada",

        VALOR_INDICACAO

    )



    # ======================================
    # HISTÓRICO DO INDICADO
    # ======================================

    adicionar_historico(

        user_id,

        "CADASTRO",

        "Indicação validada com sucesso",

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

        f"Indicador: {indicador}"

    )



    # ======================================
    # AVISAR INDICADOR
    # ======================================

    try:

        bot.send_message(

            indicador,

            f"""
🎉 <b>PARABÉNS!</b>


Uma indicação sua foi aprovada.


💰 Você recebeu:

<b>R$ {VALOR_INDICACAO:.2f}</b>


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
✅ Seu cadastro foi validado!


Sua participação está ativa.
"""

        )


    except:

        pass



    return True# ==========================================
# GERAR LINK DE INDICAÇÃO
# ==========================================

def gerar_link_indicacao(bot, user_id):

    nome_bot = bot.get_me().username


    link = (

        f"https://t.me/{nome_bot}"

        f"?start=convite_{user_id}"

    )


    return link



# ==========================================
# ESTATÍSTICAS DO USUÁRIO
# ==========================================

def estatisticas_indicacao(user_id):


    resultado = {

        "PENDENTE": 0,

        "GRUPO_OK": 0,

        "APROVADA": 0

    }



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



    for status, quantidade in dados:


        if status in resultado:

            resultado[status] = quantidade



    return resultado



# ==========================================
# LISTAR INDICAÇÕES
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


    return cursor.fetchall()



# ==========================================
# RANKING DE INDICAÇÕES
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
# VERIFICAR FRAUDE DE INDICAÇÃO
# ==========================================

def verificar_fraude(indicador, indicado):


    # AUTO INDICAÇÃO

    if indicador == indicado:


        adicionar_log(

            indicado,

            "FRAUDE",

            "Tentativa de auto indicação."

        )


        return True



    # DUPLICIDADE

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

            "Usuário já possui indicador."

        )


        return True



    return False# ==========================================
# HANDLERS DE INDICAÇÃO
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


Compartilhe com seus amigos:

🔗

<code>{link}</code>


💰 Você ganha:

<b>R$ {VALOR_INDICACAO:.2f}</b>

por cada indicação válida.


A indicação precisa:

✅ Entrar pelo seu link

✅ Entrar no grupo

✅ Cadastrar o Pix
""",

            parse_mode="HTML"

        )



    # ======================================
    # MEUS INDICADOS
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



        if posicao == 1:

            texto += "Nenhum usuário encontrado."



        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )



# ==========================================
# FIM DO INDICACOES.PY
# ==========================================
