# 📘 Teste Técnico – Desenvolvedor Python Jr

API RESTful para cadastro de usuários, avaliação de livros e recomendação personalizada com Machine Learning.  
Também inclui uma interface via Streamlit para testes visuais.

---

## 🛠 Tecnologias utilizadas

- Python 3.8+
- Flask
- Scikit-learn
- Requests
- Numpy, Pandas
- Streamlit

---

## 🚀 Como rodar a aplicação

### 1. Clone o repositório
bash
git clone https://github.com/HenriqueCanhadas/Teste-Desenvolvedor-Python-Jr.git
cd Teste-Desenvolvedor-Python-Jr


### 2. Crie e ative o ambiente virtual
bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows


### 3. Instale as dependências
bash
pip install -r requirements.txt


### 4. Execute a API
bash
python app.py

A API estará disponível em: http://localhost:5000

---

## 🧪 Endpoints da API

### 📌 Cadastro de usuário
*POST* /register  
json
{
  "nome": "João",
  "genero_preferido": "Romance"
}

📥 Retorno:
json
{
  "user_id": "1"
}

---

### 📚 Listar livros
*GET* /books  
📥 Retorna até 50 livros variados obtidos da Google Books API:
json
[
  {
    "book_id": "abc123",
    "titulo": "Orgulho e Preconceito",
    "autores": ["Jane Austen"],
    "generos": ["Fiction"]
  }
]

---

### ⭐ Avaliar livro
*POST* /rate  
json
{
  "user_id": "1",
  "book_id": "abc123",
  "nota": 5
}

---

### 🎯 Obter recomendação personalizada
*GET* /recommend/<user_id>  
📥 Requer pelo menos *2 avaliações* feitas pelo usuário.  
📤 Retorna a previsão com maior nota:
json
{
  "book_id": "xyz789",
  "titulo": "Livro Recomendado",
  "autores": ["Autor X"],
  "generos": ["Romance"],
  "nota_prevista": 4.8
}

---

### 📖 Ver avaliações do usuário
*GET* /user-ratings/<user_id>  
📤 Retorna a lista de livros avaliados com notas:
json
[
  {
    "titulo": "Livro A",
    "autores": ["Autor 1"],
    "generos": ["Fiction"],
    "book_id": "abc123",
    "nota": 5
  }
]

---

## 🧠 Como funciona o modelo de recomendação

- *Modelo*: KNeighborsRegressor do scikit-learn
- *Features usadas: apenas os **gêneros literários* dos livros (codificados via MultiLabelBinarizer)
- O modelo é *re-treinado a cada requisição* de recomendação com base nas avaliações feitas pelo usuário.
- Recomendação ocorre apenas para livros *ainda não avaliados*.
- Retorna o livro com a *maior nota prevista*.

---

## 🖥 Interface via Streamlit

### Como rodar:
bash
streamlit run streamlit_app.py

### Funcionalidades disponíveis:

- Cadastrar usuário
- Listar livros
- Avaliar livros com estrelas
- Visualizar recomendação personalizada
- Ver avaliações feitas por um usuário

---

## 📌 Observações

- Todos os dados são mantidos *em memória* (sem uso de banco de dados)
- Livros são carregados uma única vez ao iniciar a API
- Projeto modularizado em: app.py, books.py, models.py, streamlit_app.py, data.py