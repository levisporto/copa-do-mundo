import streamlit as st
import pandas as pd 
import folium
from streamlit_folium import st_folium
import altair as alt

df = pd.read_csv('world_cup.csv')
mapa = {
    'Uruguai': (1930, -33.8688, -56.1693, 'América do Sul'),
    'Itália': (1934, 41.8719, 12.5674, 'Europa'),
    'França': (1938, 46.2276, 2.2137, 'Europa'),
    'Brasil': (1950, -15.7942, -47.8822, 'América do Sul'),
    'Suiça': (1954, 46.8182, 8.2275, 'Europa'),
    'Suécia': (1958, 60.1282, 18.6435, 'Europa'),
    'Chile': (1962, -33.4489, -70.6693, 'América do Sul'),
    'Inglaterra': (1966, 51.5074, -0.1278, 'Europa'),
    'México': (1970, 19.4326, -99.1332, 'América do Norte'),
    'Alemanha Ocidental': (1974, 51.1657, 10.4515, 'Europa'),
    'Argentina': (1978, -34.6037, -58.3816, 'América do Sul'),
    'Espanha': (1982, 40.4168, -3.7038, 'Europa'),
    'EUA': (1994, 38.8951, -77.0369, 'América do Norte'),
    'Coreia do Sul': (2002, 37.5665, 126.9780, 'Ásia'),
    'Alemanha': (2006, 51.1657, 10.4515, 'Europa'),
    'África do Sul': (2010, -25.7461, 28.2293, 'África'),
    'Brasil': (2014, -15.7942, -47.8822, 'América do Sul'),
    'Rússia': (2018, 55.7558, 37.6173, 'Europa'),
    'Catar': (2022, 25.2854, 51.5310, 'Ásia'),
}
continentes = {
    'Europa': 'blue',
    'América do Sul': 'green',
    'América do Norte': 'red',
    'Ásia': 'purple',
    'África': 'orange',
}


paises = {
    'Korea Republic, Japan' : 'Coreia do Sul e Japão',
    'Uruguay': 'Uruguai',
    'Italy': 'Itália',
    'France': 'França',
    'Brazil': 'Brasil',
    'Switzerland': 'Suíça',
    'Sweden': 'Suécia',
    'Chile': 'Chile',
    'England': 'Inglaterra',
    'Mexico': 'México',
    'West Germany': 'Alemanha',
    'Argentina': 'Argentina',
    'Spain': 'Espanha',
    'United States': 'Estados Unidos',
    'USA': 'EUA',
    'Germany': 'Alemanha',
    'South Korea': 'Coreia do Sul',
    'South Africa': 'África do Sul',
    'Russia': 'Rússia',
    'Qatar': 'Catar',
    'Canada': 'Canadá',
    'Netherlands': 'Holanda',
    'Belgium': 'Bélgica',
    'Portugal': 'Portugal',
    'Australia': 'Austrália'
}
df['Host'] = df['Host'].replace(paises)
df['Champion'] = df['Champion'].replace(paises)
df = df.rename(columns={
    'Year': 'Ano',
    'Host': 'País Sede',
    'Champion': 'Campeão'
})

df['Ano'] = df['Ano'].astype(str)

#import seaborn as sns
#import matplotlib.pyplot as plt


st.title("Copas do Mundo - 1930 to 2022")
st.markdown("*Uma breve Exploração de Dados*")

st.markdown("Olá! Meu nome é **Levi S. Porto** *(www.levisporto.com)* e eu fiquei curioso para saber alguns dados históricos sobre a *Copa do Mundo da FIFA*.")

st.markdown("Com um dataset do Kaggle em mãos *(https://www.kaggle.com/datasets/piterfm/fifa-football-world-cup)*, vamos fazer algumas análises e responder algumas perguntas sobre a *Copa do Mundo*! (E torcer muito).")

st.image("bandeiras.jpg")



st.markdown("### Onde aconteceram as últimas copas?")

# Mapa com Folium

m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')

# Add markers with continent-based colors
for country, (year, lat, lon, continent) in mapa.items():
    folium.Marker(
        location=[lat, lon],
        popup=f'<b>{country}</b><br>Copa do Mundo de {year}<br>Continente: {continent}',
        tooltip=f'{country} ({year})',
        icon=folium.Icon(
            color=continentes[continent],
            icon='soccer',
            prefix='fa',
            icon_color='white'
        )
    ).add_to(m)



st_folium(m, width=700, height=400)


selected_year = st.selectbox(
    "Escolha um ano:",
    options=df["Ano"].tolist(),  # Extract years from dataframe
    index=0  # Default selection (first item)
)
filtered_df = df[df["Ano"] == selected_year]

# Display only the filtered data
st.dataframe(filtered_df[['Ano', 'País Sede', 'Campeão']], hide_index=True)

with st.expander("Ou clique aqui pra ver todos os anos"):
    st.dataframe(df[['Ano', 'País Sede', 'Campeão']], hide_index=True)



st.markdown("### Quais os times que já foram vencedores?")

times_vencedores = df['Campeão'].value_counts().reset_index()
times_vencedores.columns = ['Time', 'Vitórias']
anos_vitoria = df.groupby('Campeão')['Ano'].apply(
    lambda x: ', '.join(map(str, sorted(x)))
).reset_index()
anos_vitoria.columns = ['Time', 'Ano(s) da Vitória']


mais_tacas = times_vencedores.merge(anos_vitoria, on='Time')


mais_tacas['Vitórias'] = mais_tacas['Vitórias'].astype(str)


mais_tacas = mais_tacas.sort_values('Vitórias', ascending=False)



flag_colors = {
    'Brasil':     '#009C3B',  # flag green
    'Alemanha':   '#FFCE00',  # black-red-gold → gold (most visible on dark bg)
    'Itália':     '#CE2B37',  # green-white-red → red
    'Argentina':  '#75AADB',  # celeste / sky blue
    'Uruguai':    '#0038A8',  # flag royal blue (deeper than Argentina)
    'França':     '#002654',  # tricolor → navy blue
    'Espanha':    '#AA151B',  # red-yellow-red → deep red
    'Inglaterra': '#E8E8E8',  # St George → white field
}

chart = alt.Chart(times_vencedores).mark_bar().encode(
    x=alt.X('Time:N', sort='-y'),
    y=alt.Y('Vitórias:Q'),
    color=alt.Color(
        'Time:N',
        scale=alt.Scale(
            domain=list(flag_colors.keys()),
            range=list(flag_colors.values())
        ),
        legend=None
    ),
    tooltip=['Time', 'Vitórias']
)

st.altair_chart(chart)




st.dataframe(mais_tacas, hide_index=True)



