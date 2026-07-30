"""
=========================================
 PITBULL REFERRAL BOT V2
 Sistema de Utilizadores
=========================================
"""

from datetime import datetime

from database import conn, cursor


def cadastrar_usuario(user):

    cursor.execute(
        "SELECT id FROM usuarios WHERE id=?",
        (user.id,)
    )

    if cursor.fetchone():
        return

    username = user.username

    if username is None:
        username = ""

    cursor.execute("""

        INSERT INTO usuarios(

            id,
            nome,
            username,
            saldo,
            pix,
            indicados,
            convidado_por,
            data_cadastro

        )

        VALUES(?,?,?,?,?,?,?,?)

    """, (

        user.id,
        user.first_name,
        username,
        0,
        "",
        0,
        None,
        datetime.now().strftime("%d/%m/%Y %H:%M")

    ))

    conn.commit()
