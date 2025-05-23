# parser_VkusnoAndTochaka

Парсер меню "Вкусно – и точка" 

Этот проект представляет собой скрипт на Python, который парсит данные о товарах с сайта vkusnoitochka.ru  и сохраняет их в Excel-файл (products.xlsx). Скрипт использует библиотеку Selenium для автоматизации браузера Firefox. 
Оглавление 

    Описание функционала 
    Требования к системе 
    Установка зависимостей 
    Настройка и запуск 
    Структура выходных данных 
    Известные проблемы 
    Лицензия 
     

Описание функционала 

Скрипт выполняет следующие действия: 

    Переходит на сайт vkusnoitochka.ru/menu .
    Обрабатывает разделы меню (например, "Новинки", "Бургеры и роллы").
    Открывает карточки товаров и собирает информацию:
        Название товара.
        Цена.
        Ссылка на изображение.
         
    Сохраняет данные в файл products.xlsx в формате Excel.
    Если файл уже существует, обновляет данные, добавляя новые товары или изменяя существующие.
     

Требования к системе 

Для работы скрипта требуется: 

    Python 3.8 или выше .
    Firefox  (браузер).
    GeckoDriver  (драйвер для Firefox).
     

Установка зависимостей 

    Установите Python: 
        Скачайте Python с официального сайта .
        Во время установки убедитесь, что выбрана опция "Add Python to PATH".
         

    Установите необходимые библиотеки: 
    bash
     

     
    1
    pip install selenium openpyxl
     
     

    Установите Firefox: 
        Скачайте и установите Firefox с официального сайта .
         

    Установите GeckoDriver: 
        Скачайте GeckoDriver с официального репозитория .
        Распакуйте архив и поместите файл geckodriver.exe в папку с проектом или добавьте его в переменную PATH.
         
     

Настройка и запуск 

    Клонируйте репозиторий (если используется Git): 
    bash
     

git clone https://github.com/your-repository-url.git
cd your-repository-folder
 
 

Запустите скрипт: 
bash
 

     
    
    python main.py
     
     

    После завершения работы скрипта файл products.xlsx будет создан/обновлен в той же директории. 
     

Структура выходных данных 

Файл products.xlsx содержит таблицу с тремя столбцами: 

    Name : Название товара.
    Price : Цена товара.
    Image : Ссылка на изображение товара.
     


 
Известные проблемы 

    Модальное окно загружается медленно : 
        Если модальное окно не успевает загрузиться, скрипт может выдать ошибку. Для решения этой проблемы добавлены задержки (time.sleep) и явные ожидания (WebDriverWait).
         

    Элементы перекрываются : 
        Иногда элементы на странице перекрываются другими элементами, что приводит к ошибкам. В таких случаях можно увеличить задержки или использовать JavaScript для взаимодействия с элементами.
         

    Графический интерфейс браузера : 
        Если вы хотите запустить скрипт без графического интерфейса, используйте режим --headless. Он включен в коде, но закомментирован.
         
     

Лицензия 

Этот проект распространяется под лицензией MIT License . Вы можете свободно использовать, изменять и распространять этот код, соблюдая условия лицензии. 

Если у вас есть вопросы или предложения по улучшению, пожалуйста, создайте issue в репозитории. 