"""
=========================================
 PITBULL REFERRAL BOT V2
 Inicialização do Bot
=========================================
"""

import telebot

from config import TOKEN

# Cria o bot
bot = telebot.TeleBot(
    TOKEN,
    parse_mode="HTML"
)
