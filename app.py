from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Sample data: Temporary list for books and their availability
books = []

# Function to check availability (using your scraping logic)
def fetch_book_availability(book_name):
    # Example scraping logic for a specific library website
    url = f"http://example-library-website.com/search?query={book_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # For simplicity, let's assume the availability info is within <div class='status'>
    status = soup.find('div', class_='status').text.strip()
    
    return status

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


if __name__ == '__main__':
    app.run(debug=True)
