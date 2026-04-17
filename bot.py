# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import scrolledtext
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
# CONFIG
# =========================
ARQUIVO_JSON = "dados_linkedin.json"
ARQUIVO_HISTORICO = "historico.json"

# =========================
# LOG
# =========================
def log(msg):
    area_log.insert(tk.END, msg + "\n")
    area_log.see(tk.END)
    logging.info(msg)

# =========================
# UTIL
# =========================
def delay(min=2, max=4):
    time.sleep(random.uniform(min, max))

def salvar_dados():
    empresas = entry_empresas.get("1.0", tk.END).strip().split("\n")
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

        entry_email.insert(0, dados.get("email", ""))
        entry_senha.insert(0, dados.get("senha", ""))

        empresas = dados.get("empresas", [])
        entry_empresas.insert("1.0", "\n".join(empresas))
    except:
        pass

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
# AUTOMAÇÃO
# =========================
def executar():
    salvar_dados()

    with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
        dados = json.load(f)

    email = dados.get("email")
    senha = dados.get("senha")
    empresas = dados.get("empresas", [])

    if not empresas:
        log("Nenhuma empresa informada!")
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

        log("Login confirmado")

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
                    log(f"Já segue ou botão não encontrado: {empresa}")
                    salvar_historico(empresa, "Já seguia")

                delay(2, 4)

            except Exception as e:
                log(f" Erro na empresa: {empresa}")
                log(str(e))
                salvar_historico(empresa, "Erro")
                continue

        log("✔ Finalizado com sucesso")

    except Exception as e:
        log(f"ERRO GERAL: {str(e)}")

    finally:
        driver.quit()
        log("Navegador fechado")

# =========================
# THREAD
# =========================
def iniciar():
    threading.Thread(target=executar, daemon=True).start()

# =========================
# INTERFACE
# =========================
janela = tk.Tk()
janela.title("Robô LinkedIn")
janela.geometry("520x650")
janela.configure(bg="#f4f6f8")

frame = tk.Frame(janela, bg="#f4f6f8")
frame.pack(pady=10)

tk.Label(frame, text="Automação LinkedIn", font=("Segoe UI", 16, "bold"), bg="#f4f6f8").pack(pady=10)

def label(text):
    return tk.Label(frame, text=text, bg="#f4f6f8", anchor="w")

def entry(show=None):
    return tk.Entry(frame, width=42, relief="solid", bd=1, show=show)

label("Email").pack(anchor="w")
entry_email = entry()
entry_email.pack(pady=5)

label("Senha").pack(anchor="w")
entry_senha = entry(show="*")
entry_senha.pack(pady=5)

label("Empresas (uma por linha)").pack(anchor="w")
entry_empresas = tk.Text(frame, width=42, height=6)
entry_empresas.pack(pady=5)

tk.Button(
    frame,
    text="INICIAR ROBÔ",
    command=iniciar,
    bg="#0A66C2",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    padx=10,
    pady=5
).pack(pady=10)

area_log = scrolledtext.ScrolledText(
    frame,
    width=60,
    height=15,
    bg="#1e1e1e",
    fg="#00ff9c",
    insertbackground="white",
    font=("Consolas", 9)
)
area_log.pack(pady=10)

carregar_dados()

janela.mainloop()