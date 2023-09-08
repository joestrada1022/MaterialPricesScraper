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
    driver_option.add_argument("--headless")

    return webdriver.Chrome(options=driver_option, executable_path=CHROMEDRIVER_PATH)

def getCategoryLinks() -> list:
    links = []

    # Framing Straps and Hangers
    # links.append('https://www.whitecap.com/c/joist-hangers-and-straps-312950')
    links.append('https://www.whitecap.com/search/?query=lus') # *smaller page for testing
    # links.append('https://www.whitecap.com/search/?query=hus') # *smaller page for testing

    return links

def startCrawling():
    driver = openBrowser()
    data = crawler(driver)
    product_df = pd.DataFrame(data, columns=['Store', 'Category', 'Name', 'Price'])
    # product_df = product_df.reset_index()
    print("\n")
    # print(product_df)
    closeBrowser(driver)
    product_df.to_csv('WhiteCap/products.csv', index=False)
    print("\nSuccess!")

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
    product_list = []
    print("Crawling: " + getSiteName() + "\n")
    links = getCategoryLinks()
    button_xpath = '#product_listing > section > div > div > div:nth-child(3) > div > div > button'
    for link in links:
        print("Crawling: " + link)
        try:
            driver.get(link)
            #let page load
            time.sleep(5)
            driver.maximize_window()
        except:
            driver.refresh()
        hasMore = True
        while hasMore:
            try:
                WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_xpath)))
                button = driver.find_element(by=By.CSS_SELECTOR, value=button_xpath)
                # scroll button into view
                driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(1.25)
                button.click()
                loading = driver.find_element(by=By.XPATH, value='//*[@id="product_listing"]/div')
                while(loading.get_attribute('class') == 'spinner spinner--big active'): 
                    time.sleep(1)
                print("More loaded successfully")
            except NoSuchElementException:
                hasMore = False
            except TimeoutException:
                hasMore = False
        
        # Gets all products that are currently loaded
        products = driver.find_element(by=By.CLASS_NAME, value='product-list')
        products = products.find_elements(by=By.CLASS_NAME, value='product__wrapper')

        #Extracts info from every product
        for prod in products:
            prod_name = prod.find_element(by=By.CLASS_NAME, value='product__sku-id').text
            try:
                prod_price = prod.find_element(by=By.CLASS_NAME, value='product__price-wrapper').text
            except NoSuchElementException:
                continue
            product_list.append(['WhiteCap', 'Hardware', prod_name, prod_price])
    return product_list