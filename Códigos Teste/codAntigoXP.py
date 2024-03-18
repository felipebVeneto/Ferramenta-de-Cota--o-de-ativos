# Macro que puxa a cotação de cada ativo do cliente
import tkinter as tk
import datetime
import requests
import pandas as pd
import time
import locale

# Define a formatação dos valores monetários
locale.setlocale(locale.LC_ALL, 'pt_BR')

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


def cotarXP(nbXP, nomeCliente, bearer, subscriptionKey, dataFormatada, hora):
    
    if hora >= 15:
        print('----------------------------------------------------------------')
        print("O mercado já fechou, tente novamente antes das 15:00h do próximo dia útil!")
        print('----------------------------------------------------------------')
        return 

    planCotacao = pd.read_excel(f"Cotação {nomeCliente} - XP {nbXP} - {dataFormatada}.xlsx")

    planCotacao["QTD"] =  planCotacao["QTD"].astype('object')
    planCotacao["PU CURVA"] =  planCotacao["PU CURVA"].astype('object')
    planCotacao["PU RESG."] =  planCotacao["PU CURVA"].astype('object')
    planCotacao["TAXA RESG."] =  planCotacao["TAXA RESG."].astype('object')
    planCotacao["RESGATE BRUTO"] =  planCotacao["RESGATE BRUTO"].astype('object')
    planCotacao["RESGATE LÍQ."] =  planCotacao["RESGATE LÍQ."].astype('object')
    planCotacao["ÁGIO/DESÁGIO"] =  planCotacao["ÁGIO/DESÁGIO"].astype('object')

    codVirtual = planCotacao['CÓD VIRTUAL']

    # Determina os headers da requisição
    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey,
                'Authorization': 'Bearer ' + bearer,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
                }

    lin = 0

    for codVirtual in codVirtual:
        #print("O cod " + str(codVirtual))
        
        # Determina a URL de cada ativo
        url = f'https://api.xpi.com.br/rede-fixedincome/v1/orders/customers/{nbXP}/sales/{codVirtual}/validation'
        # print(url)
        
        time.sleep(2)

        # Realiza a requisição e armazena a resposta
        response = requests.get(url, headers=headers)

        

        #print(planCotacao)

        # Verifica se a requisição foi aceita
        if response.status_code == 200:
            
            # Pega o JSON retornado pela requisição
            data = response.json()

            #print(data)

            print('Ativo: ' + data['nickName'])
            print('-----------------')
            # Pega a quantidade do ativo na carteira do cliente
            qtd = data['quantityAvailable']
            print('Quantidade disponível: ' + str(qtd))
            print('-----------------')
            planCotacao.loc[lin, "QTD"] = qtd


            # # Pega uma lista com a posição bruta e liquida
            # price = data['price']

            # if len(price) > 0:
            #     posBruta  = price[0]
            #     posLiq = price[1]

            puCurva = data['currentPrice']
            print('O PU na Curva é ' + str(puCurva))
            planCotacao.loc[lin, "PU CURVA"] = locale.currency(puCurva)

            # print('Posição Bruta: ' + str(posBruta['grossposition']))
            # print('-----------------')
            # print('Posição com ROA Máx: ' + str(posLiq['grossposition']))
            # print('-----------------')

            # Pega uma lista com as opções de resgate
            opcoesResgate = data['redemptionOptions']

        #print(opcoesResgate)
            
            if opcoesResgate == []:           
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
            # Varre a lista de opções de resgate
                for option in opcoesResgate:
                    #print(option)

                    # Pega a opção com ROA = 0
                    if option['roa'] == 0:
                        
                        #Seleciona a taxa com ROA = 0
                        taxaResg = option['descriptionFee']
                        # print("A taxa selecionada foi: " + taxaResg)
                        # print('-----------------')
                        planCotacao.loc[lin, "TAXA RESG."] = taxaResg

                        #Pega o PU com ROA = 0
                        puResg = option['unitPrice']
                        # print("O preço unitário de resgate será: " + str(puResg))
                        # print('-----------------')
                        planCotacao.loc[lin, "PU RESG."] = locale.currency(puResg)

                        #Calcula o Valor bruto de acordo com o site
                        valorBruto = puResg * qtd
                        # print("O valor de resgate bruto será: " + str(valorBruto))
                        # print('-----------------')
                        planCotacao.loc[lin, "RESGATE BRUTO"] = locale.currency(valorBruto)
                        
                        #Calcula o valor líquido de acordo com o site
                        imposto = option['incomeTax']
                        valorLiq = valorBruto - imposto
                        planCotacao.loc[lin, "RESGATE LÍQ."] = locale.currency(valorBruto)
                        
                        #Calcula o ágio ou deságio
                        agioDesagio = (puResg/puCurva) - 1
                        planCotacao.loc[lin, "ÁGIO/DESÁGIO"] = locale.format_string('%.2f', agioDesagio, grouping=True)

                        # Verifica se retornou uma lista de opções vazia
                        if option['roa'] == []:
                            # Verifica se já passou das 15:00 horas
                            if hora >= 15:
                                print('-----------------')
                                print("O mercado já fechou")
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

                        #print(planCotacao)

                        # planCotacao.to_excel(f"Cotação {nomeCliente} - XP {nbXP} - {dataFormatada}.xlsx")
                        # print("----------------------------------------------------------------")
                        # print("Planilha Salva")
                        # print("----------------------------------------------------------------")
        else:
            print('Error:', response.status_code, response.text)
            show_error_message()

    planCotacao = planCotacao.drop(columns=[col for col in planCotacao.columns if 'Unnamed: ' in col])
    print(planCotacao)

    planCotacao.to_excel(f"Cotação {nomeCliente} - XP {nbXP} - {dataFormatada}.xlsx")
    print("----------------------------------------------------------------")
    print("Planilha Salva")
    print("----------------------------------------------------------------")