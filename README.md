# 🤖 Robô de Automação LinkedIn

Automação desenvolvida em Python utilizando Selenium para buscar empresas no LinkedIn e segui-las automaticamente, com interface gráfica e registro de histórico das ações.

---

## 📌 Funcionalidades

* 🔐 Login automatizado no LinkedIn
* 🔎 Busca de empresas por nome
* 🏢 Acesso automático à página da empresa
* ➕ Ação de seguir empresas
* 🧠 Tratamento de erros durante execução
* 💾 Salvamento de dados do usuário
* 📊 Registro de histórico das ações (JSON)
* 🖥️ Interface gráfica com logs em tempo real

---

## 🛠️ Tecnologias Utilizadas

* Python 3
* Selenium WebDriver
* Tkinter (interface gráfica)
* JSON (armazenamento de dados)

---

## 📁 Estrutura do Projeto

```
bot-linkedin/
├── bot.py
├── dados_linkedin.json
├── historico.json
```

---

## ⚙️ Como Executar

1. Instale as dependências:

```
pip install selenium
```

2. Baixe o ChromeDriver compatível com seu navegador.

3. Execute o projeto:

```
python bot.py
```

---

## 🧾 Como Utilizar

1. Insira seu e-mail e senha do LinkedIn
2. Informe as empresas (uma por linha)
3. Clique em **"Iniciar Robô"**
4. Acompanhe os logs em tempo real

---

## 📊 Histórico de Execução

O robô salva automaticamente um arquivo `historico.json` com:

* Nome da empresa
* Status da ação (Seguindo, Já seguia, Erro)
* Data e hora

---

## ⚠️ Observações

* O LinkedIn pode solicitar CAPTCHA
* Uso excessivo pode levar a bloqueios temporários
* Utilize com moderação

---

## 🚀 Melhorias Futuras

* Validação do nome exato da empresa
* Evitar ações repetidas
* Exportação para CSV/Excel
* Dashboard de resultados

---

## 👨‍💻 Autor

Projeto desenvolvido para fins de aprendizado em automação (RPA) e integração com interfaces web.

---
