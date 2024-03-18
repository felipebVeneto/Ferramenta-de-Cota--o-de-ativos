import math
import pandas as pd
import requests
from datetime import datetime
import locale

def pegarSolicitacaoBTG(nbBTG, nomeCliente, tokenJWT, dataArq):

    locale.setlocale(locale.LC_ALL, 'pt_BR')

    # Pega a cotação do cliente em questão
    btgDados = pd.read_excel(f"Cotação {nomeCliente} - BTG {nbBTG} - {dataArq}.xlsx")
    btgDados = btgDados.drop(columns=[col for col in btgDados.columns if 'Unnamed: ' in col])

    # Determina um array com os ativos sem cotação
    ativosSemCot = []

    # Cria um dicionário com os ativos sem cotação
    for cod in btgDados['CÓD VIRTUAL']:
        # Procura a linha do ativo
        res = btgDados.loc[btgDados["CÓD VIRTUAL"] == cod]
        linAtivo = res.index[0]
        status = btgDados.loc[linAtivo, "ÁGIO/DESÁGIO"]
        qtd = btgDados.loc[linAtivo, "QTD"]
        if status == "Solicitar Cotação":
            ativosSemCot.append([cod, qtd])

    # Formate a data do arquivo no formato "y-m-d"
    dataPayload = datetime.strptime(dataArq, "%d.%m.%y")
    dataPayload = dataPayload.strftime("%Y-%m-%d")
    dataPayload = dataPayload + 'T03:00:00.000Z'

    payload ={
    "dataInicial": dataPayload, 
    "orderBy": "dtCotResgate",
    "order": "desc",
    "pageNumber": 1,
    "pageSize": 100
    }

    # URL da solicitação
    url = 'https://access.btgpactualdigital.com/new-management/api/rmadmin/pre-op-aai/list'

    # Headers personalizados
    headers = {
        'Authorization': tokenJWT,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'X-System-From': 'RMADMIN'
    }

    # Realize a solicitação POST
    response = requests.post(url, headers=headers, json=payload)

    # Verifique a resposta
    if response.status_code == 200:
        response = response.json()

        if response['data'] == []:
            print('Não existem cotações solicitadas no dia de Hoje!')
            return

        for cotacao in response['data']:            
            # Converter a string em um objeto datetime
            dataCot = datetime.strptime(cotacao['dataCotarResgate'], "%Y-%m-%dT%H:%M:%S.%f")
            # Formatar a data no formato dd/mm/yyyy
            dataCotFormatada = dataCot.strftime("%d.%m.%y")
            ativoCot = cotacao['ativo']
            quantidadeCot = cotacao['quantidade']
            contaCot = cotacao['conta']
            statusCot = cotacao['preOperationStatus']
            statusCot = statusCot['descriptionStatus']

            
            if contaCot == nbBTG and dataCotFormatada == dataArq:
                ativo = [ativoCot, quantidadeCot]
                if ativo in ativosSemCot:
                    #Atualizar planilha de cotações
                    # Procura a linha do ativo
                    linAtivo = btgDados.loc[(btgDados["CÓD VIRTUAL"] == ativoCot) & (btgDados["QTD"] == quantidadeCot)]
                    linAtivo = linAtivo.index[0]

                    if statusCot == "Sem cotação para o ativo":
                        btgDados.loc[linAtivo, "ÁGIO/DESÁGIO"] = 'Sem liquidez'
                        btgDados.loc[linAtivo, "DATA"] = dataArq.replace('.', '/')
                    else:
                        taxaResg = cotacao['taxaCliente']

                        if taxaResg == None:
                            taxaResg = '-'
                        else:
                            indexador = cotacao['indice']
                            taxaResg = str((taxaResg * 100)) 
                            taxaResg = taxaResg.replace('.', ',')
                            taxaResg = indexador + taxaResg + "%"


                        puResg = cotacao['puCliente']

                        puCurva = btgDados.loc[linAtivo, "PU CURVA"]
                        puCurva = puCurva.split(' ')
                        puCurva = puCurva[1].replace(',','.')

                        if puResg == None:
                            puResg = '-'
                            agioDesagio = 'Sem liquidez'
                            resgBruto = '-'
                        else:
                            resgBruto = puResg * quantidadeCot
                            resgBruto = locale.currency(resgBruto)
                            agioDesagio = ((puResg/float(puCurva)) - 1) * 100
                            agioDesagio = str(locale.format_string('%.2f%%', agioDesagio, grouping=True))
                            puResg = locale.currency(puResg)
                        

                        btgDados.loc[linAtivo, "DATA"] = dataArq.replace('.', '/')
                        btgDados.loc[linAtivo, "TAXA RESG."] = taxaResg
                        btgDados.loc[linAtivo, "PU RESG."] = puResg
                        btgDados.loc[linAtivo, "RESGATE BRUTO"] = resgBruto
                        btgDados.loc[linAtivo, "ÁGIO/DESÁGIO"] = agioDesagio

                    print('--------------------------------')
                    print(ativoCot)
                    print(contaCot)
                    print(dataCotFormatada)
                    print(quantidadeCot)
                    print(cotacao['puCliente'])
                    print(cotacao['taxaCliente'])
                    print('--------------------------------')
    else:

        print('A solicitação falhou. Código de status:', response.status_code)

    btgDados.to_excel(f"Cotação {nomeCliente} - BTG {nbBTG} - {dataArq}.xlsx")

