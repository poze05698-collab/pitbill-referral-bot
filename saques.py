from database import (
    conn,
    cursor
)

from config import (
    VALOR_MINIMO_SAQUE,
    ADMIN_ID
)

from teclado import (
    menu_principal
)

from utils import (
    verificar_acesso,
    adicionar_log,
    adicionar_historico,
    agora
)



# ==========================================
# REGISTRAR MÓDULO DE SAQUES
# ==========================================

def registrar_saques(bot):


    # ======================================
    # SOLICITAR SAQUE
    # ======================================

    @bot.message_handler(
        func=lambda m: m.text == "💸 Solicitar Saque"
    )
    def solicitar_saque(message):


        if not verificar_acesso(
            bot,
            message
        ):

            return



        user_id = message.from_user.id



        cursor.execute(

            """
            SELECT

                saldo,

                pix

            FROM usuarios

            WHERE id=?

            """,

            (user_id,)

        )


        usuario = cursor.fetchone()



        if usuario is None:

            return



        saldo = usuario[0]

        pix = usuario[1]



        # ==================================
        # VERIFICAR PIX
        # ==================================

        if pix == "":


            bot.send_message(

                message.chat.id,

                """
❌ Você precisa cadastrar sua chave Pix antes de solicitar saque.
"""

            )

            return



        # ==================================
        # VERIFICAR SALDO
        # ==================================

        if saldo < VALOR_MINIMO_SAQUE:


            bot.send_message(

                message.chat.id,

                f"""
❌ Saldo insuficiente.

Mínimo para saque:

R$ {VALOR_MINIMO_SAQUE:.2f}
"""

            )

            return



        bot.send_message(

            message.chat.id,

            """
💸 Informe o valor do saque:

Exemplo:

15
"""

        )


        bot.register_next_step_handler(

            message,

            receber_valor_saque

        )    # ======================================
    # RECEBER VALOR DO SAQUE
    # ======================================

    def receber_valor_saque(message):

        user_id = message.from_user.id


        try:

            valor = float(

                message.text.replace(

                    ",",

                    "."

                )

            )


        except:


            bot.send_message(

                message.chat.id,

                """
❌ Valor inválido.

Digite apenas números.

Exemplo:

15
"""

            )

            return



        # ==================================
        # VERIFICAR VALOR MÍNIMO
        # ==================================

        if valor < VALOR_MINIMO_SAQUE:


            bot.send_message(

                message.chat.id,

                f"""
❌ O valor mínimo para saque é:

R$ {VALOR_MINIMO_SAQUE:.2f}
"""

            )

            return



        # ==================================
        # VERIFICAR SALDO NOVAMENTE
        # ==================================

        cursor.execute(

            """
            SELECT

                saldo,

                pix

            FROM usuarios

            WHERE id=?

            """,

            (user_id,)

        )


        usuario = cursor.fetchone()



        if usuario is None:

            return



        if valor > usuario[0]:


            bot.send_message(

                message.chat.id,

                """
❌ Você não possui saldo suficiente.
"""

            )

            return



        # ==================================
        # CRIAR SAQUE PENDENTE
        # ==================================

        cursor.execute(

            """
            INSERT INTO saques(

                usuario,

                valor,

                pix,

                status,

                data

            )

            VALUES(

                ?,?,?,?,?

            )

            """,

            (

                user_id,

                valor,

                usuario[1],

                "PENDENTE",

                agora()

            )

        )


        conn.commit()



        saque_id = cursor.lastrowid



        adicionar_log(

            user_id,

            "SAQUE SOLICITADO",

            f"Saque {saque_id} no valor R$ {valor:.2f}"

        )



        bot.send_message(

            message.chat.id,

            f"""
✅ Solicitação enviada!


💸 Valor:

R$ {valor:.2f}


Aguarde a aprovação do administrador.
"""

        )



        # ==================================
        # AVISAR ADMIN
        # ==================================

        try:


            bot.send_message(

                ADMIN_ID,

                f"""
💸 <b>NOVO SAQUE</b>


🆔 ID:

{saque_id}


👤 Usuário:

{user_id}


💰 Valor:

R$ {valor:.2f}


Use:

/aprovar {saque_id}

ou

/rejeitar {saque_id}
""",

                parse_mode="HTML"

            )


        except:


            pass    # ======================================
    # APROVAR SAQUE
    # ======================================

    @bot.message_handler(
        commands=["aprovar"]
    )
    def aprovar_saque(message):

        if message.from_user.id != ADMIN_ID:

            return



        try:

            saque_id = int(

                message.text.split()[1]

            )


        except:


            bot.reply_to(

                message,

                "Use:\n/aprovar ID_DO_SAQUE"

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



        usuario = saque[0]

        valor = saque[1]

        status = saque[2]



        if status != "PENDENTE":


            bot.reply_to(

                message,

                "⚠️ Este saque já foi processado."

            )

            return



        # ==================================
        # DESCONTAR SALDO
        # ==================================

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



        # ==================================
        # ATUALIZAR SAQUE
        # ==================================

        cursor.execute(

            """
            UPDATE saques

            SET

                status='APROVADO',

                aprovado_por=?,

                data_aprovacao=?

            WHERE id=?

            """,

            (

                ADMIN_ID,

                agora(),

                saque_id

            )

        )



        conn.commit()



        adicionar_historico(

            usuario,

            "SAQUE",

            "Saque aprovado",

            -valor

        )



        adicionar_log(

            ADMIN_ID,

            "SAQUE APROVADO",

            f"Saque {saque_id}"

        )



        bot.reply_to(

            message,

            "✅ Saque aprovado."

        )



        try:


            bot.send_message(

                usuario,

                f"""
✅ <b>SAQUE APROVADO</b>


💸 Valor:

R$ {valor:.2f}


O pagamento foi autorizado.
""",

                parse_mode="HTML"

            )


        except:


            pass



    # ======================================
    # REJEITAR SAQUE
    # ======================================

    @bot.message_handler(
        commands=["rejeitar"]
    )
    def rejeitar_saque(message):

        if message.from_user.id != ADMIN_ID:

            return



        try:

            saque_id = int(

                message.text.split()[1]

            )


        except:


            bot.reply_to(

                message,

                "Use:\n/rejeitar ID_DO_SAQUE"

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



        usuario = saque[0]

        valor = saque[1]

        status = saque[2]



        if status != "PENDENTE":


            bot.reply_to(

                message,

                "⚠️ Saque já processado."

            )

            return



        cursor.execute(

            """
            UPDATE saques

            SET

                status='REJEITADO',

                aprovado_por=?,

                data_aprovacao=?

            WHERE id=?

            """,

            (

                ADMIN_ID,

                agora(),

                saque_id

            )

        )



        conn.commit()



        adicionar_log(

            ADMIN_ID,

            "SAQUE REJEITADO",

            f"Saque {saque_id}"

        )



        bot.reply_to(

            message,

            "❌ Saque rejeitado."

        )



        try:


            bot.send_message(

                usuario,

                f"""
❌ <b>SAQUE REJEITADO</b>


Solicitação:

#{saque_id}


Valor:

R$ {valor:.2f}
""",

                parse_mode="HTML"

            )


        except:


            pass    # ======================================
    # MEUS SAQUES
    # ======================================

    @bot.message_handler(
        commands=["meussaques"]
    )
    def meus_saques(message):

        if not verificar_acesso(
            bot,
            message
        ):

            return



        user_id = message.from_user.id



        cursor.execute(

            """
            SELECT

                id,

                valor,

                status,

                data

            FROM saques

            WHERE usuario=?

            ORDER BY id DESC

            LIMIT 10

            """,

            (user_id,)

        )


        lista = cursor.fetchall()



        if not lista:


            bot.send_message(

                message.chat.id,

                """
💸 Você ainda não possui saques.
"""

            )

            return



        texto = """
💸 <b>SEUS SAQUES</b>


"""


        for saque in lista:


            texto += f"""
🆔 ID:

{saque[0]}


💰 Valor:

R$ {saque[1]:.2f}


📌 Status:

{saque[2]}


📅 Data:

{saque[3]}


────────────
"""



        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML"

        )



    # ======================================
    # CONSULTAR SAQUE
    # ======================================

    @bot.message_handler(
        commands=["saqueinfo"]
    )
    def saque_info(message):


        try:

            saque_id = int(

                message.text.split()[1]

            )


        except:


            bot.reply_to(

                message,

                "Use:\n/saqueinfo ID"

            )

            return



        cursor.execute(

            """
            SELECT

                usuario,

                valor,

                status,

                data

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



        # Somente admin ou dono

        if (

            message.from_user.id != ADMIN_ID

            and

            message.from_user.id != saque[0]

        ):

            return



        bot.send_message(

            message.chat.id,

            f"""
💸 <b>INFORMAÇÕES DO SAQUE</b>


🆔 ID:

{saque_id}


👤 Usuário:

{saque[0]}


💰 Valor:

R$ {saque[1]:.2f}


📌 Status:

{saque[2]}


📅 Data:

{saque[3]}
""",

            parse_mode="HTML"

        )



# ==========================================
# FIM DO SAQUES.PY
# ==========================================
