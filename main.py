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
# firefox_options.add_argument("--headless")  # Временно отключите headless для отладки
firefox_options.add_argument("--disable-gpu")
firefox_options.add_argument("--no-sandbox")

# Путь к GeckoDriver
service = FirefoxService(r"C:\web\geckodriver\geckodriver.exe")

# Создаем экземпляр драйвера Firefox
driver = webdriver.Firefox(service=service, options=firefox_options)
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

try:
    # Открываем сайт
    driver.get(url)
    print("Заголовок страницы:", driver.title)

    # Явное ожидание загрузки разделов
    sections = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".menu-categories__list-scrolled > a")))
    print(f"Найдено {len(sections)} разделов.")

    for section in sections:
        try:
            # Получаем название раздела
            section_name = section.text.strip()  # Берем текст из элемента <a>
            section_id = section.get_attribute("id")  # Берем id раздела
            print(f"Обрабатываем раздел: {section_name} (ID: {section_id})")

            # Прокручиваем до раздела и кликаем
            driver.execute_script("arguments[0].scrollIntoView(true);", section)
            time.sleep(1)  # Краткая задержка для стабильности
            try:
                close_button = driver.find_element(By.CSS_SELECTOR, ".modal-abstraction__close")
                close_button.click()
                wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-abstraction")))  # Ждем закрытия модального окна
            except Exception:
                pass  # Если модальное окно отсутствует, игнорируем ошибку
            section.click()

            # Явное ожидание загрузки карточек товаров
            items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card")))
            print(f"Найдено {len(items)} карточек товаров в разделе.")

            for item in items:
                try:
                    # Прокручиваем до элемента и кликаем
                    driver.execute_script("arguments[0].scrollIntoView(true);", item)
                    time.sleep(1)  # Краткая задержка для стабильности
                    actions.move_to_element(item).click().perform()

                    # Явное ожидание загрузки модального окна
                    modal = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-abstraction")))

                    # Извлекаем данные из модального окна
                    name = modal.find_element(By.CSS_SELECTOR, ".product-top__name").text.strip()
                    price = modal.find_element(By.CSS_SELECTOR, "span.font-type-6:nth-child(1)").text.strip()  # Новый селектор для цены
                    image = modal.find_element(By.CSS_SELECTOR, ".common-image__img").get_attribute("src")

                    print({
                        "name": name,
                        "price": price,
                        "image": image
                    })

                    # Закрываем модальное окно
                    close_button = modal.find_element(By.CSS_SELECTOR, ".modal-abstraction__close")
                    close_button.click()
                    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-abstraction")))  # Ждем закрытия модального окна

                except Exception as e:
                    print(f"Ошибка при парсинге товара: {e}")

        except Exception as e:
            print(f"Ошибка при обработке раздела: {e}")

finally:
    # Закрываем браузер
    driver.quit()