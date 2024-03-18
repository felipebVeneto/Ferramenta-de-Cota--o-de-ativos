import locale
import time
import pandas as pd
import requests
import datetime

def cotarBTG(nbBTG, nomeCliente, tokenJWT, dataFormatada, cpf):

    grupoBancarios = ['LCA', 'LCI', 'LF', 'CDB', 'TÍTULO PÚBLICO']

    # Formata o CPF para realizar a requisição
    cpfURL = cpf.replace('.','')
    cpfURL = cpfURL.replace('/','')
    cpfURL = cpfURL.replace('-','')

    # Determina a formatação monetária
    locale.setlocale(locale.LC_ALL, 'pt_BR')
    # Formate a data no formato "y-m-d"
    dataURL = datetime.datetime.strptime(dataFormatada, "%d.%m.%y")
    dataURL = dataURL.strftime("%Y-%m-%d")

    # Abre a planilha de template
    btgDados = pd.read_excel('templateCotacao.xlsx', "Template", skiprows=(0, 1))
    btgDados = btgDados.drop(columns=[col for col in btgDados.columns if 'Unnamed: ' in col])

    
    url = f'https://access.btgpactualdigital.com/op/api/clients/{cpfURL}/accounts/{nbBTG}/summary/{dataURL}'

    headers = {
            'Authorization': 'JWT ' + tokenJWT,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'X-System-From': 'RMADMIN'
            }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        # Determina o objeto JSON com todos os ativos de vRF
        data = response.json()
        data = data['statementAccount']
        data = data['fixedIncomes']

        lin = 1

        # Varrre cada ativo existente na carteira do cliente
        for ativo in data:
            
            grupo = ativo['accountingGroupCode']
            indexador = ativo['referenceIndexName']

            if grupo in grupoBancarios:
                # Chama a função que retorna o PU e Taxa de Resgate dos ativos Bancarios
                dadosResgate = realizarCotacaoBancarios(ativo, nbBTG, headers)
                puResgate = dadosResgate['redemptionPrice']
                txResgate = str(dadosResgate['redemptionRate'])
            else:
                # Chama a função que retorna o PU e Taxa de Resgate dos ativos de crédito privado
                dadosResgate = realizarCotacaoCP(ativo, nbBTG, headers)
                if dadosResgate == 'Error':
                    puResgate = None
                    txResgate = None
                else:
                    puResgate = dadosResgate['puResgate']
                    txResgate = str(dadosResgate['taxaResgate'])
            
            #Formata a data de vencimento
            vencimento = ativo['maturityDate']
            vencimento = datetime.datetime.strptime(vencimento, "%Y-%m-%dT%H:%M:%S.%f%z")
            vencimento = vencimento.strftime("%d/%m/%Y")
            
            # Formata o texto do grupo dos ativos
            if grupo == 'Debênture':
                grupo = 'DEB'

            emissor = ativo['issuer']
            nomeAtivo = grupo + ' ' + emissor + ' - ' + vencimento
            qtd = ativo['quantity']
            txCompra = ativo['indexYieldRate']
            puCurva = ativo['price']
            ticker = ativo['cetipCode']

            if puResgate != None and txResgate != None:
                resgBruto = locale.currency(puResgate * qtd)
                agioDesagio = ((puResgate / puCurva) - 1) * 100
                agioDesagio = locale.format_string('%.2f%%', agioDesagio, grouping=True)
                puResgate = locale.currency(puResgate)

                if txResgate != None:
                    txResgate = txResgate.replace('.', ',')
                    txResgate = indexador + ' + ' + str(txResgate) + '%'
                else:
                    txResgate = '-'
            else:
                puResgate = '-'
                
                resgBruto = '-'
                agioDesagio = 'Solicitar Cotação'

            print('--------------------------------')
            print(nomeAtivo + 'QTD - ' + str(qtd) + ' - ' + str(agioDesagio))

            # Indica em qual coluna os dados devem ser inseridos
            btgDados.loc[lin, "DATA"] = '18/10/2023'
            btgDados.loc[lin, "CLIENTE"] = nomeCliente
            btgDados.loc[lin, "ATIVO"] = nomeAtivo
            btgDados.loc[lin, "QTD"] =  int(qtd)
            btgDados.loc[lin, "TAXA COMPRA"] = txCompra
            btgDados.loc[lin, "TAXA RESG."] = txResgate
            btgDados.loc[lin, "PU CURVA"] = locale.currency(puCurva)
            btgDados.loc[lin, "PU RESG."] = puResgate
            btgDados.loc[lin, "RESGATE BRUTO"] = resgBruto
            btgDados.loc[lin, "RESGATE LÍQ."] = '-'
            btgDados.loc[lin, "ÁGIO/DESÁGIO"] = agioDesagio
            btgDados.loc[lin, "CÓD VIRTUAL"] = ticker
            lin = lin + 1
            time.sleep(2)

        #print(btgDados)

        btgDados.to_excel(f"Cotação {nomeCliente} - BTG {nbBTG} - {dataFormatada}.xlsx")
        print("----------------------------------------------------------------")
        print("                        Posições Salvas                         ")
        print("----------------------------------------------------------------")   

    else:
        print('A solicitação falhou. Código de status:', response.status_code)
        print(response.text)

def realizarCotacaoCP(ativo, nbBtg, headers):

    payload ={
            "accountNumber": nbBtg,
            "accountingGroupCode": ativo['accountingGroupCode'],
            "fixedIncomeAcquisitions": ativo['fixedIncomeAcquisitions'],
            "referenceIndexName": ativo['referenceIndexName'],
            "ticker": ativo['ticker'],
            "yield": ativo['yield']
        }

    # URL da solicitação
    url = 'https://access.btgpactualdigital.com/op/api/rmadmin/indicatives/settlement'

    # Realize a solicitação POST
    response = requests.post(url, headers=headers, json=payload)

    # Verifique a resposta
    if response.status_code == 200:
        print('Solicitação bem-sucedida')
        return response.json()
    else:   
        print('A solicitação falhou. Código de status:', response.status_code)
        return 'Error'
    

def realizarCotacaoBancarios(ativo, nbBtg, headers):

    grupo = ativo['accountingGroupCode']
    codSeguranca = ativo['securityCode']

    url = f'https://access.btgpactualdigital.com/op/api/settlement/quotations/{codSeguranca}?accountNumber={nbBtg}&accountingGroupCode={grupo}'

    # Realize a solicitação POST
    response = requests.get(url, headers=headers)

    # Verifique a resposta
    if response.status_code == 200:
        print('Solicitação bem-sucedida')
        return response.json()
    else:   
        print('A solicitação falhou. Código de status:', response.status_code)
        return response.status_code