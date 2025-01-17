import json
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from amazoncaptcha import AmazonCaptcha

# Cargar el archivo JSON con las URLs
with open('enlaces_amz.json', 'r') as file:
    urls = json.load(file)

# Configurar el driver de Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def solve_captcha(driver):
    try:
        link = driver.find_element(By.XPATH, "//div[@class='a-row a-text-center']//img").get_attribute('src')
        captcha = AmazonCaptcha.fromlink(link)
        captcha_value = AmazonCaptcha.solve(captcha)
        driver.find_element(By.ID, "captchacharacters").send_keys(captcha_value)
        driver.find_element(By.CLASS_NAME, "a-button-text").click()
        print("Captcha resuelto y botón clickeado.")
        time.sleep(5)  # Esperar 5 segundos después de resolver el captcha
    except Exception as e:
        print(f"Error al resolver el captcha: {e}")

# Iterar sobre cada URL
for url in urls:
    response = requests.get(url)
    driver.get(url)
    
    # Esperar 5 segundos para que la página cargue
    time.sleep(5)
    
    # Intentar resolver el captcha si aparece
    try:
        captcha_image = driver.find_element(By.XPATH, "//div[@class='a-row a-text-center']//img")
        if captcha_image:
            solve_captcha(driver)
    except:
        print("No se encontró captcha, continuando con el scraping.")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('span', id='productTitle')
        if title:
            print("Título:", title.get_text(strip=True))
        else:
            print("No se encontró el título del producto.")
        
        # Buscar todos los div con id 'imgTagWrapperId' y obtener los src de las imágenes
        img_divs = driver.find_elements(By.ID, 'imgTagWrapperId')
        for div in img_divs:
            img = div.find_element(By.TAG_NAME, 'img')
            if img:
                print("Imagen src:", img.get_attribute('src'))
        
        spans = driver.find_elements(By.CLASS_NAME, 'a-price-whole')
        if spans:
            print("Precio actual:", spans[0].text)
        else:
            print("No se encontraron elementos con la clase 'a-price-whole'.")
        
        discount_elements = driver.find_elements(By.XPATH, '//span[@aria-hidden="true" and contains(@class, "a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage")]')
        if discount_elements:
            print("Descuento:", discount_elements[0].text)
        else:
            print("No se encontraron elementos con las clases de descuento especificadas.")
        
        original_price_elements = driver.find_elements(By.XPATH, '//span[@aria-hidden="true" and (contains(text(), "Precio anterior:") or contains(text(), "Precio de lista:")) and not(contains(text(), "mililitro"))]')
        if original_price_elements:
            for element in original_price_elements:
                text = element.text.strip()
                if "Precio de lista:" in text or "Precio anterior:" in text:
                    print("Precio encontrado:", text)
        else:
            print("No se encontraron elementos con los textos especificados.")
        
        installment_elements = driver.find_elements(By.ID, 'installmentCalculator_feature_div')
        if installment_elements:
            for element in installment_elements:
                if "intereses" in element.text.lower():
                    filtered_text = element.text.replace("Ver 2 planes de pago", "").strip()
                    print("Meses:", filtered_text)
        else:
            print("No se encontraron elementos con el id 'installmentCalculator_feature_div'.")
    else:
        print("Error al acceder a la página:", response.status_code)
    
    # Esperar 15 segundos antes de la siguiente iteración
    time.sleep(15)

# Cerrar el driver después de procesar todas las URLs
driver.quit()







