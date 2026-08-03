"""
==================================================
PITBULL REWARDS PLATFORM V3
BOT PRINCIPAL
==================================================
"""

import telebot

# ==================================================
# CONFIG
# ==================================================

from config import (
    TOKEN,
    OWNER_ID,
    NOME_BOT
)

# ==================================================
# DATABASE
# ==================================================

from database import (
    conn,
    cursor,
    agora
)

# ==================================================
# TECLADOS
# ==================================================

from teclado import (
    menu_principal,
    menu_admin,
    menu_administradores
)

# ==================================================
# USUÁRIOS
# ==================================================

from usuarios import (

    cadastrar_usuario,

    atualizar_usuario,

    obter_usuario,

    enviar_menu,

    texto_perfil,

    obter_link_convite,

    registrar_indicacao

)

# ==================================================
# CARTEIRA
# ==================================================

from carteira import (

    texto_carteira,

    adicionar_saldo,

    remover_saldo

)

# ==================================================
# PIX
# ==================================================

from pix import (

    texto_pix,

    salvar_pix,

    validar_pix

)

# ==================================================
# SAQUES
# ==================================================

from saques import (

    solicitar_saque

)

# ==================================================
# INDICAÇÕES
# ==================================================

from indicacoes import (

    listar_indicados,

    listar_pendentes

)

# ==================================================
# ADMIN
# ==================================================

from admin.sistema import (
    criar_owner
)

from admin.menu import (
    menu_admin_principal
)

from admin.usuarios import (

    menu_admin_usuarios,

    buscar_usuario_admin,

    texto_usuario_admin

)

from admin.saques import *

from admin.indicacoes import *

from admin.config import *

from admin.broadcast import *

from admin.logs import *

from admin.estatisticas import *

from admin.antifraude import *

from admin.cargos import *

# ==================================================
# BOT
# ==================================================

bot = telebot.TeleBot(

    TOKEN,

    parse_mode="HTML"

)

# ==================================================
# ESTADOS
# ==================================================

estados = {}

# ==================================================
# CACHE
# ==================================================

cache = {}

# ==================================================
# CONSTANTES
# ==================================================

VERSAO = "3.0"

print("=" * 60)
print("🐶 PITBULL REWARDS PLATFORM")
print(f"Versão {VERSAO}")
print("=" * 60)
