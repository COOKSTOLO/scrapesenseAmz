import json
import pickle
import time
from selenium import webdriver
from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def load_enlaces(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_cookies(driver, cookies_path):
    try:
        with open(cookies_path, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print("Cookies aplicadas exitosamente.")
    except FileNotFoundError:
        print("El archivo cookies.pkl no se encontró.")
    except Exception as e:
        print(f"Error al cargar las cookies: {e}")

def solve_captcha(driver):
    try:
        link = driver.find_element(By.XPATH, "//div[@class='a-row a-text-center']//img").get_attribute('src')
        captcha = AmazonCaptcha.fromlink(link)
        captcha_value = AmazonCaptcha.solve(captcha)
        driver.find_element(By.ID, "captchacharacters").send_keys(captcha_value)
        driver.find_element(By.CLASS_NAME, "a-button-text").click()
        print("Captcha resuelto y botón clickeado.")
    except Exception as e:
        print(f"Error al resolver el captcha: {e}")

def main():
    # Configuración del navegador
    options = Options()
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Cargar enlaces desde el JSON
    enlaces = load_enlaces('enlaces_amz.json')

    for enlace in enlaces:
        try:
            driver.get(enlace)
            solve_captcha(driver)
            time.sleep(5)  # Esperar 5 segundos para que la página cargue
            load_cookies(driver, 'cookies.pkl')
        except Exception as e:
            print(f"Error al procesar el enlace {enlace}: {e}")

    driver.quit()

if __name__ == "__main__":
    main()







