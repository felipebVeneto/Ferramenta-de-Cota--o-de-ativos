import requests
import pandas as pd
import tkinter as tk
import locale
import time
import datetime

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

# Pega as posições que foram solicitadas e verifica quais foram cotadas
def pegarPosSolicitadas(subscriptionKey, bearer, nbXP, nomeCliente, dataArq):

    # Determina a URL para requisição
    url = f'https://api.xpi.com.br/rede-fixedincome/v1/orders/customers/{nbXP}'

    # Pega a cotação do cliente em questão
    xpDados = pd.read_excel(f"Cotação {nomeCliente} - XP {nbXP} - {dataArq}.xlsx")
    xpDados = xpDados.drop(columns=[col for col in xpDados.columns if 'Unnamed: ' in col])

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
        data = data['data']

        for ativo in data:      


            dataSolicitacao = ativo['schedulingDate']

            year = int(dataSolicitacao[:4])
            month = int(dataSolicitacao[5:7])
            day = int(dataSolicitacao[8:10])

            # Format the date string in the DD/MM/YYYY format.
            dataSolFormatada = datetime.datetime(year, month, day).strftime("%d.%m.%y")

            # Formata a data do dia de ontem
            hoje = datetime.date.today()
            dataOntem = hoje - datetime.timedelta(days=1)
            dataOntem = datetime.datetime(dataOntem.year, dataOntem.month, dataOntem.day).strftime("%d.%m.%y")

            
            
            # Pula as notas de negociação
            if ativo['orderStatus'] == 'Executado':
                continue
            
            if dataSolFormatada == dataArq:
                
                print('--------------------------------')    
                print(ativo['assetName'])
                print(ativo['quantity'])
                nomeAtivo = ativo['assetName']
                qtdAtivo = ativo['quantity']
                codSolicitacao = ativo['orderId']
                # Procura a linha do ativo
                res = xpDados.loc[(xpDados["ATIVO"] == nomeAtivo) & (xpDados["QTD"] == qtdAtivo)]
                linAtivo = res.index[0]

                # Verifica se a posição foi cotada
                if ativo['orderStatus'] == 'Cancelada':
                    print('Não possui cotação')
                    if xpDados.loc[linAtivo, "QTD"] == qtdAtivo:
                        xpDados.loc[linAtivo, "ÁGIO/DESÁGIO"] = 'Sem liquidez'
                        xpDados.loc[linAtivo, "DATA"] = dataArq.replace('.', '/')
                elif ativo['orderStatus'] == 'Cotação registrada':
                    print('Cotação registrada')
                    if xpDados.loc[linAtivo, "QTD"] == qtdAtivo:
                        xpDados.loc[linAtivo, "ÁGIO/DESÁGIO"] = 'Cliente cotado'
                        xpDados.loc[linAtivo, "CÓD VIRTUAL"] = codSolicitacao
                        xpDados.loc[linAtivo, "CÓD VIRTUAL"] = codSolicitacao
                        xpDados.loc[linAtivo, "DATA"] = dataArq.replace('.', '/')
            else:
                continue
        
        xpDados.to_excel(f"Cotação {nomeCliente} - XP {nbXP} - {dataArq}.xlsx")

    else:
            print('Error:', response.status_code, response.text)
            show_error_message()

def cotarSolicitados(subscriptionKey, bearer, nbXP, nomeCliente, dataArq):

    # Define a formatação dos valores monetários
    locale.setlocale(locale.LC_ALL, 'pt_BR')

    #Determina os Headers da requisição
    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey,
                'Authorization': 'Bearer ' + bearer,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
                }

    # Pega a cotação do cliente em questão
    xpDados = pd.read_excel(f"Cotação {nomeCliente} - XP {nbXP} - {dataArq}.xlsx")
    xpDados = xpDados.drop(columns=[col for col in xpDados.columns if 'Unnamed: ' in col])
    
    lin = 0
    for status in xpDados["ÁGIO/DESÁGIO"]:
        if status == "Cliente cotado":
            # Procura a linha do ativo
            ativo = xpDados.loc[lin, "ATIVO"]
            codVirtual = xpDados.loc[lin, "CÓD VIRTUAL"]

            print(ativo)
            print(codVirtual)
            
            # Determina a URL para requisição
            url = f'https://api.xpi.com.br/rede-fixedincome/v1/orders/sale/manual/customers/{nbXP}/orders/{codVirtual}'
            
            time.sleep(1)
            #Realiza a requisição
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                
                # Armazena o JSON retornado
                data = response.json()
                data = data['data']
                # Compara o nome e a quantidade para certificar que é o ativo correto
                if ativo == data['assetNickName']:
                    puCurva = data['unitPriceCurve']
                    puResg = data['unitPriceQuote']
                    taxaResg = data['assetRateRedemption']
                    resgBruto = data['redemptionQuotePosition']
                    imposto = data['incomeTax']
                    resgLiq = resgBruto - imposto
                    
                    #Calcula o ágio ou deságio
                    agioDesagio = (puResg/puCurva) - 1
                    agioDesagio = agioDesagio * 100

                    xpDados.loc[lin, "QTD"] == data['assetQuantityPosition']
                    xpDados.loc[lin, "ÁGIO/DESÁGIO"] = str(locale.format_string('%.2f%%', agioDesagio, grouping=True))
                    xpDados.loc[lin, "PU CURVA"] = locale.currency(puCurva)
                    xpDados.loc[lin, "PU RESG."] = locale.currency(puResg)
                    xpDados.loc[lin, "TAXA RESG."] = taxaResg
                    xpDados.loc[lin, "RESGATE BRUTO"] = locale.currency(resgBruto)
                    xpDados.loc[lin, "RESGATE LÍQ."] =locale.currency(resgLiq)
                    xpDados.loc[lin, "RENTABILIDADE (%CDI)"] = '-'

            else:
                print('Error:', response.status_code, response.text)
                show_error_message()

        lin = lin + 1
    xpDados.to_excel(f"Cotação {nomeCliente} - XP {nbXP} - {dataArq}.xlsx")
