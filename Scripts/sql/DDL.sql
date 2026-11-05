CREATE TABLE dim_squad (
    squad_id INT PRIMARY KEY,
    squad VARCHAR(100) UNIQUE
);

CREATE TABLE dim_player (
    player_id INT PRIMARY KEY,
    name VARCHAR(150),
    nation VARCHAR(50),
    pos VARCHAR(20),
    age INT
);

CREATE TABLE fact_matches (
    match_date DATE,
    match_time TIME,
    round INT,
    day VARCHAR(20),
    home_team_id INT REFERENCES dim_squad(squad_id),
    away_team_id INT REFERENCES dim_squad(squad_id),
    home_goals INT,
    away_goals INT,
    result VARCHAR(10),
    home_possession INT,
    attendance INT,
    home_formation VARCHAR(20),
    away_formation VARCHAR(20),
    captain VARCHAR(150),
    referee VARCHAR(100)
);

CREATE TABLE fact_player_stats (
    player_id INT REFERENCES dim_player(player_id),
    squad_id INT REFERENCES dim_squad(squad_id),
    matches_played INT,
    starts INT,
    minutes_played INT,
    nineties_played NUMERIC,
    goals INT,
    assists INT,
    goals_assists INT,
    goals_minus_pk INT,
    pk INT,
    pk_att INT,
    cards_yellow INT,
    cards_red INT,
    goals_per_90 NUMERIC,
    assists_per_90 NUMERIC,
    goals_assists_per_90 NUMERIC,
    goals_minus_pk_per_90 NUMERIC,
    goals_assists_minus_pk NUMERIC
);

CREATE TABLE fact_standings (
    squad_id INT REFERENCES dim_squad(squad_id),
    rk INT,
    matches_played INT,
    wins INT,
    draws INT,
    losses INT,
    gf INT,
    ga INT,
    gd INT,
    pts INT,
    pts_mp NUMERIC,
    avg_attendance INT,
    top_scorer_name VARCHAR(150),
    top_scorer_goals INT,
    goalkeeper VARCHAR(150),
    qualification VARCHAR(150)
);