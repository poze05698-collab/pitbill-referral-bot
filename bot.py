import telebot


# ==========================================
# CONFIG
# ==========================================

from config import TOKEN



# ==========================================
# BANCO
# ==========================================

import database



# ==========================================
# MÓDULOS
# ==========================================

from usuario import registrar_usuario

from indicacoes import registrar_indicacoes

from saques import registrar_saques

from admin import registrar_admin

from antifraude import registrar_antifraude



# ==========================================
# CRIAR BOT
# ==========================================

bot = telebot.TeleBot(

    TOKEN,

    parse_mode="HTML"

)



# ==========================================
# CARREGAR SISTEMAS
# ==========================================

registrar_usuario(bot)

registrar_indicacoes(bot)

registrar_saques(bot)

registrar_admin(bot)

registrar_antifraude(bot)



# ==========================================
# TESTE ONLINE
# ==========================================

@bot.message_handler(
    commands=["ping"]
)
def ping(message):

    bot.reply_to(

        message,

        "🏓 Bot online!"

    )



print(
    "🤖 Bot iniciado com sucesso!"
)# ==========================================
# INICIAR BOT
# ==========================================

if __name__ == "__main__":


    print(
        """
================================

🤖 BOT INICIADO

✅ Usuários carregado
✅ Indicações carregado
✅ Saques carregado
✅ Admin carregado
✅ Antifraude carregado

================================
"""
    )


    while True:


        try:


            bot.infinity_polling(

                timeout=60,

                long_polling_timeout=60

            )


        except Exception as erro:


            print(

                f"⚠️ Erro encontrado: {erro}"

            )


            print(

                "🔄 Tentando reconectar..."

            )
