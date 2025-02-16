import requests
import urllib.parse

def get_isbn_from_title(title):
    # Encode the title for use in the URL
    encoded_title = urllib.parse.quote(title)
    
    # Construct the API URL
    url = f"https://openlibrary.org/search.json?title={encoded_title}"
    
    # Send a GET request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Check if any books were found
        if data['num_found'] > 0:
            # Get the first book's ISBN (if available)
            book = data['docs'][0]
            if 'isbn' in book:
                return book['isbn'][0]
            else:
                return "ISBN not found for this book"
        else:
            return "No books found with this title"
    else:
        return "Error accessing the Open Library API"

# Example usage
title = "To Kill a Mockingbird"
isbn = get_isbn_from_title(title)
print(f"ISBN for '{title}': {isbn}")