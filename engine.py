"""
==================================================
 PITBULL REWARDS PLATFORM V3
 engine.py
==================================================
"""

from usuarios import (
    adicionar_saldo,
    adicionar_xp,
    adicionar_item,
    adicionar_bau,
    adicionar_notificacao,
    registrar_historico,
    incrementar_estatistica,
    premium_ativo
)

# ==================================================
# ENGINE DE RECOMPENSAS
# ==================================================

class Engine:

    @staticmethod
    def recompensa(

        usuario_id,

        saldo=0,

        xp=0,

        item=None,

        quantidade_item=1,

        bau=None,

        notificacao=None,

        categoria="GERAL",

        descricao=""

    ):

        """
        Distribui recompensas para um usuário.

        Todos os módulos da plataforma devem utilizar
        esta função em vez de alterar saldo, XP ou
        inventário diretamente.
        """

        if premium_ativo(usuario_id):

            saldo *= 2
            xp *= 2

        if saldo > 0:

            adicionar_saldo(

                usuario_id,

                saldo,

                categoria=categoria,

                descricao=descricao

            )

        if xp > 0:

            adicionar_xp(

                usuario_id,

                xp

            )

        if item:

            adicionar_item(

                usuario_id,

                item,

                quantidade_item

            )

        if bau:

            adicionar_bau(

                usuario_id,

                bau

            )

        if notificacao:

            adicionar_notificacao(

                usuario_id,

                "🎉 Recompensa",

                notificacao

            )

        registrar_historico(

            usuario_id,

            categoria,

            "Recompensa",

            descricao

        )

        incrementar_estatistica(

            "recompensas"

        )

        return True# ==================================================
# ENGINE FINANCEIRA
# ==================================================

class EngineFinanceira:

    @staticmethod
    def sacar(

        usuario_id,

        valor,

        descricao="Solicitação de saque"

    ):

        from usuarios import remover_saldo

        return remover_saldo(

            usuario_id,

            valor,

            categoria="SAQUE",

            descricao=descricao

        )

    @staticmethod
    def comprar(

        usuario_id,

        valor,

        descricao,

        categoria="LOJA"

    ):

        from usuarios import remover_saldo

        return remover_saldo(

            usuario_id,

            valor,

            categoria=categoria,

            descricao=descricao

        )

# ==================================================
# ENGINE PREMIUM
# ==================================================

class EnginePremium:

    @staticmethod
    def ativar(

        usuario_id,

        dias=30

    ):

        from usuarios import ativar_premium

        ativar_premium(

            usuario_id,

            dias

        )

        Engine.recompensa(

            usuario_id,

            notificacao="💎 Premium ativado com sucesso!",

            categoria="PREMIUM",

            descricao="Ativação do plano Premium"

        )

# ==================================================
# ENGINE CUPONS
# ==================================================

class EngineCupom:

    @staticmethod
    def resgatar(

        usuario_id,

        saldo=0,

        xp=0,

        item=None,

        bau=None,

        descricao="Cupom Promocional"

    ):

        Engine.recompensa(

            usuario_id,

            saldo=saldo,

            xp=xp,

            item=item,

            bau=bau,

            categoria="CUPOM",

            descricao=descricao,

            notificacao="🎁 Cupom resgatado com sucesso!"

        )

# ==================================================
# ENGINE EVENTOS
# ==================================================

class EngineEvento:

    @staticmethod
    def recompensa(

        usuario_id,

        saldo=0,

        xp=0,

        descricao="Evento"

    ):

        Engine.recompensa(

            usuario_id,

            saldo=saldo,

            xp=xp,

            categoria="EVENTO",

            descricao=descricao,

            notificacao="🎉 Você recebeu uma recompensa do evento!"

        )

# ==================================================
# ENGINE MISSÕES
# ==================================================

class EngineMissao:

    @staticmethod
    def concluir(

        usuario_id,

        saldo=0,

        xp=0,

        item=None,

        bau=None

    ):

        Engine.recompensa(

            usuario_id,

            saldo=saldo,

            xp=xp,

            item=item,

            bau=bau,

            categoria="MISSAO",

            descricao="Missão concluída",

            notificacao="🏆 Missão concluída!"

        )

print("✅ engine.py carregado com sucesso.")
