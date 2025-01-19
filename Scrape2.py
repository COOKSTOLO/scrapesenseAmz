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
import os
import random

# Configuración del Bot de Telegram
TELEGRAM_BOT_TOKEN = '7227911386:AAF-OyBnbcRfSrd7XMmk1Qq2-YZGXXRIbME'  # Reemplaza con tu token de bot
TELEGRAM_CHAT_ID = '-1002302040412'  # Reemplaza con el ID de tu grupo

# Cargar el archivo JSON con las URLs
with open('enlacesAfiliadoAmz.json', 'r') as file:
    urls = json.load(file)

# Configurar el driver de Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Ejecutar en modo headless
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def send_telegram_message(message: str, photo_url: str = None):
    try:
        if photo_url:
            # Descargar la imagen
            response = requests.get(photo_url)
            if response.status_code == 200:
                files = {'photo': response.content}
                data = {
                    'chat_id': TELEGRAM_CHAT_ID,
                    'caption': message,
                    'parse_mode': 'HTML'  # Usar HTML para el formateo
                }
                send_photo_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
                response = requests.post(send_photo_url, data=data, files=files)
                if response.status_code != 200:
                    print(f"Error al enviar la foto: {response.text}")
            else:
                # Si no se pudo descargar la imagen, enviar solo el mensaje
                send_message_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                data = {
                    'chat_id': TELEGRAM_CHAT_ID,
                    'text': message,
                    'parse_mode': 'HTML'  # Usar HTML para el formateo
                }
                response = requests.post(send_message_url, data=data)
                if response.status_code != 200:
                    print(f"Error al enviar el mensaje: {response.text}")
        else:
            # Enviar solo el mensaje
            send_message_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message,
                'parse_mode': 'HTML'  # Usar HTML para el formateo
            }
            response = requests.post(send_message_url, data=data)
            if response.status_code != 200:
                print(f"Error al enviar el mensaje: {response.text}")
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")

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

def format_price(price: str) -> str:
    # Eliminar los decimales del precio
    return re.sub(r'\.\d{2}', '', price)

def sanitize_text(text: str) -> str:
    return text.encode('utf-8', 'ignore').decode('utf-8')

# Iterar sobre cada URL
for url in urls:
    try:
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
                title_text = title.get_text(strip=True)
            else:
                title_text = "No se encontró el título del producto."
            
            # Buscar todos los div con id 'imgTagWrapperId' y obtener los src de las imágenes
            img_divs = driver.find_elements(By.ID, 'imgTagWrapperId')
            image_src = None
            for div in img_divs:
                img = div.find_element(By.TAG_NAME, 'img')
                if img:
                    image_src = img.get_attribute('src')
                    break  # Tomar la primera imagen encontrada
            
            spans = driver.find_elements(By.CLASS_NAME, 'a-price-whole')
            if spans:
                current_price = format_price(spans[0].text)
            else:
                current_price = None  # Cambiado para indicar que no se encontró el precio
            
            discount_elements = driver.find_elements(By.XPATH, '//span[@aria-hidden="true" and contains(@class, "a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage")]')
            if discount_elements:
                discount = discount_elements[0].text
            else:
                discount = None  # Cambiado para indicar que no se encontró el descuento
            
            original_price_elements = driver.find_elements(
                By.XPATH,
                '//span[@aria-hidden="true" and (contains(text(), "Precio anterior:") or contains(text(), "Precio de lista:")) and not(contains(text(), "mililitro"))]'
            )
            if original_price_elements:
                # Extraer solo el valor numérico del precio original
                original_price_text = original_price_elements[0].text.strip()
                # Usar expresión regular para eliminar "Precio anterior:" o "Precio de lista:"
                match = re.search(r'\$[\d,.]+', original_price_text)
                if match:
                    original_price = format_price(match.group())
                else:
                    original_price = "No se encontró el precio original."
            else:
                original_price = "No se encontró el precio original."
            
            installment_elements = driver.find_elements(By.ID, 'installmentCalculator_feature_div')
            if installment_elements:
                installment_text = installment_elements[0].text.strip()
                # Verificar si realmente contiene información de meses sin intereses
                if "meses sin intereses" not in installment_text.lower():
                    installment_text = None
                else:
                    # Eliminar la parte "Ver 2 planes de pago" utilizando expresión regular
                    # Suponiendo que la frase siempre está separada por un punto
                    installment_text = re.sub(r'\.\s*Ver\s*\d+\s*planes de pago', '', installment_text)
            else:
                installment_text = None
            
            # Formatear el precio
            if original_price != "No se encontró el precio original.":
                precio_formatted = f"De {original_price} A ${current_price}"
            else:
                precio_formatted = f"Precio: ${current_price}"
            
            # Construir el mensaje solo si se encontró el precio y el descuento
            if current_price and discount:
                # Seleccionar emojis aleatorios
                installment_emoji = random.choice(["🤯", "🥳", "🔥", "✨"])
                discount_emoji = random.choice(["🔥🔥", "🔥", "🧐", "⭐", "✨"])
                offer_emoji = random.choice(["👉", "👇"])
                
                # Elegir entre "Ver oferta" o "Aprovecha esta oferta"
                offer_text = random.choice(["Ver oferta", "Aprovecha esta oferta"])
                
                # Elegir entre "Enlace al Producto aquí" o "link"
                link_text = random.choice(["Enlace al Producto aquí", "link"])
                
                mensaje = (
                    f"{sanitize_text(title_text)}\n\n"  # Agregar espacio entre el título y el enlace
                    f"{offer_text} {offer_emoji}: {link_text} {url}\n\n"
                    f"{precio_formatted}\n\n"
                    f"Descuento: {discount} {discount_emoji}"
                )
                
                # Añadir 'meses sin intereses' solo si está disponible
                if installment_text:
                    mensaje += f"\n\nen {installment_text} {installment_emoji}"
                
                # Enviar el mensaje a Telegram
                send_telegram_message(mensaje, image_src)
            else:
                print(f"No se encontró el precio o el descuento para el enlace: {url}")
        
        else:
            print(f"Error al acceder a la página: {response.status_code}")
        
        # Esperar 15 segundos antes de la siguiente iteración
        time.sleep(45)
    
    except Exception as e:
        print(f"Error al procesar la URL {url}: {e}")

# Cerrar el driver después de procesar todas las URLs
driver.quit()







