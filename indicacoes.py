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
# PROCESSAR CONVITE
# Chamado pelo usuario.py
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



    # Bloquear auto indicação

    if indicador == user_id:


        adicionar_log(

            user_id,

            "FRAUDE",

            "Tentativa de auto indicação"

        )


        return None



    # Verificar indicador existe

    cursor.execute(

        """
        SELECT id

        FROM usuarios

        WHERE id=?

        """,

        (indicador,)

    )


    existe = cursor.fetchone()



    if not existe:

        return None



    # Verificar se já possui indicação

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



    # Criar indicação

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
# VERIFICAR GRUPO
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
# REGISTRAR INDICAÇÕES
# ==========================================

def registrar_indicacoes(bot):


    # ======================================
    # ENTRAR NO GRUPO
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "👥 Entrar no Grupo"
    )
    def entrar_grupo(message):


        if not GRUPO_LINK:


            bot.send_message(

                message.chat.id,

                """
⚠️ Grupo ainda não configurado.

Entre em contato com o administrador.
"""

            )

            return



        bot.send_message(

            message.chat.id,

            f"""
👥 <b>GRUPO OFICIAL</b>


Entre pelo link:

🔗 {GRUPO_LINK}


Depois volte e clique:

✅ Já Entrei
""",

            parse_mode="HTML"

        )



    # ======================================
    # CONFIRMAR ENTRADA
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "✅ Já Entrei"
    )
    def ja_entrei(message):


        user_id = message.from_user.id



        # verificar grupo

        entrou = verificar_grupo(

            bot,

            user_id

        )



        if not entrou:


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



        # Buscar indicação pendente

        cursor.execute(

            """
            SELECT id

            FROM indicacoes

            WHERE indicado=?

            AND status='PENDENTE'

            """,

            (user_id,)

        )


        indicacao = cursor.fetchone()



        if not indicacao:


            bot.send_message(

                message.chat.id,

                """
⚠️ Não existe indicação pendente.
"""

            )

            return



        # Atualizar status

        cursor.execute(

            """
            UPDATE indicacoes

            SET status='GRUPO_OK'

            WHERE id=?

            """,

            (indicacao[0],)

        )


        conn.commit()



        adicionar_log(

            user_id,

            "GRUPO CONFIRMADO",

            "Entrada no grupo confirmada."

        )



        bot.send_message(

            message.chat.id,

            """
✅ <b>Grupo confirmado!</b>


Agora cadastre sua chave Pix.

Depois disso a indicação será validada.
""",

            parse_mode="HTML"

        )# ==========================================
# FINALIZAR INDICAÇÃO
# Chamado pelo usuario.py após salvar Pix
# ==========================================

def finalizar_indicacao(bot, user_id):


    # Buscar indicação

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



    if not indicacao:

        return False



    id_indicacao = indicacao[0]

    indicador = indicacao[1]

    status = indicacao[2]



    # Precisa confirmar grupo

    if status != "GRUPO_OK":

        return False



    # Verificar Pix

    cursor.execute(

        """
        SELECT pix

        FROM usuarios

        WHERE id=?

        """,

        (user_id,)

    )


    usuario = cursor.fetchone()



    if not usuario:

        return False



    if usuario[0] == "":

        return False



    # Aprovar indicação

    cursor.execute(

        """
        UPDATE indicacoes

        SET status='APROVADA'

        WHERE id=?

        """,

        (id_indicacao,)

    )



    # Adicionar recompensa

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



    # Histórico indicador

    adicionar_historico(

        indicador,

        "INDICAÇÃO",

        "Recompensa por indicação aprovada",

        VALOR_INDICACAO

    )



    # Histórico indicado

    adicionar_historico(

        user_id,

        "VALIDAÇÃO",

        "Cadastro validado com sucesso",

        0

    )



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



    # Avisar indicador

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



    # Avisar indicado

    try:


        bot.send_message(

            user_id,

            """
✅ Cadastro validado!

Sua conta está ativa.
"""

        )


    except:


        pass



    return True# ==========================================
# GERAR LINK DE INDICAÇÃO
# ==========================================

def gerar_link_indicacao(bot, user_id):


    nome_bot = bot.get_me().username


    return (

        f"https://t.me/{nome_bot}"

        f"?start=convite_{user_id}"

    )



# ==========================================
# ESTATÍSTICAS
# ==========================================

def estatisticas_indicacao(user_id):


    dados = {

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


    resultado = cursor.fetchall()



    for status, quantidade in resultado:


        if status in dados:

            dados[status] = quantidade



    return dados



# ==========================================
# RANKING
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
# CONTINUAR REGISTRAR INDICAÇÕES
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
🔗 <b>SEU LINK DE CONVITE</b>


{link}


💰 Ganhe R$ {VALOR_INDICACAO:.2f}

por cada indicação válida.
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


        user_id = message.from_user.id



        dados = estatisticas_indicacao(

            user_id

        )



        bot.send_message(

            message.chat.id,

            f"""
👥 <b>SUAS INDICAÇÕES</b>


⏳ Pendentes:

{dados['PENDENTE']}


👥 Grupo confirmado:

{dados['GRUPO_OK']}


✅ Aprovadas:

{dados['APROVADA']}
""",

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

{posicao}º {usuario[0]}

👥 Indicados:
{usuario[1]}

💰 Saldo:
R$ {usuario[2]:.2f}

────────────
"""


            posicao += 1



        if posicao == 1:


            texto += "Nenhum indicador encontrado."



        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )



# ==========================================
# FIM DO INDICACOES.PY
# ==========================================
