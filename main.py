from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Настройка Selenium для Firefox
url = "https://vkusnoitochka.ru/menu"
firefox_options = FirefoxOptions()
firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
service = FirefoxService(r"C:\web\geckodriver\geckodriver.exe")
driver = webdriver.Firefox(service=service, options=firefox_options)
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

try:
    driver.get(url)
    print("Заголовок страницы:", driver.title)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#burgery-i-rolly"))).click()


    def is_element_visible(element):
        return element.is_displayed() and element.size["height"] > 0 and element.size["width"] > 0

    
    while True:
        items = driver.find_elements(By.CSS_SELECTOR, ".product-card")

        processed_any = False

        for item in items:
            try:
                if not is_element_visible(item):
                    continue

                
                driver.execute_script("arguments[0].scrollIntoView(true);", item)
                time.sleep(1)  
                actions.move_to_element(item).click().perform()
                modal = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-abstraction")))

                name = modal.find_element(By.CSS_SELECTOR, ".product-top__name").text.strip()
                price = modal.find_element(By.CSS_SELECTOR, "span.font-type-6:nth-child(1)").text.strip()
                image = modal.find_element(By.CSS_SELECTOR, ".common-image__img").get_attribute("src")
                print({
                    "name": name,
                    "price": price,
                    "image": image
                })

                
                close_button = modal.find_element(By.CSS_SELECTOR, ".modal-abstraction__close")
                close_button.click()
                wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-abstraction")))
                processed_any = True

            except Exception as e:
                print(f"Ошибка при парсинге товара: {e}")

        
        if not processed_any:
            break

        
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(2)  

finally:
    driver.quit()