from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Настройка Selenium для Firefox
url = "https://vkusnoitochka.ru/menu"
firefox_options = FirefoxOptions()
firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
firefox_options.set_preference("permissions.default.geo", 2)  
firefox_options.set_preference("geo.enabled", False)        
firefox_options.add_argument("--disable-gpu")
firefox_options.add_argument("--no-sandbox")
service = FirefoxService(r"C:\web\geckodriver\geckodriver.exe")
driver = webdriver.Firefox(service=service, options=firefox_options)
wait = WebDriverWait(driver, 10)

try:
    driver.get(url)
    print("Заголовок страницы:", driver.title)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#burgery-i-rolly"))).click()
    items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card")))

    for item in items:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", item)
            time.sleep(1)  
            item.click()
            modal = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-abstraction")))

            
            name_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-top__name")))
            name = name_element.text.strip()

            price = modal.find_element(By.CSS_SELECTOR, "span.font-type-6:nth-child(1)").text.strip()
            image = modal.find_element(By.CSS_SELECTOR, ".common-image__img").get_attribute("src")

            print({
                "name": name,
                "price": price,
                "image": image
            })

        except Exception as e:
            print(f"Ошибка при парсинге товара: {e}")

        finally:
            try:
                close_button = modal.find_element(By.CSS_SELECTOR, ".modal-abstraction__close")
                driver.execute_script("arguments[0].scrollIntoView(true);", close_button)
                time.sleep(1)  
                close_button.click()
                wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-abstraction")))
            except Exception:
                pass

finally:
    driver.quit()