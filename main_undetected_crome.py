import undetected_chromedriver as uc
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = uc.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(options=options)

try:
    driver.get("https://pb.nalog.ru/")
    search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "queryAll")))

    time.sleep(random.uniform(1, 3))

    # Ввод текста с задержкой
    for char in "7725838280":
        search_box.send_keys(char)
        time.sleep(random.uniform(0.02, 0.2))

    search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "bi-search")))
    time.sleep(random.uniform(1, 3))

    search_button.click()
    time.sleep(15)

except Exception as ex:
    print(f"Exception: {ex}")

finally:
    if 'driver' in locals():
        driver.quit()
