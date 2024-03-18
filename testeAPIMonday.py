import requests
import json

nb = "10096"
username = "felipe.batista"
password = "Veneto@123"

def dadosClientes(nb, username, password):
  url = 'http://api-veneto.azurewebsites.net/dadosCadastrais/clientes'  # Substitua pela URL correta da API
  
  dados = {
    "username" : username,
    "password" : password
  }

  # Enviar a requisição POST com o JSON
  response = requests.get(url, json=dados)

  # Verificar a resposta
  if response.status_code == 200:  # Se a resposta for bem sucedida (código 200)
      resposta_api = response.json()  # Converte a resposta para JSON
      # print("Login bem sucedido. Resposta da API:", resposta_api)

      cliente = next((cliente for cliente in resposta_api if cliente['cod_cliente'] == nb), None)
      nome = cliente['iniciais_cliente']
      cpf = cliente['cpf_cnpj']

  else:
      print("Falha no login. Código de status:", response.status_code)
      return


  url = 'http://api-veneto.azurewebsites.net/dadosCadastrais/contas'  # Substitua pela URL correta da API

  # # Enviar a requisição POST com o JSON
  response = requests.get(url, json=dados)

  # Verificar a resposta
  if response.status_code == 200:  # Se a resposta for bem sucedida (código 200)
      resposta_api = response.json()  # Converte a resposta para JSON

      for produto in resposta_api:
        if  produto['cod_produto'] == nb:
          print(produto)
        if produto['instituicao'] == 'XP':
          contaXP = produto['conta']
        if produto['instituicao'] == 'BTG':
          contaBTG = produto['conta']
  else:
      print("Falha no login. Código de status:", response.status_code)
      return

  return  nome, contaXP, contaBTG, cpf


nome, contaXP, contaBTG, cpf = dadosClientes(nb, username, password)

print("--------------------------------")
print(nome)
print("XP: " + str(contaXP))
print("BTG: " + str(contaBTG))
print(cpf)
print("--------------------------------")