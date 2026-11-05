-- Deve retornar 20
SELECT COUNT(*) AS total_times FROM dim_squad;

-- Deve retornar 380 (20 times * 19 jogos em casa)
SELECT COUNT(*) AS total_jogos FROM fact_matches;

-- Deve retornar 20
SELECT COUNT(*) AS total_classificacao FROM fact_standings;

-- Mostra quantos jogadores estão registrados (geralmente entre 400 e 600)
SELECT COUNT(*) AS total_jogadores FROM dim_player;

-- Verifica se um time enfrentou o mesmo oponente em casa mais de uma vez (Deve retornar ZERO linhas)
SELECT 
    "home_team_id", 
    "away_team_id", 
    COUNT(*) as qtd_jogos
FROM fact_matches
GROUP BY "home_team_id", "away_team_id"
HAVING COUNT(*) > 1;

-- Verifica se existem jogadores duplicados no mesmo time (Deve retornar ZERO linhas)
SELECT 
    "player_id", 
    "squad_id", 
    COUNT(*) 
FROM fact_player_stats
GROUP BY "player_id", "squad_id"
HAVING COUNT(*) > 1;

-- Verifica se existe algum jogo onde o time jogou contra ele mesmo (Deve retornar ZERO linhas)
SELECT * 
FROM fact_matches 
WHERE "home_team_id" = "away_team_id";

-- Verifica se a coluna de Resultado (W, D, L) bate com o saldo de gols do jogo.
-- Lembre-se: O Result está na perspectiva do mandante. (Deve retornar ZERO linhas)
SELECT * 
FROM fact_matches 
WHERE 
    ("home_goals" > "away_goals" AND "result" != 'W') OR
    ("home_goals" < "away_goals" AND "result" != 'L') OR
    ("home_goals" = "away_goals" AND "result" != 'D');

-- Verifica se algum jogador ultrapassou o limite físico de jogos em uma temporada. (Deve retornar ZERO linhas)
SELECT dp."name", fps."matches_played"
FROM fact_player_stats fps
JOIN dim_player dp ON fps."player_id" = dp."player_id"
WHERE fps."matches_played" > 38;

-- Compara os "Gols a Favor" da classificação com a soma real de gols dos jogos.
-- A coluna "diferenca_gols" deve ser ZERO para todos os 20 times.
WITH Gols_Marcados AS (
    -- Soma os gols que o time fez em casa
    SELECT "home_team_id" AS squad_id, SUM("home_goals") AS gols
    FROM fact_matches GROUP BY "home_team_id"
    UNION ALL
    -- Soma os gols que o time fez fora
    SELECT "away_team_id" AS squad_id, SUM("away_goals") AS gols
    FROM fact_matches GROUP BY "away_team_id"
),
Gols_Totais AS (
    SELECT squad_id, SUM(gols) AS total_gols_marcados
    FROM Gols_Marcados
    GROUP BY squad_id
)
SELECT 
    ds."squad",
    fs."gf" AS gols_classificacao,
    gt.total_gols_marcados AS gols_soma_jogos,
    (fs."gf" - gt.total_gols_marcados) AS diferenca_gols
FROM fact_standings fs
JOIN dim_squad ds ON fs."squad_id" = ds."squad_id"
JOIN Gols_Totais gt ON fs."squad_id" = gt.squad_id
WHERE fs."gf" != gt.total_gols_marcados;

-- Verifica se existem datas vazias nos jogos (Deve retornar ZERO)
SELECT COUNT(*) FROM fact_matches WHERE "match_date" IS NULL;

-- Verifica se alguma estatística vital de jogador está vazia (Deve retornar ZERO)
SELECT COUNT(*) FROM fact_player_stats WHERE "minutes_played" IS NULL OR "goals" IS NULL;