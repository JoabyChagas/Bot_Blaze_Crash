import time
from setup import user, senha


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

valor_aposta = '0,1'
valor_auto_retirar = '1.1'

def fazer_login():
    # apontar o caminho onde será inserido o login e senha do usuário
    caminhoUser = "//input[contains(@name,'username')]"
    caminhoSenha = "//input[@name='password']"

    # escrever o login e senha no caminho
    driver.find_element(By.XPATH, caminhoUser).send_keys(user)
    driver.find_element(By.XPATH, caminhoSenha).send_keys(senha)

    # apontar o caminho do botão 'Entrar' e clicar nele
    caminhoEntrar = "//button[normalize-space()='Entrar']"
    driver.find_element(By.XPATH, caminhoEntrar).click()

def fazer_aposta():
    # aponta o caminho 'Quantia' e inserir o valor da aposta
    caminhoQuantia = "//input[@type='number']"
    quantia = driver.find_element(By.XPATH, caminhoQuantia)
    quantia.send_keys(valor_aposta)

    # apontar o caminho 'Auto Retirar' e inserir o valor para Sair da aposta
    caminhoAutoRetirar = "//input[@data-testid='auto-cashout']"
    AutoRetirar = driver.find_element(By.XPATH, caminhoAutoRetirar)
    AutoRetirar.clear()
    AutoRetirar.send_keys(valor_auto_retirar)

    # apontar o caminho 'Começar o jogo' e clicar nele
    caminhoComecarJogo = "//button[normalize-space()='Começar o jogo']"
    driver.find_element(By.XPATH, caminhoComecarJogo).click()

def pegar_ultimos_resultados():
    # apontar caminho dos ultimos resultados e pegar os elementos
    caminhoUltimosResultados = "//div[@class='entries']"
    ultimosResultados = driver.find_element(By.XPATH,  caminhoUltimosResultados)
    # percorrer últimos resultados retorna o resultados e o texto(valores) de cada elemento
    resultados = ultimosResultados.find_elements(By.TAG_NAME, "span")
    valores = [i.text for i in resultados]
    return resultados, valores

def validar_estrategia(resultados):
    # checando a classe dos resultados
    p0, p1, p2 = (
        resultados[0].get_attribute("class"),
        resultados[1].get_attribute("class"),
        resultados[2].get_attribute("class")
    )
    print(f"{p0} - {resultados[0].text}, {p1} - {resultados[1].text}, {p2} - {resultados[2].text}")
    # estratégia
    if p0 == p1 and p1 == p2:
        return True
    return False

def main():
    fazer_login()
    while True:
        resultados, valores = pegar_ultimos_resultados()
        if validar_estrategia(resultados):
            fazer_aposta()
            break
        time.sleep(0.5)
    input()

if __name__ == '__main__':        
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://blaze.com/pt/games/crash?modal=auth&tab=login')
    main()
    driver.close()
