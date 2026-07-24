import telebot
from config import *
from database import conn, cursor

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    nome = message.from_user.first_name

    cursor.execute("SELECT * FROM usuarios WHERE id=?", (user_id,))
    usuario = cursor.fetchone()

    if usuario is None:

        args = message.text.split()

        convidado_por = None

        if len(args) > 1:
            if args[1].startswith("convite_"):
                convidado_por = int(args[1].replace("convite_", ""))

        cursor.execute(
            """
            INSERT INTO usuarios(id,nome,saldo,pix,convidados,convidado_por)
            VALUES(?,?,?,?,?,?)
            """,
            (
                user_id,
                nome,
                0,
                "",
                0,
                convidado_por
            )
        )

        conn.commit()

        if convidado_por and convidado_por != user_id:

            cursor.execute(
                "UPDATE usuarios SET saldo = saldo + ?, convidados = convidados + 1 WHERE id=?",
                (VALOR_POR_CONVIDADO, convidado_por)
            )

            conn.commit()

    link = f"https://t.me/{bot.get_me().username}?start=convite_{user_id}"

    texto = f"""
<b>🎁 Programa de Indicação</b>

Olá <b>{nome}</b>!

💰 Ganhe R$ {VALOR_POR_CONVIDADO:.2f} para cada amigo indicado.

🔗 Seu link:

<code>{link}</code>

Comandos:

/meusdados
/regras
/grupo
/saque
"""

    bot.reply_to(message, texto, parse_mode="HTML")


@bot.message_handler(commands=['grupo'])
def grupo(message):
    bot.reply_to(
        message,
        GRUPO_LINK
    )


print("Bot online!")
@bot.message_handler(commands=['meusdados'])
def meusdados(message):

    user_id = message.from_user.id

    cursor.execute(
        "SELECT saldo, convidados, pix FROM usuarios WHERE id=?",
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        bot.reply_to(message, "Use /start primeiro.")
        return

    saldo, convidados, pix = user

    chave = pix if pix else "Não cadastrada"

    texto = f"""
<b>📊 Seus Dados</b>

💰 Saldo: R$ {saldo:.2f}

👥 Indicados: {convidados}

💳 Pix:
<code>{chave}</code>
"""

    bot.reply_to(message, texto, parse_mode="HTML")


@bot.message_handler(commands=['pix'])
def pix(message):

    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        bot.reply_to(
            message,
            "Use assim:\n\n/pix sua_chave_pix"
        )
        return

    chave = args[1].strip()

    cursor.execute(
        "UPDATE usuarios SET pix=? WHERE id=?",
        (chave, message.from_user.id)
    )

    conn.commit()

    bot.reply_to(
        message,
        "✅ Sua chave Pix foi cadastrada com sucesso!"
    )


bot.infinity_polling(skip_pending=True)
