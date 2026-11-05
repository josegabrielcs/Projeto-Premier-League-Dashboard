# Premier League 2025-26 · Pipeline de Dados e Dashboard

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
| **6. Visualização** | Dashboard conectado ao PostgreSQL em modo Importação (o `.pbix` já contém os dados) | `Dashboard/PL dashboard.pbix` |

Os scripts Python rodam a partir da raiz do projeto, e a ordem importa: a modelagem começa pela classificação, porque é ela que gera a dimensão de times (`dim_squad`) usada pelas outras tabelas. Antes de carregar, o `load_to_postgres.py` esvazia as tabelas, então o pipeline pode ser executado de novo do zero sem duplicar dados. Esse teste foi feito apagando tudo, menos os dados brutos, e reconstruindo o banco e o dashboard com os mesmos resultados.

As credenciais do banco ficam em um arquivo `.env` fora do repositório, e as bibliotecas usadas estão no `requirements.txt`.

### Organização em camadas (arquitetura medalhão)

Os dados seguem a lógica da arquitetura medalhão, em que cada camada tem um nível maior de tratamento do que a anterior:

| Camada | Pasta | Conteúdo |
|---|---|---|
| 🥉 **Bronze** | `Data/raw` | Dados brutos, exatamente como foram exportados do FBref |
| 🥈 **Prata** | `Data/clean` | Dados limpos e padronizados: tipos corrigidos, colunas renomeadas, um arquivo por time |
| 🥇 **Ouro** | `Database` + PostgreSQL | Modelo dimensional (dimensões e fatos), validado e pronto para o Power BI |

Manter a camada bronze intacta permite refazer todo o tratamento sem precisar coletar os dados de novo.

---

## Tecnologias

- **Power Automate Desktop:** coleta automatizada (RPA)
- **Python:** pandas, SQLAlchemy, psycopg2 e python-dotenv (credenciais fora do código)
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
│   ├── raw/                     ← 🥉 bronze: dados coletados do FBref
│   └── clean/                   ← 🥈 prata: dados após a limpeza
├── Database/                    ← 🥇 ouro: tabelas dimensão e fato em CSV
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
├── requirements.txt             ← dependências Python
└── README.md
```

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

[![LinkedIn](https://img.shields.io/badge/LinkedIn-josegabrielcs-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/josegabrielcs/)
