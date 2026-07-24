import telebot

TOKEN = '8771309444:AAE522egqaCOPGaAZUqDCB-6zY6uK-y1lhg'
bot = telebot.TeleBot(TOKEN)

usuarios = {}

RECOMPENSAS = {
    5: "🌟 Bronze - Acesso ao grupo VIP",
    10: "⭐ Prata - 50 moedas",
    25: "💫 Ouro - 100 moedas",
    50: "👑 Elite - Cargo especial",
    100: "🔥 Lendário - Prêmio surpresa"
}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    nome = message.from_user.first_name
    
    if user_id not in usuarios:
        usuarios[user_id] = {
            'nome': nome,
            'convites': 0,
            'moedas': 0
        }
    
    bot.reply_to(message, f"👋 Olá {nome}! Seu bot está funcionando!\n\nUse /meusdados para ver suas estatísticas.")

@bot.message_handler(commands=['meusdados'])
def meus_dados(message):
    user_id = str(message.from_user.id)
    
    if user_id not in usuarios:
        usuarios[user_id] = {
            'nome': message.from_user.first_name,
            'convites': 0,
            'moedas': 0
        }
    
    user = usuarios[user_id]
    bot.reply_to(message, f"📊 Nome: {user['nome']}\n📨 Convites: {user['convites']}\n🪙 Moedas: {user['moedas']}")

@bot.message_handler(commands=['ranking'])
def ranking(message):
    bot.reply_to(message, "🏆 Ranking em breve!")

@bot.message_handler(commands=['recompensas'])
def recompensas(message):
    texto = "🎁 Recompensas:\n"
    for convites, premio in RECOMPENSAS.items():
        texto += f"\n📨 {convites} convites → {premio}"
    bot.reply_to(message, texto)

bot.infinity_polling()
