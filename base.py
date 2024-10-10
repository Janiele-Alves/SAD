import streamlit as st
import pandas as pd
import plotly.express as px

# Layout da página
st.set_page_config(layout="wide")

# Carregar os dados do arquivo "vendas.csv"
df = pd.read_csv("vendas.csv", sep=";", decimal=",")

# Converter a coluna "Date" para o formato de data
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Configuração da página
st.sidebar.write("Vendas")
st.sidebar.write("Main Page")
st.sidebar.write("Page 2")

st.sidebar.markdown("---")

# Criar uma nova coluna "Month" que contém o ano e o mês
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))

# Seleção de meses na barra lateral do dashboard
month = st.sidebar.selectbox("Selecione o Mês", df["Month"].unique())

# Filtrar os dados com base no mês selecionado
df_filtered = df[df["Month"] == month]

col1, col2 = st.columns(2)  
col3, col4, col5 = st.columns(3)  

# Personalizar as cores para os mapas:
color_palette_custom = ['#82c9f9', '#096bc6', '#ebb5b6']

# Gráfico de faturamento por dia
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por dia",
                  color_discrete_sequence=color_palette_custom)
fig_date.update_layout()

# Gráfico na primeira coluna
col1.plotly_chart(fig_date, use_container_width=True)

# Gráfico de faturamento por tipo de produto
fig_prod = px.bar(df_filtered, x="Date", y="Product line", 
                  color="City", title="Faturamento por tipo de produto",
                  orientation="h", color_discrete_sequence=color_palette_custom)
fig_prod.update_layout()

# Gráfico na segunda coluna
col2.plotly_chart(fig_prod, use_container_width=True)

# Faturamento total por cidade
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()

# Gráfico de barras para exibir o faturamento por cidade
fig_city = px.bar(city_total, x="City", y="Total", title="Faturamento por cidade",
                  color_discrete_sequence=color_palette_custom)
fig_city.update_layout()

# Gráfico na terceira coluna
col3.plotly_chart(fig_city, use_container_width=True)

# Gráfico de pizza para exibir o faturamento por tipo de pagamento
fig_kind = px.pie(df_filtered, values="Total", names="Payment", title="Faturamento por tipo de pagamento",
                  color_discrete_sequence=color_palette_custom)
fig_kind.update_layout()

# Gráfico na quarta coluna
col4.plotly_chart(fig_kind, use_container_width=True)

# Avaliação média por cidade
city_total = df_filtered.groupby("City")[["Rating"]].mean().reset_index()

# Gráfico de barras para exibir a avaliação média
fig_rating = px.bar(df_filtered, y="Rating", x="City", title="Avaliação Média",
                    color_discrete_sequence=color_palette_custom)
fig_rating.update_layout()

# Gráfico na quinta coluna
col5.plotly_chart(fig_rating, use_container_width=True)
