
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MultiLabelBinarizer
from data import ratings, books

def extract_features(book):
    return book.get('generos', [])

def get_recommendation(user_id):
    user_ratings = [r for r in ratings if r['user_id'] == user_id]
    if len(user_ratings) < 2:
        return None

    rated_ids = {r['book_id'] for r in user_ratings}
    unrated_books = [b for b in books if b['book_id'] not in rated_ids]
    if not unrated_books:
        return None

    book_map = {b['book_id']: b for b in books}
    mlb = MultiLabelBinarizer()

    X = [extract_features(book_map[r['book_id']]) for r in user_ratings]
    y = [r['nota'] for r in user_ratings]
    X_bin = mlb.fit_transform(X)

    if len(X_bin) < 2:
        return None

    model = KNeighborsRegressor(n_neighbors=2)
    model.fit(X_bin, y)

    predictions = []
    for book in unrated_books:
        features = mlb.transform([extract_features(book)])
        predicted = model.predict(features)[0]
        predictions.append((predicted, book))

    if not predictions:
        return None

    best = max(predictions, key=lambda x: x[0])
    return {
        'book_id': best[1]['book_id'],
        'titulo': best[1]['titulo'],
        'autores': best[1]['autores'],
        'generos': best[1]['generos'],
        'nota_prevista': round(best[0], 2)
    }
