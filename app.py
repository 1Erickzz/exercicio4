import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ipeadatapy as ip

st.set_page_config(page_title="Análise Contábil com IPCA", layout="centered")
st.title("Projeto Final - Análise Contábil com Ajuste Econômico")
st.write("""
Este projeto integra dados contábeis de empresas com indicadores econômicos do IPCA (Ipeadata).
""")

df_empresas = pd.read_csv("empresas_dados.csv", sep=";")

df_empresas["Margem Líquida"] = (df_empresas["Lucro Líquido"] / df_empresas["Receita Líquida"]) * 100
df_empresas["ROA"] = (df_empresas["Lucro Líquido"] / df_empresas["Ativo Total"]) * 100

df_ipca = ip.timeseries('PRECOS12_IPCA12').reset_index()
print(df_ipca.columns)
df_ipca = df_ipca[(df_ipca['YEAR'] >= 2010) & (df_ipca['YEAR'] <= 2024)]
df_ipca = df_ipca.rename(columns={'YEAR': 'Ano', 'VALUE (-)': 'IPCA'})
df_empresas = pd.read_csv("empresas_dados.csv", sep=";")
df_combinado = pd.merge(df_empresas, df_ipca, on='Ano', how='left')
df_combinado["Receita Real"] = df_combinado["Receita Líquida"] - (
    df_combinado["Receita Líquida"] * (df_combinado['IPCA'] / 100)
)
df_combinado.head()
import matplotlib.pyplot as plt

df_plot = df_combinada.groupby('Ano')[['Receita Líquida', 'Receita Real']].sum().reset_index()

plt.figure(figsize=(12,6))
plt.plot(df_plot['Ano'], df_plot['Receita Líquida'], label='Receita Líquida', marker='o')
plt.plot(df_plot['Ano'], df_plot['Receita Real'], label='Receita Real', marker='s')

plt.title('Receita Líquida vs Receita Real ao longo dos anos')
plt.xlabel('Ano')
plt.ylabel('Valor (R$)')
plt.legend()
plt.grid(True)
plt.xticks(df_plot['Ano'], rotation=45)
plt.tight_layout()
plt.show()
