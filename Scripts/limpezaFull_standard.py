import pandas as pd
import glob
import os

def limpezaStandard(df):
    
    df.columns = df.columns.droplevel(0)

    lista_colunas = list(df.columns)
    lista_colunas[16] = 'Gls_90'
    lista_colunas[17] = 'Ast_90'
    lista_colunas[18] = 'G+A_90'
    lista_colunas[19] = 'G-PK_90'
    lista_colunas[4] = 'Matches Played'
    lista_colunas[7] = '90s Played'
    df.columns = lista_colunas

    df = df.drop(columns= ['Matches', '-9999'])
    df = df.dropna(subset=['Min'])
    df = df.dropna(subset=['Pos'])

    df['Nation'] = df['Nation'].str[-3:]
    df['Pos'] = df['Pos'].str[:2]

    conversoes = {
    'Age': 'Int64',
    'Min': 'Int64',
    'Gls': 'Int64',
    'Ast': 'Int64',
    'G+A': 'Int64',  
    'G-PK': 'Int64', 
    'PK': 'Int64',
    'PKatt': 'Int64',
    'CrdY': 'Int64',
    'CrdR': 'Int64',
    }
    df = df.astype(conversoes)

    return df

pasta_raw = "Data/raw/standard_stats/*.csv"
pasta_clean = "Data/clean/standard_stats/"

csv_files_raw = glob.glob(pasta_raw)

for arquivo in csv_files_raw:
    df = pd.read_csv(arquivo, skiprows=1, header=[0, 1], encoding='utf 16')
    df = limpezaStandard(df)
    time = os.path.basename(arquivo).split("_")[0]
    df.to_csv(f"{pasta_clean}{time}_standard_clean.csv", index=False)

print("Limpeza Completa!")