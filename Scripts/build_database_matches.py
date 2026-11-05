import pandas as pd
import glob
import os

lista_dfs = []
dim_squad = pd.read_csv('Database/dim_squad.csv')

caminho_arquivos = 'Data/clean/matches_stats/*.csv'
arquivos_matches = glob.glob(caminho_arquivos)

for arquivo in arquivos_matches:
    df = pd.read_csv(arquivo)
    nome_arquivo = os.path.basename(arquivo)
    nome_time = nome_arquivo.replace('.csv', '').replace('_matches_clean', '')
    df['Squad'] = nome_time
    lista_dfs.append(df)

df_todos_jogos = pd.concat(lista_dfs, ignore_index=True)

df_jogos_unicos = df_todos_jogos[df_todos_jogos['Venue'] == 'Home']

df_jogos_unicos = df_jogos_unicos.rename(columns={
    'Squad': 'Home_Team',
    'Opponent': 'Away_Team',
    'GF': 'Home_Goals',
    'GA': 'Away_Goals',
    'Poss': 'Home_Possession',
    'Formation': 'Home_Formation',
    'Opp Formation': 'Away_Formation'
})

df_jogos_unicos = pd.merge(df_jogos_unicos, dim_squad, left_on='Home_Team', right_on='Squad', how='left')
df_jogos_unicos = df_jogos_unicos.rename(columns={'squad_id': 'Home_Team_id'})
df_jogos_unicos = df_jogos_unicos.drop(columns=['Squad'])

df_jogos_unicos = pd.merge(df_jogos_unicos, dim_squad, left_on='Away_Team', right_on='Squad', how='left')
df_jogos_unicos = df_jogos_unicos.rename(columns={'squad_id': 'Away_Team_id'})
df_jogos_unicos = df_jogos_unicos.drop(columns=['Squad'])

df_jogos_unicos = df_jogos_unicos.drop(columns=['Home_Team', 'Away_Team', 'Venue'])

ordem_colunas = [
    'Date', 'Time', 'Round', 'Day', 
    'Home_Team_id', 'Away_Team_id', 'Home_Goals', 'Away_Goals', 'Result', 
    'Home_Possession', 'Attendance', 'Home_Formation', 'Away_Formation', 
    'Captain', 'Referee'
]

df_jogos_unicos = df_jogos_unicos[ordem_colunas]

df_jogos_unicos = df_jogos_unicos.sort_values(by="Round")

df_jogos_unicos.to_csv('Database/fact_matches.csv', index=False)
print("Tabela gerada com sucesso!")

