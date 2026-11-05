# ⚽ Premier League 2025-26 · Pipeline de Dados e Dashboard

![Demonstração do dashboard](Docs/demo.gif)

## Sobre o projeto

Este é um **projeto pessoal de estudo**, criado para colocar em prática e reforçar os conceitos que venho aprendendo em cursos, na faculdade e por conta própria. A ideia foi passar por todas as etapas de um projeto de dados real, e não só pela visualização: coletar os dados, tratá-los, modelá-los em um banco relacional, validar a qualidade e, por fim, transformá-los em um dashboard interativo.

O tema escolhido foi a **temporada 2025-26 da Premier League**, com dados públicos do [FBref](https://fbref.com).

**Perguntas que o dashboard responde:**
- Como foi a temporada da liga como um todo (gols, público, vantagem do mandante)?
- Quais jogadores mais participaram de gols, e quais foram mais eficientes por minuto jogado?
- De onde vieram os pontos de cada time: em casa ou fora?
- Como um time específico se compara à média da liga, e como foi a sua evolução rodada a rodada?

---

## Pipeline

```
 Power Automate Desktop      Python (pandas)          Python (pandas)          PostgreSQL               Power BI
┌──────────────────────┐   ┌──────────────────┐   ┌────────────────────┐   ┌──────────────────┐   ┌────────────────┐
│ Coleta no FBref      │ → │ Limpeza          │ → │ Modelagem          │ → │ Carga + testes   │ → │ Dashboard      │
│ (20 times × 2 tabelas)│   │ Data/raw → clean │   │ Dimensões e fatos  │   │ de qualidade     │   │ (3 páginas)    │
└──────────────────────┘   └──────────────────┘   └────────────────────┘   └──────────────────┘   └────────────────┘
```

| Etapa | O que acontece | Onde |
|---|---|---|
| **1. Coleta** | Um fluxo de RPA percorre a lista de times e exporta as tabelas de jogadores e de partidas de cada um | [`Scripts/Power Automate/`](Scripts/Power%20Automate/) |
| **2. Limpeza** | Ajuste de cabeçalhos, tipos, nomes de colunas, nacionalidade, posição e rodada | `Scripts/limpezaFull_*.py` |
| **3. Modelagem** | Criação das tabelas dimensão e fato com chaves substitutas (`squad_id`, `player_id`) | `Scripts/build_database_*.py` |
| **4. Carga** | Criação do esquema e carga no PostgreSQL | `Scripts/sql/DDL.sql`, `Scripts/load_to_postgres.py` |
| **5. Validação** | Testes de qualidade em SQL (contagens, duplicidades, consistência de placares e gols) | `Scripts/sql/data_quality_tests.sql` |
| **6. Visualização** | Dashboard conectado ao PostgreSQL | `Dashboard/PL dashboard.pbix` |

---

## Tecnologias

- **Power Automate Desktop:** coleta automatizada (RPA)
- **Python:** pandas, SQLAlchemy, psycopg2, python-dotenv
- **Jupyter Notebook:** exploração inicial da limpeza
- **PostgreSQL:** armazenamento e testes de qualidade em SQL
- **Power BI:** modelagem, DAX e visualização

---

## Modelo de dados

O banco segue um modelo dimensional, com duas dimensões e três tabelas fato:

| Tabela | Tipo | Conteúdo |
|---|---|---|
| `dim_squad` | Dimensão | Os 20 times |
| `dim_player` | Dimensão | Jogadores (nome, nacionalidade, posição, idade) |
| `fact_matches` | Fato | As 380 partidas, uma linha por jogo, com mandante e visitante |
| `fact_player_stats` | Fato | Estatísticas de cada jogador por time na temporada |
| `fact_standings` | Fato | Classificação final, artilheiro e goleiro de cada time |

![Modelo de dados no Power BI](Docs/Modelo_dados.png)

**Decisões importantes do modelo:**
- `fact_matches` tem **duas chaves para o mesmo time** (`home_team_id` e `away_team_id`). No Power BI, uma relação fica ativa e a outra inativa, e as medidas de time usam `TREATAS` para considerar os jogos em casa e fora.
- As tabelas **Rodadas** e **Local** são auxiliares e propositalmente **sem relacionamento**. Elas servem de eixo para os gráficos, para que o filtro de time não esconda rodadas em que ele jogou fora de casa.

---

## Dashboard

### 1. Resumo Geral
Visão da liga: total e média de gols, público médio, gols por rodada, vitórias de mandantes x visitantes, participações em gols por minutos jogados e top 5 em participações.

![Página Resumo Geral](Docs/pagina1_resumo.png)

### 2. Classificação
A tabela funciona como **segmentador**: ao clicar em um time, o card mostra o aproveitamento e o artilheiro, e o gráfico de pontos em casa x fora destaca o time selecionado.

| Sem seleção | Com o Manchester City selecionado |
|---|---|
| ![Classificação](Docs/pagina2_classificacao.png) | ![Classificação com time selecionado](Docs/pagina2_time_selecionado.png) |

### 3. Time
Análise de um time escolhido no segmentador: KPIs comparados com a **média da liga**, evolução de pontos (time x líder x média), resultados em casa e fora, contribuição em gols e elenco.

| Manchester City (acima da média) | Wolves (abaixo da média) |
|---|---|
| ![Página Time - City](Docs/pagina3_time.png) | ![Página Time - Wolves](Docs/pagina3_time_wolves.png) |

### Tooltip do jogador
Ao passar o mouse sobre um jogador, aparece um cartão com time, posição, idade, nacionalidade, gols, assistências, G+A por 90 minutos e minutos jogados.

![Tooltip do jogador](Docs/Tooltip_jogador.png)

📄 [Relatório completo em PDF](Docs/PL%20dashboard.pdf)

---

## Recursos de Power BI e DAX utilizados

- **Medidas com `TREATAS`** para calcular o desempenho de um time em uma tabela com duas chaves de time por linha
- **Pontos acumulados por rodada** do time, do líder e da média da liga
- **KPIs com meta dinâmica** (média da liga), com a direção correta para métricas em que "menor é melhor" (gols sofridos e cartões)
- **Títulos dinâmicos** que mudam conforme o time selecionado
- **Tabela usada como segmentador** com realce no gráfico ao lado
- **Página de dica de ferramenta** personalizada para jogadores
- **Controle de interações** entre visuais e navegação por botões
- **Medidas organizadas em pastas** por assunto

---

## Principais insights

- **Vantagem do mandante:** 42,6% das partidas terminaram com vitória do time da casa, contra 30% dos visitantes e 27,4% de empates.
- **A defesa decidiu o título:** o **Arsenal** foi campeão com a melhor defesa da liga (27 gols sofridos), enquanto o **Manchester City** teve o melhor ataque (77 gols) e terminou em 2º.
- **Tottenham longe de casa:** fez apenas **15 pontos em casa** e 26 fora, terminou em 17º e teve o maior número de cartões amarelos da liga (101).
- **Contra a lógica do mando:** Everton, Crystal Palace e Nottingham também somaram mais pontos fora do que em casa.
- **Rei dos empates:** o **Bournemouth** empatou 18 dos 38 jogos.
- **Disciplina:** o **Chelsea** recebeu 8 cartões vermelhos, enquanto Arsenal e Manchester City não tiveram nenhum.
- **Artilharia:** **Erling Haaland** liderou as participações em gols, com 35 (27 gols e 8 assistências).

---

## Estrutura do repositório

```
Projeto PL Dashboard/
├── Dashboard/
│   ├── PL dashboard.pbix
│   └── assets/                  ← logo, fundos das páginas e tema
├── Data/
│   ├── raw/                     ← dados coletados do FBref
│   └── clean/                   ← dados após a limpeza
├── Database/                    ← tabelas dimensão e fato em CSV
├── Docs/                        ← imagens, GIF e PDF do dashboard
├── Scripts/
│   ├── Power Automate/          ← fluxos de coleta (com README próprio)
│   ├── sql/
│   │   ├── DDL.sql
│   │   └── data_quality_tests.sql
│   ├── limpeza_*.ipynb          ← notebooks de exploração
│   ├── limpezaFull_*.py         ← scripts de limpeza
│   ├── build_database_*.py      ← scripts de modelagem
│   └── load_to_postgres.py
├── requirements.txt
└── README.md
```

---

## Como executar

**Pré-requisitos:** Python 3, PostgreSQL e Power BI Desktop. Para refazer a coleta, também o Power Automate Desktop (veja o [README da coleta](Scripts/Power%20Automate/README.md)).

Os dados brutos já estão em `Data/raw`, então a coleta é opcional.

**1. Instale as dependências**
```bash
pip install -r requirements.txt
```

**2. Configure a conexão com o banco**

Crie um arquivo `.env` na raiz do projeto com a linha:
```
DATABASE_URL=postgresql://usuario:senha@localhost:5432/PL_db
```

**3. Crie as tabelas**

Crie o banco `PL_db` no PostgreSQL e execute `Scripts/sql/DDL.sql`.

**4. Rode o pipeline a partir da raiz do projeto, nesta ordem**
```bash
python Scripts/limpezaFull_standings.py
python Scripts/limpezaFull_standard.py
python Scripts/limpezaFull_matches.py
python Scripts/build_database_standings.py   # primeiro: gera o dim_squad
python Scripts/build_database_matches.py
python Scripts/build_database_players.py
python Scripts/load_to_postgres.py
```

O `load_to_postgres.py` esvazia as tabelas antes da carga, então pode ser executado mais de uma vez sem duplicar dados.

**5. Valide os dados**

Execute `Scripts/sql/data_quality_tests.sql`. O esperado é 20 times, 380 partidas e nenhuma linha nos testes de inconsistência.

**6. Abra o dashboard**

Abra `Dashboard/PL dashboard.pbix`. O arquivo já contém os dados importados. Para atualizá-los, ajuste a conexão em *Transformar dados → Configurações da fonte de dados* para apontar para o seu PostgreSQL.

---

## Melhorias futuras

- Reestruturar `fact_matches` em uma linha por time por jogo, o que simplificaria boa parte das medidas DAX
- Deixar a coleta mais robusta: usar "passar o mouse" no menu de exportação do FBref, trocar esperas fixas por esperas condicionais e adicionar pausa entre os times
- Incluir a coleta da classificação no fluxo automatizado
- Avaliar a coleta em Python (`requests` + `pandas`), deixando o pipeline inteiro em uma única linguagem
- Publicar o dashboard online quando houver uma conta com essa permissão

---

## Fonte dos dados

Dados de [FBref.com](https://fbref.com) (Sports Reference), temporada 2025-26 da Premier League. Projeto sem fins comerciais, feito para estudo e portfólio.

---

## Autor

**José Gabriel Carreiro Santana**

<!-- Adicione aqui seus links: LinkedIn, GitHub, e-mail -->
