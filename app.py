from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample data: Temporary list for books and their availability
books = []

# Route to display the reading list
@app.route('/')
def index():
    return render_template('index.html', books=books)

# Route to add a new book
@app.route('/add_book', methods=['POST'])
def add_book():
    book_name = request.form['book_name']
    genre = request.form['genre']
    availability = "Available"

    new_book = {'name': book_name, 'genre': genre, 'availability': availability}
    books.append(new_book)

    return jsonify(new_book)

# Route to delete a book
@app.route('/delete_book', methods=['POST'])
def delete_book():
    book_name = request.form['book_name']
    global books
    books = [book for book in books if book['name'] != book_name]

    return jsonify({'status': 'deleted', 'book_name': book_name})

# Route to mark a book as read
@app.route('/mark_read', methods=['POST'])
def mark_read():
    book_name = request.form['book_name']
    
    for book in books:
        if book['name'] == book_name:
            book['availability'] = "Read"
            break

    return jsonify({'status': 'marked', 'book_name': book_name, 'availability': "Read"})

# Route to toggle book availability
@app.route('/toggle_availability', methods=['POST'])
def toggle_availability():
    book_name = request.form['book_name']
    new_availability = request.form['new_availability']
    
    for book in books: 
        if book['name'] == book_name:
            book['availability'] = new_availability
            break

    return jsonify({'status': 'updated', 'book_name': book_name, 'availability': new_availability})

if __name__ == '__main__':
    app.run(debug=True)
