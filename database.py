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
# DATA/HORA
# ==================================================

def agora():

    return datetime.now().strftime(

        "%d/%m/%Y %H:%M:%S"

    )

# ==================================================
# SYSTEM
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS system(

    id INTEGER PRIMARY KEY,

    plataforma TEXT,

    versao TEXT,

    database_versao TEXT,

    owner_id INTEGER,

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

""")# ==================================================
# CONFIGURAÇÕES PADRÃO
# ==================================================

CONFIG_PADRAO = {

    # -------------------------------
    # GERAL
    # -------------------------------

    "nome_plataforma": "PITBULL REWARDS PLATFORM",

    "versao": "3.0",

    "idioma": "pt-BR",

    "fuso_horario": "America/Sao_Paulo",

    "manutencao": "0",

    "emergencia": "0",

    # -------------------------------
    # GRUPO
    # -------------------------------

    "grupo_obrigatorio": "1",

    "grupo_id": "",

    "grupo_nome": "",

    "grupo_link": "",

    "aprovacao_manual": "1",

    # -------------------------------
    # CANAL
    # -------------------------------

    "canal_obrigatorio": "0",

    "canal_id": "",

    "canal_nome": "",

    "canal_link": "",

    # -------------------------------
    # INDICAÇÕES
    # -------------------------------

    "valor_indicacao": "1.00",

    "limite_indicacoes_dia": "100",

    "tempo_minimo_grupo": "0",

    "anti_fake": "1",

    # -------------------------------
    # SAQUES
    # -------------------------------

    "saque_ativo": "1",

    "valor_minimo_saque": "20.00",

    "valor_maximo_saque": "5000.00",

    "saque_manual": "1",

    "taxa_saque": "0",

    # -------------------------------
    # PIX
    # -------------------------------

    "pix_obrigatorio": "1",

    # -------------------------------
    # ROLETA
    # -------------------------------

    "roleta_ativa": "1",

    "roleta_giros_dia": "1",

    # -------------------------------
    # RASPADINHA
    # -------------------------------

    "raspadinha_ativa": "1",

    "raspadinha_dia": "1",

    # -------------------------------
    # BONUS
    # -------------------------------

    "bonus_diario": "1",

    "bonus_streak": "1",

    # -------------------------------
    # MISSÕES
    # -------------------------------

    "missoes_ativas": "1",

    # -------------------------------
    # RANKING
    # -------------------------------

    "ranking_ativo": "1",

    # -------------------------------
    # EVENTOS
    # -------------------------------

    "eventos_ativos": "1",

    # -------------------------------
    # LOJA
    # -------------------------------

    "loja_ativa": "1",

    # -------------------------------
    # CUPONS
    # -------------------------------

    "cupons_ativos": "1",

    # -------------------------------
    # BAÚS
    # -------------------------------

    "baus_ativos": "1",

    # -------------------------------
    # JACKPOT
    # -------------------------------

    "jackpot_ativo": "1",

    # -------------------------------
    # TICKETS
    # -------------------------------

    "tickets_ativos": "1",

    # -------------------------------
    # NOTIFICAÇÕES
    # -------------------------------

    "notificacoes": "1",

    # -------------------------------
    # PREMIUM
    # -------------------------------

    "premium_ativo": "0",

    "premium_valor": "29.90",

    "premium_dias": "30",

    "premium_multiplicador": "2",

    "premium_bonus": "2",

    "premium_roleta": "2",

    "premium_raspadinha": "2",

    "premium_prioridade": "1",

    # -------------------------------
    # VIP
    # -------------------------------

    "vip_ativo": "1",

    # -------------------------------
    # BROADCAST
    # -------------------------------

    "broadcast_ativo": "1",

    # -------------------------------
    # BACKUP
    # -------------------------------

    "backup_automatico": "1",

    # -------------------------------
    # LOGS
    # -------------------------------

    "logs_admin": "1",

    "logs_financeiro": "1"

}

# ==================================================
# INSERIR CONFIGURAÇÕES
# ==================================================

for chave, valor in CONFIG_PADRAO.items():

    cursor.execute("""

        INSERT OR IGNORE INTO configuracoes(

            chave,

            valor,

            descricao,

            categoria,

            updated_at

        )

        VALUES(

            ?,?,?,?,?

        )

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

    notificacoes INTEGER DEFAULT 0,

    inventario INTEGER DEFAULT 0,

    baus INTEGER DEFAULT 0,

    jackpot INTEGER DEFAULT 0,

    criado_por_admin INTEGER DEFAULT 0,

    created_at TEXT,

    updated_at TEXT

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

conn.commit()# ==================================================
# ADMINISTRADORES
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS admins(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER UNIQUE,

    cargo TEXT,

    ativo INTEGER DEFAULT 1,

    criado_por INTEGER,

    ultimo_login TEXT,

    created_at TEXT,

    updated_at TEXT

)

""")

# ==================================================
# PERMISSÕES
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
# CARGOS PADRÃO
# ==================================================

CARGOS = {

    "OWNER": [

        "*"

    ],

    "ADMIN": [

        "usuarios",

        "saques",

        "indicacoes",

        "grupo",

        "canal",

        "tickets",

        "eventos",

        "premium",

        "vip",

        "broadcast",

        "ranking",

        "financeiro",

        "configuracoes"

    ],

    "MODERADOR": [

        "usuarios",

        "grupo",

        "tickets",

        "blacklist"

    ],

    "SUPORTE": [

        "tickets"

    ],

    "SISTEMA": [

        "*"

    ]

}

conn.commit()# ==================================================
# CARTEIRA
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS carteira(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    saldo REAL DEFAULT 0,

    saldo_pendente REAL DEFAULT 0,

    saldo_bloqueado REAL DEFAULT 0,

    total_recebido REAL DEFAULT 0,

    total_sacado REAL DEFAULT 0,

    total_bonus REAL DEFAULT 0,

    total_indicacoes REAL DEFAULT 0,

    total_jogos REAL DEFAULT 0,

    updated_at TEXT

)

""")

# ==================================================
# EXTRATO FINANCEIRO
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS extrato(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    tipo TEXT,

    categoria TEXT,

    valor REAL,

    saldo_anterior REAL,

    saldo_atual REAL,

    referencia TEXT,

    descricao TEXT,

    admin_id INTEGER,

    created_at TEXT

)

""")

# ==================================================
# PIX
# ==================================================

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

# ==================================================
# SAQUES
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS saques(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    valor REAL,

    taxa REAL DEFAULT 0,

    valor_liquido REAL,

    chave_pix TEXT,

    status TEXT,

    admin_id INTEGER,

    comprovante TEXT,

    observacao TEXT,

    created_at TEXT,

    updated_at TEXT

)

""")

# ==================================================
# HISTÓRICO DE SAQUES
# ==================================================

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

# ==================================================
# FINANCEIRO GERAL
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS financeiro(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    categoria TEXT,

    referencia TEXT,

    usuario_id INTEGER,

    valor REAL,

    observacao TEXT,

    created_at TEXT

)

""")

# ==================================================
# ÍNDICES
# ==================================================

cursor.execute("""

CREATE INDEX IF NOT EXISTS idx_carteira_usuario

ON carteira(usuario_id)

""")

cursor.execute("""

CREATE INDEX IF NOT EXISTS idx_extrato_usuario

ON extrato(usuario_id)

""")

cursor.execute("""

CREATE INDEX IF NOT EXISTS idx_saques_usuario

ON saques(usuario_id)

""")

conn.commit()# ==================================================
# INDICAÇÕES
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS indicacoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    indicador_id INTEGER,

    indicado_id INTEGER UNIQUE,

    codigo_convite TEXT,

    status TEXT DEFAULT 'PENDENTE',

    recompensa REAL DEFAULT 0,

    aprovado_por INTEGER,

    motivo_rejeicao TEXT,

    created_at TEXT,

    approved_at TEXT

)

""")

# ==================================================
# VALIDAÇÃO DE GRUPO
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS validacao_grupo(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER UNIQUE,

    grupo_id TEXT,

    entrou_grupo INTEGER DEFAULT 0,

    confirmou INTEGER DEFAULT 0,

    aprovado INTEGER DEFAULT 0,

    aprovado_por INTEGER,

    observacao TEXT,

    created_at TEXT,

    updated_at TEXT

)

""")

# ==================================================
# VALIDAÇÃO DE CANAL
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS validacao_canal(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER UNIQUE,

    canal_id TEXT,

    entrou_canal INTEGER DEFAULT 0,

    confirmado INTEGER DEFAULT 0,

    created_at TEXT,

    updated_at TEXT

)

""")

# ==================================================
# ANTI FRAUDE
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS antifraude(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    ip TEXT,

    dispositivo TEXT,

    hash_dispositivo TEXT,

    score INTEGER DEFAULT 0,

    suspeito INTEGER DEFAULT 0,

    motivo TEXT,

    created_at TEXT

)

""")

# ==================================================
# BLACKLIST
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS blacklist(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER UNIQUE,

    motivo TEXT,

    admin_id INTEGER,

    created_at TEXT

)

""")

# ==================================================
# HISTÓRICO DE INDICAÇÕES
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS historico_indicacoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    indicador_id INTEGER,

    indicado_id INTEGER,

    acao TEXT,

    descricao TEXT,

    admin_id INTEGER,

    created_at TEXT

)

""")

# ==================================================
# ÍNDICES
# ==================================================

cursor.execute("""

CREATE INDEX IF NOT EXISTS idx_indicador

ON indicacoes(indicador_id)

""")

cursor.execute("""

CREATE INDEX IF NOT EXISTS idx_indicado

ON indicacoes(indicado_id)

""")

cursor.execute("""

CREATE INDEX IF NOT EXISTS idx_validacao_grupo

ON validacao_grupo(usuario_id)

""")

conn.commit()# ==================================================
# ROLETA
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS roleta(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    premio TEXT,

    valor REAL DEFAULT 0,

    xp INTEGER DEFAULT 0,

    giros_bonus INTEGER DEFAULT 0,

    created_at TEXT

)

""")

# ==================================================
# RASPADINHA
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS raspadinha(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    premio TEXT,

    valor REAL DEFAULT 0,

    xp INTEGER DEFAULT 0,

    raspadinhas_bonus INTEGER DEFAULT 0,

    created_at TEXT

)

""")

# ==================================================
# BONUS DIÁRIO
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS bonus_diario(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    dia INTEGER,

    recompensa REAL,

    xp INTEGER,

    recebido INTEGER DEFAULT 0,

    created_at TEXT

)

""")

# ==================================================
# MISSÕES
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS missoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,

    descricao TEXT,

    tipo TEXT,

    objetivo INTEGER,

    recompensa REAL,

    xp INTEGER,

    ativo INTEGER DEFAULT 1,

    created_at TEXT

)

""")

# ==================================================
# MISSÕES DOS USUÁRIOS
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS usuario_missoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    missao_id INTEGER,

    progresso INTEGER DEFAULT 0,

    concluida INTEGER DEFAULT 0,

    recompensa_recebida INTEGER DEFAULT 0,

    created_at TEXT,

    updated_at TEXT

)

""")

# ==================================================
# CONQUISTAS
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS conquistas(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,

    descricao TEXT,

    recompensa REAL,

    xp INTEGER,

    ativo INTEGER DEFAULT 1

)

""")

# ==================================================
# CONQUISTAS DOS USUÁRIOS
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS usuario_conquistas(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    conquista_id INTEGER,

    recebido INTEGER DEFAULT 0,

    created_at TEXT

)

""")

conn.commit()# ==================================================
# PLANOS PREMIUM
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS premium_planos(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,

    descricao TEXT,

    valor REAL,

    dias INTEGER,

    multiplicador REAL DEFAULT 1,

    bonus_diario INTEGER DEFAULT 1,

    roletas INTEGER DEFAULT 1,

    raspadinhas INTEGER DEFAULT 1,

    prioridade_ticket INTEGER DEFAULT 0,

    ativo INTEGER DEFAULT 1,

    created_at TEXT,

    updated_at TEXT

)

""")

# ==================================================
# ASSINATURAS PREMIUM
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS premium_assinaturas(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    plano_id INTEGER,

    status TEXT,

    valor_pago REAL,

    inicio TEXT,

    expira TEXT,

    aprovado_por INTEGER,

    created_at TEXT,

    updated_at TEXT

)

""")

# ==================================================
# VIP
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS vip_planos(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,

    xp_minimo INTEGER,

    multiplicador REAL,

    beneficios TEXT,

    ativo INTEGER DEFAULT 1

)

""")

# ==================================================
# LOJA
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS loja(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,

    categoria TEXT,

    descricao TEXT,

    valor REAL,

    tipo_recompensa TEXT,

    recompensa TEXT,

    ativo INTEGER DEFAULT 1,

    created_at TEXT

)

""")

# ==================================================
# INVENTÁRIO
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS inventario(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    item TEXT,

    quantidade INTEGER DEFAULT 0,

    created_at TEXT,

    updated_at TEXT

)

""")

# ==================================================
# CUPONS
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS cupons(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    codigo TEXT UNIQUE,

    descricao TEXT,

    recompensa_tipo TEXT,

    recompensa_valor REAL,

    limite_uso INTEGER,

    usados INTEGER DEFAULT 0,

    ativo INTEGER DEFAULT 1,

    validade TEXT,

    criado_por INTEGER,

    created_at TEXT

)

""")

# ==================================================
# CUPONS RESGATADOS
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS usuario_cupons(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    cupom_id INTEGER,

    created_at TEXT

)

""")

# ==================================================
# BAÚS
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS baus(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    tipo TEXT,

    aberto INTEGER DEFAULT 0,

    premio TEXT,

    created_at TEXT

)

""")

# ==================================================
# JACKPOT
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS jackpot(

    id INTEGER PRIMARY KEY,

    valor REAL,

    ultimo_ganhador INTEGER,

    ultima_premiacao TEXT

)

""")

# ==================================================
# EVENTOS
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS eventos(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,

    descricao TEXT,

    bonus REAL,

    multiplicador REAL,

    inicio TEXT,

    fim TEXT,

    ativo INTEGER DEFAULT 1

)

""")

conn.commit()# ==================================================
# TICKETS
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS tickets(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    protocolo TEXT UNIQUE,

    categoria TEXT,

    assunto TEXT,

    status TEXT DEFAULT 'ABERTO',

    prioridade TEXT DEFAULT 'NORMAL',

    responsavel INTEGER,

    created_at TEXT,

    updated_at TEXT,

    fechado_em TEXT

)

""")

# ==================================================
# MENSAGENS DOS TICKETS
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS ticket_mensagens(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    ticket_id INTEGER,

    autor_id INTEGER,

    administrador INTEGER DEFAULT 0,

    mensagem TEXT,

    created_at TEXT

)

""")

# ==================================================
# NOTIFICAÇÕES
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS notificacoes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    titulo TEXT,

    mensagem TEXT,

    tipo TEXT,

    lida INTEGER DEFAULT 0,

    created_at TEXT

)

""")

# ==================================================
# BROADCAST
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS broadcasts(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    admin_id INTEGER,

    titulo TEXT,

    mensagem TEXT,

    total_enviado INTEGER DEFAULT 0,

    created_at TEXT

)

""")

# ==================================================
# ESTATÍSTICAS
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS estatisticas(

    chave TEXT PRIMARY KEY,

    valor TEXT,

    updated_at TEXT

)

""")

# ==================================================
# BACKUPS
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS backups(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    arquivo TEXT,

    tamanho TEXT,

    admin_id INTEGER,

    created_at TEXT

)

""")

# ==================================================
# AUDITORIA GERAL
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS auditoria(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    modulo TEXT,

    acao TEXT,

    referencia TEXT,

    detalhes TEXT,

    ip TEXT,

    created_at TEXT

)

""")

# ==================================================
# LOG DO SISTEMA
# ==================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS sistema_logs(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nivel TEXT,

    modulo TEXT,

    mensagem TEXT,

    created_at TEXT

)

""")

conn.commit()# ==================================================
# MÓDULOS PADRÃO
# ==================================================

MODULOS_PADRAO = [

    ("grupo", "Grupo Obrigatório", "Validação de grupo", 1),
    ("canal", "Canal Obrigatório", "Validação de canal", 0),
    ("afiliados", "Afiliados", "Sistema de indicações", 1),
    ("carteira", "Carteira", "Sistema financeiro", 1),
    ("pix", "PIX", "Cadastro de PIX", 1),
    ("saques", "Saques", "Solicitação de saque", 1),
    ("roleta", "Roleta", "Roleta diária", 1),
    ("raspadinha", "Raspadinha", "Raspadinha diária", 1),
    ("bonus", "Bônus Diário", "Bônus diário", 1),
    ("missoes", "Missões", "Sistema de missões", 1),
    ("ranking", "Ranking", "Ranking geral", 1),
    ("vip", "VIP", "Sistema VIP", 1),
    ("premium", "Premium", "Assinaturas Premium", 0),
    ("loja", "Loja", "Loja virtual", 1),
    ("tickets", "Tickets", "Atendimento", 1),
    ("eventos", "Eventos", "Eventos especiais", 1),
    ("cupons", "Cupons", "Cupons promocionais", 1),
    ("baus", "Baús", "Baús de recompensa", 1),
    ("jackpot", "Jackpot", "Prêmio acumulado", 1),
    ("notificacoes", "Notificações", "Mensagens internas", 1),
    ("broadcast", "Broadcast", "Mensagens em massa", 1),
    ("backup", "Backup", "Sistema de backup", 1)

]

for chave, nome, descricao, ativo in MODULOS_PADRAO:

    cursor.execute("""

    INSERT OR IGNORE INTO modulos(

        chave,

        nome,

        descricao,

        ativo,

        created_at,

        updated_at

    )

    VALUES(?,?,?,?,?,?)

    """, (

        chave,

        nome,

        descricao,

        ativo,

        agora(),

        agora()

    ))

# ==================================================
# PLANO PREMIUM PADRÃO
# ==================================================

cursor.execute("""

INSERT OR IGNORE INTO premium_planos(

    id,

    nome,

    descricao,

    valor,

    dias,

    multiplicador,

    bonus_diario,

    roletas,

    raspadinhas,

    prioridade_ticket,

    ativo,

    created_at,

    updated_at

)

VALUES(

    1,

    'Premium',

    'Plano Premium Oficial',

    29.90,

    30,

    2,

    2,

    2,

    2,

    1,

    1,

    ?,

    ?

)

""", (

    agora(),

    agora()

))

# ==================================================
# VIP PADRÃO
# ==================================================

VIPS = [

    (1, "Bronze", 0, 1),
    (2, "Prata", 500, 1.10),
    (3, "Ouro", 1500, 1.20),
    (4, "Diamante", 5000, 1.40)

]

for id_vip, nome, xp, mult in VIPS:

    cursor.execute("""

    INSERT OR IGNORE INTO vip_planos(

        id,

        nome,

        xp_minimo,

        multiplicador,

        beneficios,

        ativo

    )

    VALUES(?,?,?,?,?,?)

    """, (

        id_vip,

        nome,

        xp,

        mult,

        "",

        1

    ))

# ==================================================
# SYSTEM
# ==================================================

cursor.execute("""

INSERT OR IGNORE INTO system(

    id,

    plataforma,

    versao,

    database_versao,

    owner_id,

    maintenance,

    emergency,

    created_at,

    updated_at

)

VALUES(

    1,

    'PITBULL REWARDS PLATFORM',

    '3.0',

    '3.0',

    0,

    0,

    0,

    ?,

    ?

)

""", (

    agora(),

    agora()

))

# ==================================================
# FUNÇÕES
# ==================================================

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

    cursor.execute(

        """

        UPDATE configuracoes

        SET valor=?,

            updated_at=?

        WHERE chave=?

        """,

        (

            str(valor),

            agora(),

            chave

        )

    )

    conn.commit()


def modulo_ativo(chave):

    cursor.execute(

        "SELECT ativo FROM modulos WHERE chave=?",

        (chave,)

    )

    resultado = cursor.fetchone()

    if resultado:

        return resultado["ativo"] == 1

    return False


def alterar_modulo(chave, ativo):

    cursor.execute(

        """

        UPDATE modulos

        SET ativo=?,

            updated_at=?

        WHERE chave=?

        """,

        (

            ativo,

            agora(),

            chave

        )

    )

    conn.commit()

# ==================================================
# FINALIZAÇÃO
# ==================================================

conn.commit()

print("=" * 60)

print("🐶 PITBULL REWARDS PLATFORM V3")

print("✅ Database carregado com sucesso.")

print("=" * 60)
