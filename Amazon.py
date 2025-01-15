import pickle
import pyperclip
import os  # Importar el módulo os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
import requests
import json  


# Add these lines after the imports, before the rest of the code
chat_id = "5176899969"  # El ID de tu chat
token_bot = "7227911386:AAF-OyBnbcRfSrd7XMmk1Qq2-YZGXXRIbME"  # El token de tu bot de Telegram

# Leer el archivo Excel generado por el primer código
nombre_archivo_input = f"{datetime.now().strftime('%d-%m-%y')} Noafiliados.xlsx"

try:
    df = pd.read_excel(nombre_archivo_input)
    enlaces = df['Enlaces'].tolist()
    print(f"Enlaces cargados desde el archivo: {nombre_archivo_input}")
except FileNotFoundError:
    print(f"No se encontró el archivo: {nombre_archivo_input}")
    exit()

# Configuración de opciones de Chrome
options = Options()
options.add_argument("--start-maximized")

# Inicializar el controlador de Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Función para cargar cookies
def cargar_cookies(driver, archivo_cookies):
    try:
        with open(archivo_cookies, "rb") as file:
            cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
        print(f"Cookies cargadas desde: {archivo_cookies}")
        return True
    except Exception as e:
        print(f"No se pudo cargar el archivo de cookies: {archivo_cookies}. Error: {e}")
        return False

# Lista para almacenar los textos copiados
textos_copiados = []
# Nueva lista para almacenar los enlaces recopilados
enlaces_recopilados = []

# Nueva función para enviar un mensaje de texto a Telegram
def enviar_mensaje_telegram(mensaje, chat_id, token_bot):
    url = f"https://api.telegram.org/bot{token_bot}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': mensaje
    }
    respuesta = requests.post(url, data=params)
    if respuesta.status_code == 200:
        print("Mensaje enviado exitosamente al chat de Telegram.")
    else:
        print(f"Error al enviar el mensaje: {respuesta.status_code}")
# Procesar cada enlace
# Enviar mensaje indicando que se están mandando links solo una vez antes de empezar
enviar_mensaje_telegram("Mandando links...", chat_id, token_bot)  # Mensaje antes de enviar el primer link

for index, enlace in enumerate(enlaces):
    # Verificar si la última columna de la fila correspondiente contiene "finish"
    if df.iloc[index, -1] == "finish":  # Suponiendo que "finish" está en la última columna
        enviar_mensaje_telegram("Links terminados.", chat_id, token_bot)  # Mensaje de finalización
        break  # Salir del bucle si se encuentra "finish"

    driver.get(enlace)

    # Intentar cargar cookies desde el primer archivo
    cookies_cargadas = cargar_cookies(driver, "cookies.pkl")
    if not cookies_cargadas:
        # Si falla, intentar con el segundo archivo
        cargar_cookies(driver, "cookies2.pkl")

    # Refrescar para aplicar las cookies
    driver.refresh()

    try:
        # Interactuar con el primer botón
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".andes-button.generate_link_button.andes-button--medium.andes-button--loud"))
        ).click()
        print("Primer botón clickeado.")

        # Interactuar con el segundo botón
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".textfield-link:nth-child(2) .textfield-link__button"))
        ).click()
        print("Segundo botón clickeado.")

        # Leer el contenido del portapapeles
        copied_text = pyperclip.paste()
        print(f"Texto copiado del enlace {enlace}: {copied_text}")
        
        # Enviar el texto copiado al chat de Telegram
        enviar_mensaje_telegram(copied_text, chat_id, token_bot)  # Nueva función para enviar el mensaje
        
        # Agregar el texto copiado a la lista de enlaces recopilados
        enlaces_recopilados.append(copied_text)

    except Exception as e:
        print(f"Error al procesar el enlace {enlace}: {e}")


# Cerrar el navegador
driver.quit()

# Escribir enlaces_recopilados a un archivo JSON
with open('enlaces_recopilados.json', 'w', encoding='utf-8') as f:
    json.dump(enlaces_recopilados, f, ensure_ascii=False, indent=4)
print("Archivo enlaces_recopilados.json generado exitosamente.")

# Eliminar el archivo Excel del día
try:
    os.remove(nombre_archivo_input)
    print(f"Archivo {nombre_archivo_input} eliminado exitosamente.")
except Exception as e:
    print(f"No se pudo eliminar el archivo {nombre_archivo_input}: {e}")

# Imprimir la lista de enlaces recopilados
print("Enlaces recopilados:", enlaces_recopilados)


