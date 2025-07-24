import requests
from data import books

def fetch_books():
    subjects = ['romance', 'fiction', 'fantasy', 'history', 'science']
    seen_ids = set()

    for subject in subjects:
        url = f'https://www.googleapis.com/books/v1/volumes?q=subject:{subject}&maxResults=10'
        response = requests.get(url)
        if response.status_code != 200:
            continue

        items = response.json().get('items', [])
        for item in items:
            book_id = item['id']
            if book_id in seen_ids:
                continue
            seen_ids.add(book_id)

            info = item.get('volumeInfo', {})
            books.append({
                'book_id': book_id,
                'titulo': info.get('title'),
                'autores': info.get('authors', []),
                'generos': info.get('categories', [])
            })