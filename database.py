import sqlite3

conn = sqlite3.connect(
    "database.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ==========================================
# USUÁRIOS
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

    data_cadastro TEXT,

    ultimo_acesso TEXT

)
""")

# ==========================================
# SAQUES
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS saques(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    valor REAL,

    pix TEXT,

    status TEXT,

    data TEXT

)
""")

# ==========================================
# INDICAÇÕES
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
# BLOQUEADOS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios_bloqueados(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER UNIQUE,

    motivo TEXT,

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

cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_saques_usuario ON saques(usuario)"
)

cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_indicador ON indicacoes(indicador)"
)

cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_indicado ON indicacoes(indicado)"
)

cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_historico ON historico(usuario)"
)

cursor.execute(
    "INSERT OR IGNORE INTO configuracoes VALUES ('valor_indicacao','1.00')"
)

cursor.execute(
    "INSERT OR IGNORE INTO configuracoes VALUES ('valor_saque','15.00')"
)

cursor.execute(
    "INSERT OR IGNORE INTO configuracoes VALUES ('saque_liberado','SIM')"
)

cursor.execute(
    "INSERT OR IGNORE INTO configuracoes VALUES ('grupo_obrigatorio','SIM')"
)

cursor.execute(
    "INSERT OR IGNORE INTO configuracoes VALUES ('pix_obrigatorio','SIM')"
)

conn.commit()
