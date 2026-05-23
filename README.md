# ✈️ Análise e Predição de Atrasos de Voos

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-red?logo=scikit-learn)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b?logo=streamlit)
![Status](https://img.shields.io/badge/Status-Completo-brightgreen)

> Projeto desenvolvido para o Tech Challenge da Fase 3 da Pós-Graduação em
> Machine Learning Engineering — FIAP Pós Tech.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Base de Dados](#-base-de-dados)
- [Pipeline do Projeto](#-pipeline-do-projeto)
- [Principais Resultados](#-principais-resultados)
- [Modelos Utilizados](#-modelos-utilizados)
- [Como Executar](#-como-executar)
- [Tecnologias](#-tecnologias)
- [Autor](#-autor)

---

## 📌 Sobre o Projeto

O transporte aéreo é uma parte vital da infraestrutura global, mas os atrasos
de voos impactam milhões de passageiros todos os anos. Este projeto utiliza
um conjunto de dados público com informações detalhadas sobre voos nos EUA
para desenvolver análises e modelos preditivos aplicando técnicas de
**Machine Learning supervisionado e não supervisionado**.

### Objetivos
- Explorar e entender os padrões de atraso nos voos americanos
- Prever se um voo vai atrasar ou não (classificação)
- Agrupar aeroportos por perfil de atraso (clusterização)
- Identificar voos anômalos (detecção de anomalias)
- Demonstrar aprendizado semi-supervisionado

---

## 🗄️ Base de Dados

| Arquivo | Descrição | Tamanho |
|---|---|---|
| `flights.csv` | 5,8 milhões de voos (Jan-Mar/2015) | 565 MB |
| `airports.csv` | Informações e coordenadas de 322 aeroportos | 24 KB |
| `airlines.csv` | Códigos e nomes das companhias aéreas | 359 B |

> ⚠️ Os arquivos CSV não estão no repositório por serem muito grandes.
> Faça o download pelo link disponibilizado no enunciado do desafio.

### Principais variáveis

| Variável | Descrição |
|---|---|
| `ARRIVAL_DELAY` | Minutos de atraso na chegada (variável-alvo) |
| `DEPARTURE_DELAY` | Minutos de atraso na partida |
| `AIRLINE` | Código da companhia aérea |
| `ORIGIN_AIRPORT` | Aeroporto de origem |
| `DESTINATION_AIRPORT` | Aeroporto de destino |
| `MONTH`, `DAY_OF_WEEK` | Data do voo |
| `SCHEDULED_DEPARTURE` | Horário previsto de partida |
| `DISTANCE` | Distância do voo em milhas |
| `CANCELLED` | Se o voo foi cancelado |

---

## 📊 Principais Resultados

### Taxa de atraso geral
> **23,1%** dos voos atrasaram 15 minutos ou mais

### Piores companhias aéreas
| Companhia | Taxa de Atraso |
|---|---|
| F9 — Frontier Airlines | 37,6% |
| MQ — Envoy Air | 37,5% |
| NK — Spirit Airlines | 31,3% |

### Melhores companhias aéreas
| Companhia | Taxa de Atraso |
|---|---|
| AS — Alaska Airlines | 14,2% |
| HA — Hawaiian Airlines | 15,1% |
| DL — Delta Airlines | 17,6% |

### Padrões identificados
- 📅 **Piores dias:** Segunda-feira e Domingo (27,3%)
- 🌙 **Pior período:** Noite (29,0%)
- 📆 **Pior mês:** Março (32,3%)
- 🏢 **Aeroporto mais crítico:** ORD — Chicago O'Hare (35,6%)
- ⚡ **Principal causa:** Sistema aéreo (23 min médios)

### Clusters de aeroportos
| Cluster | Perfil | Aeroportos | Taxa de Atraso |
|---|---|---|---|
| 🟢 Excelente | Menor congestionamento | 31 | 16% |
| 🟡 Bom | Desempenho mediano | 64 | 21% |
| 🟠 Ruim | Problemas frequentes | 42 | 26% |
| 🔴 Crítico | Piores aeroportos | 13 | 33% |

---

## 🤖 Modelos Utilizados

### Supervisionados
| Modelo | Accuracy | ROC-AUC | Recall | F1 |
|---|---|---|---|---|
| Regressão Logística | 93% | 0.964 | 79% | 0.84 |
| Random Forest | 92% | 0.968 | 73% | 0.81 |

> **Conclusão:** A Regressão Logística teve melhor Recall — detecta mais
> voos atrasados corretamente. O principal preditor foi `DEPARTURE_DELAY`
> com 89,8% de importância, confirmando o efeito cascata de atrasos.

### Não Supervisionados
| Técnica | Resultado |
|---|---|
| K-Means (k=4) | 4 clusters de aeroportos identificados |
| PCA 2D | 79,2% da variância explicada |

### Opcionais
| Técnica | Resultado |
|---|---|
| Isolation Forest | 1% de voos anômalos (atraso médio: 257 min) |
| Label Propagation | 87% de accuracy com apenas 10% de labels |

---

## ▶️ Como Executar

### Pré-requisitos
- Python 3.12+
- Arquivos CSV da base de dados na raiz do projeto

### Instalação

```bash
# 1. Clonar o repositório
git clone https://github.com/JonatasLocateli/tech-challenge-fase3.git
cd tech-challenge-fase3

# 2. Criar e ativar o ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Iniciar o Jupyter Notebook
jupyter notebook
# Abrir: tech_challenge3.ipynb
# Executar: Kernel → Restart & Run All
```

### Dashboard interativo

```bash
# Com o venv ativo
streamlit run dashboard.py
# Acesse: http://localhost:8501
```

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.14 | Linguagem principal |
| Pandas | Manipulação de dados |
| NumPy | Cálculos numéricos |
| Matplotlib + Seaborn | Visualizações estáticas |
| Scikit-learn | Modelos de ML |
| Folium | Mapa geográfico interativo |
| Streamlit | Dashboard interativo |

---

## 📝 Limitações e Próximos Passos

### Limitações
1. Base cobre apenas Jan-Mar/2015 — não captura sazonalidade completa
2. `DEPARTURE_DELAY` domina o modelo — na prática só sabemos isso quando o voo já está atrasando
3. Amostra de 1M linhas representa ~17% da base completa
4. Dados de 2015 — padrões podem ter mudado com o tempo

### Próximos passos
1. Treinar modelo sem `DEPARTURE_DELAY` para predição antecipada
2. Incorporar dados de clima externos
3. Usar a base completa com mais recursos de hardware
4. Testar XGBoost e redes neurais
5. Expandir para todos os meses do ano

---

## 👨‍💻 Autor

**Jonatas Locateli**
FIAP Pós Tech — Machine Learning Engineering — Fase 3
---

## 🔄 Pipeline do Projeto
