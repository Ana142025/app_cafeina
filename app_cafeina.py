import streamlit as st
import pandas as pd

st.title("☕ Análise do Consumo de Cafeína")

# Perguntas simuladas
st.header("📊 Questionário")
nome = st.text_input("Digite seu nome:")
cafe = st.slider("Quantas xícaras de café você bebe por dia?", 0, 10, 2)
energetico = st.selectbox("Você consome energético?", ["Não", "Sim"])
cha = st.checkbox("Você bebe chá verde/preto?")

if st.button("Salvar resposta"):
    st.success(f"Obrigado {nome}, seus dados foram registrados!")

# Exemplo de dados fictícios
st.header("📈 Gráfico de exemplo")
df = pd.DataFrame({
    "Pessoa": ["Ana", "Carlos", "Marina", "João"],
    "Cafeína (mg/dia)": [120, 300, 80, 210]
})
st.bar_chart(df.set_index("Pessoa"))
