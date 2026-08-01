"""
==================================================
PITBULL REWARDS PLATFORM V3
DATABASE OFICIAL
==================================================
"""

import sqlite3
from datetime import datetime

from config import DATABASE

# ==================================================
# CONEXÃO
# ==================================================

conn = sqlite3.connect(
    DATABASE,
    check_same_thread=False
)

conn.row_factory = sqlite3.Row

cursor = conn.cursor()

# ==================================================
# DATA/HORA
# ==================================================

def agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# ==================================================
# CONFIGURAÇÕES
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS configuracoes(

    chave TEXT PRIMARY KEY,

    valor TEXT,

    descricao TEXT,

    categoria TEXT,

    updated_at TEXT

)
""")

CONFIG_PADRAO = {

    "nome_plataforma":"PITBULL REWARDS PLATFORM",

    "versao":"3.0",

    "grupo_id":"",

    "grupo_link":"",

    "grupo_nome":"",

    "grupo_obrigatorio":"1",

    "canal_id":"",

    "canal_link":"",

    "canal_nome":"",

    "canal_obrigatorio":"0",

    "valor_indicacao":"1.00",

    "valor_minimo_saque":"20",

    "valor_maximo_saque":"5000",

    "saque_manual":"1",

    "pix_obrigatorio":"1",

    "premium_ativo":"1",

    "vip_ativo":"1",

    "broadcast_ativo":"1",

    "tickets_ativo":"1",

    "anti_fraude":"1"

}

for chave, valor in CONFIG_PADRAO.items():

    cursor.execute("""

    INSERT OR IGNORE INTO configuracoes(

        chave,

        valor,

        descricao,

        categoria,

        updated_at

    )

    VALUES(?,?,?,?,?)

    """,(

        chave,

        valor,

        "",

        "GERAL",

        agora()

    ))

# ==================================================
# USUÁRIOS
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(

    id INTEGER PRIMARY KEY,

    codigo TEXT UNIQUE,

    nome TEXT,

    username TEXT,

    idioma TEXT DEFAULT 'pt-BR',

    status TEXT DEFAULT 'ATIVO',

    bloqueado INTEGER DEFAULT 0,

    banido INTEGER DEFAULT 0,

    aprovado INTEGER DEFAULT 0,

    grupo_verificado INTEGER DEFAULT 0,

    canal_verificado INTEGER DEFAULT 0,

    convidado_por INTEGER,

    indicados INTEGER DEFAULT 0,

    indicacoes_pendentes INTEGER DEFAULT 0,

    indicacoes_aprovadas INTEGER DEFAULT 0,

    indicacoes_rejeitadas INTEGER DEFAULT 0,

    saldo REAL DEFAULT 0,

    saldo_pendente REAL DEFAULT 0,

    saldo_bloqueado REAL DEFAULT 0,

    total_ganho REAL DEFAULT 0,

    total_sacado REAL DEFAULT 0,

    total_indicacoes REAL DEFAULT 0,

    pix TEXT,

    xp INTEGER DEFAULT 0,

    nivel INTEGER DEFAULT 1,

    vip TEXT DEFAULT 'Bronze',

    premium INTEGER DEFAULT 0,

    premium_expira TEXT,

    premium_multiplicador REAL DEFAULT 1,

    streak INTEGER DEFAULT 0,

    ultimo_bonus TEXT,

    ultima_roleta TEXT,

    ultima_raspadinha TEXT,

    ultimo_login TEXT,

    ultimo_ip TEXT,

    ultimo_dispositivo TEXT,

    tickets_abertos INTEGER DEFAULT 0,

    notificacoes INTEGER DEFAULT 1,

    inventario INTEGER DEFAULT 0,

    baus INTEGER DEFAULT 0,

    jackpot INTEGER DEFAULT 0,

    criado_por_admin INTEGER DEFAULT 0,

    created_at TEXT,

    updated_at TEXT

)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_codigo
ON usuarios(codigo)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_indicador
ON usuarios(convidado_por)
""")

conn.commit()

print("✅ Database carregado com sucesso.")
