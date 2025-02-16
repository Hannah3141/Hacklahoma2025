from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def get_library_statuses(url):
    # Set up Edge options
    edge_options = EdgeOptions()
    edge_options.add_argument("--headless")  # Run in headless mode

    # Set up the Edge WebDriver using webdriver-manager
    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=edge_options)

    try:
        # Load the page
        driver.get(url)

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

        return library_status

    finally:
        driver.quit()

# Usage
url = "https://tccl.bibliocommons.com/v2/availability/S63C1803693"
results = get_library_statuses(url)
print(results)
