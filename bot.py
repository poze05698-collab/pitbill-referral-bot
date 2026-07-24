import telebot
from datetime import datetime

TOKEN = '8771309444:AAE522egqaCOPGaAZUqDCB-6zY6uK-y1lhg'
GRUPO_LINK = 'https://t.me/pitbullslotsofc'
GRUPO_ID = None
VALOR_POR_CONVIDADO = 1.00
VALOR_MINIMO_SAQUE = 15.00

bot = telebot.TeleBot(TOKEN)

usuarios = {}
convidados_registrados = {}

# ========== COMANDOS ==========

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    nome = message.from_user.first_name
    
    if user_id not in usuarios:
        usuarios[user_id] = {
            'nome': nome,
            'saldo': 0.0,
            'convidados': [],
            'data_cadastro': datetime.now().strftime('%d/%m/%Y'),
            'link_convite': f'https://t.me/{bot.get_me().username}?start=convite_{user_id}'
        }
    
    bot.reply_to(message, f"✅ Cadastro criado, {nome}!\nUse /meusdados para ver seu saldo.")

@bot.message_handler(commands=['meusdados'])
def meus_dados(message):
    user_id = str(message.from_user.id)
    
    if user_id not in usuarios:
        bot.reply_to(message, "Use /start primeiro!")
        return
    
    user = usuarios[user_id]
    bot.reply_to(message, f"👤 {user['nome']}\n💰 Saldo: R$ {user['saldo']:.2f}\n👥 Indicados: {len(user['convidados'])}")

@bot.message_handler(commands=['regras'])
def regras(message):
    bot.reply_to(message, f"💰 R$ 1,00 por indicado\n💵 Saque mínimo: R$ 15,00\n❌ Se sair do grupo, perde o crédito")

@bot.message_handler(commands=['grupo'])
def grupo(message):
    bot.reply_to(message, f"🎯 Grupo: {GRUPO_LINK}")

print("Bot iniciado!")
bot.infinity_polling()
