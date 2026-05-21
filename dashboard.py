import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="Tech Challenge Fase 3 — Atrasos de Voos",
    page_icon="✈️",
    layout="wide"
)

@st.cache_data
def carregar_dados():
    colunas = [
        'YEAR', 'MONTH', 'DAY', 'DAY_OF_WEEK', 'AIRLINE',
        'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'SCHEDULED_DEPARTURE',
        'DEPARTURE_DELAY', 'DISTANCE', 'ELAPSED_TIME',
        'ARRIVAL_DELAY', 'CANCELLED', 'DIVERTED',
        'AIR_SYSTEM_DELAY', 'SECURITY_DELAY',
        'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY'
    ]
    df = pd.read_csv('flights.csv', usecols=colunas, nrows=1_000_000)
    df = df[df['CANCELLED'] == 0].copy()
    colunas_atraso = ['AIR_SYSTEM_DELAY', 'SECURITY_DELAY',
                      'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']
    df[colunas_atraso] = df[colunas_atraso].fillna(0)
    df = df.dropna(subset=['ARRIVAL_DELAY', 'DEPARTURE_DELAY', 'ELAPSED_TIME'])
    df['ATRASADO'] = (df['ARRIVAL_DELAY'] >= 15).astype(int)
    def periodo_dia(hora):
        hora = int(str(int(hora)).zfill(4)[:2])
        if 5 <= hora < 12:
            return 'Manhã'
        elif 12 <= hora < 18:
            return 'Tarde'
        elif 18 <= hora < 24:
            return 'Noite'
        else:
            return 'Madrugada'
    df['PERIODO'] = df['SCHEDULED_DEPARTURE'].apply(periodo_dia)
    return df

@st.cache_data
def carregar_airports():
    return pd.read_csv('airports.csv')

# Carregar dados
df = carregar_dados()
airports = carregar_airports()

# Sidebar
st.sidebar.title("✈️ Filtros")
meses = st.sidebar.multiselect(
    "Mês",
    options=[1, 2, 3],
    default=[1, 2, 3],
    format_func=lambda x: {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março'}[x]
)

companhias = st.sidebar.multiselect(
    "Companhia aérea",
    options=sorted(df['AIRLINE'].unique()),
    default=sorted(df['AIRLINE'].unique())
)

# Filtrar dados
df_filtrado = df[
    (df['MONTH'].isin(meses)) &
    (df['AIRLINE'].isin(companhias))
]

# Header
st.title("✈️ Análise de Atrasos de Voos — EUA 2015")
st.markdown("---")

# Métricas principais
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de voos", f"{len(df_filtrado):,}")
with col2:
    taxa = df_filtrado['ATRASADO'].mean() * 100
    st.metric("Taxa de atraso", f"{taxa:.1f}%")
with col3:
    atraso_medio = df_filtrado[df_filtrado['ARRIVAL_DELAY'] > 0]['ARRIVAL_DELAY'].mean()
    st.metric("Atraso médio", f"{atraso_medio:.0f} min")
with col4:
    cancelados = df[df['CANCELLED'] == 1].shape[0] if 'CANCELLED' in df.columns else 0
    st.metric("Voos analisados", f"{len(df_filtrado):,}")

st.markdown("---")

# Gráficos linha 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Taxa de atraso por companhia")
    atraso_airline = df_filtrado.groupby('AIRLINE')['ATRASADO'].mean().sort_values(ascending=False) * 100
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(atraso_airline.index, atraso_airline.values, color='#e74c3c', edgecolor='white')
    ax.axhline(y=atraso_airline.mean(), color='navy', linestyle='--', label='Média')
    ax.set_xlabel('Companhia')
    ax.set_ylabel('% atrasados')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("Taxa de atraso por dia da semana")
    dias = {1: 'Seg', 2: 'Ter', 3: 'Qua', 4: 'Qui', 5: 'Sex', 6: 'Sáb', 7: 'Dom'}
    atraso_dia = df_filtrado.groupby('DAY_OF_WEEK')['ATRASADO'].mean() * 100
    atraso_dia.index = atraso_dia.index.map(dias)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(atraso_dia.index, atraso_dia.values, color='#3498db', edgecolor='white')
    ax.axhline(y=atraso_dia.mean(), color='navy', linestyle='--', label='Média')
    ax.set_xlabel('Dia da semana')
    ax.set_ylabel('% atrasados')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# Gráficos linha 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("Taxa de atraso por período do dia")
    atraso_periodo = df_filtrado.groupby('PERIODO')['ATRASADO'].mean() * 100
    ordem = ['Manhã', 'Tarde', 'Noite', 'Madrugada']
    atraso_periodo = atraso_periodo.reindex(ordem)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(atraso_periodo.index, atraso_periodo.values,
           color=['#f39c12', '#e67e22', '#c0392b', '#2c3e50'], edgecolor='white')
    ax.set_xlabel('Período')
    ax.set_ylabel('% atrasados')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("Heatmap — hora × dia da semana")
    df_filtrado2 = df_filtrado.copy()
    df_filtrado2['HORA'] = df_filtrado2['SCHEDULED_DEPARTURE'].apply(
        lambda x: int(str(int(x)).zfill(4)[:2])
    )
    df_filtrado2['FAIXA_HORA'] = (df_filtrado2['HORA'] // 2) * 2
    pivot = df_filtrado2.pivot_table(
        values='ATRASADO', index='FAIXA_HORA',
        columns='DAY_OF_WEEK', aggfunc='mean'
    ) * 100
    pivot.columns = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn_r',
                linewidths=0.5, ax=ax)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# Mapa
st.subheader("🗺️ Mapa de clusters dos aeroportos")

aeroporto_perfil = df.groupby('ORIGIN_AIRPORT').agg(
    total_voos=('ATRASADO', 'count'),
    taxa_atraso=('ATRASADO', 'mean'),
    atraso_medio=('ARRIVAL_DELAY', 'mean'),
    atraso_partida=('DEPARTURE_DELAY', 'mean'),
    distancia_media=('DISTANCE', 'mean'),
    atraso_clima=('WEATHER_DELAY', 'mean'),
    atraso_companhia=('AIRLINE_DELAY', 'mean'),
    atraso_sistema=('AIR_SYSTEM_DELAY', 'mean')
).reset_index()

aeroporto_perfil = aeroporto_perfil[aeroporto_perfil['total_voos'] >= 500]

features_cluster = ['taxa_atraso', 'atraso_medio', 'atraso_partida',
                    'distancia_media', 'atraso_clima', 'atraso_companhia', 'atraso_sistema']

scaler = StandardScaler()
X_cluster = scaler.fit_transform(aeroporto_perfil[features_cluster])
km = KMeans(n_clusters=4, random_state=42, n_init=10)
aeroporto_perfil['CLUSTER'] = km.fit_predict(X_cluster)

mapa_data = aeroporto_perfil.merge(
    airports[['IATA_CODE', 'AIRPORT', 'CITY', 'STATE', 'LATITUDE', 'LONGITUDE']],
    left_on='ORIGIN_AIRPORT', right_on='IATA_CODE', how='inner'
)

cores_cluster = {0: '#f39c12', 1: '#e74c3c', 2: '#2ecc71', 3: '#c0392b'}
labels_cluster = {0: 'Bom (21%)', 1: 'Ruim (26%)', 2: 'Excelente (16%)', 3: 'Crítico (33%)'}

mapa = folium.Map(location=[39.5, -98.35], zoom_start=4, tiles='CartoDB positron')

for _, row in mapa_data.iterrows():
    folium.CircleMarker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        radius=8,
        color=cores_cluster[row['CLUSTER']],
        fill=True,
        fill_color=cores_cluster[row['CLUSTER']],
        fill_opacity=0.8,
        popup=folium.Popup(
            f"""<b>{row['IATA_CODE']} — {row['AIRPORT']}</b><br>
            Cidade: {row['CITY']}, {row['STATE']}<br>
            Cluster: {labels_cluster[row['CLUSTER']]}<br>
            Taxa de atraso: {row['taxa_atraso']*100:.1f}%<br>
            Atraso médio: {row['atraso_medio']:.1f} min""",
            max_width=250
        )
    ).add_to(mapa)

try:
    from streamlit_folium import folium_static
    folium_static(mapa)
except:
    st.info("Instale streamlit-folium para ver o mapa interativo")

st.markdown("---")
st.caption("Tech Challenge Fase 3 — FIAP Pós Tech — Machine Learning Engineering")
