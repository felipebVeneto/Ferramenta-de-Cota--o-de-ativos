import os

def encontrarArquivo(nomeCliente, instituicao):
  diretorio = 'C:\\Users\\felipe.batista\\Desktop\\Ferramenta de Cotação de ativos'

  dataArq = None

  files = os.listdir(diretorio)

  for file in files:
    if nomeCliente in file:
      nomeArq = file.split(' - ')
      dataArq = nomeArq[-1].split('.xlsx')[0]
      instituicaoArq = nomeArq[1].split(' ')[0]
      if instituicaoArq == instituicao:
        return  dataArq
    
  return  None
