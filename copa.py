import streamlit as st
import pandas as pd 
import folium
from streamlit_folium import st_folium
df = pd.read_csv('world_cup.csv')
mapa = {
    'Uruguay': (1930, -33.8688, -56.1693, 'South America'),
    'Italy': (1934, 41.8719, 12.5674, 'Europe'),
    'France': (1938, 46.2276, 2.2137, 'Europe'),
    'Brazil': (1950, -15.7942, -47.8822, 'South America'),
    'Switzerland': (1954, 46.8182, 8.2275, 'Europe'),
    'Sweden': (1958, 60.1282, 18.6435, 'Europe'),
    'Chile': (1962, -33.4489, -70.6693, 'South America'),
    'England': (1966, 51.5074, -0.1278, 'Europe'),
    'Mexico': (1970, 19.4326, -99.1332, 'North America'),
    'West Germany': (1974, 51.1657, 10.4515, 'Europe'),
    'Argentina': (1978, -34.6037, -58.3816, 'South America'),
    'Spain': (1982, 40.4168, -3.7038, 'Europe'),
    'USA': (1994, 38.8951, -77.0369, 'North America'),
    'South Korea': (2002, 37.5665, 126.9780, 'Asia'),
    'Germany': (2006, 51.1657, 10.4515, 'Europe'),
    'South Africa': (2010, -25.7461, 28.2293, 'Africa'),
    'Brazil': (2014, -15.7942, -47.8822, 'South America'),
    'Russia': (2018, 55.7558, 37.6173, 'Europe'),
    'Qatar': (2022, 25.2854, 51.5310, 'Asia'),
}
continentes = {
    'Europe': 'blue',
    'South America': 'green',
    'North America': 'red',
    'Asia': 'purple',
    'Africa': 'orange',
}


paises = {
    'Uruguay': 'Uruguai',
    'Italy': 'Itália',
    'France': 'França',
    'Brazil': 'Brasil',
    'Switzerland': 'Suíça',
    'Sweden': 'Suécia',
    'Chile': 'Chile',
    'England': 'Inglaterra',
    'Mexico': 'México',
    'West Germany': 'Alemanha Ocidental',
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

selected_year = st.selectbox(
    "Escolha um ano:",
    options=df["Ano"].tolist(),  # Extract years from dataframe
    index=0  # Default selection (first item)
)
filtered_df = df[df["Ano"] == selected_year]

# Display only the filtered data
st.dataframe(filtered_df[['Ano', 'País Sede', 'Campeão']], hide_index=True)

m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')

# Add markers with continent-based colors
for country, (year, lat, lon, continent) in mapa.items():
    folium.Marker(
        location=[lat, lon],
        popup=f'<b>{country}</b><br>World Cup {year}<br>Continent: {continent}',
        tooltip=f'{country} ({year})',
        icon=folium.Icon(
            color=continentes[continent],
            icon='soccer',
            prefix='fa',
            icon_color='white'
        )
    ).add_to(m)



st_folium(m, width=700, height=400)




st.markdown("### Quais os times com mais taças?")

mais_tacas = df['Campeão'].value_counts().reset_index()
mais_tacas.columns = ['Time', 'Vitórias']
anos_vitoria = df.groupby('Campeão')['Ano'].apply(
    lambda x: ', '.join(map(str, sorted(x)))
).reset_index()
anos_vitoria.columns = ['Time', 'Ano da Vitória']


mais_tacas = mais_tacas.merge(anos_vitoria, on='Time')


mais_tacas['Vitórias'] = mais_tacas['Vitórias'].astype(str)


mais_tacas = mais_tacas.sort_values('Vitórias', ascending=False)

st.dataframe(mais_tacas, hide_index=True)