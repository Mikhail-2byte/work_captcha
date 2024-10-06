import undetected_chromedriver as uc
import time
import random
import pickle
import io
import requests
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Список User-Agent для случайной подмены
user_agents = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]

options = uc.ChromeOptions()
options.add_argument(f"user-agent={random.choice(user_agents)}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-extensions")
driver = uc.Chrome(options=options)

# Загрузка cookies из файла
def load_cookies():
    try:
        with open("cookies.pkl", "rb") as f:
            cookies = pickle.load(f)
        driver.get("https://pb.nalog.ru/")  # Открываем нужный домен
        for cookie in cookies:
            if cookie['domain'] in driver.current_url:  # Проверяем, что куки соответствуют текущему домену
                driver.add_cookie(cookie)
    except FileNotFoundError:
        print("Cookies file not found. Starting fresh.")

# Сохранение cookies в файл
def save_cookies():
    cookies = driver.get_cookies()
    with open("cookies.pkl", "wb") as f:
        pickle.dump(cookies, f)

# Функция для захвата и сохранения изображения CAPTCHA
def save_captcha_image():
    captcha_image_element = driver.find_element(By.XPATH, "//img[contains(@src, 'captcha.bin')]")
    captcha_image_src = captcha_image_element.get_attribute("src")
    
    # Загружаем изображение CAPTCHA
    captcha_image_url = f"https://pb.nalog.ru{captcha_image_src}"
    captcha_image = requests.get(captcha_image_url)
    image = Image.open(io.BytesIO(captcha_image.content))
    image.save("captcha_image.png")

try:
    driver.get("https://pb.nalog.ru/")  # Сначала открываем страницу
    load_cookies()  # Затем загружаем куки

    # Имитация движения мыши перед вводом текста
    actions = ActionChains(driver)
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "queryAll")))
    actions.move_to_element(element).perform()
    
    time.sleep(random.uniform(1, 3))

    # Ввод текста с задержкой между символами
    for char in "7725838280":
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

    search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "bi-search")))
    
    actions.move_to_element(search_button).perform()
    time.sleep(random.uniform(1, 4))
    
    search_button.click()

    # Подождите, чтобы страница результатов загрузилась
    time.sleep(10)  # Увеличиваем время ожидания

    # Отладка: проверьте код страницы
    print(driver.page_source)

    # Проверка на наличие CAPTCHA
    try:
        # Ожидание появления CAPTCHA
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'captcha.bin')]")))
        print("CAPTCHA appeared.")
        save_captcha_image()  # Сохранение изображения CAPTCHA
        print("CAPTCHA image saved as captcha_image.png.")
    except Exception as captcha_ex:
        print("No CAPTCHA appeared or was not found.")
        print(captcha_ex)

    time.sleep(random.uniform(10, 200))
    save_cookies()

except Exception as ex:
    print(f"Exception: {ex}")

finally:
    if 'driver' in locals():
        driver.quit()
