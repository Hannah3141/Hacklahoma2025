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

def get_library2_statuses(title):
    response = driver.get(
        f"https://flwl-monarch.search.monarchcatalog.org/search?query={title}&searchType=title&pageSize=10&materialTypeIds=41,36,1&pageNum=0"
    )
    file = open("monarch2.html", "w", encoding="utf-8")
    file.write(driver.page_source)
    file.close()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    first_result = soup.find('div', class_='card py-4 px-4')
    if first_result == None:
        return False
    title_elem = first_result.find('a', class_='notranslate ng-star-inserted')
    #magic_number = first_result.find('a', attrs={'data-key': 'bib-title'})['href'] 

    library_status = {}
    try:
        header = first_result.find('drag-scroll')
        formats = header.find_all('a', class_='tab-label nav-link nav-item ng-star-inserted') + header.find_all('a', class_='tab-label nav-link nav-item active ng-star-inserted')
        for header in formats:
            status_elem = header.find('div', class_="status d-inline-flex ng-star-inserted")
            variated_status_elem = status_elem.find('span')
            status = variated_status_elem.contents if status_elem else "Unknown"
            format_elem = header.find('div', class_="label ng-star-inserted")
            format = format_elem.text.strip() if format_elem else "Unknown" 
            if format[0] == 'Book' or format[0] == 'eBook' or format[0] == 'eAudiobook' or format[0] == 'Graphic Novel':
                library_status[format] = status
    except Exception:
        library_status[format] = "Error retrieving status"
    
    return library_status
# Terminal display
# url = "https://tccl.bibliocommons.com/v2/availability/S63C1803693"
# titles = ['To Kill A Mockingbird']
# results = get_library_statuses(titles)
# print(results)
