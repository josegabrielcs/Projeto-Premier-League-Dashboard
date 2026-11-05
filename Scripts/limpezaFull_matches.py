import pandas as pd
import glob
import os

def limpezaMatches(df):
    
    df = df.drop(columns= ['Match Report', 'Notes'])

    df['Time'] = df['Time'].str[:5]
    df['Round'] = df['Round'].str.replace('Matchweek ', '')

    df['Date'] = pd.to_datetime(df['Date'])
    df['Round'] = pd.to_numeric(df['Round'])

    df = df.sort_values(by="Round")

    return df

pasta_raw = "Data/raw/matches_stats/*.csv"
pasta_clean = "Data/clean/matches_stats/"

csv_files_raw = glob.glob(pasta_raw)

for arquivo in csv_files_raw:
    df = pd.read_csv(arquivo, skiprows=1, encoding='utf 16')
    df = limpezaMatches(df)
    time = os.path.basename(arquivo).split("_")[0]
    df.to_csv(f"{pasta_clean}{time}_matches_clean.csv", index=False)

print("Limpeza Completa!")