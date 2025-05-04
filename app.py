import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'segredo_simples'  # Necessário para usar flash

basedir = os.path.abspath(os.path.dirname(__file__))

CAMINHO_MENSAGENS = os.path.join(basedir, 'data', 'mensagens.json')
CAMINHO_JOGADORES = os.path.join(basedir, 'data', 'jogadores.json')
CAMINHO_JOGOS = os.path.join(basedir, 'data', 'jogos.json')
CAMINHO_ESTATISTICAS = os.path.join(basedir, 'data', 'estatisticas.json')

@app.route('/')
def home():
    return render_template('index.html')

def carregar_estatisticas():
    if os.path.exists(CAMINHO_ESTATISTICAS):
        with open(CAMINHO_ESTATISTICAS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "ranking_valve": "",
        "ranking_world": "",
        "win_rate": ""
    }

def salvar_estatisticas(estatisticas):
    print("Salvando em:", CAMINHO_ESTATISTICAS)
    with open(CAMINHO_ESTATISTICAS, 'w', encoding='utf-8') as f:
        json.dump(estatisticas, f, ensure_ascii=False, indent=4)

@app.route('/mensagens', methods=['GET', 'POST'])
def mensagens():
    mensagem_atual = ''

    if os.path.exists(CAMINHO_MENSAGENS):
        with open(CAMINHO_MENSAGENS, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            mensagem_atual = dados.get('mensagem', '')

    if request.method == 'POST':
        nova_mensagem = request.form.get('mensagem', '').strip()
        if nova_mensagem:
            with open(CAMINHO_MENSAGENS, 'w', encoding='utf-8') as f:
                json.dump({"mensagem": nova_mensagem, "enviado": False}, f, ensure_ascii=False, indent=4)
            flash('✅ Mensagem salva com sucesso! Será enviada para os usuários.')
            return redirect(url_for('mensagens'))

    return render_template('mensagens.html', mensagem_atual=mensagem_atual)

def carregar_jogadores():
    if os.path.exists(CAMINHO_JOGADORES):
        with open(CAMINHO_JOGADORES, 'r', encoding='utf-8') as f:
            return json.load(f)  
    return {}

def salvar_jogadores(jogadores):
    with open(CAMINHO_JOGADORES, 'w', encoding='utf-8') as f:
        json.dump(jogadores, f, ensure_ascii=False, indent=4)

@app.route('/jogadores', methods=['GET', 'POST'])
def jogadores():
    jogadores = carregar_jogadores()

    if request.method == 'POST':
        novo_jogador = {
        "bio": request.form["bio"],
        "foto": request.form["foto"],
        "instagram": f"[{request.form['instagram_nome']}]({request.form['instagram_url']})",
        "twitch": f"[{request.form['twitch_nome']}]({request.form['twitch_url']})"
    }

        # Usamos o nome do jogador como chave no dicionário
        jogadores[request.form["nome"]] = novo_jogador
        salvar_jogadores(jogadores)

        flash("✅ Jogador adicionado com sucesso!")
        return redirect(url_for('jogadores'))

    # Converte o dicionário para uma lista de jogadores
    jogadores_list = [{'nome': nome, **dados} for nome, dados in jogadores.items()]

    return render_template('jogadores.html', jogadores=jogadores_list)

@app.route('/jogadores/editar/<nome>', methods=['GET', 'POST'])
def editar_jogador(nome):
    jogadores = carregar_jogadores()
    jogador = jogadores.get(nome)

    if not jogador:
        flash("❌ Jogador não encontrado.")
        return redirect(url_for('jogadores'))

    if request.method == 'POST':
        jogador["bio"] = request.form["bio"]
        jogador["foto"] = request.form["foto"]
        jogador["instagram"] = request.form["instagram"]
        jogador["twitch"] = request.form["twitch"]
        salvar_jogadores(jogadores)
        flash("✅ Jogador editado com sucesso!")
        return redirect(url_for('jogadores'))

    return render_template('editar_jogador.html', jogador=jogador)

@app.route('/jogadores/excluir/<nome>')
def excluir_jogador(nome):
    jogadores = carregar_jogadores()
    if nome in jogadores:
        del jogadores[nome]
        salvar_jogadores(jogadores)
        flash("🗑️ Jogador excluído.")
    else:
        flash("❌ Jogador não encontrado.")
    return redirect(url_for('jogadores'))

@app.route("/jogos", methods=["GET", "POST"])
def jogos():
    with open(CAMINHO_JOGOS, "r", encoding="utf-8") as f:
        jogos = json.load(f)

    if request.method == "POST":
        nova_descricao = request.form["descricao"]
        novo_link = request.form["link"]
        novo_jogo = {"descricao": nova_descricao, "link": novo_link}
        jogos.append(novo_jogo)
        with open(CAMINHO_JOGOS, "w", encoding="utf-8") as f:
            json.dump(jogos, f, indent=4, ensure_ascii=False)
        return redirect("/jogos")

    return render_template("jogos.html", jogos=jogos)

@app.route("/jogos/editar/<int:id>", methods=["GET", "POST"])
def editar_jogo(id):
    with open(CAMINHO_JOGOS, "r", encoding="utf-8") as f:
        jogos = json.load(f)

    jogo = jogos[id]
    
    if request.method == "POST":
        jogo['descricao'] = request.form['descricao']
        jogo['link'] = request.form['link']
        
        with open(CAMINHO_JOGOS, "w", encoding="utf-8") as f:
            json.dump(jogos, f, indent=4, ensure_ascii=False)
        return redirect("/jogos")

    return render_template("editar_jogo.html", jogo=jogo, id=id)

@app.route("/jogos/excluir/<int:id>", methods=["GET"])
def excluir_jogo(id):
    with open(CAMINHO_JOGOS, "r", encoding="utf-8") as f:
        jogos = json.load(f)

    jogos.pop(id) 
    
    with open(CAMINHO_JOGOS, "w", encoding="utf-8") as f:
        json.dump(jogos, f, indent=4, ensure_ascii=False)

    return redirect("/jogos")

@app.route("/estatisticas", methods=["GET", "POST"])
def editar_estatisticas():
    if request.method == "POST":
        estatisticas = {
            "ranking_valve": request.form.get("ranking_valve", ""),
            "ranking_world": request.form.get("ranking_world", ""),
            "win_rate": request.form.get("win_rate", "")
        }
        salvar_estatisticas(estatisticas)
        return redirect(url_for("editar_estatisticas"))

    estatisticas = carregar_estatisticas()
    return render_template("estatisticas.html", estatisticas=estatisticas)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
