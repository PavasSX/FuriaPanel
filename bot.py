import json
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ==================== CONFIGURAÇÕES DE CAMINHO PARA ARQUIVOS JSON ====================
USUARIOS_CAMINHO = 'data/usuarios.json'
MENSAGENS_CAMINHO = 'data/mensagens.json'
JOGADORES_CAMINHO = 'data/jogadores.json'
JOGOS_CAMINHO = 'data/jogos.json'
CAMINHO_ESTATISTICAS = 'data/estatisticas.json'


# ==================== TOKEN DO BOT TELEGRAM ==================== #
TOKEN = os.getenv("TOKEN_TG")

# ==================== FUNÇÕES AUXILIARES ==================== #
def carregar_usuarios():
    try:
        if os.path.exists(USUARIOS_CAMINHO):
            with open(USUARIOS_CAMINHO, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar usuários: {e}")
    return []

def salvar_usuarios(lista_ids):
    try:
        with open(USUARIOS_CAMINHO, 'w', encoding='utf-8') as f:
            json.dump(lista_ids, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar usuários: {e}")

def carregar_json(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar {caminho}: {e}")
    return {}

def ler_estatisticas():
    if os.path.exists(CAMINHO_ESTATISTICAS):
        with open(CAMINHO_ESTATISTICAS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# ==================== CARREGAR DADOS ==================== #
JOGADORES = carregar_json(JOGADORES_CAMINHO)
JOGOS = carregar_json(JOGOS_CAMINHO)

# ==================== COMANDOS ==================== #
def teclado_menu_principal():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 Próximos Jogos", callback_data='jogos')],
        [InlineKeyboardButton("👥 Jogadores", callback_data='jogadores')],
        [InlineKeyboardButton("📊 Estatísticas", callback_data='estatisticas')],
        [InlineKeyboardButton("🛍 Loja", callback_data='loja')]
    ])


# ==================== SALVA O ID DO USUÁRIO PARA MENSAGENS AUTOMÁTICAS ==================== #
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    usuarios = carregar_usuarios()
    if user_id not in usuarios:
        usuarios.append(user_id)
        salvar_usuarios(usuarios)

    await update.message.reply_text(
        """
🔥 Fala, TORCEDOR! 🔥

Bem-vindo ao time! Você acaba de entrar no lugar certo.🐾💛🖤

Aqui, você vai ficar por dentro de tudo que rola na FURIA — jogos, jogadores, estatísticas e ainda poder conferir nossa loja oficial para vestir o manto com muito orgulho! 🛍️

🔫 Prepare-se para se emocionar com cada jogada épica, cada vitória suada e cada momento inesquecível! O CS é nossa casa, e você agora faz parte dela!

👉 Vamos juntos nessa jornada? Escolha o que você quer acompanhar e bora agitar!

Vamo FURIA!""",
        reply_markup=teclado_menu_principal()
    )

# ==================== JOGADORES ==================== #
async def mostrar_jogadores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(j.upper(), callback_data=f"j_{j}")] for j in JOGADORES]
    keyboard.append([InlineKeyboardButton("Voltar ao menu principal", callback_data='voltar_menu_inicial')])
    await update.callback_query.message.reply_text("👥 Escolha um jogador:", reply_markup=InlineKeyboardMarkup(keyboard))

async def mostrar_detalhes_jogador(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jogador = update.callback_query.data[2:]
    if jogador in JOGADORES:
        dados = JOGADORES[jogador]
        media = InputMediaPhoto(
            dados["foto"],
            caption=f"{dados['bio']}\n\n📷 Instagram - {dados['instagram']}\n🟣 Twitch - {dados['twitch']}\n\nSiga [@furiagg](https://www.instagram.com/furiagg/) 🐾💛🖤",
            parse_mode='Markdown'
        )
        keyboard = [
            [InlineKeyboardButton("Voltar à Seleção de Jogadores", callback_data='voltar_jogadores')],
            [InlineKeyboardButton("Voltar ao menu principal", callback_data='voltar_menu_inicial')]
        ]
        await update.callback_query.answer()
        await update.callback_query.edit_message_media(media=media, reply_markup=InlineKeyboardMarkup(keyboard))

# ==================== BOTÕES ==================== #
async def voltar_menu_inicial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("🔥 Voltamos pro lobby! Escolhe aí o próximo passo e segue com a tropa!", reply_markup=teclado_menu_principal())

async def voltar_jogadores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await mostrar_jogadores(update, context)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    if data == 'jogos':
        msg = "\n\n".join([
            f"📅 {j['descricao']}\n🎥 [Assistir]({j['link']})"
            for j in JOGOS
        ])

        keyboard = [
            [InlineKeyboardButton("Voltar ao menu principal", callback_data='voltar_menu_inicial')]
        ]

        await update.callback_query.edit_message_text(
            text=msg,
            parse_mode='Markdown', 
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == 'jogadores':
        await mostrar_jogadores(update, context)
    elif data.startswith("j_"):
        await mostrar_detalhes_jogador(update, context)
    elif data == 'estatisticas':
        estatisticas = ler_estatisticas()
        if estatisticas:
            mensagem = (
                f"📈 <b>Estatísticas da FURIA</b>\n\n"
                f"🏆 <b>Ranking Valve:</b> {estatisticas.get('ranking_valve', 'N/A')}\n"
                f"🌍 <b>World Ranking:</b> {estatisticas.get('ranking_world', 'N/A')}\n"
                f"🔥 <b>Win Rate:</b> {estatisticas.get('win_rate', 'N/A')}"
            )

            keyboard = [
                [InlineKeyboardButton("Voltar ao menu principal", callback_data='voltar_menu_inicial')]
            ]
            # Enviando a mensagem com o botão
            await update.callback_query.edit_message_text(
                text=mensagem, 
                parse_mode='HTML', 
                reply_markup=InlineKeyboardMarkup(keyboard) 
            )

        else:
            mensagem = "❌ Não foi possível carregar as estatísticas."
            await update.callback_query.edit_message_text(text=mensagem, parse_mode='HTML')
    
    elif data == 'loja':
        keyboard = [
            [InlineKeyboardButton("🛍 Acessar Loja", url='https://www.furia.gg')],
            [InlineKeyboardButton("Voltar ao menu principal", callback_data='voltar_menu_inicial')]
        ]
        await update.callback_query.edit_message_text(
            text="""🛍 LOJA OFICIAL DA FURIA

Aqui é paixão, é raça, é FURIA na pele e no coração!

Chegou a hora de mostrar pro mundo que você é da matilha!

Camisas insanas, bonés estilosos, acessórios irados... tudo pra deixar o look no pique da elite do CS.
Não importa se é dia de jogo ou rolê com os amigos — quem é FURIA, veste a camisa em qualquer lugar!

🐾 Clica no botão e já garante o teu.
💛🖤 Vem com a gente... FURIA É VIBE!""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == 'voltar_menu_inicial':
        await voltar_menu_inicial(update, context)
    elif data == 'voltar_jogadores':
        await voltar_jogadores(update, context)

# ==================== MENSAGENS PARA TODOS OS USUÁRIOS ==================== #
async def verificar_mensagens_periodicamente(app):
    while True:
        if os.path.exists(MENSAGENS_CAMINHO):
            try:
                with open(MENSAGENS_CAMINHO, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    nova_mensagem = dados.get("mensagem", "").strip()

                    if nova_mensagem and not dados.get("enviado", False):
                        print("🟡 Nova mensagem encontrada. Enviando para todos os usuários...")

                        for user_id in carregar_usuarios():
                            try:
                                await app.bot.send_message(chat_id=user_id, text=nova_mensagem)
                            except Exception as e:
                                print(f"Erro ao enviar para {user_id}: {e}")

                        dados["enviado"] = True
                        with open(MENSAGENS_CAMINHO, 'w', encoding='utf-8') as f:
                            json.dump(dados, f, ensure_ascii=False, indent=4)
                        print("✅ Mensagem enviada e marcada como entregue.")
            except Exception as e:
                print(f"Erro ao verificar mensagens: {e}")
        await asyncio.sleep(5)

# ==================== INICIALIZAÇÃO DO BOT ==================== #
async def main():
    if not TOKEN:
        print("❌ TOKEN não definido.")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot rodando... Pressione Ctrl+C para parar.")
    asyncio.create_task(verificar_mensagens_periodicamente(app))
    await app.run_polling()

if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
