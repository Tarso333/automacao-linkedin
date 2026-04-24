# -*- coding: utf-8 -*-
import customtkinter as ctk
import threading
import json
import time
import random
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =========================
# CONFIGURAÇÃO GERAL
# =========================
ARQUIVO_JSON = "dados_linkedin.json"
ARQUIVO_HISTORICO = "historico.json"

# Configuração do visual do CustomTkinter
ctk.set_appearance_mode("dark")  # Outras opções se quiser: "dark", "light", "system"
ctk.set_default_color_theme("blue")  #Outras opções se quiser: "blue", "green", "dark-blue"

# =========================
# LOG
# =========================
def log(msg):
    area_log.insert("end", msg + "\n")
    area_log.see("end")
    logging.info(msg)

# =========================
# UTILIDADES
# =========================
def delay(min=2, max=4):
    time.sleep(random.uniform(min, max))

def salvar_dados():
    # Pega o texto da CTkTextbox (linha 1, coluna 0 até o final)
    empresas = entry_empresas.get("1.0", "end-1c").strip().split("\n")
    empresas = [e.strip() for e in empresas if e.strip()]

    dados = {
        "email": entry_email.get(),
        "senha": entry_senha.get(),
        "empresas": empresas
    }

    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)

def carregar_dados():
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # Preenche os campos se houver dados salvos
        if "email" in dados:
            entry_email.insert(0, dados["email"])
        if "senha" in dados:
            entry_senha.insert(0, dados["senha"])

        empresas = dados.get("empresas", [])
        if empresas:
            entry_empresas.insert("1.0", "\n".join(empresas))
    except Exception:
        pass # Se o arquivo não existir ou der erro, segue a vida

# =========================
# HISTÓRICO
# =========================
def salvar_historico(empresa, status):
    registro = {
        "empresa": empresa,
        "status": status,
        "data": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except:
        dados = []

    dados.append(registro)

    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# =========================
# AUTOMAÇÃO (SELENIUM)
# =========================
def executar():
    salvar_dados()

    with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
        dados = json.load(f)

    email = dados.get("email")
    senha = dados.get("senha")
    empresas = dados.get("empresas", [])

    if not empresas:
        log(" Nenhuma empresa informada!")
        return

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 25)

    try:
        log("Abrindo LinkedIn...")
        driver.get("https://www.linkedin.com/login")

        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
        driver.find_element(By.ID, "password").send_keys(senha)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "global-nav__me"))
        )

        log("✔ Login confirmado")

        for i, empresa in enumerate(empresas, start=1):
            try:
                log(f"\n=== [{i}/{len(empresas)}] {empresa} ===")

                # busca direta
                url = f"https://www.linkedin.com/search/results/companies/?keywords={empresa.replace(' ', '%20')}"
                driver.get(url)

                wait.until(EC.presence_of_element_located((By.XPATH, "//ul")))
                delay(3, 5)

                # primeira empresa
                empresa_link = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "(//a[contains(@href,'/company/')])[1]"))
                )
                empresa_link.click()

                delay(3, 5)

                # botão seguir (robusto)
                try:
                    botao = wait.until(
                        EC.presence_of_element_located((
                            By.XPATH,
                            "//span[text()='Seguir' or text()='Follow']/ancestor::button"
                        ))
                    )

                    driver.execute_script("arguments[0].scrollIntoView(true);", botao)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", botao)

                    log(f"✔ Seguindo: {empresa}")
                    salvar_historico(empresa, "Seguindo")

                except:
                    log(f"ℹ Já segue ou botão não encontrado: {empresa}")
                    salvar_historico(empresa, "Já seguia")

                delay(2, 4)

            except Exception as e:
                log(f"Erro na empresa: {empresa}")
                log(str(e))
                salvar_historico(empresa, "Erro")
                continue

        log("\n✔ Processo finalizado com sucesso!")

    except Exception as e:
        log(f"ERRO GERAL: {str(e)}")

    finally:
        driver.quit()
        log("Navegador fechado")

# =========================
# THREAD
# =========================
def iniciar():
    log("Iniciando robô...")
    # Cria uma thread para o Selenium rodar sem congelar a interface
    t = threading.Thread(target=executar)
    t.daemon = True 
    t.start()

# =========================
# INTERFACE GRÁFICA (CTK)
# =========================
janela = ctk.CTk()
janela.title("Robô LinkedIn")
janela.geometry("1024x760")

# 1. Título
titulo = ctk.CTkLabel(janela, text="Informe os dados ao Robô", font=("Segoe UI", 24, "bold"))
titulo.pack(pady=(30, 20))

# 2. Campos de Entrada (Email e Senha)
entry_email = ctk.CTkEntry(janela, placeholder_text="Digite seu e-mail do LinkedIn", width=400, height=40)
entry_email.pack(pady=(0, 15))

entry_senha = ctk.CTkEntry(janela, placeholder_text="Digite sua Senha", show="*", width=400, height=40)
entry_senha.pack(pady=(0, 20))

# 3. Campo de Empresas
label_empresas = ctk.CTkLabel(janela, text="Empresas (uma por linha):", font=("Segoe UI", 12))
label_empresas.pack(anchor="w", padx=100)

entry_empresas = ctk.CTkTextbox(janela, width=400, height=120)
entry_empresas.pack(pady=(0, 20))

# 4. Botão Iniciar
btn_iniciar = ctk.CTkButton(
    janela, 
    text="INICIAR ROBÔ", 
    command=iniciar, 
    width=400, 
    height=45, 
    font=("Segoe UI", 14, "bold"),
    fg_color="#005582", # Um tom de azul estilo LinkedIn
    hover_color="#003e5e"
)
btn_iniciar.pack(pady=(0, 30))

# 5. Área de Logs
label_logs = ctk.CTkLabel(janela, text="Logs de Execução:", font=("Segoe UI", 12))
label_logs.pack(anchor="w", padx=100)

area_log = ctk.CTkTextbox(janela, width=400, height=180, text_color="#00ff9c", font=("Consolas", 12))
area_log.pack(pady=(0, 20))

# 6. Carregar Dados Salvos
carregar_dados()

# 7. Iniciar a Janela
janela.mainloop()