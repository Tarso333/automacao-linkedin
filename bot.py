from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

browser = webdriver.Chrome()
browser.get("https://www.linkedin.com/login")

wait = WebDriverWait(browser, 20)

# campo email
input_email = wait.until(
    EC.presence_of_element_located((By.ID, "username"))
)
input_email.send_keys("seuemail@aqui")

# campo senha
input_senha = browser.find_element(By.ID, "password")
input_senha.send_keys("suasenha_aqui")

# botão login
btn_login = browser.find_element(By.XPATH, "//button[@type='submit']")
btn_login.click()

# pausa para CAPTCHA
input("Resolva o CAPTCHA e pressione ENTER...")

# clicar no botão de busca
botao_busca = wait.until(
    EC.element_to_be_clickable((By.CLASS_NAME, "search-global-typeahead__collapsed-search-button"))
)
botao_busca.click()

# campo de busca
busca = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Pesquisar']"))
)

busca.send_keys("Tribunal Regional Federal da 1ª Região")
busca.send_keys(Keys.RETURN)

# aguardar resultados carregarem
time.sleep(3)

# clicar no filtro "Empresas"
filtro_empresas = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//label[contains(text(),'Empresas')]"))
)
filtro_empresas.click()

# aguardar carregar resultados filtrados
time.sleep(3)

# clicar no botão "Seguir"
seguir = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label,'Seguir Tribunal Regional Federal da 1ª Região')]"))
)
seguir.click()

input("Pressione ENTER para fechar...")