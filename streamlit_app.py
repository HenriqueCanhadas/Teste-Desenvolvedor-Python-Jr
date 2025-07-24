import streamlit as st
import requests

BASE_URL = "http://localhost:5000"

st.title("📚 Recomendação de Livros")

# Cadastro
st.header("👤 Cadastro")
nome = st.text_input("Nome")
genero = st.text_input("Gênero preferido")

if st.button("Cadastrar usuário"):
    res = requests.post(f"{BASE_URL}/register", json={
        "nome": nome,
        "genero_preferido": genero
    })
    st.write(res.json())

# Listar livros
st.header("📖 Livros disponíveis")
if st.button("Listar livros"):
    res = requests.get(f"{BASE_URL}/books")
    livros = res.json()
    for l in livros[:10]:
        st.write(f"{l['titulo']} - {l['autores']} ({l['generos']})")
        st.write(f"book_id: {l['book_id']}")

# Avaliação
st.header("⭐ Avaliar livro")
user_id = st.text_input("ID do usuário")
book_id = st.text_input("ID do livro")
nota = st.slider("Nota", 1, 5)

if st.button("Enviar avaliação"):
    res = requests.post(f"{BASE_URL}/rate", json={
        "user_id": user_id,
        "book_id": book_id,
        "nota": nota
    })
    st.write(res.json())

# Recomendação
st.header("🎯 Recomendação personalizada")
if st.button("Obter recomendação"):
    res = requests.get(f"{BASE_URL}/recommend/{user_id}")
    st.write(res.json())
