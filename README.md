# Painel de Gerenciamento do Bot da FURIA 🎮

Este projeto consiste em um painel web feito com Flask que permite gerenciar mensagens, jogadores e conteúdo dinâmico de um bot da FURIA no Telegram.

---

## 📌 Funcionalidades

* 🔧 **Painel Flask**:

  * Editar e excluir jogadores.
  * Envio de mensagens dinamicas para todos usuários que interagiram com o bot.
  * Interface simples e direta para controle do conteúdo exibido pelo bot.
  * Verificação no site da HLTV para modificação de estátiscas manuais.

* 🤖 **Bot Telegram**:

  * Envia mensagens pré-configuradas.
  * Usa teclado inline para facilitar interação dos usuários.


## 💪 Tecnologias Utilizadas

* Python 3.10+
* Flask
* python-telegram-bot
* HTML + CSS (interface do painel)

---

## 🚀 Como usar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Adicione variáveis de ambiente (como token do bot)

Crie um arquivo `.env` (ou configure manualmente no seu ambiente) com:

```
BOT_TOKEN=seu_token_aqui
```

### 5. Rode a aplicação

```bash
python app.py  # ou bot.py, conforme desejado
```

---

## 📁 Estrutura do Projeto

```
.
├── app.py                # Painel em Flask
├── bot.py                # Bot Telegram
├── templates/            # HTMLs do painel
├── static/               # CSS e imagens
├── data/        # Base de dados
├── requirements.txt
└── README.md
```

---

## ✍️ Contribuindo

Pull requests são bem-vindos! Sinta-se à vontade para abrir uma issue com sugestões ou melhorias.

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
