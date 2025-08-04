from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import requests
import json
from bs4 import BeautifulSoup

# Set up Edge options
edge_options = EdgeOptions()
edge_options.add_argument("--headless")  # Run in headless mode

# Set up the Edge WebDriver using webdriver-manager
# I've got no idea how to add this on GitHub, but right click EdgeChromiumDriverManager, click Go To Definition, and change the urls to "https://msedgedriver.microsoft.com" and "https://msedgedriver.microsoft.com/LATEST_RELEASE" instead of the azure ones.
service = EdgeService(EdgeChromiumDriverManager().install()) 
SelDriver = webdriver.Edge(service=service, options=edge_options)

def get_library_statuses(title):
    response = requests.get(
        f"https://tccl.bibliocommons.com/v2/search?query={title}&searchType=title"
    )
    soup = BeautifulSoup(response.text, 'html.parser')
    file = open("debug.html", "w", encoding="utf-8")
    file.write(soup.prettify())
    file.close()
    first_result = soup.find('div', class_='cp-search-result-item-content') 
    if first_result == None:
        return False
    title_section = first_result.find('h2', class_='cp-title') 
    title_elem = title_section.find('span', class_='title-content') 
    magic_number = first_result.find('a', attrs={'data-key': 'bib-title'})['href'] 
    
    #if title_elem.text.strip() == title[0]:  # Compare with the first (and only) element of the title list

    '''
    # Only process the first result's formats (all formats, not just physical books)
    format_links = first_result.find_all('a', attrs={'data-key': 'bib-title'})
    if not format_links:
        return False

    # Only use the first format link (corresponds to the first result)
    link = format_links[0]
    if not link.has_attr('href'):
        return False
    format_name = link.text.strip() # this is not the format, idk what it is copilot
    availability_url = "https://tccl.bibliocommons.com" + magic_number #link['href']

    

    SelDriver.get(availability_url)
    '''
    library_status = {}
    #try:
    #table = WebDriverWait(SelDriver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cp-manifestation-list"))
    table = soup.find('div', class_='cp-manifestation-list')
    #table = SelDriver.find_element(By.CLASS_NAME, "cp-manifestation-list")
    
    rows = table.find_all('div', class_="manifestation-item cp-manifestation-list-item row")
    for row in rows:
            #try:
                status_elem = row.find('span', class_="cp-availability-status")
                print(status_elem.contents) #Little Women works, Black Beauty does not
                status = status_elem.contents 
                format = row.find('span', class_="cp-screen-reader-message").contents
                print(format)
            #except Exception:
            #    status = "Unknown"
                library_status[format[0]] = status[0]
    #except Exception:
    #    library_status[format_name] = "Unavailable"

    return library_status

# Terminal display
# url = "https://tccl.bibliocommons.com/v2/availability/S63C1803693"
# titles = ['To Kill A Mockingbird']
# results = get_library_statuses(titles)
# print(results)
