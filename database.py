"""
=========================================
 PITBULL REFERRAL BOT V2
 Banco de Dados
=========================================
"""

import sqlite3

from config import DATABASE

# Conexão com o banco
conn = sqlite3.connect(DATABASE, check_same_thread=False)
cursor = conn.cursor()


# ===========================
# TABELA USUÁRIOS
# ===========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (

    id INTEGER PRIMARY KEY,

    nome TEXT,

    username TEXT,

    saldo REAL DEFAULT 0,

    pix TEXT DEFAULT '',

    indicados INTEGER DEFAULT 0,

    convidado_por INTEGER,

    data_cadastro TEXT

)
""")


# ===========================
# TABELA SAQUES
# ===========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS saques (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    valor REAL,

    pix TEXT,

    status TEXT,

    data TEXT

)
""")


# ===========================
# TABELA INDICAÇÕES
# ===========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS indicacoes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    indicador INTEGER,

    indicado INTEGER,

    recompensa REAL,

    data TEXT

)
""")


conn.commit()
