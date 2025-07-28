import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://localhost:5000"
GENRES_VALIDOS = ['romance', 'fiction', 'fantasy', 'history', 'science']

#Título da pagina
st.title("📚 Recomendação de Livros")

#Cadastro de usuário
st.header("👤 Cadastro")

#Campo de cadastro
nome = st.text_input("Nome")
genero = st.text_input("Gênero preferido")

col1, col2 = st.columns([3, 0.7])

mensagem = None
mensagem_tipo = None
resposta_api = None

#Botão de cadastro
with col1:
    if st.button("Cadastrar usuário"):
        if genero.strip().lower() not in GENRES_VALIDOS:
            mensagem = "Gênero inválido. Clique em 'Listar Gêneros' para ver as opções disponíveis."
            mensagem_tipo = "erro"
        else:
            res = requests.post(f"{BASE_URL}/register", json={
                "nome": nome,
                "genero_preferido": genero
            })
            mensagem = "Usuário cadastrado com sucesso!"
            mensagem_tipo = "sucesso"
            resposta_api = res.json()

#Botão de listagem
with col2:
    if st.button("Listar Gêneros"):
        mensagem = f"Gêneros válidos: {', '.join(GENRES_VALIDOS)}"
        mensagem_tipo = "info"

#Mensagens de erro/sucesso/info 
if mensagem:
    if mensagem_tipo == "erro":
        st.error(mensagem)
    elif mensagem_tipo == "sucesso":
        st.success(mensagem)
    elif mensagem_tipo == "info":
        st.info(mensagem)

#Retorno da resposta da API
if resposta_api:
    st.write(resposta_api)

# Listagem de livros
st.header("📖 Livros disponíveis")
if st.button("Listar livros"):
    res = requests.get(f"{BASE_URL}/books")
    livros = res.json()

    #Organização em dados no formato de tabela
    tabela_livros = pd.DataFrame([{
        "Título": livro['titulo'],
        "Autores": ", ".join(livro['autores']) if livro['autores'] else "Desconhecido",
        "Gêneros": ", ".join(livro['generos']) if livro['generos'] else "N/A",
        "book_id": livro['book_id']
    } for livro in livros])

    st.dataframe(tabela_livros, use_container_width=True)

#Avaliação de livro
st.header("⭐ Avaliar livro")

#Campo de cadastro
user_id = st.text_input("ID do usuário")
book_id = st.text_input("ID do livro")

nota_str = st.radio("Nota",
                    options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
                    horizontal=False)

#Converte as estrelas para número
nota = len(nota_str)

#Botão de avaliação
if st.button("Enviar avaliação"):
    erro = None

    #Verifica se o usuário existe
    user_check = requests.get(f"{BASE_URL}/user-ratings/{user_id}")
    if user_check.status_code != 200:
        erro = "Usuário não encontrado."

    #Verifica se o livro existe
    books_res = requests.get(f"{BASE_URL}/books")
    livros = books_res.json()
    book_ids = [livro["book_id"] for livro in livros]
    if book_id not in book_ids:
        erro = "Livro não encontrado."

    #Retorna erros ou registra a avaliação
    if erro:
        st.error(erro)
    else:
        res = requests.post(f"{BASE_URL}/rate", json={
            "user_id": user_id,
            "book_id": book_id,
            "nota": nota
        })
        st.success("Avaliação registrada com sucesso!")
        st.write(res.json())

#Recomendação de livro
st.header("🎯 Recomendação personalizada")

#Botão de avaliação
if st.button("Obter recomendação"):
    if not user_id:
        st.warning("Por favor, insira o ID do usuário antes de solicitar a recomendação.")
    else:
        res = requests.get(f"{BASE_URL}/recommend/{user_id}")

        #Mensagem de erro caso o usuário ainda não avaliou livros o suficiente
        if res.status_code == 404:
            st.warning("Usuário ainda não avaliou livros suficientes para gerar recomendação. Avalie pelo menos 2 livros.")
        elif res.status_code == 200:
            rec = res.json()
            with st.container():
                st.subheader("📚 Livro recomendado:")
                st.markdown(f"*Título:* {rec['titulo']}")
                st.markdown(f"*Autor(es):* {', '.join(rec['autores']) if rec['autores'] else 'Desconhecido'}")
                st.markdown(f"*Gêneros:* {', '.join(rec['generos']) if rec['generos'] else 'N/A'}")
                st.markdown(f"*Nota prevista:* ⭐ {rec['nota_prevista']}")
                st.code(f"book_id: {rec['book_id']}", language='text')
        else:
            st.error("Ocorreu um erro ao buscar recomendação.")

#Avaliações do usuário
st.header("📖 Avaliações do usuário")

#Campo separado para evitar conflito com 'user_id'
user_id_avaliacoes = st.text_input("ID do usuário para ver avaliações", key="avaliacoes")

#Botão de avaliação do usuário
if st.button("Ver avaliações"):
    if not user_id_avaliacoes:
        st.warning("Informe o ID do usuário.")
    else:
        res = requests.get(f"{BASE_URL}/user-ratings/{user_id_avaliacoes}")
        if res.status_code == 404:
            st.error("Usuário não encontrado.")
        else:
            avaliacoes = res.json()
            if not avaliacoes:
                st.info("Este usuário ainda não avaliou nenhum livro.")
            else:
                st.success(f"Usuário avaliou {len(avaliacoes)} livro(s):")
                for livro in avaliacoes:
                    with st.container():
                        st.markdown(f"### 📘 Título: {livro['titulo']}")
                        st.markdown(f"*Autor(es):* {', '.join(livro['autores']) if livro.get('autores') else 'Desconhecido'}")
                        st.markdown(f"*Gêneros:* {', '.join(livro['generos']) if livro.get('generos') else 'N/A'}")
                        st.markdown(f"*Nota dada:* {'⭐' * int(livro['nota'])}")
                        st.code(f"book_id: {livro.get('book_id', 'N/A')}", language='text')
                        st.markdown("---")