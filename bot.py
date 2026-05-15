# ==========================================
# IMPORTAÇÕES
# ==========================================
# Selenium e bibliotecas auxiliares para:
# - automação do navegador
# - captura de logs
# - espera inteligente
# - screenshots
# - tratamento de exceções

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
import os
from datetime import datetime

# ==========================================
# CONFIGURAÇÕES GERAIS
# ==========================================
# Credenciais do sistema e configurações principais do robô

EMAIL = "seuemail@"
SENHA = "suasenha"

BASE_URL = "https://www.manuel-scribe.com.br"

# Pastas onde serão armazenados:
# - screenshots dos testes
# - logs de execução
PASTA_SCREENSHOTS = "screenshots"
PASTA_LOGS = "logs"

# Limite máximo de elementos testados
MAX_TESTES = 30

os.makedirs(PASTA_SCREENSHOTS, exist_ok=True)
os.makedirs(PASTA_LOGS, exist_ok=True)

# ==========================================
# CONFIGURAÇÃO DO CHROME
# ==========================================
# Ativa captura de logs:
# - browser console
# - network/performance

chrome_options = Options()

chrome_options.set_capability("goog:loggingPrefs", {
    "browser": "ALL",
    "performance": "ALL"
})

driver = webdriver.Chrome(options=chrome_options)

# Espera inteligente do Selenium
wait = WebDriverWait(driver, 15)

# ==========================================
# SISTEMA DE LOGS
# ==========================================
# Guarda mensagens da execução
# e possíveis erros encontrados

logs_gerais = []
erros_encontrados = []

def log(msg):
    """
    Exibe mensagem no terminal
    e salva no array de logs
    """
    print(msg)
    logs_gerais.append(msg)

def salvar_logs():
    """
    Salva todos os logs em arquivo .txt
    com data e hora da execução
    """

    agora = datetime.now().strftime("%Y%m%d_%H%M%S")

    with open(f"{PASTA_LOGS}/log_{agora}.txt", "w", encoding="utf-8") as f:
        for linha in logs_gerais:
            f.write(linha + "\n")

def screenshot(nome):
    """
    Captura screenshot da tela atual
    """

    try:

        nome = nome.replace("/", "_").replace("\\", "_")

        path = f"{PASTA_SCREENSHOTS}/{nome}.png"

        driver.save_screenshot(path)

    except:
        pass

# ==========================================
# LOGIN AUTOMÁTICO
# ==========================================
# Realiza login procurando:
# - campo email
# - campo senha
# - botão entrar/login

def fazer_login():

    log("🔐 Fazendo login...")

    driver.get(f"{BASE_URL}/auth/login")

    wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "input"))
    )

    inputs = driver.find_elements(By.TAG_NAME, "input")

    email_input = None
    senha_input = None

    for inp in inputs:

        tipo = inp.get_attribute("type")

        if tipo == "email":
            email_input = inp

        if tipo == "password":
            senha_input = inp

    if not email_input or not senha_input:
        raise Exception("Campos de login não encontrados")

    email_input.clear()
    email_input.send_keys(EMAIL)

    senha_input.clear()
    senha_input.send_keys(SENHA)

    botoes = driver.find_elements(By.TAG_NAME, "button")

    for botao in botoes:

        texto = botao.text.lower()

        if "entrar" in texto or "login" in texto:
            botao.click()
            break

    time.sleep(5)

    log("✅ Login realizado")

# ==========================================
# VERIFICAÇÃO DE ERROS NO CONSOLE
# ==========================================
# Captura:
# - warnings
# - erros javascript
# - falhas do navegador

def verificar_console():

    try:

        browser_logs = driver.get_log("browser")

        for entry in browser_logs:

            level = entry["level"]
            message = entry["message"]

            if level in ["SEVERE", "WARNING"]:

                erro = f"[Console][{level}] {message}"

                if erro not in erros_encontrados:

                    erros_encontrados.append(erro)

                    log(f"🚨 {erro}")

    except Exception as e:
        log(f"Erro console: {e}")

# ==========================================
# VERIFICAÇÃO DE REQUESTS HTTP
# ==========================================
# Detecta erros de API e backend:
# - 404
# - 500
# - 422

def verificar_requests():

    try:

        logs = driver.get_log("performance")

        for entry in logs:

            message = entry["message"]

            if "Network.responseReceived" in message:

                if '"status":404' in message:
                    log("🚨 HTTP 404 detectado")

                if '"status":500' in message:
                    log("🚨 HTTP 500 detectado")

                if '"status":422' in message:
                    log("🚨 HTTP 422 detectado")

    except Exception as e:
        log(f"Erro requests: {e}")

# ==========================================
# BUSCA DE ELEMENTOS CLICÁVEIS
# ==========================================
# Procura:
# - botões
# - links
# - elementos com role=button

def pegar_elementos():

    elementos = []

    seletores = [
        "button",
        "a",
        "[role='button']"
    ]

    # Elementos ignorados:
    # - calendário
    # - textos vazios
    # - elementos inúteis
    textos_ignorados = [

        "",

        "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "10", "11", "12", "13", "14", "15", "16",
        "17", "18", "19", "20", "21", "22", "23",
        "24", "25", "26", "27", "28", "29", "30", "31",

        ".", "..", "...",

    ]

    for seletor in seletores:

        encontrados = driver.find_elements(By.CSS_SELECTOR, seletor)

        for e in encontrados:

            try:

                texto = e.text.strip()

                if not texto:
                    texto = e.get_attribute("aria-label")

                if not texto:
                    continue

                texto = texto.strip()

                if texto in textos_ignorados:
                    continue

                # Ignora elementos invisíveis
                if not e.is_displayed():
                    continue

                # Ignora elementos muito pequenos
                size = e.size

                if size["width"] < 20 or size["height"] < 10:
                    continue

                elementos.append((texto, e))

            except:
                pass

    return elementos

# ==========================================
# TESTE DE ELEMENTOS
# ==========================================
# Faz:
# - scroll
# - clique
# - screenshot
# - validação de erros

def testar_elemento(nome):

    try:

        log(f"➡️ Testando: {nome}")

        elementos = pegar_elementos()

        alvo = None

        for texto, elemento in elementos:

            if texto == nome:
                alvo = elemento
                break

        if not alvo:
            return

        # Scroll até o elemento
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            alvo
        )

        time.sleep(1)

        # Primeiro tenta clique normal
        try:
            alvo.click()

        # Se falhar usa JavaScript
        except:
            driver.execute_script(
                "arguments[0].click();",
                alvo
            )

        time.sleep(3)

        # Verificações após clique
        verificar_console()
        verificar_requests()

        log(f"🌐 URL: {driver.current_url}")

        screenshot(nome)

    except Exception as e:

        erro = f"Erro ao testar '{nome}': {str(e)}"

        log(f"🚨 {erro}")

        screenshot(f"erro_{nome}")

# ==========================================
# EXECUÇÃO PRINCIPAL
# ==========================================
# Fluxo geral:
# 1. Abre dashboard
# 2. Faz login se necessário
# 3. Procura elementos
# 4. Testa cada botão/link
# 5. Salva logs e screenshots

try:

    log("➡️ Abrindo dashboard...")

    driver.get(f"{BASE_URL}/dashboard")

    time.sleep(3)

    # Caso seja redirecionado para login
    if "login" in driver.current_url:
        fazer_login()

    time.sleep(5)

    elementos_testados = set()

    contador_testes = 0

    max_ciclos = 1
    ciclos = 0

    while ciclos < max_ciclos:

        log(f"\n🔄 CICLO {ciclos + 1}")

        elementos = pegar_elementos()

        log(f"✅ {len(elementos)} elementos encontrados")

        for texto, _ in elementos:

            if contador_testes >= MAX_TESTES:
                log("🛑 Limite de testes atingido")
                break

            texto_limpo = texto.strip()

            if not texto_limpo:
                continue

            # Evita repetir testes
            if texto_limpo in elementos_testados:
                continue

            # Ignora ações perigosas
            palavras_perigosas = [
                "sair",
                "logout",
                "delete",
                "excluir",
                "remover",
                "apagar"
            ]

            if any(p in texto_limpo.lower() for p in palavras_perigosas):
                log(f"⏭️ Ignorando: {texto_limpo}")
                continue

            elementos_testados.add(texto_limpo)

            testar_elemento(texto_limpo)

            contador_testes += 1

        ciclos += 1

    log("\n🏁 TESTE FINALIZADO")

    log(f"\n✅ Total de elementos testados: {contador_testes}")

    log(f"🚨 Total de erros encontrados: {len(erros_encontrados)}")

    for erro in erros_encontrados:
        log(erro)

finally:

    # Salva logs finais
    salvar_logs()

    time.sleep(3)

    # Fecha navegador
    driver.quit()