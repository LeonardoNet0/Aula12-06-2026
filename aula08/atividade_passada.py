import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
try:
    print('Obtendo os dados....')
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

   # utf-8, iso8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep= ';', encoding='iso-8859-1')
   
    #delimitando as variaveis
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]
    

    # TOTALIZANDO OS ROUBOS PELOS MUNICIPIOS
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum() # as_index ele reseta os indices, voltando a tabela original.

    df_roubo_veiculo = df_roubo_veiculo.sort_values(by= 'roubo_veiculo', ascending=False)
    

    print(df_roubo_veiculo.head(10))

except Exception as e:
    print(f'Erro ao obter dados {e}')


# OBTENDO AS MEDIDAS
try:
    print('Calculando as Medidas...')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia = abs((media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100)

    print('\nMedidas de Tendência Central')
    print(30*'=')
    print(f'Média: {media_roubo_veiculo:.2f}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distancia : {distancia:.2f} %')


except Exception as e:
    print('Erro ao calcular a medida')


#OBTENDO MEDIDAS DESCRITIVAS
try:
    print('Processando os quartis')

    q1 = np.quantile(array_roubo_veiculo, .25)
    q3 = np.quantile(array_roubo_veiculo, .75)

    print('\n Quartis')
    print(30*'=')
    print(f' Q1: {q1}')
    print(f' Mediana: {mediana_roubo_veiculo}')
    print(f' Q3: {q3}')


    # MUNICIPIO COM MENOS ROUBOS
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]
    # MUNICIPIO COM MAIS ROUBOS
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]

    print('\n Municípios com menos casos de roubos')
    print(30*'=')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))

    print('\n Municípios com menos casos de roubos')
    print(30*'=')
    print(df_roubo_veiculo_maiores)

except Exception as e:
    print(f'Erro ao obter a distribuição {e}')



#OBTENDO MEDIDA DE DISPERSÃO
try:
    # Amplitude Total
    # mplitude = maximo - mínimo
    # Quanto mais próximo do Zero, baixa dispersão
    # Se for 0, quer dizer que todos os dados são iguais
    # Se mais próximo do maior valor, alta dispersão
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo
    print('\n Medidas de Dispersão')
    print(30*'=')
    print(f'Máximo: {maximo}')
    print(f'Mínimo:{minimo}')
    print(f'Amplitude total:{amplitude}')



except Exception as e:
    print(f'Erro ao calcula medidas de dispersão: {e}')


#CALCULAR OUTLIERS
try:
    # IQR (INTERVALO INTERQUARTIL) - AMPLITUDE DOS 50% DOS DADOS MAIS CENTRAIS
    # IQR = Q3 - Q1 
    # ELE IGNORA OS VALORES EXTREMOS. MAX E MIN ESTÃO FORA DO INTERVALO IQR
    # NÃO SOFRE INTERFERÊNCIA DOS VALORES EXTREMOS.
    # QUANTO MAIS PROXIMO DO ZERO, MAIS HOMOGÊNEOS SÃO OS DADOS
    # QUANTO MAIS PROXIMO DO Q3, MENOS HOMOGÊNEOS SÃO OS DADOS
    iqr = q3 - q1

    # limite inferior: 
    # É UMA MEDIDA QUE IDENTIFICAR COMO OUTLIERS, OS VALORES ABAIXO DELE
    limite_inferior = q1 - (1.5 * iqr)
    
    # limite superior: 
    # É UMA MEDIDA QUE IDENTIFICAR COMO OUTLIERS, OS VALORES ACIMA DELE
    limite_superior = q3 + (1.5 * iqr)

    print('\n Medidas')
    print(30*'=')
    print(f'Mínimo: {minimo}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Mediana: {mediana_roubo_veiculo}') # Q2
    print(f'Q3: {q3}')
    print(f'Limite Superior: {limite_superior}')
    print(f'Máximo: {maximo}')
    

except Exception as e:
    print(f'Erro ao Calcular os limites: {e}')

# EXIBINDO OS OUTLIERS
try:
    # OUTLIERS SUPERIORES
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    
    # OUTLIERS INFERIORES
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]

    print('\n Municípios c/ Outliers Inferiores')
    print(30*'=')
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print('Não existe Outliers Inferiores!.')
    else:
        print(df_roubo_veiculo_outliers_inferiores.sort_values(by= 'roubo_veiculo', ascending=True))

    print('\n Municípios c/ Outliers Superiores')
    print(30*'=')
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print('Não existe Outliers Superiores!.')
    else:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by= 'roubo_veiculo', ascending=False))

except Exception as e:
    print(f'Erro ao Calcular Outliers {e}')


try:
    plt.bar(df_roubo_veiculo_maiores['munic'], df_roubo_veiculo_maiores['roubo_veiculo'])
    plt.show()




except Exception as e:
    print(f'Erro grafico {e}')