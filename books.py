import requests
#Lista de livros mantida em memória local
from data import books 

#Função para buscar livros de gêneros variados na API do Google Books
def fetch_books():
    #Lista de gêneros a serem buscados
    subjects = ['romance', 'fiction', 'fantasy', 'history', 'science']
    #Conjunto para rastrear IDs já adicionados e evitar duplicatas
    seen_ids = set()

    #Para cada gênero, realiza uma requisição na API do Google Books
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

            #Extrai as informações do volume
            info = item.get('volumeInfo', {})
            books.append({
                'book_id': book_id,
                'titulo': info.get('title'),
                'autores': info.get('authors', []),
                'generos': info.get('categories', [])
            })