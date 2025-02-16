import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key='AIzaSyCJhZA-00AjixPDrf3DZ3MYLg1H1VLSUqg')

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

def get_book_recommendations(user_books):
    prompt = f"Based on the following books: {user_books}, recommend 3 similar books with their titles and authors."
    response = model.generate_content(prompt)
    return response.text

# Example usage
user_books = "To Kill a Mockingbird, Where the Sidewalk Ends, The Hobbit"
recommendations = get_book_recommendations(user_books)
print(recommendations)
