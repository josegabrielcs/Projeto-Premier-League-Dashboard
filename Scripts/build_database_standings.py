import pandas as pd
import os

caminho_standings = 'Data/clean/league_standings/League_standings_clean.csv'

df_standings = pd.read_csv(caminho_standings)

df_dim = df_standings[['Squad']].drop_duplicates()

df_dim.reset_index(inplace=True)
df_dim = df_dim.rename(columns = {'index':'squad_id'})
df_dim['squad_id'] = df_dim['squad_id'] + 1

df_fact = pd.merge(df_dim, df_standings)

colunas_finais = [
    'squad_id', 'Rk', 'MP', 'Wins', 'Draws', 'Loses', 'GF', 'GA', 'GD', 'Pts', 'Pts_MP', 
    'Avg_Attendance', 'Top Scorer Name', 'Top Scorer Goals', 'Goalkeeper', 'Qualification'
]
df_fact = df_fact[colunas_finais]

caminho_dim = 'Database/dim_squad.csv'
caminho_fact = 'Database/fact_standings.csv'

df_dim.to_csv(caminho_dim, index=False)
df_fact.to_csv(caminho_fact, index=False)

print("Tabelas geradas com sucesso!")