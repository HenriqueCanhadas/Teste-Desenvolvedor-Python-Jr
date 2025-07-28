from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MultiLabelBinarizer
from data import ratings, books

#Extrai as features de um livro (apenas os gêneros literéarios)
def extract_features(book):
    return book.get('generos', [])

#Gera uma recomendação de livro para o usuário
def get_recommendation(user_id):

    #Filtro de todas as avaliações ja feitas pelo usuário
    user_ratings = [r for r in ratings if r['user_id'] == user_id]

    #Quantidade mínima de 2 avaliações
    if len(user_ratings) < 2:
        return None

    #Identificador de livros que o usuário ja avaliou
    rated_ids = {r['book_id'] for r in user_ratings}

    #Seleciona livros ainda não avaliados pelo usuário
    unrated_books = [b for b in books if b['book_id'] not in rated_ids]
    if not unrated_books:
        return None

    #Mapeamento de livros por ID para acesso mais eficaz 
    book_map = {b['book_id']: b for b in books}

    #Codificador de gêneros literários em vetores binários
    mlb = MultiLabelBinarizer()

    #Prepara os dados de treino
    X = [extract_features(book_map[r['book_id']]) for r in user_ratings] #Gêneros dos livros avaliados
    y = [r['nota'] for r in user_ratings] #Notas atribuidas

    #Aplica codifição (one-hot) aos gêneros
    X_bin = mlb.fit_transform(X)

    #Garantia que exista pelo menos dois pontos para treinar
    if len(X_bin) < 2:
        return None
    
    #Inicializa e treina o modelo de K-vizinhos
    model = KNeighborsRegressor(n_neighbors=2)
    model.fit(X_bin, y)

    predictions = []

    #Para cada livro não avaliado, prevê a nota com base nos gêneros
    for book in unrated_books:
        features = mlb.transform([extract_features(book)])
        predicted = model.predict(features)[0]
        predictions.append((predicted, book))

    if not predictions:
        return None

    #Seleciona o livro com a maior nota prevista
    best = max(predictions, key=lambda x: x[0])
    return {
        'book_id': best[1]['book_id'],
        'titulo': best[1]['titulo'],
        'autores': best[1]['autores'],
        'generos': best[1]['generos'],
        'nota_prevista': round(best[0], 2)
    }
