from indicacoes import processar_convite

# ==========================================
# START INTEGRADO COM INDICAÇÕES
# ==========================================

@bot.message_handler(commands=["start"])
def start(message):

    if not verificar_acesso(bot, message):
        return


    user_id = message.from_user.id

    nome = message.from_user.first_name

    username = (
        "@" + message.from_user.username
        if message.from_user.username
        else ""
    )


    cursor.execute(
        """
        SELECT id

        FROM usuarios

        WHERE id=?
        """,
        (user_id,)
    )


    usuario = cursor.fetchone()


    # ======================================
    # NOVO USUÁRIO
    # ======================================

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
                admin,
                data_cadastro,
                ultimo_acesso

            )

            VALUES(

                ?,?,?,?,?,?,?,?,?,?

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
                0,
                agora(),
                agora()

            )

        )


        conn.commit()


        adicionar_log(

            user_id,

            "CADASTRO",

            "Novo usuário criado"

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


    # ======================================
    # PROCESSAR CONVITE
    # ======================================

    indicador = processar_convite(

        user_id,

        message.text

    )


    if indicador:


        bot.send_message(

            message.chat.id,

            """
🎁 Você entrou através de um convite!

Para validar sua indicação:

👥 Entre no grupo

✅ Confirme sua entrada

💳 Cadastre seu Pix

Após completar tudo, a recompensa será liberada.
"""

        )


    else:


        bot.send_message(

            message.chat.id,

            f"""
🎉 Bem-vindo(a), {nome}!

Use o menu abaixo para começar.
"""

        )
