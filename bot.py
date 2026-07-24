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
                        f"✅ *Novo indicado!*\n\n👤 {nome} entrou pelo seu link!\n💰 Você ganhou: R$ {VALOR_POR_CONVIDADO:.2f}\n💵 Saldo atual: R$ {usuarios[inviter_id]['saldo']:.2f}",
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

👋 Olá, *{nome}*!

💰 Ganhe *R$ {VALOR_POR_CONVIDADO:.2f}* para cada pessoa que entrar no grupo pelo seu link!

━━━━━━━━━━━━━━━

🔗 *Seu link de indicacao:*
{usuarios[user_id]['link_convite']}

━━━━━━━━━━━━━━━

📋 *Regras:*
• Minimo para saque: *R$ {VALOR_MINIMO_SAQUE:.2f}*
• Indicado deve permanecer no grupo
• Se sair, o credito e cancelado ❌

━━━━━━━━━━━━━━━

📊 *Comandos:*
/meusdados - Seu saldo e indicados
/saque - Solicitar saque
/regras - Ver regras completas
/grupo - Link do grupo

⚡ *Compartilhe seu link e ganhe dinheiro!*
"""
    bot.reply_to(message, texto, parse_mode='Markdown')

@bot.message_handler(commands=['meusdados'])
def meus_dados(message):
    user_id = str(message.from_user.id)
    
    if user_id not in usuarios:
        bot.reply_to(message, "❌ Use /start primeiro!")
        return
    
    user = usuarios[user_id]
    total_indicados = len(user['convidados'])
    
    texto = f"""
📊 *SEUS DADOS*

👤 Nome: *{user['nome']}*
📅 Cadastro: {user['data_cadastro']}

━━━━━━━━━━━━━━━

💰 *Saldo atual: R$ {user['saldo']:.2f}*
👥 Total de indicados: *{total_indicados}*

━━━━━━━━━━━━━━━

🔗 Seu link:
{user['link_convite']}
"""
    
    if user['saldo'] >= VALOR_MINIMO_SAQUE:
        texto += f"\n✅ Voce ja pode sacar! Use /saque"
    else:
        falta = VALOR_MINIMO_SAQUE - user['saldo']
        texto += f"\n⏳ Faltam R$ {falta:.2f} para o saque minimo"
    
    if user['convidados']:
        texto += "\n\n👥 *Ultimos indicados:*"
        for convidado_id in user['convidados'][-5:]:
            if convidado_id in usuarios:
                texto += f"\n• {usuarios[convidado_id]['nome']}"
    
    bot.reply_to(message, texto, parse_mode='Markdown')

@bot.message_handler(commands=['saque'])
def saque(message):
    user_id = str(message.from_user.id)
    
    if user_id not in usuarios:
        bot.reply_to(message, "❌ Use /start primeiro!")
        return
    
    user = usuarios[user_id]
    
    if user['saldo'] < VALOR_MINIMO_SAQUE:
        falta = VALOR_MINIMO_SAQUE - user['saldo']
        bot.reply_to(message, f"❌ Saldo insuficiente!\n\n💰 Seu saldo: R$ {user['saldo']:.2f}\n⏳ Faltam: R$ {falta:.2f}\n\nMinimo para saque: R$ {VALOR_MINIMO_SAQUE:.2f}")
        return
    
    texto = f"""
🏦 *SOLICITACAO DE SAQUE*

👤 Nome: {user['nome']}
💰 Valor: R$ {user['saldo']:.2f}
👥 Indicados: {len(user['convidados'])}

✅ Sua solicitacao foi enviada!Um administrador entrara em contato para realizar o pagamento.
"""
    bot.reply_to(message, texto, parse_mode='Markdown')

@bot.message_handler(commands=['regras'])
def regras(message):
    texto = f"""
📋 *REGRAS DO PROGRAMA*

━━━━━━━━━━━━━━━

1️⃣ Crie seu link exclusivo
2️⃣ Envie para amigos
3️⃣ Receba *R$ {VALOR_POR_CONVIDADO:.2f}* por indicado
4️⃣ Quando atingir *R$ {VALOR_MINIMO_SAQUE:.2f}*, solicite o saque

━━━━━━━━━━━━━━━

⚠️ *Regras importantes:*
• Valor minimo: *R$ {VALOR_MINIMO_SAQUE:.2f}*
• Indicado deve permanecer no grupo
• Se o convidado sair, o credito e cancelado ❌
• Nao e permitido convidar contas falsas

💡 *Dicas:*
• Divulgue em outros grupos
• Compartilhe nas redes sociais
• Incentive seus indicados a ficarem ativos
"""
    bot.reply_to(message, texto, parse_mode='Markdown')

@bot.message_handler(commands=['grupo'])
def grupo(message):
    texto = f"""
🎯 *GRUPO OFICIAL*

Entre no nosso grupo:
{GRUPO_LINK}

Compartilhe seu link de indicacao e ganhe dinheiro!
Use /start para gerar seu link.
"""
    bot.reply_to(message, texto, parse_mode='Markdown')

@bot.message_handler(content_types=['new_chat_members'])
def novo_membro(message):
    global GRUPO_ID
    GRUPO_ID = message.chat.id
    
    for member in message.new_chat_members:
        user_id = str(member.id)
        
        if user_id in convidados_registrados:
            inviter_id = convidados_registrados[user_id]
            
            if inviter_id in usuarios:
                try:
                    bot.send_message(
                        inviter_id,
                        f"✅ *{member.first_name}* entrou no grupo!\n💰 Credito de R$ {VALOR_POR_CONVIDADO:.2f} confirmado!",
                        parse_mode='Markdown'
                    )
                except:
                    pass

@bot.message_handler(content_types=['left_chat_member'])
def membro_saiu(message):
    user_id = str(message.left_chat_member.id)
    
    if user_id in convidados_registrados:
        inviter_id = convidados_registrados[user_id]
        
        if inviter_id in usuarios and user_id in usuarios[inviter_id]['convidados']:
            usuarios[inviter_id]['convidados'].remove(user_id)
            usuarios[inviter_id]['saldo'] -= VALOR_POR_CONVIDADO
            
            if usuarios[inviter_id]['saldo'] < 0:
                usuarios[inviter_id]['saldo'] = 0
            
            try:
                bot.send_message(
                    inviter_id,
                    f"❌ Um indicado saiu do grupo.\n💰 Seu saldo foi ajustado.\n💵 Saldo atual: R$ {usuarios[inviter_id]['saldo']:.2f}",
                    parse_mode='Markdown'
                )
            except:
                pass
            
            del convidados_registrados[user_id]

print("🤖 Bot iniciado!")
bot.infinity_polling()
