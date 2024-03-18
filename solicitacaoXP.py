from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

# print("----------------------------------------------------------------")
# print("Bem vindo ao robô de solicitações de cotações na XP. Forneça os dados para seguir com a operação!")
# print("----------------------------------------------------------------")

def solicitarCotacao(nbXP, nomeCliente, dataFormatada, usuario, senha, xpToken):

    # nbCliente = 325461

    # Pega a cotação do cliente em questão
    xpDados = pd.read_excel(f"Cotação {nomeCliente} - XP {nbXP} - {dataFormatada}.xlsx")
    xpDados = xpDados.drop(columns=[col for col in xpDados.columns if 'Unnamed: ' in col])

    # Determina um array com os ativos sem cotação para serem solicitados
    ativosSemCot = []

    # Cria um dicionário com os ativos sem cotação para serem solicitados
    for cod in xpDados['CÓD VIRTUAL']:
        # Procura a linha do ativo
        res = xpDados.loc[xpDados["CÓD VIRTUAL"] == cod]
        linAtivo = res.index[0]
        status = xpDados.loc[linAtivo, "ÁGIO/DESÁGIO"]
        qtd = xpDados.loc[linAtivo, "QTD"]
        ativo = xpDados.loc[linAtivo, "ATIVO"]
        if status == "Solicitar Cotação":
            ativosSemCot.append([ativo, qtd])

    print(ativosSemCot)

    # ativoTeste = ['CRI CONSTRUTORA TENDA - ABR/2028', 38]

    # if ativoTeste in ativosSemCot:
    #     index = ativosSemCot.index(ativoTeste)
    #     print(ativosSemCot[index])

    # # Pega o nome do usuário
    # usuario = 'FELIPE.GCA63276'

    # # Pega a senha do usuário
    # senha = 'VenetoRF12'

    # Pega o token do usuário
    # token = input("Digite o token: ")

    # Determina as opções do driver
    service = Service(executable_path='./chromedriver.exe')
    options = webdriver.ChromeOptions()

    # Inicializar o WebDriver do Chrome
    driver = webdriver.Chrome(service=service, options=options)

    # Abrir o site de login
    driver.get("https://hub.xpi.com.br/dashboard-ws/#/performance")

    # Aguardar um pouco para que o processo de login seja concluído
    time.sleep(5)

    # Localizar os campos de entrada (geralmente por meio de seus IDs, nomes ou outros seletotes)
    userField = driver.find_element("name","Username")
    passField = driver.find_element("name","Password")
    tokenField = driver.find_element("name","Token")
    botaoLogin = driver.find_element("id","btnEntrar")

    # Preencher os campos de entrada
    userField.send_keys(usuario)
    passField.send_keys(senha)
    tokenField.send_keys(xpToken)

    botaoLogin.click()

    # Aguardar um pouco para que o processo de login seja concluído
    time.sleep(5)

    #Navega para a página de posições RF
    driver.get("http://hub.xpi.com.br/renda-fixa-gerencial/#/posicoes")

    # Determina o tempo de espera pelo carregamento de um elemento
    wait = WebDriverWait(driver, 5)

    # Determina o campo de pesquisa de clientes
    search = driver.execute_script("""return document.getElementsByTagName('soma-search')[0].shadowRoot.querySelector('input[type=search]')""")

    print(search)

    # Escreve o nb do cliente no campo de search
    search.send_keys(nbXP)

    time.sleep(5)

    # Determina o nome do cliente para posterior verificação
    nomeCliente = driver.execute_script("""return document.getElementsByTagName('soma-menu-item')[0]""")

    print(nomeCliente.text)

    # Abre o browser em fullscreen para não travar
    driver.fullscreen_window()

    time.sleep(2)

    # Clica no nome do cliente
    nomeCliente.send_keys(['Enter'])
    nomeCliente.click()

    time.sleep(3)

    # Pega o cabeçalho da tabela e determina a quantidade de ativos que o cliente possui
    cabecalhoTabela = driver.execute_script("""return document.getElementsByTagName('soma-table-head')[0]""")
    nAtivos = cabecalhoTabela.text
    nAtivos = nAtivos.split("\n")
    nAtivos = nAtivos[0].split(" ")
    nAtivos = nAtivos[0]

    i = 0


    # Faz um loop por cada botão de resgate
    for i in range(int(nAtivos)):
        try:
            time.sleep(5)
            # Abre o browser em fullscreen para não travar
            driver.fullscreen_window()
            #botaoResg = wait.until(EC.presence_of_all_elements_located(("id",f"button-redemption-{i}")))
            botaoResg = driver.find_element("id",f"button-redemption-{i}")
            ativo = botaoResg.get_attribute("data-wa")
            ativo = ativo.split(';')
            ativo = ativo[2].split('Resgatar ')
            ativo = ativo[1]
            print(ativo)
            botaoResg.click()
            time.sleep(5)
            qtd = driver.find_element("xpath", "/html/body/div[1]/div[3]/div[3]/div[2]/div/section/section[2]/div[2]/span")
            qtd = qtd.text
            qtd = int(qtd.replace(".",""))
            # qtd = int(qtd)
            print(qtd)

            ativo = [ativo, qtd]
            if ativo in ativosSemCot:
                try:
                    #botaoQtdTotal = wait.until(EC.presence_of_all_elements_located(("xpath","/html/body/div[1]/div[3]/div[3]/div[2]/div/section/section[3]/div[2]/div/label/div")))
                    botaoQtdTotal = driver.find_element("xpath","/html/body/div[1]/div[3]/div[3]/div[2]/div/section/section[3]/div[2]/div/label/div")
                    botaoQtdTotal.click()
                    textoQtdTotal = driver.find_element("xpath","/html/body/div[1]/div[3]/div[3]/div[2]/div/section/section[3]/div[1]/div/div[2]/input")
                    qtdTotal = textoQtdTotal.get_attribute("value")
                    if qtd == int(qtdTotal):
                        botaoContinuar = driver.find_element("xpath","/html/body/div[1]/div[3]/div[3]/div[2]/div/section/section[4]/button[2]")
                        botaoContinuar.click()
                        time.sleep(2)
                        botaoSolicitar = driver.find_element("xpath","/html/body/div[1]/div[3]/div[3]/div[2]/div/section/div/section/button[2]")
                        botaoSolicitar.click()
                        print(f"Cotação solicitada para o ativo {ativo} - QTD {qtd}!")
                        time.sleep(2)
                except:
                    print(f"Não foi possível solicitar a cotação para o ativo: {ativo} - QTD {qtd}!") 
                    continue
                time.sleep(2)
            #botaoFecharModal = wait.until(EC.presence_of_all_elements_located(("xpath","/html/body/div[1]/div[3]/div[3]/div[1]/img")))
            botaoFecharModal = driver.find_element("xpath","/html/body/div[1]/div[3]/div[3]/div[1]/img")
            botaoFecharModal.click()   
            time.sleep(3)
            driver.refresh()
        except:
            continue
        


    # botaoResg = wait.until(EC.presence_of_all_elements_located(
    #             ("id", 'button-redemption-0')))


    # Aguarda o carregamento da página
    time.sleep(5)
    # Fechar o navegador
    driver.quit()
