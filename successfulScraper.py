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
        f"https://tccl.bibliocommons.com/v2/search?query={title[0]}&searchType=title&f_FORMAT=BK"
    )
    soup = BeautifulSoup(response.text, 'html.parser')
    first_result = soup.find('div', class_='cp-search-result-item-content')
    if first_result == None:
        return False
    title_elem = first_result.find('span', class_='title-content')
    magic_number = first_result.find('a', attrs={'data-key': 'bib-title'})['data-test-id'][10:]
    
    #if title_elem.text.strip() == title[0]:  # Compare with the first (and only) element of the title list

    # Only process the first result's formats (all formats, not just physical books)
    format_links = first_result.find_all('a', attrs={'data-key': 'bib-title'})
    if not format_links:
        return False

    # Only use the first format link (corresponds to the first result)
    link = format_links[0]
    if not link.has_attr('href'):
        return False
    format_name = link.text.strip() # this is not the format, idk what it is copilot
    availability_url = "https://tccl.bibliocommons.com" + link['href']

    library_status = {}

    SelDriver.get(availability_url)
    try:
        table = WebDriverWait(SelDriver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cp-manifestation-list"))
        )
        rows = table.find_elements(By.CLASS_NAME, "manifestation-item")
        for row in rows:
            try:
                status_elem = row.find_element(By.CLASS_NAME, "cp-availability-status")
                status = status_elem.text.strip()
            except Exception:
                status = "Unknown"
            library_status[format_name] = status
    except Exception:
        library_status[format_name] = "Unavailable"

    return library_status


     # Extract the data
    rows = table.find_elements(By.CLASS_NAME, "manifestation-item cp-manifestation-list-item row")
    library_status = {}

    for row in rows:
        format = row.find_element(By.CLASS_NAME, "cp-screen-reader-message")
        status = row.find_element(By.CLASS_NAME, "cp-availability-status available")
        library_status[format] = status

    #SelDriver.quit() would quit after the first book?

    return library_status



# Usage
#url = "https://tccl.bibliocommons.com/v2/availability/S63C1803693"
# titles = ['To Kill A Mockingbird']
# results = get_library_statuses(titles)
# print(results)
