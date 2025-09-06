import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="📊 Consumo de Cafeína", page_icon="☕", layout="centered")

# ---------------------------
# Catálogo de bebidas (mg por porção padrão)
# ---------------------------
catalogo = {
    "Café coado (200 ml)": 95,
    "Expresso (50 ml)": 65,
    "Chá preto (200 ml)": 40,
    "Chá verde (200 ml)": 30,
    "Energético (250 ml)": 80,
    "Refrigerante cola (350 ml)": 40,
    "Achocolatado (200 ml)": 10,
    "Pré-treino (1 dose)": 150
}

# ---------------------------
# Funções auxiliares
# ---------------------------
def calcular_janela(ultimo_consumo, hora_dormir):
    if ultimo_consumo and hora_dormir:
        return (hora_dormir - ultimo_consumo).seconds / 3600
    return None

def semaforo(janela_horas):
    if janela_horas is None:
        return "⚪ Sem dados"
    elif janela_horas > 9:
        return "🟢 Verde (seguro)"
    elif janela_horas > 6:
        return "🟡 Amarelo (atenção)"
    else:
        return "🔴 Vermelho (risco para o sono)"

# ---------------------------
# Entrada de dados
# ---------------------------
st.title("☕ Análise do Consumo de Cafeína e Sono")

st.subheader("📌 Dados do dia")
data = st.date_input("Data", datetime.today())
hora_dormir = st.time_input("⏰ Hora prevista de dormir", value=datetime.strptime("23:00", "%H:%M").time())

st.subheader("🥤 Registre suas bebidas")
bebida = st.selectbox("Escolha a bebida:", list(catalogo.keys()))
hora_consumo = st.time_input("Horário do consumo")
quantidade = st.number_input("Quantas porções?", min_value=1, value=1)

if "registros" not in st.session_state:
    st.session_state["registros"] = []

if st.button("➕ Adicionar consumo"):
    mg = catalogo[bebida] * quantidade
    st.session_state["registros"].append({
        "Data": data,
        "Bebida": bebida,
        "Porções": quantidade,
        "Hora_consumo": hora_consumo,
        "Mg_cafeina": mg
    })
    st.success(f"Adicionado: {bebida} ({mg} mg) às {hora_consumo}")

# ---------------------------
# Exibir registros do dia
# ---------------------------
df = pd.DataFrame(st.session_state["registros"])
if not df.empty:
    st.subheader("📋 Consumos registrados")
    st.dataframe(df)

    # Último consumo do dia
    ultimo = df["Hora_consumo"].max()
    hora_dormir_dt = datetime.combine(data, hora_dormir)
    ultimo_dt = datetime.combine(data, ultimo)
    janela = calcular_janela(ultimo_dt, hora_dormir_dt)

    st.subheader("🚦 Semáforo do Sono")
    st.write(f"Último consumo às **{ultimo.strftime('%H:%M')}** → Janela até dormir: **{janela:.1f} h**")
    st.markdown(f"### {semaforo(janela)}")

    # Total de cafeína
    total = df["Mg_cafeina"].sum()
    st.metric("☕ Total de cafeína no dia (mg)", total)

    # Gráfico
    st.bar_chart(df.groupby("Bebida")["Mg_cafeina"].sum())

    # Exportar CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Baixar dados (CSV)", csv, "dados_cafeina.csv", "text/csv")

else:
    st.info("Nenhum consumo registrado ainda.")
