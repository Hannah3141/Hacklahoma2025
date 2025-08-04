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

try:
    # Set up Edge options
    edge_options = EdgeOptions()
    edge_options.add_argument("--headless")  # Run in headless mode

    # Set up the Edge WebDriver using webdriver-manager
    # I've got no idea how to add this on GitHub, but right click EdgeChromiumDriverManager, click Go To Definition, and change the urls to "https://msedgedriver.microsoft.com" and "https://msedgedriver.microsoft.com/LATEST_RELEASE" instead of the azure ones.
    service = EdgeService(EdgeChromiumDriverManager().install()) 
    driver = webdriver.Edge(service=service, options=edge_options)
except Exception:
    print("Edge WebDriver setup failed. Falling back to Firefox.")
    # Set up Firefox options
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--headless")  # Run in headless mode
    # Set up the Firefox WebDriver
    service = webdriver.FirefoxService() #i don't think this actually works, idk what to do
    driver = webdriver.Firefox(options=firefox_options)


def get_library_statuses(title):
    response = requests.get(
        f"https://tccl.bibliocommons.com/v2/search?query={title}&searchType=title"
    )
    soup = BeautifulSoup(response.text, 'html.parser')
    file = open("tccl2.html", "w", encoding="utf-8")
    file.write(soup.prettify())
    file.close()
    first_result = soup.find('div', class_='cp-search-result-item-content') 
    if first_result == None:
        return False
    title_section = first_result.find('h2', class_='cp-title') 
    title_elem = title_section.find('span', class_='title-content') 
    magic_number = first_result.find('a', attrs={'data-key': 'bib-title'})['href'] 
    
    #if title_elem.text.strip() == title[0]:  # Compare with the first (and only) element of the title list

    library_status = {}
    try:
        table = soup.find('div', class_='cp-manifestation-list')
        
        rows = table.find_all('div', class_="manifestation-item cp-manifestation-list-item row")
        for row in rows:
                try:
                    format_label = row.find('span', class_="cp-screen-reader-message").contents
                    format = format_label[0].split(',')  # Get the first word, which is the format
                except Exception:
                     format = "Error retrieving format"
                try:
                    status_elem = row.find('span', class_="cp-availability-status") #Little Women works, Black Beauty does not
                    status = status_elem.contents 
                except Exception:
                    status = "Unknown"
                if format[0] == 'Book' or format[0] == 'eBook' or format[0] == 'eAudiobook' or format[0] == 'Graphic Novel':
                    if format[0] not in library_status or library_status[format[0]] == 'All copies in use':
                        library_status[format[0]] = status[0] 
    except Exception:
        library_status[format[0]] = "Error retrieving status"
    return library_status

# Terminal display
# url = "https://tccl.bibliocommons.com/v2/availability/S63C1803693"
# titles = ['To Kill A Mockingbird']
# results = get_library_statuses(titles)
# print(results)
