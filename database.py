import sqlite3

# ==========================================
# CONEXÃO
# ==========================================

conn = sqlite3.connect(
    "database.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ==========================================
# TABELA USUÁRIOS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(

    id INTEGER PRIMARY KEY,

    nome TEXT NOT NULL,

    username TEXT,

    saldo REAL DEFAULT 0,

    pix TEXT DEFAULT '',

    convidados INTEGER DEFAULT 0,

    convidado_por INTEGER,

    bloqueado INTEGER DEFAULT 0,

    admin INTEGER DEFAULT 0,

    data_cadastro TEXT,

    ultimo_acesso TEXT

)
""")

# ==========================================
# TABELA INDICAÇÕES
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS indicacoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    indicador INTEGER,

    indicado INTEGER,

    recompensa REAL,

    status TEXT,

    data TEXT

)
""")

# ==========================================
# TABELA SAQUES
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS saques(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    valor REAL,

    pix TEXT,

    status TEXT,

    data TEXT,

    aprovado_por INTEGER,

    data_aprovacao TEXT

)
""")

# ==========================================
# HISTÓRICO
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS historico(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    tipo TEXT,

    descricao TEXT,

    valor REAL,

    data TEXT

)
""")

# ==========================================
# LOGS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    acao TEXT,

    detalhes TEXT,

    data TEXT

)
""")

# ==========================================
# CONFIGURAÇÕES
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS configuracoes(

    chave TEXT PRIMARY KEY,

    valor TEXT

)
""")

# ==========================================
# BACKUPS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS backups(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,

    data TEXT

)
""")

# ==========================================
# NOTIFICAÇÕES
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS notificacoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    mensagem TEXT,

    lida INTEGER DEFAULT 0,

    data TEXT

)
""")

# ==========================================
# CUPONS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS cupons(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    codigo TEXT UNIQUE,

    valor REAL,

    limite INTEGER,

    usados INTEGER DEFAULT 0,

    ativo INTEGER DEFAULT 1

)
""")

# ==========================================
# ÍNDICES
# ==========================================

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_usuario
ON usuarios(id)
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
CREATE INDEX IF NOT EXISTS idx_saque
ON saques(usuario)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_historico
ON historico(usuario)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_logs
ON logs(usuario)
""")

# ==========================================
# CONFIGURAÇÕES PADRÃO
# ==========================================

configuracoes = [

    ("valor_indicacao", "1.00"),

    ("valor_minimo_saque", "15.00"),

    ("grupo_obrigatorio", "SIM"),

    ("pix_obrigatorio", "SIM"),

    ("anti_fraude", "SIM"),

    ("modo_manutencao", "NAO"),

    ("saques_liberados", "SIM")

]

for chave, valor in configuracoes:

    cursor.execute(

        """
        INSERT OR IGNORE INTO configuracoes
        VALUES(?,?)
        """,

        (chave, valor)

    )

conn.commit()
