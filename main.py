"""
=========================================
 PITBULL REFERRAL BOT V2
 Arquivo Principal
=========================================
"""

from bot import bot
import database


@bot.message_handler(commands=["start"])
def start(message):
    nome = message.from_user.first_name

    bot.reply_to(
        message,
        f"👋 Olá, <b>{nome}</b>!\n\n"
        "🚀 Bem-vindo ao Pitbull Referral Bot V2.\n\n"
        "O bot está funcionando com sucesso!"
    )


print("===================================")
print("🤖 Pitbull Referral Bot V2")
print("✅ Bot iniciado com sucesso!")
print("===================================")

bot.infinity_polling(skip_pending=True)
