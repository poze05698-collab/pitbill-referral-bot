import telebot


from config import (
    TOKEN
)


# ==========================================
# IMPORTAR BANCO
# ==========================================

import database



# ==========================================
# IMPORTAR MÓDULOS
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
# REGISTRAR SISTEMAS
# ==========================================

registrar_usuario(bot)

registrar_indicacoes(bot)

registrar_saques(bot)

registrar_admin(bot)

registrar_antifraude(bot)



# ==========================================
# COMANDO PING
# ==========================================

@bot.message_handler(
    commands=["ping"]
)
def ping(message):

    bot.reply_to(

        message,

        "🏓 Bot online!"

    )



# ==========================================
# ERRO GERAL
# ==========================================

@bot.message_handler(
    func=lambda m: True
)
def mensagens_nao_reconhecidas(message):

    pass# ==========================================
# INICIAR BOT
# ==========================================

if __name__ == "__main__":


    print(
        """
================================

🤖 BOT INICIADO COM SUCESSO

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

                f"Erro no bot: {erro}"

            )


            print(

                "Tentando reconectar..."

            )
