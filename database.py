"""
=========================================
 PITBULL REWARDS PLATFORM V2
 Database
=========================================
"""

import sqlite3
from datetime import datetime

from config import DATABASE

# =====================================================
# CONEXÃO
# =====================================================

conn = sqlite3.connect(DATABASE, check_same_thread=False)
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

# =====================================================
# TABELA SYSTEM
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS system(

    id INTEGER PRIMARY KEY,

    bot_version TEXT,
    database_version TEXT,

    maintenance INTEGER DEFAULT 0,
    emergency INTEGER DEFAULT 0,

    created_at TEXT

)
""")

# =====================================================
# CONFIGURAÇÕES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS configuracoes(

    chave TEXT PRIMARY KEY,

    valor TEXT

)
""")

# =====================================================
# ADMINS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins(

    id INTEGER PRIMARY KEY,

    cargo TEXT,

    ativo INTEGER DEFAULT 1,

    created_at TEXT

)
""")

# =====================================================
# USUÁRIOS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(

    id INTEGER PRIMARY KEY,

    codigo TEXT UNIQUE,

    nome TEXT,

    username TEXT,

    idioma TEXT DEFAULT 'pt',

    saldo REAL DEFAULT 0,

    saldo_pendente REAL DEFAULT 0,

    saldo_bloqueado REAL DEFAULT 0,

    total_ganho REAL DEFAULT 0,

    total_sacado REAL DEFAULT 0,

    xp INTEGER DEFAULT 0,

    nivel INTEGER DEFAULT 1,

    vip TEXT DEFAULT 'Bronze',

    indicados INTEGER DEFAULT 0,

    indicacoes_pendentes INTEGER DEFAULT 0,

    indicacoes_aprovadas INTEGER DEFAULT 0,

    indicacoes_rejeitadas INTEGER DEFAULT 0,

    convidado_por INTEGER,

    streak INTEGER DEFAULT 0,

    ultimo_bonus TEXT,

    ultima_roleta TEXT,

    ultima_raspadinha TEXT,

    status TEXT DEFAULT 'ATIVO',

    is_admin INTEGER DEFAULT 0,

    banido INTEGER DEFAULT 0,

    motivo_ban TEXT,

    created_at TEXT,

    updated_at TEXT

)
""")

# =====================================================
# INDICAÇÕES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS indicacoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    indicador INTEGER,

    indicado INTEGER UNIQUE,

    valor REAL,

    status TEXT,

    aprovado_por INTEGER,

    motivo_rejeicao TEXT,

    created_at TEXT,

    approved_at TEXT

)
""")

# =====================================================
# CARTEIRA
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS wallet(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    tipo TEXT,

    valor REAL,

    saldo_anterior REAL,

    saldo_atual REAL,

    status TEXT,

    descricao TEXT,

    referencia TEXT,

    admin_id INTEGER,

    created_at TEXT

)
""")

# =====================================================
# PIX
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS pix(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER UNIQUE,

    tipo TEXT,

    chave TEXT,

    nome TEXT,

    documento TEXT,

    status TEXT DEFAULT 'ATIVO',

    created_at TEXT,

    updated_at TEXT

)
""")

# =====================================================
# SAQUES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS saques(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    valor REAL,

    taxa REAL DEFAULT 0,

    pix TEXT,

    status TEXT,

    aprovado_por INTEGER,

    comprovante TEXT,

    observacao TEXT,

    created_at TEXT,

    updated_at TEXT

)
""")# =====================================================
# HISTÓRICO
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS historico(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    categoria TEXT,

    titulo TEXT,

    descricao TEXT,

    referencia TEXT,

    created_at TEXT

)
""")

# =====================================================
# LOGS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    admin INTEGER,

    tipo TEXT,

    acao TEXT,

    usuario INTEGER,

    detalhes TEXT,

    ip TEXT,

    created_at TEXT

)
""")

# =====================================================
# TICKETS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    categoria TEXT,

    assunto TEXT,

    status TEXT DEFAULT 'ABERTO',

    atendente INTEGER,

    prioridade TEXT DEFAULT 'NORMAL',

    created_at TEXT,

    updated_at TEXT

)
""")

# =====================================================
# MENSAGENS DOS TICKETS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS ticket_mensagens(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    ticket INTEGER,

    remetente INTEGER,

    tipo TEXT,

    mensagem TEXT,

    created_at TEXT

)
""")

# =====================================================
# NOTIFICAÇÕES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS notificacoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    titulo TEXT,

    mensagem TEXT,

    lida INTEGER DEFAULT 0,

    created_at TEXT

)
""")

# =====================================================
# BLACKLIST
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS blacklist(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER UNIQUE,

    motivo TEXT,

    admin INTEGER,

    created_at TEXT

)
""")

# =====================================================
# FINANCEIRO
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS financeiro(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    tipo TEXT,

    origem TEXT,

    referencia TEXT,

    valor REAL,

    saldo REAL,

    created_at TEXT

)
""")

# =====================================================
# GRUPOS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS grupos(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,

    telegram_id TEXT,

    link TEXT,

    ativo INTEGER DEFAULT 1,

    principal INTEGER DEFAULT 0,

    created_at TEXT

)
""")

# =====================================================
# CANAIS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS canais(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,

    telegram_id TEXT,

    link TEXT,

    ativo INTEGER DEFAULT 1,

    principal INTEGER DEFAULT 0,

    created_at TEXT

)
""")

# =====================================================
# RANKING
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS ranking(

    usuario INTEGER PRIMARY KEY,

    pontos INTEGER DEFAULT 0,

    posicao INTEGER DEFAULT 0,

    updated_at TEXT

)
""")

# =====================================================
# VIP
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS vip(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT UNIQUE,

    minimo_indicados INTEGER,

    bonus_indicacao REAL,

    giros INTEGER,

    raspadinhas INTEGER,

    created_at TEXT

)
""")

# =====================================================
# MISSÕES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS missoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    titulo TEXT,

    descricao TEXT,

    recompensa REAL,

    xp INTEGER,

    tipo TEXT,

    ativa INTEGER DEFAULT 1

)
""")

# =====================================================
# MISSÕES DOS USUÁRIOS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS missoes_usuario(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    missao INTEGER,

    progresso INTEGER DEFAULT 0,

    concluida INTEGER DEFAULT 0,

    created_at TEXT

)
""")

# =====================================================
# EVENTOS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS eventos(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,

    descricao TEXT,

    ativo INTEGER DEFAULT 0,

    inicio TEXT,

    fim TEXT

)
""")

# =====================================================
# LOJA
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS loja(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,

    descricao TEXT,

    preco REAL,

    tipo TEXT,

    quantidade INTEGER DEFAULT 0,

    ativo INTEGER DEFAULT 1

)
""")

# =====================================================
# CUPÕES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS cupons(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    codigo TEXT UNIQUE,

    recompensa REAL,

    limite INTEGER,

    utilizados INTEGER DEFAULT 0,

    ativo INTEGER DEFAULT 1

)
""")# =====================================================
# ÍNDICES (Performance)
# =====================================================

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_usuario
ON usuarios(id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_username
ON usuarios(username)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_indicador
ON indicacoes(indicador)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_indicado
ON indicacoes(indicado)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_wallet_usuario
ON wallet(usuario)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_saque_usuario
ON saques(usuario)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_ticket_usuario
ON tickets(usuario)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_historico_usuario
ON historico(usuario)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_financeiro_usuario
ON financeiro(usuario)
""")

# =====================================================
# CONFIGURAÇÕES PADRÃO
# =====================================================

config_padrao = {

    "grupo_obrigatorio": "1",
    "canal_obrigatorio": "0",

    "valor_indicacao": "1.00",

    "valor_minimo_saque": "20.00",

    "valor_maximo_saque": "1000.00",

    "ticket_ativo": "1",

    "roleta_ativa": "1",

    "raspadinha_ativa": "1",

    "bonus_diario": "1",

    "evento_ativo": "0",

    "modo_manutencao": "0",

    "modo_emergencia": "0",

    "cadastro_liberado": "1",

    "saque_liberado": "1",

    "tickets_liberados": "1"

}

for chave, valor in config_padrao.items():

    cursor.execute("""

    INSERT OR IGNORE INTO configuracoes

    (chave, valor)

    VALUES (?,?)

    """, (chave, valor))

# =====================================================
# SYSTEM
# =====================================================

cursor.execute("""

INSERT OR IGNORE INTO system(

id,

bot_version,

database_version,

maintenance,

emergency,

created_at

)

VALUES(

1,

'2.0',

'2.0',

0,

0,

?

)

""", (datetime.now().strftime("%d/%m/%Y %H:%M:%S"),))

# =====================================================
# VIP PADRÃO
# =====================================================

vip_padrao = [

("Bronze",0,1.00,1,1),

("Prata",25,1.20,2,2),

("Ouro",75,1.50,3,3),

("Diamante",150,2.00,4,4),

("Lendário",500,3.00,5,5)

]

for nome,minimo,bonus,giros,raspadinhas in vip_padrao:

    cursor.execute("""

    INSERT OR IGNORE INTO vip(

    nome,

    minimo_indicados,

    bonus_indicacao,

    giros,

    raspadinhas,

    created_at

    )

    VALUES(?,?,?,?,?,?)

    """,(

    nome,

    minimo,

    bonus,

    giros,

    raspadinhas,

    datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    ))# =====================================================
# INVENTÁRIO
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventario(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    item TEXT,

    quantidade INTEGER DEFAULT 0,

    created_at TEXT,

    updated_at TEXT

)
""")

# =====================================================
# CONQUISTAS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS conquistas(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT UNIQUE,

    descricao TEXT,

    recompensa REAL,

    xp INTEGER,

    ativa INTEGER DEFAULT 1

)
""")

# =====================================================
# CONQUISTAS DO USUÁRIO
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuario_conquistas(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    conquista INTEGER,

    created_at TEXT
)
""")

# =====================================================
# ANÚNCIOS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS anuncios(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    titulo TEXT,

    mensagem TEXT,

    ativo INTEGER DEFAULT 1,

    created_at TEXT
)
""")

# =====================================================
# AUDITORIA
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS auditoria(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    modulo TEXT,

    acao TEXT,

    detalhes TEXT,

    created_at TEXT
)
""")

# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================

def execute(query, params=()):
    cursor.execute(query, params)
    conn.commit()


def fetchone(query, params=()):
    cursor.execute(query, params)
    return cursor.fetchone()


def fetchall(query, params=()):
    cursor.execute(query, params)
    return cursor.fetchall()


def get_config(chave):

    cursor.execute(
        "SELECT valor FROM configuracoes WHERE chave=?",
        (chave,)
    )

    resultado = cursor.fetchone()

    if resultado:
        return resultado["valor"]

    return None


def set_config(chave, valor):

    cursor.execute("""

    UPDATE configuracoes

    SET valor=?

    WHERE chave=?

    """, (str(valor), chave))

    conn.commit()


# =====================================================
# COMMIT FINAL
# =====================================================

conn.commit()

print("✅ Database V2 carregado com sucesso.")
