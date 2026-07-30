"""
=========================================
 PITBULL REFERRAL BOT V2
 Arquivo Principal
=========================================
"""

import database

from bot import bot
from usuarios import cadastrar_usuario


@bot.message_handler(commands=["start"])
def start(message):

    # Cadastra o utilizador
    cadastrar_usuario(message.from_user)

    nome = message.from_user.first_name

    bot.reply_to(
        message,
        f"""
👋 Olá, <b>{nome}</b>!

🎉 Seja bem-vindo ao <b>Pitbull Referral Bot V2</b>.

✅ O seu cadastro foi realizado com sucesso!

Em breve terá acesso ao sistema de afiliados, carteira e saques.
""",
        parse_mode="HTML"
    )


print("===================================")
print("🤖 Pitbull Referral Bot V2")
print("✅ Bot iniciado com sucesso!")
print("===================================")

bot.infinity_polling(skip_pending=True)
