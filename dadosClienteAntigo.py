import pandas as pd
import math

def buscarDados(nbVeneto):

    monday = pd.read_excel('monday.xlsx', skiprows=(0, 1), dtype={'CONTA BTG': str})

    #Verifica se o NB existe na base
    resultado = monday.loc[monday["CONTA VENETO"] == nbVeneto]

    if resultado.empty:
        monday = pd.read_excel('monday4plan.xlsx', skiprows=(0, 1), dtype={'CONTA BTG': str})

        try:
            resultado = monday.loc[monday["CONTA VENETO"] == nbVeneto]
            # Retorna erro caso não encotre o NB em nenhuma das duas bases
            if resultado.empty:
                print('O NB fornecido não existe na base!')
                return 'ERROR'
        except:
                print('O NB fornecido não existe na base!')
                return 'ERROR'


    # Determina a linha dos dados do cliente
    try:
        lin = resultado.index[0]

        # Pega o NB da XP
        nbXP = monday.loc[lin, "CONTA XP"]
        
        if math.isnan(nbXP):
            nbXP = "-"
        else:
            nbXP = int(nbXP)
        
        # Pega o NB do BTG
        nbBTG = monday.loc[lin, "CONTA BTG"]
        
        if type(nbBTG) == float and math.isnan(nbBTG):
            nbBTG = "-"


        # Pega o nome
        nomeCliente = monday.loc[lin, "Name"]

        cpf = monday.loc[lin, "CPF / CNPJ"]
        # Pega o nome do Officer
        officer = monday.loc[lin, "FARMER"]

        return nbXP, nbBTG, officer, nomeCliente, cpf
    except:
        print('Ocorreu um erro!')
        return 
        
