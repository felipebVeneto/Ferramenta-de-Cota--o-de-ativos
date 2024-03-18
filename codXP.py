import requests
import pandas as pd
import tkinter as tk
import time
import locale

# Função que configura a mensagem de error caso a requisição falhe
def show_error_message():
    root = tk.Tk()
    root.title("Erro na requisição")
    label = tk.Label(root, text="Ocorreu um erro na requisição. Verifique os dados.")
    label.config(font=("Roboto", 14))
    #image = tk.PhotoImage(file="error.png")
    button = tk.Button(root, command=root.destroy)
    label.pack()
    button.pack()
    root.mainloop()

# Função que verifica se a marcação da carteira do cliente
def definirMarcação(nbXP, subscriptionKey, bearer):
    #Determina a URL para requisição
    url = f'https://apis.xpi.com.br/advisor-customer-consolidated-portfolio/api/customers/{nbXP}/customer-info'

    #Determina os Headers da requisição
    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey,
            'Authorization': 'Bearer ' + bearer,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
            }
    
    #Realiza a requisição
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        dadosCliente = response.json()
        marcacao = dadosCliente['output']['visulizationType']
        print(marcacao)
        return marcacao
    else:
        print('Error:', response.status_code, response.text)
        show_error_message()

# Função que puxa as posições da XP do Cliente
def puxarPosXP(nbXP, nomeCliente, bearer, subscriptionKey, dataHoje, dataFormatada):

    xpDados = pd.read_excel('templateCotacao.xlsx', "Template", skiprows=(0, 1))

    xpDados = xpDados.drop(columns=[col for col in xpDados.columns if 'Unnamed: ' in col])

    #Determina a URL para requisição
    url = f'https://api.xpi.com.br/rede-fixedincome/v1/positions/{nbXP}'

    #Determina os Headers da requisição
    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey,
            'Authorization': 'Bearer ' + bearer,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
            }

    #Realiza a requisição
    response = requests.get(url, headers=headers)

    # Verifica se a requisição obteve sucesso
    if response.status_code == 200:

        # Armazena o JSON retornado
        data = response.json()

        # Pega as posições do cliente
        customerPositionAssets = data['customerPositionAssets']

        lin = 1

        # print(ultLin)
        #Varre cada posição do cliente
        for ativos in customerPositionAssets:
            # Indica em qual coluna os dados devem ser inseridos
            xpDados.loc[lin, "DATA"] = dataHoje
            xpDados.loc[lin, "CLIENTE"] = nomeCliente
            xpDados.loc[lin, "ATIVO"] = ativos['nickName']
            xpDados.loc[lin, "QTD"] = '-'
            xpDados.loc[lin, "TAXA COMPRA"] = '-'
            xpDados.loc[lin, "TAXA RESG."] = '-'
            xpDados.loc[lin, "PU CURVA"] = '-'
            xpDados.loc[lin, "PU RESG."] = '-'
            xpDados.loc[lin, "TAXA RESG."] = '-'
            xpDados.loc[lin, "RESGATE BRUTO"] = '-'
            xpDados.loc[lin, "RESGATE LÍQ."] = '-'
            xpDados.loc[lin, "ÁGIO/DESÁGIO"] = '-'
            xpDados.loc[lin, "RENTABILIDADE (%CDI)"] = '-'
            xpDados.loc[lin, "CÓD VIRTUAL"] = ativos['virtualId']

            lin = lin + 1
        
        # print(xpDados)
        xpDados.to_excel(f"Cotação {nomeCliente} - XP {nbXP} - {dataFormatada}.xlsx")
        print("----------------------------------------------------------------")
        print("Posições Salvas")
        print("----------------------------------------------------------------")   
    else:
        print('Error:', response.status_code, response.text)
        show_error_message()

# Função que cota a carteira do cliente na XP
def cotarXP(nbXP, nomeCliente, bearer, subscriptionKey, dataFormatada, hora, marcacao):

    # Define a formatação dos valores monetários
    locale.setlocale(locale.LC_ALL, 'pt_BR')

    if hora >= 15:
        print('----------------------------------------------------------------')
        print("O mercado já fechou, tente novamente antes das 15:00h do próximo dia útil!")
        print('----------------------------------------------------------------')
        return 

    planCotacao = pd.read_excel(f"Cotação {nomeCliente} - XP {nbXP} - {dataFormatada}.xlsx")

    codVirtual = planCotacao['CÓD VIRTUAL']

    # Determina os headers da requisição
    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey,
                'Authorization': 'Bearer ' + bearer,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
                }

    lin = 0

    for codVirtual in codVirtual:

        # Determina a URL de cada ativo
        url = f'https://api.xpi.com.br/rede-fixedincome/v1/orders/customers/{nbXP}/sales/{codVirtual}/validation'
        
        time.sleep(2)

        # Realiza a requisição e armazena a resposta
        response = requests.get(url, headers=headers)

        # Verifica se a requisição foi aceita
        if response.status_code == 200:
            
            # Pega o JSON retornado pela requisição
            data = response.json()

            ativo = data['nickName']
            print('-----------------')
            print('ATIVO: ' + ativo)
            print('-----------------')
            # Pega a quantidade do ativo na carteira do cliente
            qtd = data['quantityAvailable']
            print(ativo + ' - ' + str(qtd))
            planCotacao.loc[lin, "QTD"] = qtd

            # Define o PU e as taxas de acordo com a marcação do cliente
            if marcacao == 'Curva':
                puCurva = data['currentPrice']
                planCotacao.loc[lin, "PU CURVA"] = locale.currency(puCurva)
                
                #Taxa de compra
                taxaCompra = data['descriptionFee']
                planCotacao.loc[lin, "TAXA COMPRA"] = taxaCompra
            elif marcacao == 'Mercado':
                dadosMercado = data['mtm']
                if dadosMercado != None:
                    puCurva = dadosMercado['unitPrice']
                    planCotacao.loc[lin, "PU CURVA"] = locale.currency(puCurva)
                    
                    #Taxa de compra
                    taxaCompra = data['mtm']['rateDescription']
                    planCotacao.loc[lin, "TAXA COMPRA"] = taxaCompra
                else:
                    puCurva = 1
                    planCotacao.loc[lin, "PU CURVA"] = '-'
                    planCotacao.loc[lin, "TAXA COMPRA"] = data['descriptionFee']
                    

            # Verifica se o ativo é um CDB
            if 'CDB' in ativo or 'LCA' in ativo or 'LCI' in ativo:
                # Pega os dados do CDB
                puResg = data['redemptionPrice']
                planCotacao.loc[lin, "PU RESG."] = locale.currency(puResg)
                #print('PU RESGATE: ' + str(puResg))
                taxaResg = data['descriptionFee']
                planCotacao.loc[lin, "TAXA RESG."] = taxaResg
                #print('TAXA: ' + str(taxaResg))

                #Calcula o Valor bruto de acordo com o site
                valorBruto = puResg * qtd
                planCotacao.loc[lin, "RESGATE BRUTO"] = locale.currency(valorBruto)
                            
                #Calcula o valor líquido de acordo com o site
                imposto = data['redemptionIncomeTax']
                valorLiq = valorBruto - imposto
                planCotacao.loc[lin, "RESGATE LÍQ."] = locale.currency(valorLiq)

                #Calcula o ágio ou deságio
                agioDesagio = (puResg/puCurva) - 1
                agioDesagio = agioDesagio * 100
                planCotacao.loc[lin, "ÁGIO/DESÁGIO"] = locale.format_string('%.2f%%', agioDesagio, grouping=True)

                #Pega a rentabilidade em relação ao CDI
                if data['customerProfitability'] == None:
                    planCotacao.loc[lin, "RENTABILIDADE (%CDI)"] = '-'
                else:
                    rentCDI = data['customerProfitability']
                    planCotacao.loc[lin, "RENTABILIDADE (%CDI)"] = locale.format_string('%.2f%%', rentCDI, grouping=True)

                lin = lin + 1
            else:
                # Pega uma lista com as opções de resgate
                opcoesResgate = data['redemptionOptions']

                if opcoesResgate == []:      
                    print("Solicitar Cotação")
                    #print('-----------------')
                
                    textoSoliciatação = str("Solicitar Cotação")
                    planCotacao.loc[lin, "PU RESG."] = '-'
                    planCotacao.loc[lin, "TAXA RESG."] = '-'
                    planCotacao.loc[lin, "PU CURVA"] = '-'
                    planCotacao.loc[lin, "PU RESG."] = '-'
                    planCotacao.loc[lin, "TAXA RESG."] = '-'
                    planCotacao.loc[lin, "RESGATE BRUTO"] = '-'
                    planCotacao.loc[lin, "RESGATE LÍQ."] = '-'
                    planCotacao.loc[lin, "ÁGIO/DESÁGIO"] = textoSoliciatação

                    lin = lin + 1
                else:
                # Varre a lista de opções de resgate
                    # for option in opcoesResgate:
                        # Pega a opção com ROA = 0
                        option = opcoesResgate.pop()

                        if option['roa'] == 0:
                            #Seleciona a taxa com ROA = 0
                            taxaResg = option['descriptionFee']
                            planCotacao.loc[lin, "TAXA RESG."] = taxaResg

                            #Pega o PU com ROA = 0
                            puResg = option['unitPrice']
                            planCotacao.loc[lin, "PU RESG."] = locale.currency(puResg)

                            #Calcula o Valor bruto de acordo com o site
                            valorBruto = puResg * qtd
                            planCotacao.loc[lin, "RESGATE BRUTO"] = locale.currency(valorBruto)
                            
                            #Calcula o valor líquido de acordo com o site
                            imposto = option['incomeTax']
                            valorLiq = valorBruto - imposto
                            planCotacao.loc[lin, "RESGATE LÍQ."] = locale.currency(valorLiq)
                            
                            #Calcula o ágio ou deságio
                            agioDesagio = (puResg/puCurva) - 1
                            agioDesagio = agioDesagio * 100
                            planCotacao.loc[lin, "ÁGIO/DESÁGIO"] = locale.format_string('%.2f%%', agioDesagio, grouping=True)

                            #Pega a rentabilidade em relação ao CDI
                            rentCDI = option['customerProfitability']
                            planCotacao.loc[lin, "RENTABILIDADE (%CDI)"] = locale.format_string('%.2f%%', rentCDI, grouping=True)

                            # Verifica se retornou uma lista de opções vazia
                            if option['roa'] == []:
                                # Verifica se já passou das 15:00 horas
                                if hora >= 15:
                                    print('-----------------')
                                    print("O mercado já fechou, tente novamente antes das 15:00h do próximo dia útil!")
                                    print('-----------------')
                                    break
                                else:
                                    print('-----------------')
                                    print("Solicitar Cotação")
                                    print('-----------------')

                                    textoSoliciatação = str("Solicitar Cotação")
                                    planCotacao.loc[lin, "PU RESG."] = textoSoliciatação
                                    planCotacao.loc[lin, "TAXA RESG."] = textoSoliciatação
                                    planCotacao.loc[lin, "PU CURVA"] = textoSoliciatação
                                    planCotacao.loc[lin, "PU RESG."] = textoSoliciatação
                                    planCotacao.loc[lin, "TAXA RESG."] = textoSoliciatação
                                    planCotacao.loc[lin, "RESGATE BRUTO"] = textoSoliciatação
                                    planCotacao.loc[lin, "RESGATE LÍQ."] = textoSoliciatação
                                    planCotacao.loc[lin, "ÁGIO/DESÁGIO"] = textoSoliciatação

                            lin = lin + 1
                        else:
                                print('-----------------')
                                print("Solicitar Cotação")
                                print('-----------------')

                                textoSoliciatação = str("Solicitar Cotação")
                                planCotacao.loc[lin, "PU RESG."] = textoSoliciatação
                                planCotacao.loc[lin, "TAXA RESG."] = textoSoliciatação
                                planCotacao.loc[lin, "PU CURVA"] = textoSoliciatação
                                planCotacao.loc[lin, "PU RESG."] = textoSoliciatação
                                planCotacao.loc[lin, "TAXA RESG."] = textoSoliciatação
                                planCotacao.loc[lin, "RESGATE BRUTO"] = textoSoliciatação
                                planCotacao.loc[lin, "RESGATE LÍQ."] = textoSoliciatação
                                planCotacao.loc[lin, "ÁGIO/DESÁGIO"] = textoSoliciatação

        else:
            print('Error:', response.status_code, response.text)
            continue 

    # planCotacao.sort_values("ÁGIO/DESÁGIO", inplace=True, ascending=True)
    planCotacao = planCotacao.drop(columns=[col for col in planCotacao.columns if 'Unnamed: ' in col])
    #print(planCotacao)

    planCotacao.to_excel(f"Cotação {nomeCliente} - XP {nbXP} - {dataFormatada}.xlsx")
