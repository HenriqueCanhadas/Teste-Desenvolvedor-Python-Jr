# Dados em memória (sem banco de dados)
users = {}      # user_id: {nome, genero_preferido}
books = []      # Lista de livros (book_id, titulo, autores, generos)
ratings = []    # Lista de avaliações: {user_id, book_id, nota}
user_counter = 1  # Contador incremental de usuários