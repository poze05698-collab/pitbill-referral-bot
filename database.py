import sqlite3


# ==========================================
# CONEXÃO BANCO
# ==========================================

conn = sqlite3.connect(

    "database.db",

    check_same_thread=False

)


cursor = conn.cursor()



# ==========================================
# TABELA USUÁRIOS
# ==========================================

cursor.execute(

"""
CREATE TABLE IF NOT EXISTS usuarios(

    id INTEGER PRIMARY KEY,

    nome TEXT,

    username TEXT,

    saldo REAL DEFAULT 0,

    pix TEXT DEFAULT '',

    convidados INTEGER DEFAULT 0,

    bloqueado INTEGER DEFAULT 0,

    data_cadastro TEXT,

    ultimo_acesso TEXT

)

"""

)



# ==========================================
# TABELA INDICAÇÕES
# ==========================================

cursor.execute(

"""
CREATE TABLE IF NOT EXISTS indicacoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    indicador INTEGER,

    indicado INTEGER,

    recompensa REAL,

    status TEXT,

    data TEXT

)

"""

)



# ==========================================
# TABELA SAQUES
# ==========================================

cursor.execute(

"""
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

"""

)



conn.commit()# ==========================================
# TABELA HISTÓRICO
# ==========================================

cursor.execute(

"""
CREATE TABLE IF NOT EXISTS historico(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    tipo TEXT,

    descricao TEXT,

    valor REAL,

    data TEXT

)

"""

)



# ==========================================
# TABELA LOGS
# ==========================================

cursor.execute(

"""
CREATE TABLE IF NOT EXISTS logs(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario INTEGER,

    acao TEXT,

    detalhes TEXT,

    data TEXT

)

"""

)



# ==========================================
# TABELA CUPONS
# ==========================================

cursor.execute(

"""
CREATE TABLE IF NOT EXISTS cupons(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    codigo TEXT UNIQUE,

    valor REAL,

    limite INTEGER,

    usados INTEGER DEFAULT 0,

    ativo INTEGER DEFAULT 1

)

"""

)



# ==========================================
# TABELA CONFIGURAÇÕES
# ==========================================

cursor.execute(

"""
CREATE TABLE IF NOT EXISTS configuracoes(

    chave TEXT PRIMARY KEY,

    valor TEXT

)

"""

)



# ==========================================
# CONFIGURAÇÕES INICIAIS
# ==========================================

cursor.execute(

"""
INSERT OR IGNORE INTO configuracoes(

    chave,

    valor

)

VALUES

('modo_manutencao','NAO')

"""

)



# ==========================================
# SALVAR BANCO
# ==========================================

conn.commit()



print(
    "Banco de dados carregado com sucesso."
)
