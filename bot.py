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

@bot.message_handler(commands=['saque'])
def saque(message):

    user_id = message.from_user.id

    cursor.execute(
        "SELECT saldo, pix FROM usuarios WHERE id=?",
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        bot.reply_to(message, "Use /start primeiro.")
        return

    saldo, pix = user

    if saldo < VALOR_MINIMO_SAQUE:
        falta = VALOR_MINIMO_SAQUE - saldo

        bot.reply_to(
            message,
            f"❌ Você ainda não pode sacar.\n\nFaltam R$ {falta:.2f}."
        )
        return

    if pix == "":
        bot.reply_to(
            message,
            "❌ Cadastre sua chave Pix primeiro usando:\n\n/pix sua_chave"
        )
        return

    cursor.execute(
        """
        INSERT INTO saques(usuario, valor, status)
        VALUES(?,?,?)
        """,
        (
            user_id,
            saldo,
            "PENDENTE"
        )
    )

    conn.commit()

    bot.reply_to(
        message,
        "✅ Seu pedido de saque foi enviado para análise."
    )

@bot.message_handler(commands=['pedidos'])
def pedidos(message):

    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Você não tem permissão.")
        return

    cursor.execute(
        "SELECT id, usuario, valor FROM saques WHERE status=?",
        ("PENDENTE",)
    )

    pedidos = cursor.fetchall()

    if not pedidos:
        bot.reply_to(message, "Não existem saques pendentes.")
        return

    texto = "📋 Saques pendentes:\n\n"

    for saque in pedidos:
        texto += (
            f"ID: {saque[0]}\n"
            f"Usuário: {saque[1]}\n"
            f"Valor: R$ {saque[2]:.2f}\n\n"
        )

    bot.reply_to(message, texto)

@bot.message_handler(commands=['aprovar'])
def aprovar(message):

    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Você não tem permissão.")
        return

    try:
        saque_id = int(message.text.split()[1])
    except:
        bot.reply_to(
            message,
            "Use assim:\n/aprovar ID_DO_SAQUE"
        )
        return

    cursor.execute(
        "SELECT usuario, valor, status FROM saques WHERE id=?",
        (saque_id,)
    )

    saque = cursor.fetchone()

    if not saque:
        bot.reply_to(message, "❌ Saque não encontrado.")
        return

    usuario, valor, status = saque

    if status != "PENDENTE":
        bot.reply_to(
            message,
            "❌ Esse saque já foi processado."
        )
        return

    cursor.execute(
        "UPDATE saques SET status=? WHERE id=?",
        ("APROVADO", saque_id)
    )

    conn.commit()

    bot.send_message(
    usuario,
    f"✅ Seu saque de R$ {valor:.2f} foi aprovado!"
)
    
    bot.reply_to(
        message,
        f"✅ Saque ID {saque_id} aprovado."
    )

@bot.message_handler(commands=['rejeitar'])
def rejeitar(message):

    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Você não tem permissão.")
        return

    try:
        saque_id = int(message.text.split()[1])
    except:
        bot.reply_to(
            message,
            "Use assim:\n/rejeitar ID_DO_SAQUE"
        )
        return

    cursor.execute(
        "SELECT status FROM saques WHERE id=?",
        (saque_id,)
    )

    saque = cursor.fetchone()

    if not saque:
        bot.reply_to(message, "❌ Saque não encontrado.")
        return

    if saque[0] != "PENDENTE":
        bot.reply_to(
            message,
            "❌ Esse saque já foi processado."
        )
        return

    cursor.execute(
        "UPDATE saques SET status=? WHERE id=?",
        ("REJEITADO", saque_id)
    )

    conn.commit()

    bot.send_message(
    usuario,
    f"❌ Seu saque de R$ {valor:.2f} foi rejeitado."
)
    
    bot.reply_to(
        message,
        f"❌ Saque ID {saque_id} rejeitado."
    )

@bot.message_handler(commands=['saldo'])
def saldo(message):

    user_id = message.from_user.id

    cursor.execute(
        "SELECT saldo FROM usuarios WHERE id=?",
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        bot.reply_to(
            message,
            "Use /start primeiro."
        )
        return

    saldo = user[0]

    bot.reply_to(
        message,
        f"💰 Seu saldo é: R$ {saldo:.2f}"
    )

@bot.message_handler(commands=['saldo'])
def saldo(message):

    user_id = message.from_user.id

    cursor.execute(
        "SELECT saldo FROM usuarios WHERE id=?",
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        bot.reply_to(
            message,
            "Use /start primeiro."
        )
        return

    saldo = user[0]

    bot.reply_to(
        message,
        f"💰 Seu saldo é: R$ {saldo:.2f}"
    )
bot.infinity_polling(skip_pending=True)
