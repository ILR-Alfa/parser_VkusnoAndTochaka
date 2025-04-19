from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time

url = "https://vkusnoitochka.ru/menu"

firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")  
firefox_options.add_argument("--disable-gpu")
firefox_options.add_argument("--no-sandbox")


service = FirefoxService("C:/web/geckodriver/geckodriver.exe")  

driver = webdriver.Firefox(service=service, options=firefox_options)

try:
    driver.get(url)
    time.sleep(5)  

    
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    
    products = driver.find_elements(By.CSS_SELECTOR, ".product-card")  
    data = []

    for product in products:
        try:
            name = product.find_element(By.CSS_SELECTOR, ".product-name").text 
            price = product.find_element(By.CSS_SELECTOR, ".product-price").text  
            image = product.find_element(By.CSS_SELECTOR, ".product-image img").get_attribute("src")  
            data.append({
                "name": name,
                "price": price,
                "image": image
            })
        except Exception as e:
            print(f"Ошибка при парсинге товара: {e}")

    for item in data:
        print(item)

finally:
    driver.quit()