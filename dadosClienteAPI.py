import requests

def buscarDadosClientes(username, password):

  url = 'http://api-veneto.azurewebsites.net/dadosCadastrais/clientes'  # Substitua pela URL correta da API
  
  dados = {
    "username" : username,
    "password" : password
  }

  # Enviar a requisição POST com o JSON
  response = requests.get(url, json=dados)

  # Verificar a resposta
  if response.status_code == 200:  # Se a resposta for bem sucedida (código 200)
      dadosClientes = response.json()  # Converte a resposta para JSON
  else:
      print("Falha no login. Código de status:", response.status_code)
      return None
  
  url = 'http://api-veneto.azurewebsites.net/dadosCadastrais/contas'  # Substitua pela URL correta da API

  # # Enviar a requisição POST com o JSON
  response = requests.get(url, json=dados)

  # Verificar a resposta
  if response.status_code == 200:  # Se a resposta for bem sucedida (código 200)
      dadosContas = response.json()  # Converte a resposta para JSON
  else:
      print("Falha no login. Código de status:", response.status_code)
      return None

  return dadosClientes, dadosContas
  
  