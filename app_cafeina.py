import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# -----------------------------
# Inicialização do "banco de dados" na sessão
# -----------------------------
if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=["ID", "Data", "Bebida", "Cafeina_mg", "Horas_de_Sono"])

st.set_page_config(page_title="App Cafeína & Sono", layout="centered")

st.title("☕ Monitor de Cafeína & Sono 😴")

# -----------------------------
# Entradas do usuário
# -----------------------------
st.subheader("Registro de Consumo")

id_usuario = st.text_input("Digite seu nome: ")
bebida = st.selectbox("Selecione a bebida:", ["Café", "Chá", "Refrigerante", "Energético", "Outros"])
cafeina = st.number_input("Quantidade estimada de cafeína (mg):", min_value=0, max_value=500, step=10)
horas_sono = st.number_input("Quantas horas você dormiu na última noite?", min_value=0.0, max_value=24.0, step=0.5)
data = datetime.today().strftime("%d/%m/%Y")

if st.button("Adicionar Registro"):
    novo = pd.DataFrame({
        "ID": [id_usuario],
        "Data": [data],
        "Bebida": [bebida],
        "Cafeina_mg": [cafeina],
        "Horas_de_Sono": [horas_sono]
    })
    st.session_state.dados = pd.concat([st.session_state.dados, novo], ignore_index=True)
    st.success("✅ Registro adicionado com sucesso!")

# -----------------------------
# Exibição da tabela
# -----------------------------
st.subheader("📋 Seus Registros")
st.dataframe(st.session_state.dados)

# -----------------------------
# Semáforo da qualidade do sono
# -----------------------------
st.subheader("🚦 Indicador de Sono")
if horas_sono >= 8:
    st.success("🟢 Sono ideal (8h ou mais)")
elif 6 <= horas_sono < 8:
    st.warning("🟡 Sono moderado (6h a 7h59)")
else:
    st.error("🔴 Sono insuficiente (menos de 6h)")

# -----------------------------
# Gráficos
# -----------------------------
if not st.session_state.dados.empty:
    st.subheader("📊 Gráficos")

    fig1, ax1 = plt.subplots()
    st.session_state.dados.groupby("Data")["Cafeina_mg"].sum().plot(kind="bar", ax=ax1)
    ax1.set_title("Consumo diário de cafeína")
    ax1.set_ylabel("Cafeína (mg)")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    st.session_state.dados.groupby("Data")["Horas_de_Sono"].mean().plot(kind="line", marker="o", ax=ax2)
    ax2.set_title("Média de horas de sono por dia")
    ax2.set_ylabel("Horas de sono")
    st.pyplot(fig2)

# -----------------------------
# Exportação
# -----------------------------
st.subheader("📥 Exportar Dados")
csv = st.session_state.dados.to_csv(index=False).encode("utf-8")
st.download_button("Baixar CSV", csv, "dados_cafeina_sono.csv", "text/csv")
