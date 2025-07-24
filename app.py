from flask import Flask, request, jsonify
from data import users, books, ratings, user_counter
from books import fetch_books
from models import get_recommendation

app = Flask(__name__)

fetch_books()

@app.route('/register', methods=['POST'])
def register():
    global user_counter
    data = request.get_json()
    user_id = str(user_counter)
    users[user_id] = {
        'nome': data['nome'],
        'genero_preferido': data['genero_preferido']
    }
    user_counter += 1
    return jsonify({'user_id': user_id})

@app.route('/books', methods=['GET'])
def list_books():
    return jsonify(books)

@app.route('/rate', methods=['POST'])
def rate():
    data = request.get_json()
    ratings.append(data)
    return jsonify({'message': 'Avaliação registrada'})

@app.route('/recommend/<user_id>', methods=['GET'])
def recommend(user_id):
    result = get_recommendation(user_id)
    if result:
        return jsonify(result)
    return jsonify({'message': 'Sem recomendações'}), 404

@app.route('/user-ratings/<user_id>', methods=['GET'])
def get_ratings(user_id):
    user_ratings = [r for r in ratings if r['user_id'] == user_id]
    books_map = {b['book_id']: b for b in books}
    result = []
    for r in user_ratings:
        book = books_map.get(r['book_id'], {})
        result.append({
            'titulo': book.get('titulo'),
            'autores': book.get('autores'),
            'nota': r['nota']
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
