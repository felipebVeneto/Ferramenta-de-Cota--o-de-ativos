# Importa as funções
from codBTG import cotarBTG
from codXP import cotarXP, definirMarcação,puxarPosXP
from compararCotacao import compararCotacao
from dadosClienteAPI import buscarDadosClientes
from dadosClienteAntigo import buscarDados
from encontrarArquivo import encontrarArquivo
from encontrarArquivoRecente import encontrarArquivoRecente
from pegarSolicitadosBTG import pegarSolicitacaoBTG
from pegarSolicitadosXP import pegarPosSolicitadas, cotarSolicitados
from solicitacaoXP import solicitarCotacao
import time

# Importa as bibliotecas
import PySimpleGUI as sg
import datetime

# Define os padrões do tema que a ferramenta irá utilizar
sg.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {'BACKGROUND': '#0F1A2F',
                                        'TEXT': '#FFFFFF',
                                        'INPUT': '#FFFFFF',
                                        'TEXT_INPUT': '#0F1A2F',
                                        'SCROLL': '#99CC99',
                                        'BUTTON': ('#000000', '#FFFFFF'),
                                        'PROGRESS': ('#D1826B', '#CC8019'),
                                        'BORDER': 1, 'SLIDER_DEPTH': 0, 
                                        'PROGRESS_DEPTH': 0, }

# Define o tema que a ferramenta irá utilizar
sg.theme('MyCreatedTheme')

# Define estilos padrões
inputStyle = {'size':(100,20), 'font':('Roboto','12'), 'pad':(0,15)}
textStyle = {'font':('Roboto', 16),'pad':(0,15)}
buttonStyle = {'font':('Roboto','12'),'size':(18,2), 'pad':(20,15)}
statusStyle = {'background_color':'#FFFFFF', 'text_color':'#0F1A2F','font':('Roboto', '12')}

# Define o layout da ferramenta
layout = [
    [sg.Push(),sg.Image('./assets/logoNova.png', size=(80,57), pad=(0,10)), sg.Text("Ferramenta de cotação",font=('Roboto', 35)), sg.Push()],
    [sg.Push(),sg.Text('Digite o NB do cliente: ', **textStyle), sg.InputText(key="nbVeneto", size=(10,30),font=('Roboto', 16), pad=(10,10) ,enable_events=True),sg.Push()],
    [sg.Push(),sg.Button('Buscar Dados', **buttonStyle), sg.Push()],
    [sg.Push(),sg.Text('Selecione a instituição: ',font=('Roboto', 16), pad=(0,15)),sg.Push()],
    [sg.Push(),sg.Checkbox("XP", key='XP', font=('Roboto', 16), pad=(0, 15)),sg.Checkbox("BTG", key='BTG', font=('Roboto', 16)),sg.Push()],
    [sg.Push(),sg.Button("Cotar Carteira", **buttonStyle ),sg.Button("Solicitar cotações", **buttonStyle ),sg.Button("Comparar cotações", **buttonStyle ),sg.Push()],
    [sg.Push()],
    [sg.Push(),sg.Output(size=(100, 30), key='-OUTPUT-',font=('Roboto', 16), pad=(0, 15)), sg.Push()],
]

# Define configurações da janela da ferramenta
janela = sg.Window('Ferramenta de Cotação', layout, icon='./assets/logoAzul.ico', size=(1000,800), resizable=True )

# Inicia as váriaveis como NONE para posterior Checagem
nbXP = None 
nbBTG = None
officer = None
nomeCliente = None
bearer = None

# username = "felipe.batista"
# password = "Veneto@123"
  
# # Marca o tempo inicial
# inicio = time.time()

# dadosClientes, dadosContas = buscarDadosClientes(username, password)

# # Marca o tempo final
# fim = time.time()
# # Calcula a diferença para obter o tempo total
# tempo_total = fim - inicio

# Loop que iniciar a ferramenta
while True:

    # Trata a data do dia atual
    agora = datetime.datetime.now()
    dataHoje = agora.strftime('%d/%m/%y')
    #dataHoje = '10/10/23'
    dataFormatada = dataHoje.replace('/', '.')
    hora = agora.hour

    # Esta chave não muda na XP
    subscriptionKey = "4099b36f826749e1acab295989795688"

    #Determina as váriaveis do forms
    evento, valores = janela.read()
    
    # print('Demrou: ' + str(tempo_total))

    # Executa a função de encerramento
    if evento == sg.WIN_CLOSED: 
        break

    # Busca os dados do cliente
    if evento == "Buscar Dados":
        sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, time_between_frames=80)

        #Verifica se foi fornecido um NB
        if valores["nbVeneto"] == '':
            print("Forneça um NB Válido!")
            sg.PopupAnimated(None)
            continue
        
        # Verifica se o NB inserido é numérico
        try:
            nbVeneto = int(valores["nbVeneto"])
        except:
            print("Forneça um NB Válido!")
            sg.PopupAnimated(None)
            continue
        
        

        # # Pega os dados pessoais do cliente
        # cliente = next((cliente for cliente in dadosClientes if cliente['cod_cliente'] == str(nbVeneto)), None)
        
        # if cliente == None:
        #     print("Este cliente não existe na base! Forneça um NB Válido!")
        #     sg.PopupAnimated(None)
        #     continue

        # nomeCliente = cliente['iniciais_cliente']
        # cpf = cliente['cpf_cnpj']

        # # Pega as contas do cliente
        # for conta in dadosContas:
        #     if conta['cod_produto'] == str(nbVeneto):
        #         if conta['instituicao'] == 'XP':
        #             nbXP = conta['conta']
        #         if conta['instituicao'] == 'BTG':
        #             nbBTG = conta['conta']
        

        # if nbXP == None:
        #     nbXP = '-'
        # if nbBTG == None:
        #     nbBTG = '-'

        
        # Executar Função que busca os dados da planilha do monday  
        dadosCliente = buscarDados(nbVeneto)
        
        # Verifica se a função encontrou dados
        if dadosCliente == 'ERROR':
            sg.PopupAnimated(None)
            continue
        else:
            # Pega os dados da função
            nbXP, nbBTG, officer, nomeCliente, cpf = dadosCliente

        # Printa os dados do Cliente no quadro de logs
        print('________________________________')
        print(' ')
        print('                  Dados do cliente       ')
        print('________________________________')
        print(' ')
        print('   Cliente: ' + nomeCliente)
        print('   XP: ' + str(nbXP))
        print('   BTG: ' + str(nbBTG))
        print('   CPF: ' + cpf)
        print(' ')
        print('________________________________')
        sg.PopupAnimated(None)

    # Realiza a cotação da carteira
    if evento == "Cotar Carteira":
        
        # Verifica se os dados do cliente foram buscados
        if nbXP is None or nbBTG is None or nomeCliente is None:
            print("É necessário buscar os dados do cliente primeiro!")
            continue
        
        # Verifica qual instituição foi selecionada
        if valores['XP'] == True and valores['BTG'] == False:
            instituicao = 'XP'
        elif valores['XP'] == False and valores['BTG'] == True:
            instituicao = 'BTG'
        elif valores['XP'] == True and valores['BTG'] == True:
            instituicao = 'Todas'
        else:
            janela['-OUTPUT-'].update('')
            print("Indique pelomenos uma instituição para prosseguir!")
            sg.PopupAnimated(None)
            continue

        # Cota as contas selecionadas
        if instituicao == 'XP':
            print("Você deseja Cotar a carteira da conta XP desse cliente!")
            bearer = sg.popup_get_text("Forneça o Bearer Token da XP!", grab_anywhere=True, no_titlebar=True)
            if bearer is None:
                print("É necessário fornecer o Bearer Token primeiro!")
                continue
            else:
                # Verifica se existe alguma cotação para o cliente na pasta
                dataArq = encontrarArquivo(nomeCliente , instituicao)
                # Define o valor padrão variavel atualizar e comparar
                atualizar = "No"
                # Caso exista algum arquivo com o nome do cliente, verifica se o usuário irá comparar ou atualizar
                # a cotação que ja existe ou gerar uma nova
                if dataArq != None:
                    # Verifica se o usuário deseja solicitar a cotação para os ativos que não possuem
                    atualizar = sg.popup_yes_no(f"Foi encontrada uma cotação para o cliente {nomeCliente} no dia {dataArq} deseja atualizar a cotação?", grab_anywhere=True,no_titlebar=True)
                # Função de atualização
                if atualizar == "Yes":
                    sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, time_between_frames=80)
                    pegarPosSolicitadas(subscriptionKey, bearer, nbXP, nomeCliente, dataArq)
                    cotarSolicitados(subscriptionKey, bearer, nbXP, nomeCliente, dataArq)     
                # Apenas executa a cotação
                else:
                    sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, time_between_frames=80)
                    cotarXPInterface(bearer)
        elif instituicao == 'BTG':
            print("Você deseja Cotar a carteira da conta BTG desse cliente!")
            tokenJWT = sg.popup_get_text("Forneça o token JWT do BTG!", grab_anywhere=True, no_titlebar=True)
            if tokenJWT is None:
                print("É necessário fornecer o JWT Token primeiro!")
                continue
            else:
                # Verifica se existe alguma cotação para o cliente na pasta
                dataArq = encontrarArquivo(nomeCliente , instituicao)
                # Define o valor padrão variavel atualizar
                atualizar = "No"
                # Caso exista algum arquivo com o nome do cliente, verifica se o usuário irá atualizar
                # a cotação que ja existe ou gerar uma nova
                if dataArq != None:
                    # Verifica se o usuário deseja solicitar a cotação para os ativos que não possuem
                    atualizar = sg.popup_yes_no(f"Foi encontrada uma cotação para o cliente {nomeCliente} no dia {dataArq} deseja atualizar a cotação?", grab_anywhere=True,no_titlebar=True)
                if atualizar == "Yes":
                    pegarSolicitacaoBTG(nbBTG, nomeCliente, tokenJWT, dataArq)     
                else:
                    cotarBTGInterface(tokenJWT)     
        elif instituicao == 'Todas':
            print("Você deseja Cotar a carteira das contas XP e BTG desse cliente!")
            # Pega os tokens necessários
            bearer = sg.popup_get_text("Forneça o Bearer Token da XP!", grab_anywhere=True, no_titlebar=True)
            tokenJWT = sg.popup_get_text("Forneça o token JWT do BTG!", grab_anywhere=True, no_titlebar=True)
            
            # Realiza a cotação da XP
            if bearer is None:
                print("É necessário fornecer o Bearer Token primeiro!")
                continue
            else:
                # Verifica se existe alguma cotação para o cliente na pasta
                dataArq = encontrarArquivo(nomeCliente , instituicao)
                # Define o valor padrão variavel atualizar
                atualizar = "No"
                # Caso exista algum arquivo com o nome do cliente, verifica se o usuário irá atualizar
                # a cotação que ja existe ou gerar uma nova
                if dataArq != None:
                    # Verifica se o usuário deseja solicitar a cotação para os ativos que não possuem
                    atualizar = sg.popup_yes_no(f"Foi encontrada uma cotação para o cliente {nomeCliente} no dia {dataArq} deseja atualizar a cotação?", grab_anywhere=True)
                if atualizar == "Yes":
                    pegarPosSolicitadas(subscriptionKey, bearer, nbXP, nomeCliente, dataArq)
                    cotarSolicitados(subscriptionKey, bearer, nbXP, nomeCliente, dataArq)     
                else:
                    cotarXPInterface(bearer)  

            # Realiza a cotação do BTG
            if tokenJWT is None:
                print("É necessário fornecer o JWT Token primeiro!")
                continue
            else:
                # Verifica se existe alguma cotação para o cliente na pasta
                dataArq = encontrarArquivo(nomeCliente , instituicao)
                # Define o valor padrão variavel atualizar
                atualizar = "No"
                # Caso exista algum arquivo com o nome do cliente, verifica se o usuário irá atualizar
                # a cotação que ja existe ou gerar uma nova
                if dataArq != None:
                    # Verifica se o usuário deseja solicitar a cotação para os ativos que não possuem
                    atualizar = sg.popup_yes_no(f"Foi encontrada uma cotação para o cliente {nomeCliente} no dia {dataArq} deseja atualizar a cotação?", grab_anywhere=True)
                if atualizar == "Yes":
                    pegarSolicitacaoBTG(nbBTG, nomeCliente, tokenJWT, dataArq)     
                else:
                    cotarBTGInterface(tokenJWT)  
        sg.PopupAnimated(None)
    # Código para a solicitação de ativos de forma posterior a realização da cotação
    if evento == "Solicitar cotações":

        # Verifica se os dados do cliente foram buscados
        if nbXP is None or nbBTG is None or nomeCliente is None:
            print("É necessário buscar os dados do cliente primeiro!")
            continue
        

        if valores["instituicao"] == 'XP':
            print("Você deseja solicitar a carteira da conta XP desse cliente!")
            solicitarXPInterface()
        elif valores["instituicao"] == 'BTG':
            print("Você deseja solicitar a carteira da conta BTG desse cliente!")
            # Aqui virá a macro de solicitação do BTG
        elif valores["instituicao"] == 'Todas':
            print("Você deseja solicitar a carteira das contas XP e BTG desse cliente!")
            # Aqui virá a macro de solicitação de ambas as carteiras

    if evento == "Comparar cotações":
        # Verifica se os dados do cliente foram buscados
        if nbXP is None or nbBTG is None or nomeCliente is None:
            print("É necessário buscar os dados do cliente primeiro!")
            continue
        
                # Verifica qual instituição foi selecionada
        if valores['XP'] == True and valores['BTG'] == False:
            instituicao = 'XP'
        elif valores['XP'] == False and valores['BTG'] == True:
            instituicao = 'BTG'
        elif valores['XP'] == True and valores['BTG'] == True:
            instituicao = 'Todas'
        else:
            janela['-OUTPUT-'].update('')
            print("Indique pelomenos uma instituição para prosseguir!")
            sg.PopupAnimated(None)
            continue

        dataArqRecente, arqAtual = encontrarArquivoRecente(nomeCliente, instituicao, officer, dataHoje)
        dataArqRecente = dataArqRecente.strftime('%d.%m.%y')
        if arqAtual == True:
            if dataArqRecente != '':
                # Verifica se o usuário deseja solicitar a cotação para os ativos que não possuem
                comparar = sg.popup_yes_no("Deseja comparar a cotação de hoje com a do dia " + dataArqRecente + ' ?', grab_anywhere=True)
                if comparar == 'Yes':
                    compararCotacao(nomeCliente, officer, dataArqRecente, dataFormatada, instituicao)
                else:
                    compararOutraData = sg.popup_yes_no("Deseja comparar a cotação de hoje com a de outra data desejada?", grab_anywhere=True)
                    if compararOutraData == 'Yes':
                        outraData = sg.popup_get_text("Forneça a data do arquivo desejado:", grab_anywhere=True)
                        compararCotacao(nomeCliente, officer, outraData, dataFormatada, instituicao)
                    else:
                        continue
            else:
                print('Não foi encontrada contação recente para o cliente além da realizada no dia de hoje!')
                continue
        else:
            print('Não foi encontrada cotação do dia de hoje para o cliente! Favor realizar a cotação antes da comparação!')
            continue

    # Define a função de cotação da XP
    def cotarXPInterface(bearer):
            print("Cotando Carteira XP do cliente " + nomeCliente +  "!")
            # Caso não exista cotação recente para esse cliente, a carteira dele será cotizada do zero
            marcacao = definirMarcação(nbXP, subscriptionKey, bearer)
            puxarPosXP(nbXP, nomeCliente, bearer, subscriptionKey, dataHoje, dataFormatada)
            cotarXP(nbXP, nomeCliente, bearer, subscriptionKey, dataFormatada, hora, marcacao)
                
            # Verifica se o usuário deseja solicitar a cotação para os ativos que não possuem
            resp = sg.popup_yes_no("Deseja solicitar os ativos que não possuem cotação?", grab_anywhere=True,no_titlebar=True)
                
            # Solicita a cotação para os ativos que não possuem
            if resp == "Yes":
                solicitarXPInterface()
                print("Cotação finalizada. As cotações indisponíveis foram solicitadas! Verifique a pasta!")
            else:
                print("Cotação finalizada. As cotações indisponíveis não foram solicitadas! Verifique a pasta!")
    
    # Define a função de cotação do BTG
    def cotarBTGInterface(tokenJWT):
        print("Cotando Carteira BTG do cliente " + nomeCliente +  "!")
        cotarBTG(nbBTG, nomeCliente, tokenJWT, dataFormatada, cpf)
        # Aqui entrará a futura macro de solicitaçoes de cotação do BTG

    # Define a função de solicitação da XP
    def solicitarXPInterface():
        usuario = sg.popup_get_text("Usuário XP", grab_anywhere=True, no_titlebar=True)
        senha = sg.popup_get_text("Senha XP", grab_anywhere=True, password_char="*", no_titlebar=True)
        xpToken = sg.popup_get_text("Token XP", grab_anywhere=True, no_titlebar=True)
        solicitarCotacao(nbXP, nomeCliente, dataFormatada, usuario, senha, xpToken)
        print("Cotação finalizada. As cotações indisponíveis foram solicitadas! Verifique a pasta!")

janela.close()
