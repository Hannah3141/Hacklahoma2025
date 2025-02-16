from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

books = []

def fetch_book_availability(book_name):
    url = f"https://tccl.bibliocommons.com/v2/search?query={book_name}&searchType=smart"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    first_result = soup.find('div', class_='cp-search-result-item-content')
    
    if first_result:
        title_elem = first_result.find('span', class_='title-content')
        author_elem = first_result.find('a', class_='author-link')
        availability_elem = first_result.find('span', class_='cp-availability-status')
        
        title = title_elem.text.strip() if title_elem else "Title not found"
        author = author_elem.text.strip() if author_elem else "Author not found"
        availability = availability_elem.text.strip() if availability_elem else "Availability information not found"
        
        return {"title": title, "author": author, "availability": availability}
    else:
        return {"title": "Book not found", "author": "N/A", "availability": "N/A"}

@app.route('/')
def index():
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    book_name = request.form['book_name']
    genre = request.form['genre']
    
    book_info = fetch_book_availability(book_name)
    
    new_book = {
        'name': book_info['title'],
        'author': book_info['author'],
        'genre': genre,
        'availability': book_info['availability']
    }
    
    books.append(new_book)
    return jsonify(new_book)

if __name__ == '__main__':
    app.run(debug=True)