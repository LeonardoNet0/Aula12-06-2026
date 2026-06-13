import pandas as pd 
import numpy as np 

try:
    print('Obtendo os dados...')
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    # utf-8, iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    # delimitando as variáveis
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]
    # print(df_roubo_veiculo)

    # Totalizando os roubos pelos municípios
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()
    
    # ordenado o dataframe
    df_roubo_veiculo = df_roubo_veiculo.sort_values(by='roubo_veiculo', ascending=False)
    # print(df_roubo_veiculo.head(10))
    print(df_roubo_veiculo)

except Exception as e:
    print(f'Erro ao obter dados {e}')


# Obtendo a medidas
try:
    print('Calculando as medidas... ')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)


    distancia = abs((media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100)

    print('\nMedidas de Tendência Central')
    print(30*"=")
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distancia: {distancia} %')

except Exception as e:
    print(f'Erro ao processar as medidas {e}')


# Obtendo a distribuição
try:
    print('Processando os quartis')

    q1 = np.quantile(array_roubo_veiculo, .25)
    q3 = np.quantile(array_roubo_veiculo, .75)

    print('\nQuartis')
    print(30*"=")
    print(f'Q1: {q1}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Q3: {q3}')


    # Municípios com menos roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]

    # Municípios com mais roubos
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]

    print('\nMunicípios com menos casos de roubos: ')
    print(30*"=")
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))

    print('\nMunicípios com Mais Roubos: ')
    print(30*"=")
    print(df_roubo_veiculo_maiores)

except Exception as e:
    print(f'Erro ao obter a distribuição {e}')

#obtendo medidas de dispersão
try:
    #amplitude total
    #amplitude = maximo - minimo
    #resultado: mais proximo do minimo, baixa dispersao.
    #se for 0, quer dizer que todos os dados sao iguais 
    #se mais proximo do maior valor, alta dispersao.
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo

    print(f'Medidas de dispersao')
    print(30*'=')
    print(f'maximo: {maximo}')
    print(f'maximo: {minimo}')
    print(f'amplitude total: {amplitude}')



except Exception as e:
    print(f'Erro ao calcular medidas de dispersao: {e}')



#calcular outliers
try: 
#iqr (intervalo interquartil) - A amplitude dos 50% dos dados mais centrais.
#iqr = q3 - q1
# Ele ignora os valores extremos . max e min estao fora do intervalo iqr
#nao sofre interferencia dos valores extremos.
#quanto mais proximo do zero, mais homogeneos sao os dados
#quanto mais proximo do q3, menos homogeneos sao os dados
    iqr = q3 - q1


#limite inferior: 
# é uma medida que vai identificar como outliers os valores abaixo dele.
    limite_inferior = q1 - (1.5 * iqr)



#limite superior: 
# é uma medida que vai identificar como outliers os valores acima dele.
    limite_superior = q3 + (1.5 * iqr)

    print(f'Medidas')
    print(30*'=')
    print(f'minimo: {minimo}')
    print(f'limite inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'mediana:{mediana_roubo_veiculo}') #q2
    print(f'Q3: {q3}')
    print(f'limite superior: {limite_superior}')
    print(f'Maximo: {maximo}')

   


except Exception as e:
    print(f'Erro ao calcular outliers: {e}')

 #exibindo os outliers

try:
    #outliers superiores
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]

    #outliers inferiores 
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]

    print(f'\nMunicipios c/ Outliers inferiores ')
    print(30*'=')
    if len(df_roubo_veiculo_outliers_inferiores) == 0:

        print('nao existe outliers inferiores ')

    else: 
        print(df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=False))





    print(f'\nMunicipios c/ Outliers superiores ')
    print(30*'=')
    if len(df_roubo_veiculo_outliers_superiores) == 0:

        print('nao existe outliers superiores ')

    else: 
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=True))

except Exception as e: 
    print(f'erro ao calcular Outliers: {e}')




 