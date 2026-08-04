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

    codigo TEXT UNIQUE NOT NULL,

    nome TEXT NOT NULL,

    username TEXT,

    idioma TEXT DEFAULT 'pt-BR',

    status TEXT DEFAULT 'ATIVO',

    bloqueado INTEGER DEFAULT 0,

    banido INTEGER DEFAULT 0,

    aprovado INTEGER DEFAULT 0,

    convidado_por INTEGER,

    xp INTEGER DEFAULT 0,

    nivel INTEGER DEFAULT 1,

    experiencia_total INTEGER DEFAULT 0,

    notificacoes INTEGER DEFAULT 1,

    criado_por_admin INTEGER DEFAULT 0,

    ultimo_login TEXT,

    ultimo_ip TEXT,

    ultimo_dispositivo TEXT,

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

    total_indicacoes REAL DEFAULT 0,

    total_bonus REAL DEFAULT 0,

    total_saques REAL DEFAULT 0,

    total_depositos REAL DEFAULT 0,

    total_gasto REAL DEFAULT 0,

    ultima_movimentacao TEXT,

    created_at TEXT,

    updated_at TEXT,

    FOREIGN KEY(usuario_id)
    REFERENCES usuarios(id)

)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_carteira_usuario
ON carteira(usuario_id)
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

    usuario_id INTEGER NOT NULL,

    tipo TEXT NOT NULL,

    chave TEXT NOT NULL,

    nome TEXT,

    documento TEXT,

    banco TEXT,

    principal INTEGER DEFAULT 1,

    verificado INTEGER DEFAULT 0,

    status TEXT DEFAULT 'ATIVO',

    observacao TEXT,

    created_at TEXT,

    updated_at TEXT,

    FOREIGN KEY(usuario_id)
    REFERENCES usuarios(id)

)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_pix_usuario
ON pix(usuario_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_pix_chave
ON pix(chave)
""")


# =====================================================
# SAQUES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS saques(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER NOT NULL,

    pix_id INTEGER,

    valor REAL NOT NULL,

    taxa REAL DEFAULT 0,

    valor_liquido REAL NOT NULL,

    status TEXT DEFAULT 'PENDENTE',

    admin_id INTEGER,

    comprovante TEXT,

    observacao_admin TEXT,

    ip_solicitacao TEXT,

    dispositivo TEXT,

    data_solicitacao TEXT,

    data_aprovacao TEXT,

    data_pagamento TEXT,

    created_at TEXT,

    updated_at TEXT,

    FOREIGN KEY(usuario_id)
    REFERENCES usuarios(id),

    FOREIGN KEY(admin_id)
    REFERENCES administradores(usuario_id),

    FOREIGN KEY(pix_id)
    REFERENCES pix(id)

)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_saques_usuario
ON saques(usuario_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_saques_status
ON saques(status)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_saques_admin
ON saques(admin_id)
""")


# =====================================================
# EXTRATO FINANCEIRO
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS extrato(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER NOT NULL,

    tipo TEXT NOT NULL,

    categoria TEXT NOT NULL,

    valor REAL NOT NULL,

    saldo_anterior REAL DEFAULT 0,

    saldo_atual REAL DEFAULT 0,

    descricao TEXT,

    referencia_id INTEGER,

    referencia_tabela TEXT,

    admin_id INTEGER,

    ip TEXT,

    dispositivo TEXT,

    created_at TEXT,

    FOREIGN KEY(usuario_id)
    REFERENCES usuarios(id),

    FOREIGN KEY(admin_id)
    REFERENCES administradores(usuario_id)

)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_extrato_usuario
ON extrato(usuario_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_extrato_categoria
ON extrato(categoria)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_extrato_tipo
ON extrato(tipo)
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

    codigo_convite TEXT NOT NULL,

    recompensa REAL DEFAULT 0,

    status TEXT DEFAULT 'PENDENTE',

    grupo_obrigatorio INTEGER DEFAULT 1,

    grupo_verificado INTEGER DEFAULT 0,

    canal_obrigatorio INTEGER DEFAULT 0,

    canal_verificado INTEGER DEFAULT 0,

    aprovado_por INTEGER,

    data_cadastro TEXT,

    data_aprovacao TEXT,

    data_rejeicao TEXT,

    motivo_rejeicao TEXT,

    ip TEXT,

    dispositivo TEXT,

    observacao_admin TEXT,

    created_at TEXT,

    updated_at TEXT,

    FOREIGN KEY(indicador_id)
    REFERENCES usuarios(id),

    FOREIGN KEY(indicado_id)
    REFERENCES usuarios(id),

    FOREIGN KEY(aprovado_por)
    REFERENCES administradores(usuario_id)

)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_indicador
ON indicacoes(indicador_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_indicado
ON indicacoes(indicado_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_status_indicacao
ON indicacoes(status)
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

    grupo_id TEXT,

    grupo_nome TEXT,

    entrou INTEGER DEFAULT 0,

    verificado INTEGER DEFAULT 0,

    data_entrada TEXT,

    data_verificacao TEXT,

    ultima_consulta TEXT,

    FOREIGN KEY(usuario_id)
    REFERENCES usuarios(id)

)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_grupo_usuario
ON grupo(usuario_id)
""")

# =====================================================
# CANAL
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS canal(

    usuario_id INTEGER PRIMARY KEY,

    canal_id TEXT,

    canal_nome TEXT,

    entrou INTEGER DEFAULT 0,

    verificado INTEGER DEFAULT 0,

    data_entrada TEXT,

    data_verificacao TEXT,

    ultima_consulta TEXT,

    FOREIGN KEY(usuario_id)
    REFERENCES usuarios(id)

)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_canal_usuario
ON canal(usuario_id)
""")

# =====================================================
# ANTI FRAUDE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS antifraude(

    usuario_id INTEGER PRIMARY KEY,

    ip TEXT,

    dispositivo TEXT,

    hash_dispositivo TEXT,

    score INTEGER DEFAULT 100,

    contas_mesmo_ip INTEGER DEFAULT 0,

    contas_mesmo_dispositivo INTEGER DEFAULT 0,

    vpn INTEGER DEFAULT 0,

    proxy INTEGER DEFAULT 0,

    emulador INTEGER DEFAULT 0,

    suspeito INTEGER DEFAULT 0,

    motivo TEXT,

    ultima_analise TEXT,

    created_at TEXT,

    updated_at TEXT,

    FOREIGN KEY(usuario_id)
    REFERENCES usuarios(id)

)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_antifraude_usuario
ON antifraude(usuario_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_antifraude_score
ON antifraude(score)
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
# BROADCAST
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS broadcast(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    admin_id INTEGER,

    mensagem TEXT,

    usuarios_enviados INTEGER DEFAULT 0,

    usuarios_recebidos INTEGER DEFAULT 0,

    status TEXT DEFAULT 'PENDENTE',

    created_at TEXT,

    FOREIGN KEY(admin_id)
    REFERENCES administradores(usuario_id)

)
""")


# =====================================================
# LOGS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    admin_id INTEGER,

    categoria TEXT,

    acao TEXT,

    descricao TEXT,

    ip TEXT,

    dispositivo TEXT,

    created_at TEXT,

    FOREIGN KEY(usuario_id)
    REFERENCES usuarios(id),

    FOREIGN KEY(admin_id)
    REFERENCES administradores(usuario_id)

)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_logs_usuario
ON logs(usuario_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_logs_admin
ON logs(admin_id)
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

print("=" * 60)
print("🐶 PITBULL REWARDS PLATFORM V3")
print("✅ Database carregado com sucesso.")
print("=" * 60)
