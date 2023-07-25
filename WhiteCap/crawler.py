from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

CHROMEDRIVER_PATH = "ChromeDriver\chromedriver.exe"

def getMainURL():
    url = 'https://www.whitecap.com/'
    return url

def getSiteName() -> str:
    name = "WhiteCap"
    return name

def create_webdriver() -> webdriver:

    driver_option = webdriver.ChromeOptions()
    driver_option.add_argument("--incognito")
    driver_option.add_argument("--log-level=3")
    # driver_option.add_experimental_option("detach", True)

    return webdriver.Chrome(options=driver_option, executable_path=CHROMEDRIVER_PATH)

def getCategoryLinks() -> list:
    links = []

    # Framing Straps and Hangers
    links.append('https://www.whitecap.com/c/joist-hangers-and-straps-312950')

    return links

def startCrawling():
    driver = openBrowser()
    data = crawler(driver)
    product_df = pd.DataFrame.from_dict(data, orient='index')
    product_df = product_df.reset_index()
    product_df.columns = ['Product_ID', 'Price']
    print(product_df)
    closeBrowser(driver)

def openBrowser() -> webdriver:
    print("Opening Browser...")

    driver = create_webdriver()
    driver.get(getMainURL())

    time.sleep(2.5)
    print("Browser Connected")

    return driver

def closeBrowser(driver: webdriver):
    print("Closing Browser...")
    driver.quit()
    time.sleep(3)
    return

def crawler(driver: webdriver) -> dict:
    print("Crawling: " + getSiteName() + "\n")
    links = getCategoryLinks()
    for link in links:
        print("Crawling: " + link)
        try:
            driver.get(link)
            #let page load
            time.sleep(5)
        except:
            driver.refresh()
        # Gets all products that are currently loaded
        products = driver.find_element(by=By.CLASS_NAME, value='product-list')
        products = products.find_elements(by=By.CLASS_NAME, value='product__wrapper')

        #Extracts info from every product
        product_list = {}
        for prod in products:
            prod_name = prod.find_element(by=By.CLASS_NAME, value='product__sku-id').text
            prod_price = prod.find_element(by=By.CLASS_NAME, value='product__price-wrapper').text
            product_list[prod_name] = prod_price
    return product_list


# TODO: configure Better Comments Extension. probably watch tutorial
'''
TODO: Write code that gets current category name and saves current dataframe in a csv (make function and make
crawler call this function)
TODO: Make page loader that loads the page completely first then get all products. 
TODO: add checker in driver creation for site being down
'''
