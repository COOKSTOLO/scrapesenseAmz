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
import pickle  # Para guardar/cargar cookies si lo requieres
from datetime import datetime
import pandas as pd
import logging 

# ------------------------ Telethon (como usuario real) ------------------------
from telethon.sync import TelegramClient
from io import BytesIO

import logging

logging.getLogger("telethon").setLevel(logging.CRITICAL)


# Credenciales de Telethon (debes obtenerlas en https://my.telegram.org)
api_id = 25673948  # Debe ser un número (entero)
api_hash = '783586f391e313a21333e749ec85b931'
phone = '+529932516506'  # Tu número de teléfono con código de país

# Nombre de usuario del grupo (puedes usar el username o el link)
TELEGRAM_GROUP = 'OfertonazosMx'  # Este es el nombre del grupo según el link: https://t.me/OfertonazosMx

# Iniciar el cliente de Telethon (se creará un archivo de sesión 'session_name.session')
client = TelegramClient('session_name', api_id, api_hash)
client.start(phone=phone)
print("Cliente de Telethon iniciado con éxito.")

# --------------------- Configuración de Selenium ---------------------
# Cargar el archivo JSON con las URLs
with open('enlacesAfiliadoAmz.json', 'r') as file:
    urls = json.load(file)

# Configurar opciones del driver de Selenium
options = webdriver.ChromeOptions()

# Lista de User Agents de escritorio
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/120.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19042',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Brave/120.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Vivaldi/6.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/22.1.0 Yowser/2.5 Safari/537.36',
]

# Elegir un User-Agent aleatorio
selected_user_agent = random.choice(user_agents)

# Configurar el User-Agent en las opciones de Chrome
options.add_argument(f"--user-agent={selected_user_agent}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# (Opcional) Si necesitas definir headers personalizados para requests, puedes usarlos cuando hagas solicitudes HTTP.
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

# ------------------------- Funciones -------------------------
def send_telegram_message(message: str, photo_url: str = None):
    """
    Envía un mensaje (y opcionalmente una imagen) al chat/grupo de Telegram usando Telethon.
    """
    try:
        if photo_url:
            response = requests.get(photo_url)
            if response.status_code == 200:
                # Usar BytesIO para enviar la imagen sin necesidad de guardarla en disco
                from io import BytesIO
                photo_file = BytesIO(response.content)
                photo_file.name = 'image.jpg'
                client.send_file(TELEGRAM_GROUP, photo_file, caption=message, parse_mode='html')
            else:
                # Si no se pudo descargar la imagen, enviar solo el mensaje
                client.send_message(TELEGRAM_GROUP, message, parse_mode='html')
        else:
            client.send_message(TELEGRAM_GROUP, message, parse_mode='html')
        print("Mensaje enviado a Telegram correctamente.")
    except Exception as e:
        print(f"Error al enviar mensaje vía Telethon: {e}")

def solve_captcha(driver):
    try:
        # Se asume que cuentas con una clase o método AmazonCaptcha para resolver el captcha.
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
        new_row = pd.DataFrame([data])
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Guardar el DataFrame en el archivo Excel
        df.to_excel(excel_filename, index=False)
    except Exception as e:
        print(f"Error al guardar el título en Excel: {e}")

def check_title_in_excel(title: str) -> bool:
    # Obtener la fecha de ayer
    yesterday_date = (datetime.now() - pd.Timedelta(days=1)).strftime("%d-%m-%Y")
    excel_filename = f'titulos_enviados_{yesterday_date}.xlsx'
    
    if os.path.exists(excel_filename):
        df = pd.read_excel(excel_filename)
        return title in df['titulo'].values
    return False

# ------------------------- Bucle principal -------------------------
for url in urls[:]:  # Usamos una copia de la lista para evitar problemas al modificarla
    try:
        # Acceder a la URL (dos veces para asegurarnos de establecer cookies si las hubiese)
        driver.get(url)
        driver.get(url)
        
        # Esperar a que la página cargue
        time.sleep(10)

        # Resolver CAPTCHA si es necesario
        try:
            captcha_image = driver.find_element(By.XPATH, "//div[@class='a-row a-text-center']//img")
            if captcha_image:
                solve_captcha(driver)
        except Exception as e:
            print("No se encontró captcha, continuando con el scraping.")

        # Usar el contenido de Selenium para el scraping
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Extraer el título del producto
        title = soup.find('span', id='productTitle')
        if title:
            title_text = title.get_text(strip=True)
        else:
            # Intentar obtenerlo de otra forma
            time.sleep(5)
            try:
                title_element = driver.find_element(By.CLASS_NAME, 'a-size-large.product-title-word-break')
                title_text = title_element.text
                print(f"Título del producto: {title_text}")
            except Exception as e:
                title_text = "No se encontró el título."
                print(f"Error al encontrar el título: {e}")

        # Extraer el precio
        price_whole = driver.find_elements(By.CLASS_NAME, 'a-price-whole')
        if price_whole:
            current_price = format_price(price_whole[0].text)
        else:
            time.sleep(5)
            try:
                price_span = driver.find_element(By.CLASS_NAME, 'a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay')
                price_whole_elements = price_span.find_elements(By.CLASS_NAME, 'a-price-whole')
                for i, element in enumerate(price_whole_elements, 1):
                    print(f"Precio entero {i}: {element.text}")
                current_price = format_price(price_whole_elements[0].text) if price_whole_elements else None
            except Exception as e:
                current_price = None
                print(f"Error al encontrar el precio: {e}")

        # Extraer la imagen
        img_divs = driver.find_elements(By.ID, 'imgTagWrapperId')
        if img_divs:
            img = img_divs[0].find_element(By.TAG_NAME, 'img')
            image_src = img.get_attribute('src') if img else None
        else:
            time.sleep(5)
            try:
                img_wrapper = driver.find_element(By.ID, 'imgTagWrapperId')
                img_element = img_wrapper.find_element(By.TAG_NAME, 'img')
                image_src = img_element.get_attribute('src')
                print(f"URL de la imagen: {image_src}")
            except Exception as e:
                image_src = None
                print(f"Error al encontrar la imagen: {e}")
        
        # Extraer el descuento (si existe)
        discount_elements = driver.find_elements(
            By.XPATH,
            '//span[@aria-hidden="true" and contains(@class, "a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage")]'
        )
        discount = discount_elements[0].text if discount_elements else None
        
        # Extraer el precio original (si existe)
        original_price_elements = driver.find_elements(
            By.XPATH,
            '//span[@aria-hidden="true" and (contains(text(), "Precio anterior:") or contains(text(), "Precio de lista:")) and not(contains(text(), "mililitro"))]'
        )
        if original_price_elements:
            original_price_text = original_price_elements[0].text.strip()
            match = re.search(r'\$[\d,.]+', original_price_text)
            if match:
                original_price = format_price(match.group())
            else:
                original_price = "No se encontró el precio original."
        else:
            original_price = "No se encontró el precio original."
        
        # Extraer información de meses sin intereses (si existe)
        installment_elements = driver.find_elements(By.ID, 'installmentCalculator_feature_div')
        if installment_elements:
            installment_text = installment_elements[0].text.strip()
            if "meses sin intereses" not in installment_text.lower():
                installment_text = None
            else:
                installment_text = re.sub(r'\.\s*Ver\s*\d+\s*planes de pago', '', installment_text)
        else:
            installment_text = None
        
        # Formatear el precio para el mensaje
        if original_price != "No se encontró el precio original.":
            precio_formatted = f"De {original_price} A ${current_price}"
        else:
            try:
                price_span = driver.find_element(By.CLASS_NAME, 'a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay')
                price_whole_elements = price_span.find_elements(By.CLASS_NAME, 'a-price-whole')
                if price_whole_elements:
                    current_price = format_price(price_whole_elements[0].text)
                    precio_formatted = f"Precio: ${current_price}"
                else:
                    current_price = None  # Si no hay precio, establecer current_price como None
            except Exception as e:
                current_price = None  # Si hay error, establecer current_price como None
                print(f"Error al obtener el precio: {e}")
        
        # Si se encontró precio, construir y enviar el mensaje
        if current_price and current_price != "No se encontró el precio.":
            # Seleccionar emojis y textos aleatorios
            installment_emoji = random.choice(["🤯", "🥳", "🔥", "✨"])
            offer_emoji = random.choice(["👉", "👇"])
            offer_text = random.choice(["Ver oferta", "Aprovecha esta oferta"])
            link_text = random.choice(["Enlace al Producto aquí", "link"])
            
            mensaje = (
                f"{sanitize_text(title_text)}\n\n"
                f"{offer_text} {offer_emoji}: {link_text} {url}\n\n"
                f"{precio_formatted}\n\n"
            )
            
            if installment_text:
                mensaje += f"en {installment_text} {installment_emoji}\n\n"
            
            if discount:
                mensaje += f"Descuento: {discount} {random.choice(['🔥🔥', '🔥', '🧐', '⭐', '✨'])}\n\n"
            
            mensaje += "⚡️Únete a nuestros otros grupos: linktr.ee/GigaOfertasMx\n#OfertasAmazon #GigaOfertasMx"
            
            # Verificar si el título ya existe en el Excel de ayer
            if check_title_in_excel(title_text):
                print(f"El título '{title_text}' ya existe en el archivo de ayer. No se enviará el mensaje a Telegram.")
            else:
                send_telegram_message(mensaje, image_src)
                # Eliminar el enlace de la lista después de enviarlo
                urls.remove(url)
            
            # Guardar el título en el Excel
            save_title_to_excel(title_text)
        else:
            print(f"No se encontró el precio para el enlace: {url}")
            # No se envía el mensaje a Telegram si no se encuentra el precio
            urls.remove(url)  # También removemos la URL si no se encuentra el precio
        
        # Esperar 15 minutos (450 segundos) antes de la siguiente iteración
        time.sleep(1300)
        
        # Actualizar el archivo JSON (guardamos la lista actualizada)
        with open('enlacesAfiliadoAmz.json', 'w') as file:
            json.dump(urls, file, indent=4)
    
    except Exception as e:
        print(f"Error al procesar la URL {url}: {e}")

# Cerrar el driver de Selenium
driver.quit()
print("Proceso finalizado, driver cerrado.")
