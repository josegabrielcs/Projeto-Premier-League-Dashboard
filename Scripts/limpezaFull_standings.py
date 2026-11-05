import pandas as pd


def limpezaStandings(df):

    # Remove a seta das notas de classificação (ex.: "→ Champions League")
    df['Notes'] = df['Notes'].str.replace('→ ', '')

    # Separa "Nome - Gols" em duas colunas
    df[['Top Scorer Name', 'Top Scorer Goals']] = df['Top Team Scorer'].str.split(' - ', expand=True)
    df = df.drop(columns='Top Team Scorer')

    # Artilheiros empatados: mantém apenas o primeiro nome listado
    df['Top Scorer Name'] = df['Top Scorer Name'].str.split().str[:2].str.join(' ')

    df = df.rename(columns={
        'Attendance': 'Avg_Attendance',
        'Pts/MP': 'Pts_MP',
        'Notes': 'Qualification',
        'W': 'Wins',
        'D': 'Draws',
        'L': 'Loses'
    })

    df['Top Scorer Goals'] = pd.to_numeric(df['Top Scorer Goals'])

    return df


arquivo_raw = "Data/raw/league_standings/standings.csv"
arquivo_clean = "Data/clean/league_standings/League_standings_clean.csv"

df = pd.read_csv(arquivo_raw, skiprows=1, encoding='utf-8')
df = limpezaStandings(df)
df.to_csv(arquivo_clean, index=False)

print("Limpeza Completa!")
