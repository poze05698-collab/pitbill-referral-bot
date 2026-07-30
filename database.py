"""
=========================================
 PITBULL REWARDS PLATFORM V2
 Database V2.1
=========================================
"""

import sqlite3
from datetime import datetime

from config import DATABASE

# =====================================================
# CONEXÃO
# =====================================================

conn = sqlite3.connect(
    DATABASE,
    check_same_thread=False,
    timeout=30
)

# Ativar Foreign Keys
conn.execute("PRAGMA foreign_keys = ON")

conn.row_factory = sqlite3.Row

cursor = conn.cursor()

# =====================================================
# DATA/HORA
# =====================================================

def agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# =====================================================
# SYSTEM
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS system(

    id INTEGER PRIMARY KEY,

    bot_version TEXT NOT NULL,

    database_version TEXT NOT NULL,

    maintenance INTEGER DEFAULT 0,

    emergency INTEGER DEFAULT 0,

    last_update TEXT,

    created_at TEXT

)
""")

# =====================================================
# CONFIGURAÇÕES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS configuracoes(

    chave TEXT PRIMARY KEY,

    valor TEXT NOT NULL

)
""")

# =====================================================
# ADMINS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins(

    id INTEGER PRIMARY KEY,

    cargo TEXT NOT NULL,

    ativo INTEGER DEFAULT 1,

    criado_por INTEGER,

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

    nome TEXT NOT NULL,

    username TEXT,

    idioma TEXT DEFAULT 'pt',

    foto TEXT,

    email TEXT,

    telefone TEXT,

    saldo REAL DEFAULT 0,

    saldo_pendente REAL DEFAULT 0,

    saldo_bloqueado REAL DEFAULT 0,

    total_ganho REAL DEFAULT 0,

    total_sacado REAL DEFAULT 0,

    xp INTEGER DEFAULT 0,

    nivel INTEGER DEFAULT 1,

    vip TEXT DEFAULT 'Bronze',

    trust_score INTEGER DEFAULT 100,

    indicados INTEGER DEFAULT 0,

    indicacoes_pendentes INTEGER DEFAULT 0,

    indicacoes_aprovadas INTEGER DEFAULT 0,

    indicacoes_rejeitadas INTEGER DEFAULT 0,

    convidado_por INTEGER,

    streak INTEGER DEFAULT 0,

    ultimo_bonus TEXT,

    ultima_roleta TEXT,

    ultima_raspadinha TEXT,

    ultimo_login TEXT,

    ultima_atividade TEXT,

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

    indicador INTEGER NOT NULL,

    indicado INTEGER UNIQUE NOT NULL,

    valor REAL DEFAULT 0,

    status TEXT DEFAULT 'PENDENTE',

    aprovado_por INTEGER,

    motivo_rejeicao TEXT,

    created_at TEXT,

    approved_at TEXT,

    FOREIGN KEY(indicador) REFERENCES usuarios(id),

    FOREIGN KEY(indicado) REFERENCES usuarios(id)

)
""")

# =====================================================
# CARTEIRA
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS wallet(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER NOT NULL,

    tipo TEXT,

    origem TEXT,

    valor REAL,

    saldo_anterior REAL,

    saldo_atual REAL,

    status TEXT,

    descricao TEXT,

    observacao TEXT,

    referencia TEXT,

    admin_id INTEGER,

    created_at TEXT,

    FOREIGN KEY(usuario) REFERENCES usuarios(id)

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

    updated_at TEXT,

    FOREIGN KEY(usuario) REFERENCES usuarios(id)

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

    status TEXT DEFAULT 'PENDENTE',

    aprovado_por INTEGER,

    comprovante TEXT,

    observacao TEXT,

    created_at TEXT,

    updated_at TEXT,

    FOREIGN KEY(usuario) REFERENCES usuarios(id)

)
""")# =====================================================
# HISTÓRICO
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS historico(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER NOT NULL,

    categoria TEXT,

    titulo TEXT,

    descricao TEXT,

    referencia TEXT,

    created_at TEXT,

    FOREIGN KEY(usuario) REFERENCES usuarios(id)

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

    created_at TEXT,

    FOREIGN KEY(admin) REFERENCES admins(id),

    FOREIGN KEY(usuario) REFERENCES usuarios(id)

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

    created_at TEXT,

    FOREIGN KEY(usuario) REFERENCES usuarios(id)

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

    prioridade TEXT DEFAULT 'NORMAL',

    atendente INTEGER,

    fechado_por INTEGER,

    fechado_em TEXT,

    created_at TEXT,

    updated_at TEXT,

    FOREIGN KEY(usuario) REFERENCES usuarios(id),

    FOREIGN KEY(atendente) REFERENCES admins(id)

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

    created_at TEXT,

    FOREIGN KEY(ticket) REFERENCES tickets(id)

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

    created_at TEXT,

    FOREIGN KEY(usuario) REFERENCES usuarios(id),

    FOREIGN KEY(admin) REFERENCES admins(id)

)
""")

# =====================================================
# FINANCEIRO
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS financeiro(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    categoria TEXT,

    origem TEXT,

    referencia TEXT,

    valor REAL,

    saldo REAL,

    created_at TEXT,

    FOREIGN KEY(usuario) REFERENCES usuarios(id)

)
""")

# =====================================================
# ESTATÍSTICAS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS estatisticas(

    usuario INTEGER PRIMARY KEY,

    logins INTEGER DEFAULT 0,

    convites INTEGER DEFAULT 0,

    saques INTEGER DEFAULT 0,

    tickets INTEGER DEFAULT 0,

    roletas INTEGER DEFAULT 0,

    raspadinhas INTEGER DEFAULT 0,

    missoes INTEGER DEFAULT 0,

    FOREIGN KEY(usuario) REFERENCES usuarios(id)

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

    created_at TEXT,

    FOREIGN KEY(usuario) REFERENCES usuarios(id)

)
""")# =====================================================
# VIP
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS vip(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT UNIQUE,

    minimo_indicados INTEGER DEFAULT 0,

    bonus_indicacao REAL DEFAULT 1.00,

    bonus_bonus_diario REAL DEFAULT 0,

    giros INTEGER DEFAULT 0,

    raspadinhas INTEGER DEFAULT 0,

    prioridade_saque INTEGER DEFAULT 0,

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

    updated_at TEXT,

    FOREIGN KEY(usuario) REFERENCES usuarios(id)

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

    tipo TEXT,

    objetivo INTEGER,

    recompensa REAL,

    xp INTEGER,

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

    recompensa_recebida INTEGER DEFAULT 0,

    created_at TEXT,

    FOREIGN KEY(usuario) REFERENCES usuarios(id),

    FOREIGN KEY(missao) REFERENCES missoes(id)

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

    recompensa REAL,

    xp INTEGER,

    inicio TEXT,

    fim TEXT,

    ativo INTEGER DEFAULT 0

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

    tipo TEXT,

    preco REAL,

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

    xp INTEGER DEFAULT 0,

    limite INTEGER,

    utilizados INTEGER DEFAULT 0,

    ativo INTEGER DEFAULT 1

)
""")

# =====================================================
# INVENTÁRIO
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventario(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    item TEXT,

    quantidade INTEGER DEFAULT 0,

    created_at TEXT,

    updated_at TEXT,

    FOREIGN KEY(usuario) REFERENCES usuarios(id)

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
# CONQUISTAS DOS USUÁRIOS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuario_conquistas(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    conquista INTEGER,

    created_at TEXT,

    FOREIGN KEY(usuario) REFERENCES usuarios(id),

    FOREIGN KEY(conquista) REFERENCES conquistas(id)

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

    principal INTEGER DEFAULT 0,

    ativo INTEGER DEFAULT 1,

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

    principal INTEGER DEFAULT 0,

    ativo INTEGER DEFAULT 1,

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
# VERSÕES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS versoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    versao TEXT,

    descricao TEXT,

    data TEXT

)
""")# =====================================================
# ÍNDICES
# =====================================================

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_usuario_id
ON usuarios(id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_usuario_username
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
CREATE INDEX IF NOT EXISTS idx_pix_usuario
ON pix(usuario)
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
CREATE INDEX IF NOT EXISTS idx_notificacao_usuario
ON notificacoes(usuario)
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

    (chave,valor)

    VALUES(?,?)

    """,(chave,valor))

# =====================================================
# SYSTEM PADRÃO
# =====================================================

cursor.execute("""

INSERT OR IGNORE INTO system(

id,

bot_version,

database_version,

maintenance,

emergency,

last_update,

created_at

)

VALUES(

1,

'2.1',

'2.1',

0,

0,

?,

?

)

""",(agora(),agora()))

# =====================================================
# VIP PADRÃO
# =====================================================

vip_padrao=[

("Bronze",0,1.00,0,1,1,0),

("Prata",25,1.20,5,2,2,0),

("Ouro",75,1.50,10,3,3,1),

("Diamante",150,2.00,20,4,4,1),

("Lendário",500,3.00,30,5,5,1)

]

for vip in vip_padrao:

    cursor.execute("""

    INSERT OR IGNORE INTO vip(

    nome,

    minimo_indicados,

    bonus_indicacao,

    bonus_bonus_diario,

    giros,

    raspadinhas,

    prioridade_saque,

    created_at

    )

    VALUES(?,?,?,?,?,?,?,?)

    """,(

    vip[0],

    vip[1],

    vip[2],

    vip[3],

    vip[4],

    vip[5],

    vip[6],

    agora()

    ))

# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================

def execute(sql, params=()):

    cursor.execute(sql, params)

    conn.commit()


def fetchone(sql, params=()):

    cursor.execute(sql, params)

    return cursor.fetchone()


def fetchall(sql, params=()):

    cursor.execute(sql, params)

    return cursor.fetchall()


def get_config(chave):

    cursor.execute(

        "SELECT valor FROM configuracoes WHERE chave=?",

        (chave,)

    )

    resultado=cursor.fetchone()

    if resultado:

        return resultado["valor"]

    return None


def set_config(chave, valor):

    cursor.execute("""

    UPDATE configuracoes

    SET valor=?

    WHERE chave=?

    """,(str(valor),chave))

    conn.commit()

# =====================================================
# FINALIZAÇÃO
# =====================================================

conn.commit()

print("="*50)
print(" PITBULL REWARDS PLATFORM V2.1 ")
print(" Database carregado com sucesso.")
print("="*50)
