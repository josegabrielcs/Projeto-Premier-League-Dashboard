import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
string_conexao = os.getenv('DATABASE_URL')

if not string_conexao:
    raise SystemExit("DATABASE_URL não encontrada. Crie o arquivo .env na raiz do projeto (veja o README).")

engine = create_engine(string_conexao)

pasta_db = 'Database'

mapeamento_colunas = {
    # dim_squad
    'Squad': 'squad',
    
    # dim_player
    'Name': 'name', 
    'Nation': 'nation',
    'Pos': 'pos',
    'Age': 'age',
    
    # fact_matches
    'Date': 'match_date',
    'Time': 'match_time',
    'Round': 'round',
    'Day': 'day',
    'Home_Goals': 'home_goals',
    'Away_Goals': 'away_goals',
    'Result': 'result',
    'Home_Possession': 'home_possession',
    'Attendance': 'attendance',
    'Home_Formation': 'home_formation',
    'Away_Formation': 'away_formation',
    'Captain': 'captain',
    'Referee': 'referee',
    
    # fact_standings
    'Rk': 'rk',
    'MP': 'matches_played',
    'Wins': 'wins',
    'Draws': 'draws',
    'Loses': 'losses', # Cobrindo caso esteja Loses ou Losses
    'Losses': 'losses',
    'GF': 'gf',
    'GA': 'ga',
    'GD': 'gd',
    'Pts': 'pts',
    'Pts_MP': 'pts_mp',
    'Avg_Attendance': 'avg_attendance',
    'Top Scorer Name': 'top_scorer_name',
    'Top Scorer Goals': 'top_scorer_goals',
    'Goalkeeper': 'goalkeeper',
    'Qualification': 'qualification',
    
    # fact_player_stats
    'Matches Played': 'matches_played',
    'Starts': 'starts',
    'Min': 'minutes_played',
    '90s Played': 'nineties_played',
    'Gls': 'goals',
    'Ast': 'assists',
    'G+A': 'goals_assists',
    'G-PK': 'goals_minus_pk',
    'PK': 'pk',
    'PKatt': 'pk_att',
    'CrdY': 'cards_yellow',
    'CrdR': 'cards_red',
    'Gls_90': 'goals_per_90',
    'Ast_90': 'assists_per_90',
    'G+A_90': 'goals_assists_per_90',
    'G-PK_90': 'goals_minus_pk_per_90',
    'G+A-PK': 'goals_assists_minus_pk'
}

def carregar_tabela(nome_arquivo, nome_tabela):
    caminho_completo = f'{pasta_db}/{nome_arquivo}'
    try:
        df = pd.read_csv(caminho_completo)
        df = df.rename(columns=mapeamento_colunas)
        df.columns = df.columns.str.lower()
        df.to_sql(nome_tabela, con=engine, if_exists='append', index=False)
        print(f"Tabela '{nome_tabela}' carregada com sucesso! ({len(df)} linhas)")
    except Exception as e:
        print(f" Erro ao carregar a tabela '{nome_tabela}': {e}")

# Esvazia as tabelas antes da carga, para o script poder ser executado de novo sem duplicar dados.
# As tabelas precisam existir (execute Scripts/sql/DDL.sql uma vez antes).
with engine.begin() as conexao:
    conexao.execute(text('TRUNCATE fact_player_stats, fact_standings, fact_matches, dim_player, dim_squad'))

carregar_tabela('dim_squad.csv', 'dim_squad')
carregar_tabela('dim_player.csv', 'dim_player')
carregar_tabela('fact_matches.csv', 'fact_matches')
carregar_tabela('fact_standings.csv', 'fact_standings')
carregar_tabela('fact_player_stats.csv', 'fact_player_stats')

print("Carga finalizada com sucesso!")       