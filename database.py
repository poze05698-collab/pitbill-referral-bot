"""
==================================================
PITBULL REWARDS PLATFORM V3
Database Oficial
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
# DATA / HORA
# ==================================================

def agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# ==================================================
# SYSTEM
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS system(

    id INTEGER PRIMARY KEY,

    plataforma TEXT,

    versao TEXT,

    database_versao TEXT,

    owner_id INTEGER DEFAULT 0,

    maintenance INTEGER DEFAULT 0,

    emergency INTEGER DEFAULT 0,

    created_at TEXT,

    updated_at TEXT

)
""")


# ==================================================
# MÓDULOS
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS modulos(

    chave TEXT PRIMARY KEY,

    nome TEXT,

    descricao TEXT,

    ativo INTEGER DEFAULT 1,

    editavel INTEGER DEFAULT 1,

    created_at TEXT,

    updated_at TEXT

)
""")


# ==================================================
# CONFIGURAÇÕES
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS configuracoes(

    chave TEXT PRIMARY KEY,

    valor TEXT,

    descricao TEXT,

    categoria TEXT,

    editavel INTEGER DEFAULT 1,

    updated_at TEXT

)
""")


# ==================================================
# CONFIGURAÇÕES PADRÃO
# ==================================================

CONFIG_PADRAO = {

    "nome_plataforma": "PITBULL REWARDS PLATFORM",

    "versao": "3.0",

    "grupo_obrigatorio": "1",

    "grupo_id": "",

    "grupo_nome": "",

    "grupo_link": "",

    "canal_obrigatorio": "0",

    "canal_id": "",

    "canal_nome": "",

    "canal_link": "",

    "valor_indicacao": "1.00",

    "valor_minimo_saque": "20.00",

    "valor_maximo_saque": "5000.00",

    "pix_obrigatorio": "1",

    "saque_manual": "1",

    "aprovacao_manual": "1",

    "premium_ativo": "0",

    "vip_ativo": "1",

    "broadcast_ativo": "1",

    "tickets_ativos": "1",

    "logs_admin": "1"

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

    """, (

        chave,

        valor,

        "",

        "GERAL",

        agora()

    ))

conn.commit()# ==================================================
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

    grupo_verificado INTEGER DEFAULT 0,

    canal_verificado INTEGER DEFAULT 0,

    aprovado INTEGER DEFAULT 0,

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

    experiencia_total INTEGER DEFAULT 0,

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


# ==================================================
# ADMINISTRADORES
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS administradores(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER UNIQUE,

    cargo TEXT NOT NULL,

    status TEXT DEFAULT 'ATIVO',

    criado_por INTEGER,

    created_at TEXT,

    updated_at TEXT

)
""")


# ==================================================
# PERMISSÕES DOS ADMINS
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS permissoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    admin_id INTEGER,

    permissao TEXT,

    permitido INTEGER DEFAULT 1,

    created_at TEXT

)
""")


# ==================================================
# LOGS ADMINISTRATIVOS
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs_admin(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    admin_id INTEGER,

    acao TEXT,

    categoria TEXT,

    usuario_alvo INTEGER,

    referencia TEXT,

    detalhes TEXT,

    created_at TEXT

)
""")


# ==================================================
# ÍNDICES
# ==================================================

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_usuario_codigo
ON usuarios(codigo)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_usuario_indicador
ON usuarios(convidado_por)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_usuario_status
ON usuarios(status)
""")

conn.commit()
