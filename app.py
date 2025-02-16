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
    # Get data from the form
    book_name = request.form['book_name']
    genre = request.form['genre']

    # Set a placeholder availability value for now
    availability = "Available"  # Placeholder value for now

    # Create a new book dictionary
    new_book = {
        'name': book_name,
        'genre': genre,
        'availability': availability
    }

    # Add the book to the list 
    books.append(new_book)

    # Return the new book as a JSON response
    return jsonify(new_book)

# Route to delete a book
@app.route('/delete_book', methods=['POST'])
def delete_book():
    book_name = request.form['book_name']
    
    # Find and remove the book from the list
    global books
    books = [book for book in books if book['name'] != book_name]

    return jsonify({'status': 'deleted', 'book_name': book_name})

# Route to mark a book as read
@app.route('/mark_read', methods=['POST'])
def mark_read():
    book_name = request.form['book_name']
    
    # Find the book and update its availability
    for book in books:
        if book['name'] == book_name:
            book['availability'] = "Read"
            break

    return jsonify({'status': 'marked', 'book_name': book_name, 'availability': "Read"})

if __name__ == '__main__':
    app.run(debug=True)
