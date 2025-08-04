from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
import requests
import json
from bs4 import BeautifulSoup
import successfulScraper

app = Flask(__name__)

# Set up Edge options
edge_options = EdgeOptions()
edge_options.add_argument("--headless")  # Run in headless mode

# Set up the Edge WebDriver using webdriver-manager
# I've got no idea how to add this on GitHub, but right click EdgeChromiumDriverManager, click Go To Definition, and change the urls to "https://msedgedriver.microsoft.com" and "https://msedgedriver.microsoft.com/LATEST_RELEASE" instead of the azure ones.
service = EdgeService(EdgeChromiumDriverManager().install()) 
driver = webdriver.Edge(service=service, options=edge_options)

# Sample data: Temporary list for books and their availability
books = []

# Route to get book availability
@app.route('/toggle_availability', methods=['POST'])
def fetch_TCCL_results():
    book_name = request.form['book_name']
    url = f"https://tccl.bibliocommons.com/v2/search?query={book_name}&searchType=smart&f_FORMAT=BK"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    file = open("tccl1.html", "w", encoding="utf-8")
    file.write(soup.prettify())
    file.close()
    
    first_result = soup.find('div', class_='cp-search-result-item-content')
    
    if first_result:
        title_elem = first_result.find('span', class_='title-content')
        author_elem = first_result.find('a', class_='author-link')

        title = title_elem.text.strip() if title_elem else "Title not found"
        author = author_elem.text.strip() if author_elem else "Author not found"

        return {"title": title, "author": author}
    else:
        return {"title": book_name, "author": "Unknown"}
    
@app.route('/toggle_availability', methods=['POST'])   
def fetch_Monarch_results():
    book_name = request.form['book_name']
    url = f"https://flwl-monarch.search.monarchcatalog.org/search?query={book_name}&searchType=title&pageSize=10&materialTypeIds=41,36,1&pageNum=0"
    #BeautifulSoup version
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    file = open("monarch1.html", "w", encoding="utf-8")
    file.write(soup.prettify())
    file.close()

    '''first_result = soup.find('div', class_='card py-4 px-4')
    
    if first_result:
        title_elem = first_result.find('a', class_='notranslate ng-star-inserted')
        author_elem = first_result.find('span', class_='notranslate')

        title = title_elem.text.strip() if title_elem else "Title not found"
        author = author_elem.text.strip() if author_elem else "Author not found"

        return {"title": title, "author": author}
    else:
        return {"title": book_name, "author": "Unknown"}
    '''
    
    # Selenium version
    response = driver.get(url)
    file = open("monarch1.html", "w", encoding="utf-8") #idk which encoding
    file.write(driver.page_source)
    file.close()
    
    first_result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "app-entities")) #what do you want from me???
    )

    file = open("monarch1.html", "w", encoding="utf-8") #idk which encoding
    file.write(driver.page_source)
    file.close()
 
# Route to display the reading list
@app.route('/')
def index():
    return render_template('index.html', books=books)

# Route to add a new book
@app.route('/add_book', methods=['POST'])
def add_book():
    TCCL_info = fetch_TCCL_results() # this is the one actually listed in the catalog
    available_list = successfulScraper.get_library_statuses(TCCL_info['title'])

    monarch_info = fetch_Monarch_results() # this is the one that Monarch returns
    
    
    new_book = {
        'name': TCCL_info['title'],
        'author': TCCL_info['author'],
        'availability': available_list if available_list else None
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
