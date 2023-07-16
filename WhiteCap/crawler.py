from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

driver_option = webdriver.ChromeOptions()
driver_option.add_argument("--incognito")
driver_option.add_experimental_option('excludeSwitches', ['enable-logging'])
driver_option.add_experimental_option("detach", True)

def getMainURL():
    url = 'https://www.whitecap.com/'
    return url

def getSiteName():
    name = "WhiteCap"
    return name

def create_webdriver():
    return webdriver.Chrome(options=driver_option)

browser = create_webdriver()
browser.get(getMainURL())