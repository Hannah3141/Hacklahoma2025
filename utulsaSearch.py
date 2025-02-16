from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Set up Edge options
edge_options = EdgeOptions()
edge_options.add_argument("--headless")  # Run in headless mode

# Set up the Edge WebDriver using webdriver-manager
service = EdgeService(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=edge_options)

def get_utulsa_statuses(title):
    # Load the page
    driver.get(f"https://universityoftulsa.on.worldcat.org/search?queryString=ti{title[0]}")

    # Wait for the table to be present
    title_element = WebDriverWait(driver, 20).until(
        #TODO: it times out bc it can't find any of my elements; it found elements way at the top, so everything outside the parentheses works
        EC.presence_of_element_located((By.CSS_SELECTOR, "class*='cssltr-1serysv'"))
    )
    title = title_element.text
    print(f"The title of the first book is: {title}")
    driver.quit()
'''  
    return library_status
'''
get_utulsa_statuses("The Hobbit")