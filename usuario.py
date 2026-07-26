import telebot

from datetime import datetime

from config import *
from database import conn, cursor
from teclado import menu_principal, menu_pix
from indicacoes import validar_indicacao

# ==========================================
# REGISTRAR MÓDULO USUÁRIO
# ==========================================

def registrar_usuario(bot):

    # ======================================
    # START
    # ======================================

    @bot.message_handler(commands=["start"])
    def start(message):

        user_id = message.from_user.id
        nome = message.from_user.first_name

        username = (
            "@" + message.from_user.username
            if message.from_user.username
            else "Não possui"
        )

        cursor.execute(
            "SELECT id FROM usuarios WHERE id=?",
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
                    data_cadastro,
                    ultimo_acesso

                )

                VALUES(

                    ?,?,?,?,?,?,?,?,?,?

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
                    datetime.now().strftime("%d/%m/%Y %H:%M"),
                    datetime.now().strftime("%d/%m/%Y %H:%M")

                )

            )

            # Registrar indicação

            if convidado_por:

                cursor.execute(
                    """
                    INSERT INTO indicacoes(

                        indicador,
                        indicado,
                        recompensa,
                        status,
                        data

                    )

                    VALUES(

                        ?,?,?,?,?

                    )
                    """,
                    (
                        convidado_por,
                        user_id,
                        0,
                        "PENDENTE",
                        datetime.now().strftime("%d/%m/%Y %H:%M")
                    )
                )

            conn.commit()

        else:

            cursor.execute(
                """
                UPDATE usuarios

                SET ultimo_acesso=?

                WHERE id=?
                """,
                (
                    datetime.now().strftime("%d/%m/%Y %H:%M"),
                    user_id
                )
            )

            conn.commit()

        texto = f"""
🎉 <b>Bem-vindo, {nome}!</b>

💰 Convide seus amigos e ganhe dinheiro.

Escolha uma opção no menu abaixo.
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

        if not pix:
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

        user_id = message.from_user.id

        cursor.execute(

            "SELECT saldo FROM usuarios WHERE id=?",

            (user_id,)

        )

        usuario = cursor.fetchone()

        if usuario is None:

            bot.reply_to(
                message,
                "Use /start primeiro."
            )

            return

        bot.send_message(

            message.chat.id,

            f"""
💰 <b>Seu saldo atual</b>

R$ {usuario[0]:.2f}
""",

            parse_mode="HTML",

            reply_markup=menu_principal()

        )

    # ======================================
    # LINK DE INDICAÇÃO
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "🔗 Meu Link")
    def meu_link(message):

        user_id = message.from_user.id

        username_bot = bot.get_me().username

        link = (
            f"https://t.me/"
            f"{username_bot}"
            f"?start=convite_{user_id}"
        )

        texto = f"""
🔗 <b>Seu link de indicação</b>

Compartilhe este link:

<code>{link}</code>

Cada indicação válida poderá gerar recompensa.
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

        user_id = message.from_user.id

        cursor.execute(
            """
            SELECT

            COUNT(*)

            FROM indicacoes

            WHERE indicador=?
            """,
            (user_id,)
        )

        total = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT

            COUNT(*)

            FROM indicacoes

            WHERE indicador=?

            AND status='APROVADA'
            """,
            (user_id,)
        )

        aprovadas = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT

            COUNT(*)

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

        user_id = message.from_user.id

        cursor.execute(
            "SELECT pix FROM usuarios WHERE id=?",
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
💳 <b>PIX</b>

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

        bot.send_message(
            message.chat.id,
            "✍️ Envie sua chave Pix:"
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

        bot.send_message(
            message.chat.id,
            "✍️ Envie a nova chave Pix:"
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

        user_id = message.from_user.id

        cursor.execute(
            "SELECT pix FROM usuarios WHERE id=?",
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
            f"💳 Sua chave Pix:\n\n<code>{chave}</code>",
            parse_mode="HTML",
            reply_markup=menu_pix()
        )

    # ======================================
    # SALVAR PIX
    # ======================================

    def salvar_pix(message):

        user_id = message.from_user.id

        chave = message.text.strip()

        if len(chave) < 5:

            bot.reply_to(
                message,
                "❌ Chave Pix inválida."
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

        # Valida indicação automaticamente
        validar_indicacao(bot, user_id)

        bot.send_message(
            message.chat.id,
            "✅ Chave Pix salva com sucesso!",
            reply_markup=menu_principal()
        )

    # ======================================
    # REGRAS
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "📜 Regras")
    def regras(message):

        texto = """
📜 <b>REGRAS</b>

✅ Apenas uma conta por pessoa.

✅ Autoindicação é proibida.

✅ É obrigatório cadastrar uma chave Pix.

✅ O administrador analisa todos os saques.

✅ Tentativas de fraude resultam em bloqueio.
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

        texto = f"""
ℹ️ <b>{NOME_BOT}</b>

💰 Valor por indicação:
R$ {VALOR_INDICACAO:.2f}

💸 Saque mínimo:
R$ {VALOR_MINIMO_SAQUE:.2f}

📞 Suporte:
{SUPORTE}

Versão:
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

        bot.send_message(
            message.chat.id,
            "🏠 Menu Principal",
            reply_markup=menu_principal()
        )
