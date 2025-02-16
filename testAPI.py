import requests
import json

def get_book(title):
    response = requests.get(
        f"http://opl.bibliocommons.com/search?query={title}&searchType=title"
    )
    #data = response.json()
    return response

results = get_book("The Worlds I See")

#wResults = results.read()
#wjResults = json.loads(results)
print(results)