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
service = EdgeService(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=edge_options)

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
    
    if title_elem.contents == title: #if in system
    # Load the page
        driver.get(f"https://tccl.bibliocommons.com/v2/availability/{magic_number}")

        # Wait for the table to be present
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cp-table"))
        )

        # Extract the data
        rows = table.find_elements(By.CLASS_NAME, "cp-table-row")
        library_status = {}

        for row in rows:
            cells = row.find_elements(By.CLASS_NAME, "cp-table-cell")
            if len(cells) >= 4:
                library = cells[0].text.split('\n')[-1]
                status = cells[3].text.split('\n')[-1]
                library_status[library] = status
        
        driver.quit()
        
        return library_status
    else:
        return title_elem.contents #TODO: can we ask the user about this?

# Usage
#url = "https://tccl.bibliocommons.com/v2/availability/S63C1803693"
titles = ['To Kill A Mockingbird']
results = get_library_statuses(titles)
print(results)