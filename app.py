from flask import Flask, render_template, request, jsonify
import requests
#from google import generativeai as genai
import os
from bs4 import BeautifulSoup

app = Flask(__name__)

# Sample data: Temporary list for books and their availability
books = []

# Configures the Gemini API
#genai.configure(api_key='AIzaSyCJhZA-00AjixPDrf3DZ3MYLg1H1VLSUqg')

# using 1.5 bc its free yay
#model = genai.GenerativeModel('gemini-1.5-flash')

# Route to get book availability
@app.route('/toggle_availability', methods=['POST'])
def fetch_book_availability(book_name):
    url = f"https://tccl.bibliocommons.com/v2/search?query={book_name}&searchType=smart"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
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

# Route to display the reading list
@app.route('/')
def index():
    return render_template('index.html', books=books)

# Route to add a new book
@app.route('/add_book', methods=['POST'])
def add_book():
    book_name = request.form['book_name']
    
    book_info = fetch_book_availability(book_name)
    
    new_book = {
        'name': book_info['title'],
        'author': book_info['author'],
        'availability': book_info['availability']
    }
    
    books.append(new_book)
    return jsonify(new_book)

# Route to delete a book
@app.route('/delete_book', methods=['POST'])
def delete_book():
    book_name = request.form['book_name']
    global books
    books = [book for book in books if book['name'] != book_name]

    return jsonify({'status': 'deleted', 'book_name': book_name})

'''@app.route('/get_book_recs', methods=['POST'])
def get_book_recs(user_books):
    prompt = f"Based on the following books: {user_books}, recommend 3 similar books with their titles and authors."
    response = model.generate_content(prompt)
    return response.text'''

# Route to mark a book as read
@app.route('/mark_read', methods=['POST'])
def mark_read():
    book_name = request.form['book_name']
    
    for book in books:
        if book['name'] == book_name:
            book['availability'] = "Read"
            break

    return jsonify({'status': 'marked', 'book_name': book_name, 'availability': "Read"})

if __name__ == '__main__':
    app.run(debug=True)
