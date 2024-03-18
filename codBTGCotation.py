import requests

def realizarCotacaoCP(ativo, nbBtg, headers):

    payload ={
            "accountNumber": '00' + str(nbBtg),
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
        return response.status_code
    

def realizarCotacaoBancarios(ativo, nbBtg, headers):

    grupo = ativo['accountingGroupCode']
    codSeguranca = ativo['securityCode']

    url = f'https://access.btgpactualdigital.com/op/api/settlement/quotations/{codSeguranca}?accountNumber=00{nbBtg}&accountingGroupCode={grupo}'

    # Realize a solicitação POST
    response = requests.get(url, headers=headers)

    # Verifique a resposta
    if response.status_code == 200:
        print('Solicitação bem-sucedida')
        return response.json()
    else:   
        print('A solicitação falhou. Código de status:', response.status_code)
        return response.status_code