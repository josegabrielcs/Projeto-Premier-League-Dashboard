import pandas as pd
import glob
import os

lista_dfs = []
dim_squad = pd.read_csv('Database/dim_squad.csv')

caminho_arquivos = 'Data/clean/standard_stats/*.csv'
arquivos_matches = glob.glob(caminho_arquivos)

for arquivo in arquivos_matches:
    df = pd.read_csv(arquivo)
    nome_arquivo = os.path.basename(arquivo)
    nome_time = nome_arquivo.replace('.csv', '').replace('_standard_clean', '')
    df['Squad Name'] = nome_time
    lista_dfs.append(df)

df_todos_jogadores = pd.concat(lista_dfs, ignore_index=True)

df_todos_jogadores = pd.merge(df_todos_jogadores, dim_squad, left_on='Squad Name', right_on='Squad', how='left')
df_todos_jogadores = df_todos_jogadores.drop(columns=['Squad Name', 'Squad'])

df_todos_jogadores = df_todos_jogadores.rename(columns={'Player': 'Name'})

colunas_cadastro = ['Name', 'Nation', 'Pos', 'Age']
df_dim = df_todos_jogadores[colunas_cadastro]

df_dim = df_dim.drop_duplicates(subset=['Name'], keep='first').reset_index(drop=True)

df_dim.reset_index(inplace=True)
df_dim = df_dim.rename(columns={'index':'player_id'})
df_dim['player_id'] = df_dim['player_id'] + 1

df_merge = pd.merge(
    df_todos_jogadores,
    df_dim
)

colunas_stats = [
    'player_id', 'squad_id', 'Matches Played', 'Starts', 'Min', '90s Played', 
    'Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR', 
    'Gls_90', 'Ast_90', 'G+A_90', 'G-PK_90', 'G+A-PK'
]

df_fact = df_merge[colunas_stats].copy()

caminho_dim = 'Database/dim_player.csv'
caminho_fact = 'Database/fact_player_stats.csv'

df_dim.to_csv(caminho_dim, index=False)

df_fact.to_csv(caminho_fact, index=False)

print("Tabelas geradas com sucesso!")