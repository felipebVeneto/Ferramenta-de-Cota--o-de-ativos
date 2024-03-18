import os
from datetime import datetime

def encontrarArquivoRecente(nomeCliente, instituicao, officer, dataHoje):

  diretorio = f'Z:\\RENDA FIXA\\Área de Análise\\Renda Fixa\\Cotações\\{officer}'
  dataArq = None
  dataHoje = datetime.strptime(dataHoje, "%d/%m/%y")

  files = os.listdir(diretorio)

  ultDif = 100
  dataMaisRecente = ''
  arqExiste = False

  for file in files:
    if nomeCliente in file and 'Comparação' not in file:
      nomeArq = file.split(' - ')
      dataArq = nomeArq[-1].split('.xlsx')[0]
      dataArq = dataArq.split('.')
      dia = dataArq[0]
      mes = dataArq[1]
      ano = dataArq[2]
      dataArq = dia + '/' + mes + '/' + ano
      dataArq = datetime.strptime(dataArq, "%d/%m/%y")
      instituicaoArq = nomeArq[1].split(' ')[0]
      if instituicaoArq == instituicao:
        difData =  dataHoje - dataArq
        difEmDias = difData.days
        if difEmDias < ultDif and dataArq != dataHoje:
            ultDif = difEmDias
            dataMaisRecente = dataArq
        elif dataArq == dataHoje:
            arqExiste = True
    
  return  dataMaisRecente, arqExiste

