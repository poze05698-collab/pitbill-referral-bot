import telebot
from telebot import types

# ========== CONFIGURAÇÃO ==========
TOKEN = '8771309444:AAE522egqaCOPGaAZUqDCB-6zY6uK-y1lhg'  # Vamos trocar depois
bot = telebot.TeleBot(TOKEN)

# Banco de dados simples (dicionário)
usuarios = {}

# Recompensas por número de convites
RECOMPENSAS = {
    5: "🌟 Bronze - Acesso ao grupo VIP",
    10: "⭐ Prata - 50 moedas",
    25: "💫 Ouro - 100 moedas",
    50: "👑 Elite - Cargo especial",
    100: "🔥 Lendário - Prêmio surpresa"
}

# ========== COMANDOS ==========

@bot.message_handler(commands=['start'])
def comando_start(message):
    user_id = str(message.from_user.id)
    nome = message.from_user.first_name
    
    # Verifica se foi convidado por alguém
    if len(message.text.split()) > 1:
        codigo = message.text.split()[1]
        if codigo.startswith('convite_'):
            inviter_id = codigo.replace('convite_', '')
            adicionar_convite(inviter_id, user_id)
    
    # Cria usuário se não existir
    if user_id not in usuarios:
        usuarios[user_id] = {
            'nome': nome,
            'convites': 0,
            'moedas': 0,
            'link': f'https://t.me/{bot.get_me().username}?start=convite_{user_id}'
        }
    
    texto = f"""
👋 *Olá, {nome}!*

📨 *Ganhe recompensas convidando amigos!*

🔗 *Seu link de convite:*
{usuarios[user_id]['link']}

📊 *Comandos disponíveis:*
/meusdados - Ver suas estatísticas
/ranking - Top convidadores
/recompensas - Lista de prêmios

⚡ *Compartilhe seu link e ganhe!*
"""
    bot.reply_to(message, texto, parse_mode='Markdown')

@bot.message_handler(commands=['meusdados'])
def comando_meus_dados(message):
    user_id = str(message.from_user.id)
    
    if user_id not in usuarios:
        bot.reply_to(message, "❌ Use /start primeiro!")
        return
    
    user = usuarios[user_id]
    
    # Verifica próxima recompensa
    proxima = None
    for convites, recompensa in sorted(RECOMPSENSAS.items()):
        if user['convites'] < convites:
            proxima = (convites, recompensa)
            break
    
    texto = f"""
📊 *Seus Dados*

👤 Nome: {user['nome']}
📨 Convites: {user['convites']}
🪙 Moedas: {user['moedas']}

🔗 Seu link:
{user['link']}
"""
    
    if proxima:
        faltam = proxima[0] - user['convites']
        texto += f"\n🎯 Próxima recompensa: *{proxima[1]}*\n📌 Faltam: *{faltam}* convites"
    
    bot.reply_to(message, texto, parse_mode='Markdown')

@bot.message_handler(commands=['ranking'])
def comando_ranking(message):
    if not usuarios:
        bot.reply_to(message, "📊 Nenhum convite ainda!")
        return
    
    ranking = sorted(usuarios.items(), key=lambda x: x[1]['convites'], reverse=True)[:10]
    
    texto = "🏆 *TOP 10 CONVIDADORES*\n\n"
    medalhas = ['🥇', '🥈', '🥉']
    
    for i, (uid, user) in enumerate(ranking):
        medalha = medalhas[i] if i < 3 else f"{i+1}º"
        texto += f"{medalha} {user['nome']}: {user['convites']} convites\n"
    
    bot.reply_to(message, texto, parse_mode='Markdown')

@bot.message_handler(commands=['recompensas'])
def comando_recompensas(message):
    texto = "🎁 *RECOMPENSAS*\n\n"
    
    for convites, recompensa in sorted(RECOMPSENSAS.items()):
        texto += f"📨 *{convites} convites* → {recompensa}\n"
    
    bot.reply_to(message, texto, parse_mode='Markdown')

# ========== FUNÇÕES ==========

def adicionar_convite(inviter_id, new_user_id):
    if inviter_id in usuarios and inviter_id != new_user_id:
        usuarios[inviter_id]['convites'] += 1
        usuarios[inviter_id]['moedas'] += 10
        
        # Verifica recompensas
        convites = usuarios[inviter_id]['convites']
        if convites in RECOMPENSAS:
            try:
                bot.send_message(
                    inviter_id,
                    f"🎉 *Parabéns!*\nVocê atingiu {convites} convites!\nRecompensa: *{RECOMPENSAS[convites]}*",
                    parse_mode='Markdown'
                )
            except:
                pass

# ========== INICIAR BOT ==========
print("🤖 Bot iniciado!")
bot.infinity_polling()
