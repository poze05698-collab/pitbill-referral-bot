from datetime import datetime

from config import *

from database import conn, cursor

from teclado import (
    menu_principal,
    menu_pix
)

from utils import (
    verificar_acesso,
    adicionar_log,
    adicionar_historico,
    agora
)

# ==========================================
# REGISTRAR MÓDULO
# ==========================================

def registrar_usuario(bot):

    # ======================================
    # /START
    # ======================================

    @bot.message_handler(commands=["start"])
    def start(message):

        if not verificar_acesso(bot, message):
            return

        user_id = message.from_user.id

        nome = message.from_user.first_name

        username = (
            "@" + message.from_user.username
            if message.from_user.username
            else ""
        )

        cursor.execute(

            """
            SELECT id

            FROM usuarios

            WHERE id=?
            """,

            (user_id,)

        )

        usuario = cursor.fetchone()

        # ==================================
        # NOVO USUÁRIO
        # ==================================

        if usuario is None:

            convidado_por = None

            args = message.text.split()

            if len(args) > 1:

                codigo = args[1]

                if codigo.startswith("convite_"):

                    try:

                        convidado_por = int(

                            codigo.replace(

                                "convite_",

                                ""

                            )

                        )

                    except:

                        convidado_por = None

            # Não pode indicar a si mesmo

            if convidado_por == user_id:

                convidado_por = None

            cursor.execute(

                """
                INSERT INTO usuarios(

                    id,

                    nome,

                    username,

                    saldo,

                    pix,

                    convidados,

                    convidado_por,

                    bloqueado,

                    admin,

                    data_cadastro,

                    ultimo_acesso

                )

                VALUES(

                    ?,?,?,?,?,?,?,?,?,?,?

                )
                """,

                (

                    user_id,

                    nome,

                    username,

                    0,

                    "",

                    0,

                    convidado_por,

                    0,

                    0,

                    agora(),

                    agora()

                )

            )

            conn.commit()

            adicionar_log(

                user_id,

                "CADASTRO",

                "Novo usuário"

            )

            adicionar_historico(

                user_id,

                "CADASTRO",

                "Cadastro realizado",

                0

            )

        else:

            cursor.execute(

                """
                UPDATE usuarios

                SET ultimo_acesso=?

                WHERE id=?
                """,

                (

                    agora(),

                    user_id

                )

            )

            conn.commit()

        texto = f"""
🎉 <b>Bem-vindo(a), {nome}!</b>

💰 Convide amigos.

🎁 Ganhe recompensas.

Escolha uma opção abaixo.
"""

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML",

            reply_markup=menu_principal()

        )    # ======================================
    # PERFIL
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "👤 Perfil")
    def perfil(message):

        if not verificar_acesso(bot, message):
            return

        user_id = message.from_user.id

        cursor.execute(
            """
            SELECT

                saldo,
                convidados,
                pix,
                data_cadastro

            FROM usuarios

            WHERE id=?
            """,
            (user_id,)
        )

        usuario = cursor.fetchone()

        if usuario is None:

            bot.reply_to(
                message,
                "Use /start primeiro."
            )

            return

        saldo, convidados, pix, cadastro = usuario

        if pix == "":
            pix = "Não cadastrada"

        texto = f"""
👤 <b>SEU PERFIL</b>

🆔 ID:
<code>{user_id}</code>

💰 Saldo:
<b>R$ {saldo:.2f}</b>

👥 Indicados:
<b>{convidados}</b>

💳 Pix:
<code>{pix}</code>

📅 Cadastro:

{cadastro}
"""

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML",

            reply_markup=menu_principal()

        )

    # ======================================
    # SALDO
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "💰 Saldo")
    def saldo(message):

        if not verificar_acesso(bot, message):
            return

        user_id = message.from_user.id

        cursor.execute(

            """
            SELECT saldo

            FROM usuarios

            WHERE id=?
            """,

            (user_id,)

        )

        saldo = cursor.fetchone()

        if saldo is None:

            bot.reply_to(
                message,
                "Use /start primeiro."
            )

            return

        bot.send_message(

            message.chat.id,

            f"""
💰 <b>SEU SALDO</b>

Saldo disponível:

<b>R$ {saldo[0]:.2f}</b>
""",

            parse_mode="HTML",

            reply_markup=menu_principal()

        )

    # ======================================
    # MEU LINK
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "🔗 Meu Link")
    def meu_link(message):

        if not verificar_acesso(bot, message):
            return

        user_id = message.from_user.id

        username_bot = bot.get_me().username

        link = f"https://t.me/{username_bot}?start=convite_{user_id}"

        texto = f"""
🔗 <b>SEU LINK DE INDICAÇÃO</b>

Compartilhe o link abaixo:

<code>{link}</code>

Cada usuário válido poderá gerar uma recompensa.
"""

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML",

            disable_web_page_preview=True,

            reply_markup=menu_principal()

        )

    # ======================================
    # INDICADOS
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "👥 Indicados")
    def indicados(message):

        if not verificar_acesso(bot, message):
            return

        user_id = message.from_user.id

        cursor.execute(

            """
            SELECT COUNT(*)

            FROM indicacoes

            WHERE indicador=?
            """,

            (user_id,)

        )

        total = cursor.fetchone()[0]

        cursor.execute(

            """
            SELECT COUNT(*)

            FROM indicacoes

            WHERE indicador=?

            AND status='APROVADA'
            """,

            (user_id,)

        )

        aprovadas = cursor.fetchone()[0]

        cursor.execute(

            """
            SELECT COUNT(*)

            FROM indicacoes

            WHERE indicador=?

            AND status='PENDENTE'
            """,

            (user_id,)

        )

        pendentes = cursor.fetchone()[0]

        texto = f"""
👥 <b>SUAS INDICAÇÕES</b>

👤 Total:

<b>{total}</b>

✅ Aprovadas:

<b>{aprovadas}</b>

⏳ Pendentes:

<b>{pendentes}</b>
"""

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML",

            reply_markup=menu_principal()

        )    # ======================================
    # MENU PIX
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "💳 Pix")
    def menu_pix_usuario(message):

        if not verificar_acesso(bot, message):
            return

        user_id = message.from_user.id

        cursor.execute(
            """
            SELECT pix
            FROM usuarios
            WHERE id=?
            """,
            (user_id,)
        )

        usuario = cursor.fetchone()

        if usuario is None:

            bot.reply_to(
                message,
                "Use /start primeiro."
            )

            return

        chave = usuario[0]

        if chave == "":
            chave = "Nenhuma chave cadastrada."

        texto = f"""
💳 <b>ÁREA PIX</b>

Sua chave atual:

<code>{chave}</code>

Escolha uma opção abaixo.
"""

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML",

            reply_markup=menu_pix()

        )

    # ======================================
    # CADASTRAR PIX
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "➕ Cadastrar Pix")
    def cadastrar_pix(message):

        if not verificar_acesso(bot, message):
            return

        bot.send_message(

            message.chat.id,

            """
✍️ Envie sua chave Pix.

Exemplo:

CPF
E-mail
Telefone
Chave Aleatória
"""

        )

        bot.register_next_step_handler(

            message,

            salvar_pix

        )

    # ======================================
    # ALTERAR PIX
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "✏️ Alterar Pix")
    def alterar_pix(message):

        if not verificar_acesso(bot, message):
            return

        bot.send_message(

            message.chat.id,

            "✍️ Envie sua nova chave Pix."

        )

        bot.register_next_step_handler(

            message,

            salvar_pix

        )

    # ======================================
    # VER PIX
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "👁 Ver Pix")
    def ver_pix(message):

        if not verificar_acesso(bot, message):
            return

        user_id = message.from_user.id

        cursor.execute(

            """
            SELECT pix

            FROM usuarios

            WHERE id=?
            """,

            (user_id,)

        )

        usuario = cursor.fetchone()

        if usuario is None:

            bot.reply_to(

                message,

                "Use /start primeiro."

            )

            return

        chave = usuario[0]

        if chave == "":

            chave = "Nenhuma chave cadastrada."

        bot.send_message(

            message.chat.id,

            f"""
💳 <b>SUA CHAVE PIX</b>

<code>{chave}</code>
""",

            parse_mode="HTML",

            reply_markup=menu_pix()

        )

    # ======================================
    # SALVAR PIX
    # ======================================

    def salvar_pix(message):

        if not verificar_acesso(bot, message):
            return

        user_id = message.from_user.id

        chave = message.text.strip()

        if len(chave) < 5:

            bot.reply_to(

                message,

                """
❌ Chave Pix inválida.

Tente novamente.
"""

            )

            return

        cursor.execute(

            """
            UPDATE usuarios

            SET pix=?

            WHERE id=?
            """,

            (

                chave,

                user_id

            )

        )

        conn.commit()

        adicionar_log(

            user_id,

            "PIX",

            "Pix atualizado"

        )

        adicionar_historico(

            user_id,

            "PIX",

            "Cadastro/Alteração da chave Pix",

            0

        )

        bot.send_message(

            message.chat.id,

            """
✅ Chave Pix salva com sucesso.
""",

            reply_markup=menu_principal()

        )

        # A Parte 4 implementará a validação automática
        # da indicação após o cadastro do Pix.    # ======================================
    # HISTÓRICO
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "📜 Histórico")
    def historico(message):

        if not verificar_acesso(bot, message):
            return

        user_id = message.from_user.id

        cursor.execute(
            """
            SELECT

                tipo,
                descricao,
                valor,
                data

            FROM historico

            WHERE usuario=?

            ORDER BY id DESC

            LIMIT 20
            """,
            (user_id,)
        )

        registros = cursor.fetchall()

        if len(registros) == 0:

            bot.send_message(

                message.chat.id,

                """
📜 Você ainda não possui histórico.
""",

                reply_markup=menu_principal()

            )

            return

        texto = "📜 <b>SEU HISTÓRICO</b>\n\n"

        for registro in registros:

            tipo, descricao, valor, data = registro

            texto += f"""
📌 <b>{tipo}</b>

{descricao}

💰 R$ {valor:.2f}

📅 {data}

──────────────────

"""

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML",

            reply_markup=menu_principal()

        )

    # ======================================
    # REGRAS
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "📜 Regras")
    def regras(message):

        if not verificar_acesso(bot, message):
            return

        texto = f"""
📜 <b>REGRAS DO {NOME_BOT}</b>

✅ Apenas uma conta por pessoa.

✅ Auto indicação é proibida.

✅ Fraudes geram banimento.

✅ É obrigatório cadastrar uma chave Pix.

✅ O administrador analisa todos os saques.

💰 Valor por indicação:

<b>R$ {VALOR_INDICACAO:.2f}</b>

💸 Valor mínimo para saque:

<b>R$ {VALOR_MINIMO_SAQUE:.2f}</b>
"""

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML",

            reply_markup=menu_principal()

        )

    # ======================================
    # INFORMAÇÕES
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "ℹ️ Informações")
    def informacoes(message):

        if not verificar_acesso(bot, message):
            return

        texto = f"""
ℹ️ <b>{NOME_BOT}</b>

🤖 Sistema de indicações.

💰 Ganhe convidando amigos.

📞 Suporte:

{SUPORTE}

📦 Versão:

{VERSAO}
"""

        bot.send_message(

            message.chat.id,

            texto,

            parse_mode="HTML",

            reply_markup=menu_principal()

        )

    # ======================================
    # MENU
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "🏠 Menu")
    def menu(message):

        if not verificar_acesso(bot, message):
            return

        bot.send_message(

            message.chat.id,

            """
🏠 <b>MENU PRINCIPAL</b>

Escolha uma opção abaixo.
""",

            parse_mode="HTML",

            reply_markup=menu_principal()

        )    # ======================================
    # ATUALIZAR ÚLTIMO ACESSO
    # ======================================

    def atualizar_ultimo_acesso(user_id):

        cursor.execute(
            """
            UPDATE usuarios

            SET ultimo_acesso=?

            WHERE id=?
            """,
            (
                agora(),
                user_id
            )
        )

        conn.commit()

    # ======================================
    # VERIFICAR PIX
    # ======================================

    def possui_pix(user_id):

        cursor.execute(
            """
            SELECT pix

            FROM usuarios

            WHERE id=?
            """,
            (user_id,)
        )

        usuario = cursor.fetchone()

        if usuario is None:
            return False

        return usuario[0] != ""

    # ======================================
    # TOTAL DE INDICADOS
    # ======================================

    def total_indicados(user_id):

        cursor.execute(
            """
            SELECT COUNT(*)

            FROM indicacoes

            WHERE indicador=?
            """,
            (user_id,)
        )

        return cursor.fetchone()[0]

    # ======================================
    # TOTAL DE INDICAÇÕES APROVADAS
    # ======================================

    def total_aprovadas(user_id):

        cursor.execute(
            """
            SELECT COUNT(*)

            FROM indicacoes

            WHERE indicador=?

            AND status='APROVADA'
            """,
            (user_id,)
        )

        return cursor.fetchone()[0]

    # ======================================
    # ATUALIZAR CONTADOR
    # ======================================

    def atualizar_contador(user_id):

        cursor.execute(
            """
            UPDATE usuarios

            SET convidados=?

            WHERE id=?
            """,
            (
                total_aprovadas(user_id),
                user_id
            )
        )

        conn.commit()

    # ======================================
    # ENVIAR MENU PRINCIPAL
    # ======================================

    def enviar_menu(chat_id):

        bot.send_message(

            chat_id,

            """
🏠 Menu Principal

Escolha uma das opções abaixo.
""",

            reply_markup=menu_principal()

        )

    # ======================================
    # VALIDAÇÃO DE INDICAÇÃO
    # ======================================

    def validar_indicacao_usuario(user_id):

        """
        Esta função será utilizada
        pelo arquivo indicacoes.py.

        Aqui apenas deixamos
        preparada para integração.
        """

        pass

    # ======================================
    # FIM DO MÓDULO
    # ======================================
