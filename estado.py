"""
=========================================
 PITBULL REWARDS PLATFORM V3
 estado.py
=========================================
"""

# Estados temporários dos usuários
_estados = {}


def definir_estado(usuario_id, estado):

    _estados[usuario_id] = estado


def obter_estado(usuario_id):

    return _estados.get(usuario_id)


def limpar_estado(usuario_id):

    if usuario_id in _estados:
        del _estados[usuario_id]
