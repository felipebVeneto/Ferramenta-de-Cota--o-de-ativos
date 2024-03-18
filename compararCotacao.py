from datetime import datetime
import locale
import pandas as pd

def compararCotacao(cliente, officer, dataArq, dataHoje, instituicao):
    locale.setlocale(locale.LC_ALL, 'pt_BR')
    caminho = f'Z:\RENDA FIXA\Área de Análise\Renda Fixa\Cotações\{officer}\\'

    arqAtual = f'Cotação {cliente} - {instituicao} - {dataHoje}.xlsx'
    arqComparacao = f'Cotação {cliente} - {instituicao} - {dataArq}.xlsx'

    cotacaoAtual = pd.read_excel(caminho + arqAtual, "Sheet1")
    
    # Testa se o arquivo a ser comparado realmente existe
    try:
        cotacaoComparacao = pd.read_excel(caminho + arqComparacao, "Sheet1")
    except:
        print ('Não foi encontrada cotação na data ' + dataArq +'! Verifique a pasta e os dados do cliente!')
        return
    
    templateComparacao = pd.read_excel('templateComparacao.xlsx', "Template")

    print(templateComparacao)

    ativos = cotacaoAtual['ATIVO']

    lin = 0
    for ativo in ativos:

        linAtivo = cotacaoAtual.loc[cotacaoAtual["ATIVO"] == ativo]
        linAtivo = linAtivo.index[0]
        qtdAtivo = cotacaoAtual.loc[linAtivo, "QTD"]
        txaCompra = cotacaoAtual.loc[linAtivo, "TAXA COMPRA"]
        agioDesagio = cotacaoAtual.loc[linAtivo, "ÁGIO/DESÁGIO"] 
        taxaResg = cotacaoAtual.loc[linAtivo, "TAXA RESG."]
        puResg = cotacaoAtual.loc[linAtivo, "PU RESG."] 
        resgBruto = cotacaoAtual.loc[linAtivo, "RESGATE BRUTO"] 
        
        if qtdAtivo == 0 and agioDesagio == 'Sem liquidez':
            linAtivoComparado = cotacaoComparacao.loc[(cotacaoComparacao["ATIVO"] == ativo) & (cotacaoComparacao["TAXA COMPRA"] == txaCompra)]
            linAtivoComparado = linAtivoComparado.index[0]
        else:
            linAtivoComparado = cotacaoComparacao.loc[(cotacaoComparacao["ATIVO"] == ativo) & (cotacaoComparacao["QTD"] == qtdAtivo) & (cotacaoComparacao["TAXA COMPRA"] == txaCompra)]
            linAtivoComparado = linAtivoComparado.index[0]
        
        ativoComparado = cotacaoComparacao.loc[linAtivoComparado, "ATIVO"]
        qtdAtivoComparado = cotacaoComparacao.loc[linAtivoComparado, "QTD"]
        txaCompraComparado = cotacaoComparacao.loc[linAtivoComparado, "TAXA COMPRA"]
        agioDesagioComparado = cotacaoComparacao.loc[linAtivoComparado, "ÁGIO/DESÁGIO"] 
        puCurvaComparado = cotacaoComparacao.loc[linAtivoComparado, "PU CURVA"]
        puResgComparado = cotacaoComparacao.loc[linAtivoComparado, "PU RESG."]
        taxaResgComparado = cotacaoComparacao.loc[linAtivoComparado, "TAXA RESG."]
        resgBrutoComparado = cotacaoComparacao.loc[linAtivoComparado, "RESGATE BRUTO"]
        if instituicao == 'XP':
            resgLiqComparado = cotacaoComparacao.loc[linAtivoComparado, "RESGATE LÍQ."]

        data = datetime.strptime(dataArq, "%d.%m.%y")
        data = data.strftime("%d/%m/%Y")

        if agioDesagio == 'Sem liquidez' or agioDesagioComparado == 'Sem liquidez':
            diferenca = '-'
            status = 'SEM LIQUIDEZ'
            agioDesagioComparado = '-'
            agioDesagio = '-'
        else:
            # Compara os deságios e verifica se o ativo pode ou não ser vendido
            diferenca = agioDesagio - agioDesagioComparado
            puCurvaComparado = locale.currency(puCurvaComparado)
            puResgComparado = locale.currency(puResgComparado)
            resgBrutoComparado = locale.currency(resgBrutoComparado)
            puResg = locale.currency(puResg)
            resgBruto = locale.currency(resgBruto)
            
            if instituicao == 'XP':
                resgLiqComparado = locale.currency(resgLiqComparado)
            # else:
            #     resgLiqComparado = '-'

            if diferenca < (-0.005):
                status = 'VERIFICAR COM OFFICER'
            else:
                status = 'VENDA PERMITIDA'

            agioDesagioComparado = agioDesagioComparado * 100
            agioDesagio = agioDesagio * 100
            agioDesagio = locale.format_string('%.2f%%', agioDesagio, grouping=True) 
            agioDesagioComparado = locale.format_string('%.2f%%', agioDesagioComparado, grouping=True)     
            print(agioDesagio)
            print(agioDesagioComparado)
            diferenca = diferenca * 100
            diferenca = locale.format_string('%.2f%%', diferenca, grouping=True) 
        
        # Cola os dados da cotação comparada
        templateComparacao.loc[lin,'DATA'] = data
        templateComparacao.loc[lin,'CLIENTE'] = cliente
        templateComparacao.loc[lin,'ATIVO'] = ativoComparado
        templateComparacao.loc[lin,'QTD'] = qtdAtivoComparado
        templateComparacao.loc[lin,'TAXA COMPRA'] = txaCompraComparado
        templateComparacao.loc[lin,'TAXA RESG.'] = taxaResgComparado
        templateComparacao.loc[lin,'TAXA RESG. - ATUAL'] = taxaResg
        templateComparacao.loc[lin,'PU CURVA'] = puCurvaComparado
        templateComparacao.loc[lin,'PU RESG.'] = puResgComparado
        templateComparacao.loc[lin,'RESGATE BRUTO'] = resgBrutoComparado
        if instituicao == 'XP':
            templateComparacao.loc[lin,'RESGATE LÍQ.'] = resgLiqComparado
        templateComparacao.loc[lin,'ÁGIO/DESÁGIO - ATUAL'] = agioDesagio
        templateComparacao.loc[lin,'ÁGIO/DESÁGIO'] = agioDesagioComparado
        templateComparacao.loc[lin,'DIFERENÇA'] = diferenca
        templateComparacao.loc[lin,'PU RESG. - ATUAL'] = puResg
        templateComparacao.loc[lin,'RESGATE BRUTO - ATUAL'] = resgBruto
        templateComparacao.loc[lin,'STATUS'] = status

        lin = lin + 1

    print(templateComparacao)
    templateComparacao.to_excel(f"{caminho}Comparação {cliente} - {instituicao} - {dataArq} Vs {dataHoje}.xlsx")

