# Tech Challenge Fase 3 — Machine Learning Engineering

## Objetivo
Análise e predição de atrasos de voos nos EUA utilizando técnicas de Machine Learning supervisionado e não supervisionado.

## Base de dados
- **flights.csv** — 5.8 milhões de voos (Jan-Mar/2015)
- **airports.csv** — informações dos aeroportos
- **airlines.csv** — informações das companhias aéreas

## Estrutura do projeto
tech-challenge-3/
│
├── tech_challenge3.ipynb  # Notebook principal
├── README.md              # Este arquivo
└── requirements.txt       # Dependências

## Etapas do projeto
1. **EDA** — Exploração e limpeza dos dados
2. **Modelagem Supervisionada** — Regressão Logística e Random Forest
3. **Modelagem Não Supervisionada** — K-Means + PCA

## Principais resultados
- Taxa geral de atraso: **23.1%**
- Melhor modelo: **Regressão Logística** (AUC = 0.9644, Recall = 79%)
- Principal preditor: **DEPARTURE_DELAY** (89.8% de importância)
- **4 clusters** de aeroportos identificados (Excelente → Crítico)
- Piores aeroportos: ORD, LGA, JFK, BOS
- Pior companhia: F9/Frontier (37.6% de atraso)

## Como executar
```bash
# 1. Clonar o repositório
git clone https://github.com/JonatasLocateli/tech-challenge-fase3.git

# 2. Criar e ativar o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Iniciar o Jupyter
jupyter notebook
```

## Dependências
Ver `requirements.txt`

## Autor
Jonatas Locateli — FIAP Pós Tech — Machine Learning Engineering
