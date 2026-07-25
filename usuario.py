import telebot

from datetime import datetime

from config import *
from database import conn, cursor
from teclado import *

# ==========================================
# REGISTRAR COMANDOS DO USUÁRIO
# ==========================================

def registrar_usuario(bot):

    # ======================================
    # START
    # ======================================

    @bot.message_handler(commands=["start"])
    def start(message):

        user_id = message.from_user.id
        nome = message.from_user.first_name

        if message.from_user.username:
            username = "@" + message.from_user.username
        else:
            username = "Não possui"

        cursor.execute(
            "SELECT * FROM usuarios WHERE id=?",
            (user_id,)
        )

        usuario = cursor.fetchone()

        # ==================================
        # USUÁRIO NOVO
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

            # ==================================
            # ANTI AUTO INDICAÇÃO
            # ==================================

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

            conn.commit()

            # ==================================
            # REGISTRAR INDICAÇÃO
            # ==================================

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

                    VALUES(?,?,?,?,?)
                    """,
                    (
                        convidado_por,
                        user_id,
                        0,
                        "PENDENTE",
                        datetime.now().strftime(
                            "%d/%m/%Y %H:%M"
                        )
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
                    datetime.now().strftime(
                        "%d/%m/%Y %H:%M"
                    ),
                    user_id
                )
            )

            conn.commit()

        texto = f"""
🎉 <b>Bem-vindo {nome}!</b>

💰 Ganhe dinheiro indicando amigos.

Use os botões abaixo para navegar.
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

        if not usuario:
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

🆔 ID: <code>{user_id}</code>

💰 Saldo:
R$ {saldo:.2f}

👥 Indicados:
{convidados}

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
            """
            SELECT saldo
            FROM usuarios
            WHERE id=?
            """,
            (user_id,)
        )

        usuario = cursor.fetchone()

        if not usuario:
            bot.reply_to(
                message,
                "Use /start primeiro."
            )
            return

        bot.send_message(
            message.chat.id,
            f"💰 Seu saldo é de R$ {usuario[0]:.2f}",
            reply_markup=menu_principal()
        )

    # ======================================
    # MEU LINK
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "🔗 Meu Link")
    def meu_link(message):

        user_id = message.from_user.id

        bot_username = bot.get_me().username

        link = (
            f"https://t.me/"
            f"{bot_username}"
            f"?start=convite_{user_id}"
        )

        texto = f"""
🔗 <b>Seu link de indicação</b>

Compartilhe este link com seus amigos.

<code>{link}</code>
"""

        bot.send_message(
            message.chat.id,
            texto,
            parse_mode="HTML",
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
👥 <b>INDICAÇÕES</b>

Total:
{total}

✅ Aprovadas:
{aprovadas}

⏳ Pendentes:
{pendentes}
"""

        bot.send_message(
            message.chat.id,
            texto,
            parse_mode="HTML",
            reply_markup=menu_principal()
        )    # ======================================
    # PIX
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "💳 Pix")
    def pix_menu(message):

        user_id = message.from_user.id

        cursor.execute(
            "SELECT pix FROM usuarios WHERE id=?",
            (user_id,)
        )

        usuario = cursor.fetchone()

        if not usuario:
            bot.reply_to(
                message,
                "Use /start primeiro."
            )
            return

        pix = usuario[0]

        if pix == "":
            pix = "Nenhuma chave cadastrada."

        texto = f"""
💳 <b>PIX</b>

Sua chave atual:

<code>{pix}</code>

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
            "Envie sua chave Pix."
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
            "Envie a nova chave Pix."
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

        if not usuario:
            bot.reply_to(
                message,
                "Use /start primeiro."
            )
            return

        pix = usuario[0]

        if pix == "":
            pix = "Nenhuma chave cadastrada."

        bot.send_message(
            message.chat.id,
            f"💳 Sua chave Pix:\n\n<code>{pix}</code>",
            parse_mode="HTML",
            reply_markup=menu_pix()
        )


    # ======================================
    # SALVAR PIX
    # ======================================

    def salvar_pix(message):

        user_id = message.from_user.id

        chave = message.text.strip()

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

✅ O usuário indicado deve cumprir
os requisitos para validar a indicação.

✅ Tentativas de fraude resultam
em bloqueio permanente.

✅ O saque será analisado
pela administração.
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

        texto = """
ℹ️ <b>INFORMAÇÕES</b>

💰 Ganhe indicando amigos.

👥 Convide pessoas usando
seu link exclusivo.

💳 Cadastre sua chave Pix.

💸 Solicite seu saque
quando atingir o valor mínimo.

Boa sorte!
"""

        bot.send_message(
            message.chat.id,
            texto,
            parse_mode="HTML",
            reply_markup=menu_principal()
        )    # ======================================
    # VALIDAR INDICAÇÕES
    # ======================================

    def validar_indicacao(user_id):

        cursor.execute(
            """
            SELECT
            convidado_por,
            pix
            FROM usuarios
            WHERE id=?
            """,
            (user_id,)
        )

        usuario = cursor.fetchone()

        if not usuario:
            return

        indicador, pix = usuario

        if indicador is None:
            return

        # PIX obrigatório
        if pix == "":
            return

        # Verifica se já foi aprovada
        cursor.execute(
            """
            SELECT status
            FROM indicacoes
            WHERE indicado=?
            """,
            (user_id,)
        )

        registro = cursor.fetchone()

        if not registro:
            return

        if registro[0] == "APROVADA":
            return

        # Valor da recompensa
        cursor.execute(
            """
            SELECT valor
            FROM configuracoes
            WHERE chave='valor_indicacao'
            """
        )

        config = cursor.fetchone()

        if config:
            recompensa = float(config[0])
        else:
            recompensa = 1.00

        # Aprova indicação
        cursor.execute(
            """
            UPDATE indicacoes
            SET recompensa=?,
                status='APROVADA'
            WHERE indicado=?
            """,
            (
                recompensa,
                user_id
            )
        )

        # Soma saldo ao indicador
        cursor.execute(
            """
            UPDATE usuarios
            SET saldo = saldo + ?,
                convidados = convidados + 1
            WHERE id=?
            """,
            (
                recompensa,
                indicador
            )
        )

        # Histórico
        cursor.execute(
            """
            INSERT INTO historico(
                usuario,
                tipo,
                descricao,
                valor,
                data
            )
            VALUES(?,?,?,?,?)
            """,
            (
                indicador,
                "INDICACAO",
                "Bônus por indicação",
                recompensa,
                datetime.now().strftime("%d/%m/%Y %H:%M")
            )
        )

        conn.commit()

        # Notifica o indicador
        try:

            bot.send_message(

                indicador,

                f"""
🎉 Parabéns!

Sua indicação foi validada.

💰 Você recebeu
R$ {recompensa:.2f}

O valor já foi adicionado ao seu saldo.
"""

            )

        except:
            pass


    # ======================================
    # MENU
    # ======================================

    @bot.message_handler(func=lambda m: m.text == "🏠 Menu")
    def voltar_menu(message):

        bot.send_message(

            message.chat.id,

            """
🏠 Menu Principal

Escolha uma opção abaixo.
""",

            reply_markup=menu_principal()

        )


    # ======================================
    # CHAMAR VALIDAÇÃO
    # ======================================

    @bot.message_handler(func=lambda m: True)
    def verificar_usuario(message):

        validar_indicacao(
            message.from_user.id
        )
