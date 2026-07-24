import telebot
from datetime import datetime

TOKEN = '8771309444:AAE522egqaCOPGaAZUqDCB-6zY6uK-y1lhg'
GRUPO_LINK = 'https://t.me/pitbullslotsofc'
VALOR_POR_CONVIDADO = 1.00
VALOR_MINIMO_SAQUE = 15.00

bot = telebot.TeleBot(TOKEN)

usuarios = {}
convidados_registrados = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    nome = message.from_user.first_name
    
    args = message.text.split()
    if len(args) > 1 and args[1].startswith('convite_'):
        inviter_id = args[1].replace('convite_', '')
        
        if inviter_id != user_id and inviter_id in usuarios:
            convidados_registrados[user_id] = inviter_id
            
            if user_id not in usuarios[inviter_id]['convidados']:
                usuarios[inviter_id]['convidados'].append(user_id)
                usuarios[inviter_id]['saldo'] += VALOR_POR_CONVIDADO
                
                try:
                    bot.send_message(
                        inviter_id,
                        f"✅ *Novo indicado!*\n👤 {nome}\n💰 +R$ {VALOR_POR_CONVIDADO:.2f}\n💵 Saldo: R$ {usuarios[inviter_id]['saldo']:.2f}",
                        parse_mode='Markdown'
                    )
                except:
                    pass
    
    if user_id not in usuarios:
        usuarios[user_id] = {
            'nome': nome,
            'saldo': 0.0,
            'convidados': [],
            'data_cadastro': datetime.now().strftime('%d/%m/%Y'),
            'link_convite': f'https://t.me/{bot.get_me().username}?start=convite_{user_id}'
        }
    
    texto = f"""
✨ *PROGRAMA DE RECOMPENSAS* ✨

👋 *{nome}*

💰 R$ {VALOR_POR_CONVIDADO:.2f} por indicado
💵 Saque minimo: R$ {VALOR_MINIMO_SAQUE:.2f}

🔗 Seu link:
{usuarios[user_id]['link_convite']}

📊 /meusdados - Saldo
📋 /regras - Regras
🏦 /saque - Sacar
"""
    bot.reply_to(message, texto, parse_mode='Markdown')

@bot.message_handler(commands=['meusdados'])
def meus_dados(message):
    user_id = str(message.from_user.id)
    
    if user_id not in usuarios:
        bot.reply_to(message, "Use /start primeiro!")
        return
    
    user = usuarios[user_id]
    
    texto = f"""
📊 *SEUS DADOS*

👤 {user['nome']}
📅 {user['data_cadastro']}
💰 Saldo: R$ {user['saldo']:.2f}
👥 Indicados: {len(user['convidados'])}
"""
    if user['saldo'] >= VALOR_MINIMO_SAQUE:
        texto += "\n✅ Voce ja pode sacar! Use /saque"
    else:
        falta = VALOR_MINIMO_SAQUE - user['saldo']
        texto += f"\n⏳ Faltam R$ {falta:.2f} para sacar"
    
    bot.reply_to(message, texto, parse_mode='Markdown')

@bot.message_handler(commands=['saque'])
def saque(message):
    user_id = str(message.from_user.id)
    
    if user_id not in usuarios:
        bot.reply_to(message, "Use /start primeiro!")
        return
    
    user = usuarios[user_id]
    
    if user['saldo'] < VALOR_MINIMO_SAQUE:
        falta = VALOR_MINIMO_SAQUE - user['saldo']
        bot.reply_to(message, f"❌ Saldo insuficiente!\n💰 R$ {user['saldo']:.2f}\n⏳ Faltam R$ {falta:.2f}")
        return
    
    bot.reply_to(message, f"✅ Solicitacao enviada!\n💰 Valor: R$ {user['saldo']:.2f}\nUm admin entrara em contato.")

@bot.message_handler(commands=['regras'])
def regras(message):
    bot.reply_to(message, f"""
📋 REGRAS:
• R$ {VALOR_POR_CONVIDADO:.2f} por indicado
• Minimo saque: R$ {VALOR_MINIMO_SAQUE:.2f}
• Indicado deve ficar no grupo
• Se sair, perde o credito ❌
""")

@bot.message_handler(commands=['grupo'])
def grupo(message):
    bot.reply_to(message, f"🎯 {GRUPO_LINK}")

print("Bot iniciado!")
bot.infinity_polling()
