import json
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import os
import random
import pickle  # Asegúrate de importar el módulo pickle
from datetime import datetime
import pandas as pd

# Configuración del Bot de Telegram
TELEGRAM_BOT_TOKEN = '7227911386:AAF-OyBnbcRfSrd7XMmk1Qq2-YZGXXRIbME'  # Reemplaza con tu token de bot
TELEGRAM_CHAT_ID = '-1002302040412'  # Reemplaza con el ID de tu grupo

# Cargar el archivo JSON con las URLs
with open('enlacesAfiliadoAmz.json', 'r') as file:
    urls = json.load(file)

# Configurar opciones del driver de Selenium
options = webdriver.ChromeOptions()
# Variar el User-Agent
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
]
# Elegir un User-Agent aleatorio
selected_user_agent = random.choice(user_agents)

options.add_argument(f"--user-agent={selected_user_agent}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Configurar encabezados personalizados
custom_headers = {
    'User-Agent': selected_user_agent,
    'Accept-Language': 'da, en-gb, en',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
}

# Iniciar el driver de Selenium
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

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

def save_title_to_excel(title: str):
    # Obtener la fecha actual
    current_date = datetime.now().strftime("%d-%m-%Y")
    
    # Crear un diccionario con el título
    data = {
        'titulo': title
    }
    
    # Guardar en el archivo Excel con la fecha en el nombre
    try:
        # Cambiar el nombre del archivo para incluir la fecha
        excel_filename = f'titulos_enviados_{current_date}.xlsx'
        
        # Leer el archivo existente o crear uno nuevo
        if os.path.exists(excel_filename):
            df = pd.read_excel(excel_filename)
        else:
            df = pd.DataFrame(columns=['titulo'])
        
        # Verificar si el título ya está en el archivo del día anterior
        yesterday_date = (datetime.now() - pd.Timedelta(days=1)).strftime("%d-%m-%Y")
        yesterday_filename = f'titulos_enviados_{yesterday_date}.xlsx'
        if os.path.exists(yesterday_filename):
            df_yesterday = pd.read_excel(yesterday_filename)
            if title in df_yesterday['titulo'].values:
                print(f"El título '{title}' ya existe en el archivo de ayer. No se guardará.")
                return  # No guardar si ya existe en el archivo de ayer
        
        # Añadir el nuevo título al DataFrame usando pd.concat
        new_row = pd.DataFrame([data])  # Crear un DataFrame de una fila
        df = pd.concat([df, new_row], ignore_index=True)  # Concatenar el nuevo DataFrame
        
        # Guardar el DataFrame en el archivo Excel
        df.to_excel(excel_filename, index=False)
    except Exception as e:
        print(f"Error al guardar el título en Excel: {e}")

def check_title_in_excel(title: str) -> bool:
    # Obtener la fecha de ayer
    yesterday_date = (datetime.now() - pd.Timedelta(days=1)).strftime("%d-%m-%Y")
    excel_filename = f'titulos_enviados_{yesterday_date}.xlsx'
    
    # Verificar si el archivo existe y leerlo
    if os.path.exists(excel_filename):
        df = pd.read_excel(excel_filename)
        # Comprobar si el título ya está en el DataFrame
        return title in df['titulo'].values
    return False

# Cargar las cookies desde el archivo antes de hacer scraping

# Iterar sobre cada URL
for url in urls[:]:  # Usar una copia de la lista para evitar problemas al modificarla
    try:
        driver.get(url)  # Primero, accede a la URL para establecer el dominio
        driver.get(url)  # Acceder nuevamente a la URL después de cargar las cookies
        
        # Esperar 5 segundos para que la página cargue
        time.sleep(10)

        # Resolver CAPTCHA si es necesario
        try:
            captcha_image = driver.find_element(By.XPATH, "//div[@class='a-row a-text-center']//img")
            if captcha_image:
                solve_captcha(driver)
        except:
            print("No se encontró captcha, continuando con el scraping.")

        # Usar el contenido de Selenium en lugar de requests
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Verificar si se encontró el título
        title = soup.find('span', id='productTitle')
        if title:
            title_text = title.get_text(strip=True)
        else:
            # Intentar buscar el título de otra manera
            time.sleep(5)  # Esperar 5 segundos
            try:
                title_element = driver.find_element(By.CLASS_NAME, 'a-size-large.product-title-word-break')
                title_text = title_element.text
                print(f"Título del producto: {title_text}")
            except Exception as e:
                title_text = "No se encontró el título."
                print(f"Error al encontrar el título: {e}")

        # Verificar si se encontró el precio
        price_whole = driver.find_elements(By.CLASS_NAME, 'a-price-whole')
        if price_whole:
            current_price = format_price(price_whole[0].text)
        else:
            # Intentar buscar el precio de otra manera
            time.sleep(5)  # Esperar 5 segundos
            try:
                price_span = driver.find_element(By.CLASS_NAME, 'a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay')
                price_whole_elements = price_span.find_elements(By.CLASS_NAME, 'a-price-whole')
                for i, element in enumerate(price_whole_elements, 1):
                    print(f"Precio entero {i}: {element.text}")
                current_price = format_price(price_whole_elements[0].text) if price_whole_elements else None
            except Exception as e:
                current_price = None
                print(f"Error al encontrar el precio: {e}")

        # Verificar si se encontró la imagen
        img_divs = driver.find_elements(By.ID, 'imgTagWrapperId')
        if img_divs:
            img = img_divs[0].find_element(By.TAG_NAME, 'img')
            image_src = img.get_attribute('src') if img else None
        else:
            # Intentar buscar la imagen de otra manera
            time.sleep(5)  # Esperar 5 segundos
            try:
                img_wrapper = driver.find_element(By.ID, 'imgTagWrapperId')
                img_element = img_wrapper.find_element(By.TAG_NAME, 'img')
                image_src = img_element.get_attribute('src')
                print(f"URL de la imagen: {image_src}")
            except Exception as e:
                image_src = None
                print(f"Error al encontrar la imagen: {e}")
        
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
        
        # Verificar si se encontró el precio original
        if original_price != "No se encontró el precio original.":
            precio_formatted = f"De {original_price} A ${current_price}"
        else:
            # Intentar obtener el precio entero si no se encontró el precio original
            price_span = driver.find_element(By.CLASS_NAME, 'a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay')
            price_whole_elements = price_span.find_elements(By.CLASS_NAME, 'a-price-whole')
            if price_whole_elements:
                current_price = format_price(price_whole_elements[0].text)
                precio_formatted = f"Precio: ${current_price}"
            else:
                precio_formatted = "No se encontró el precio."
        
        # Construir el mensaje solo si se encontró el precio
        if current_price:
            # Seleccionar emojis aleatorios
            installment_emoji = random.choice(["🤯", "🥳", "🔥", "✨"])
            offer_emoji = random.choice(["👉", "👇"])
            
            # Elegir entre "Ver oferta" o "Aprovecha esta oferta"
            offer_text = random.choice(["Ver oferta", "Aprovecha esta oferta"])
            
            # Elegir entre "Enlace al Producto aquí" o "link"
            link_text = random.choice(["Enlace al Producto aquí", "link"])
            
            mensaje = (
                f"{sanitize_text(title_text)}\n\n"  # Doble salto de línea después del título
                f"{offer_text} {offer_emoji}: {link_text} {url}\n\n"  # Doble salto de línea después de la oferta
                f"{precio_formatted}\n\n"  # Doble salto de línea después del precio
            )
            
            # Añadir 'meses sin intereses' solo si está disponible
            if installment_text:
                mensaje += f"en {installment_text} {installment_emoji}\n\n"  # Doble salto de línea después de los meses sin intereses
            
            # Añadir el descuento al mensaje solo si está disponible
            if discount:
                mensaje += f"Descuento: {discount} {random.choice(['🔥🔥', '🔥', '🧐', '⭐', '✨'])}\n\n"  # Doble salto de línea después del descuento
            
            # Añadir el mensaje de grupos al final
            mensaje += "⚡️Únete a nuestros otros grupos: linktr.ee/GigaOfertasMx\n#OfertasAmazon #GigaOfertasMx"  # Texto agregado
            
            # Verificar si el título ya existe en el archivo de ayer antes de enviar el mensaje
            if check_title_in_excel(title_text):  # Verificar si el título ya existe en el Excel de ayer
                print(f"El título '{title_text}' ya existe en el archivo de ayer. No se enviará el mensaje a Telegram.")
            else:
                # Enviar el mensaje a Telegram
                send_telegram_message(mensaje, image_src)
                
                # Eliminar el enlace de la lista después de enviar el mensaje
                urls.remove(url)  # Eliminar el enlace de la lista
            
            # Guardar el título en el archivo Excel
            save_title_to_excel(title_text)  # Llamar a la función para guardar el título
        else:
            print(f"No se encontró el precio para el enlace: {url}")
        
        # Esperar 15 minutos antes de la siguiente iteración
        time.sleep(20)
        
        # Actualizar el archivo JSON después de eliminar el enlace
        with open('enlacesAfiliadoAmz.json', 'w') as file:
            json.dump(urls, file, indent=4)  # Guardar la lista actualizada en el archivo JSON con formato

    except Exception as e:
        print(f"Error al procesar la URL {url}: {e}")

# Cerrar el driver después de procesar todas las URLs
driver.quit()







