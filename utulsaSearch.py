from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import NoSuchElementException

# Set up Edge options
edge_options = EdgeOptions()
edge_options.add_argument("--headless")  # Run in headless mode

# Set up the Edge WebDriver using webdriver-manager
service = EdgeService(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=edge_options)

def get_utulsa_statuses(title):
    # Load the page
    driver.get(f"https://universityoftulsa.on.worldcat.org/search?queryString=ti:({title[0]})")

    # Wait for the table to be present
    box_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-9.jss85.cssltr-3m06hh"))
    )
    try:
        first_element = box_element.find_element(By.CSS_SELECTOR, "li[data-testid='record-0']")
    except NoSuchElementException:
        return "No results found"
    try:
        #title_element = first_element.find_element(By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-h6.MuiTypography-alignLeft.jss229.cssltr-k1mv2p")
        title_element = first_element.find_element(By.CSS_SELECTOR, "span[data-testid='highlighted-term-container']")
        print(title_element.text)
    except NoSuchElementException:
        print("No such title element")

    '''
    title = title_element.text
    print(f"The title of the first book is: {title}")
    driver.quit()

    return library_status
'''
get_utulsa_statuses("The Worlds I See")