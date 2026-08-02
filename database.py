import sqlite3
from datetime import datetime

from config import DATABASE


# =====================================================
# CONEXÃO
# =====================================================

conn = sqlite3.connect(
    DATABASE,
    check_same_thread=False
)

conn.row_factory = sqlite3.Row

cursor = conn.cursor()


# =====================================================
# DATA
# =====================================================

def agora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# =====================================================
# EXECUTOR SQL
# =====================================================

def executar(sql, parametros=()):
    cursor.execute(sql, parametros)
    conn.commit()


# =====================================================
# BUSCAR UM
# =====================================================

def buscar(sql, parametros=()):
    cursor.execute(sql, parametros)
    return cursor.fetchone()


# =====================================================
# BUSCAR TODOS
# =====================================================

def buscar_todos(sql, parametros=()):
    cursor.execute(sql, parametros)
    return cursor.fetchall()


# =====================================================
# CONFIGURAÇÕES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS configuracoes(

    chave TEXT PRIMARY KEY,

    valor TEXT,

    descricao TEXT,

    categoria TEXT,

    updated_at TEXT

)
""")# =====================================================
# USUÁRIOS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(

    id INTEGER PRIMARY KEY,

    codigo TEXT UNIQUE,

    nome TEXT NOT NULL,

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


# =====================================================
# ADMINISTRADORES
# =====================================================

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


# =====================================================
# PERMISSÕES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS permissoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    admin_id INTEGER,

    permissao TEXT,

    permitido INTEGER DEFAULT 1,

    created_at TEXT

)
""")


# =====================================================
# CARTEIRA
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS carteira(

    usuario_id INTEGER PRIMARY KEY,

    saldo REAL DEFAULT 0,

    saldo_pendente REAL DEFAULT 0,

    saldo_bloqueado REAL DEFAULT 0,

    total_recebido REAL DEFAULT 0,

    total_sacado REAL DEFAULT 0,

    total_bonus REAL DEFAULT 0,

    total_indicacoes REAL DEFAULT 0,

    updated_at TEXT

)
""")


# =====================================================
# ÍNDICES
# =====================================================

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_usuario_codigo
ON usuarios(codigo)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_usuario_indicador
ON usuarios(convidado_por)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_admin_usuario
ON administradores(usuario_id)
""")

conn.commit()# =====================================================
# PIX
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS pix(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER UNIQUE,

    tipo TEXT,

    chave TEXT,

    nome TEXT,

    documento TEXT,

    status TEXT DEFAULT 'ATIVO',

    verificado INTEGER DEFAULT 0,

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

    usuario_id INTEGER,

    valor REAL,

    taxa REAL DEFAULT 0,

    valor_liquido REAL,

    chave_pix TEXT,

    status TEXT DEFAULT 'PENDENTE',

    admin_id INTEGER,

    observacao TEXT,

    comprovante TEXT,

    created_at TEXT,

    updated_at TEXT

)
""")


# =====================================================
# EXTRATO
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS extrato(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    tipo TEXT,

    categoria TEXT,

    valor REAL,

    saldo_anterior REAL,

    saldo_atual REAL,

    descricao TEXT,

    referencia TEXT,

    admin_id INTEGER,

    created_at TEXT

)
""")


# =====================================================
# HISTÓRICO FINANCEIRO
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS financeiro(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    categoria TEXT,

    tipo TEXT,

    valor REAL,

    referencia TEXT,

    observacao TEXT,

    created_at TEXT

)
""")


# =====================================================
# LOG DOS SAQUES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS saque_logs(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    saque_id INTEGER,

    admin_id INTEGER,

    status TEXT,

    observacao TEXT,

    created_at TEXT

)
""")


# =====================================================
# ÍNDICES
# =====================================================

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_pix_usuario
ON pix(usuario_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_saques_usuario
ON saques(usuario_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_extrato_usuario
ON extrato(usuario_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_financeiro_usuario
ON financeiro(usuario_id)
""")

conn.commit()# =====================================================
# INDICAÇÕES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS indicacoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    indicador_id INTEGER NOT NULL,

    indicado_id INTEGER UNIQUE NOT NULL,

    codigo_convite TEXT,

    recompensa REAL DEFAULT 0,

    status TEXT DEFAULT 'PENDENTE',

    aprovado_por INTEGER,

    motivo_rejeicao TEXT,

    created_at TEXT,

    updated_at TEXT

)
""")


# =====================================================
# APROVAÇÕES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS aprovacoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    indicador_id INTEGER,

    admin_id INTEGER,

    status TEXT,

    observacao TEXT,

    created_at TEXT

)
""")


# =====================================================
# GRUPO
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS grupo(

    usuario_id INTEGER PRIMARY KEY,

    entrou INTEGER DEFAULT 0,

    verificado INTEGER DEFAULT 0,

    data_entrada TEXT,

    data_verificacao TEXT

)
""")


# =====================================================
# CANAL
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS canal(

    usuario_id INTEGER PRIMARY KEY,

    entrou INTEGER DEFAULT 0,

    verificado INTEGER DEFAULT 0,

    data_entrada TEXT,

    data_verificacao TEXT

)
""")


# =====================================================
# ANTI FRAUDE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS antifraude(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    ip TEXT,

    dispositivo TEXT,

    hash_dispositivo TEXT,

    score INTEGER DEFAULT 100,

    suspeito INTEGER DEFAULT 0,

    motivo TEXT,

    created_at TEXT

)
""")


# =====================================================
# BLACKLIST
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS blacklist(

    usuario_id INTEGER PRIMARY KEY,

    motivo TEXT,

    admin_id INTEGER,

    created_at TEXT

)
""")


# =====================================================
# LOG INDICAÇÕES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS log_indicacoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    indicador_id INTEGER,

    indicado_id INTEGER,

    acao TEXT,

    admin_id INTEGER,

    descricao TEXT,

    created_at TEXT

)
""")


# =====================================================
# ÍNDICES
# =====================================================

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_indicador
ON indicacoes(indicador_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_indicado
ON indicacoes(indicado_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_grupo
ON grupo(usuario_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_canal
ON canal(usuario_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_antifraude
ON antifraude(usuario_id)
""")

conn.commit()# =====================================================
# VIP
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS vip(

    usuario_id INTEGER PRIMARY KEY,

    plano TEXT,

    multiplicador REAL DEFAULT 1,

    expira_em TEXT,

    ativo INTEGER DEFAULT 0,

    created_at TEXT,

    updated_at TEXT

)
""")


# =====================================================
# PREMIUM
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS premium(

    usuario_id INTEGER PRIMARY KEY,

    plano TEXT,

    beneficios TEXT,

    expira_em TEXT,

    ativo INTEGER DEFAULT 0,

    created_at TEXT,

    updated_at TEXT

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

    ativo INTEGER DEFAULT 1

)
""")


# =====================================================
# MISSÕES DOS USUÁRIOS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios_missoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    missao_id INTEGER,

    progresso INTEGER DEFAULT 0,

    concluida INTEGER DEFAULT 0,

    recompensa_recebida INTEGER DEFAULT 0,

    updated_at TEXT

)
""")


# =====================================================
# BONUS DIÁRIO
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS bonus_diario(

    usuario_id INTEGER PRIMARY KEY,

    streak INTEGER DEFAULT 0,

    ultimo_resgate TEXT

)
""")


# =====================================================
# TICKETS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    assunto TEXT,

    mensagem TEXT,

    status TEXT DEFAULT 'ABERTO',

    admin_id INTEGER,

    resposta TEXT,

    created_at TEXT,

    updated_at TEXT

)
""")


# =====================================================
# BROADCAST
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS broadcast(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    admin_id INTEGER,

    mensagem TEXT,

    enviados INTEGER DEFAULT 0,

    created_at TEXT

)
""")


# =====================================================
# LOGS GERAIS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    categoria TEXT,

    usuario_id INTEGER,

    admin_id INTEGER,

    descricao TEXT,

    created_at TEXT

)
""")


# =====================================================
# ESTATÍSTICAS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS estatisticas(

    chave TEXT PRIMARY KEY,

    valor TEXT

)
""")


# =====================================================
# VALORES PADRÃO
# =====================================================

cursor.execute("""
INSERT OR IGNORE INTO estatisticas(chave,valor)
VALUES
('usuarios','0'),
('saques','0'),
('indicacoes','0'),
('valor_pago','0'),
('valor_indicacoes','0')
""")

conn.commit()

print("="*60)
print("🐶 PITBULL REWARDS PLATFORM V3")
print("✅ Database carregado com sucesso.")
print("="*60)
