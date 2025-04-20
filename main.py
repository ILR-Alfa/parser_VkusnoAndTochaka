from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


url = "https://vkusnoitochka.ru/menu"

firefox_options = FirefoxOptions()
firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
# firefox_options.add_argument("--headless")  
firefox_options.add_argument("--disable-gpu")
firefox_options.add_argument("--no-sandbox")


service = FirefoxService(r"C:\web\geckodriver\geckodriver.exe")


driver = webdriver.Firefox(service=service, options=firefox_options)
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

try:
    driver.get(url)
    print("Заголовок страницы:", driver.title)

    sections = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".menu-categories__list-scrolled > a")))
    print(f"Найдено {len(sections)} разделов.")

    for section in sections:
        try:
            section_name = section.text.strip()  
            section_id = section.get_attribute("id")  
            print(f"Обрабатываем раздел: {section_name} (ID: {section_id})")

            
            driver.execute_script("arguments[0].scrollIntoView(true);", section)
            time.sleep(1)  
            try:
                close_button = driver.find_element(By.CSS_SELECTOR, ".modal-abstraction__close")
                close_button.click()
                wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-abstraction")))  
            except Exception:
                pass  
            section.click()

            
            items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card")))
            print(f"Найдено {len(items)} карточек товаров в разделе.")

            for item in items:
                try:
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

                except Exception as e:
                    print(f"Ошибка при парсинге товара: {e}")

        except Exception as e:
            print(f"Ошибка при обработке раздела: {e}")

finally:
    
    driver.quit()