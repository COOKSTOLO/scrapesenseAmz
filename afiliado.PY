import json
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime, timedelta
import os
import random

def load_enlaces_from_json():
    # Obtener la fecha actual y la del día anterior
    fecha_actual = datetime.now().strftime('%d-%m-%y')
    fecha_anterior = (datetime.now() - timedelta(days=1)).strftime('%d-%m-%y')
    
    # Leer el archivo JSON del día actual
    nombre_archivo_actual = f"{fecha_actual} Noafiliados.json"
    with open(nombre_archivo_actual, 'r') as file:
        enlaces_actuales = json.load(file)
    
    # No se lee el archivo del día anterior
    enlaces_anteriores = []
    
    # Eliminar duplicados (ya no se compara con el día anterior)
    enlaces_unicos = enlaces_actuales
    
    return enlaces_unicos

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
    
    # Agregar User-Agent aleatorio
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    ]
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
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(
        service=service,
        options=options
    )

    # Cargar enlaces desde el archivo JSON
    enlaces = load_enlaces_from_json()
    enlaces_afiliados = []

    for enlace in enlaces:
        try:
            driver.get(enlace)
            time.sleep(3)  # Esperar 3 segundos antes de resolver el captcha
            solve_captcha(driver)
            time.sleep(2)  # Esperar 3 segundos después de resolver el captcha
            
            # Cargar cookies
            load_cookies(driver, 'cookies.pkl')
            
            # Intentar hacer clic en el botón de cierre si está presente
            try:
                close_button = driver.find_element(By.CSS_SELECTOR, ".a-icon.aod-close-button")
                close_button.click()
                print("Botón de cierre detectado y clickeado.")
            except Exception as e:
                print(f"No se encontró el botón de cierre: {e}")
            
            # Intentar hacer clic en el elemento con id 'amzn-ss-text-link'
            try:
                driver.find_element(By.ID, "amzn-ss-text-link").click()
                print("Hizo clic en el enlace de Amazon.")
                
                # Esperar un momento para que el contenido cargue
                time.sleep(15)
                
                # Buscar el textarea dentro del div con la clase 'amzn-ss-text-textarea-container'
                try:
                    textarea = driver.find_element(By.XPATH, "//div[@class='amzn-ss-text-textarea-container']//textarea[@id='amzn-ss-text-shortlink-textarea']")
                    enlace_afiliado = textarea.get_attribute('value')
                    enlaces_afiliados.append(enlace_afiliado)
                    print(f"Enlace afiliado encontrado: {enlace_afiliado}")
                except Exception as e:
                    print(f"Error al encontrar el enlace afiliado: {e}")
            
            except Exception as e:
                print(f"Error al hacer clic en el enlace de Amazon: {e}")
            
            time.sleep(20)  # Esperar 20 segundos entre cada página
        except Exception as e:
            print(f"Error al procesar el enlace {enlace}: {e}")

    # Guardar los enlaces afiliados en un archivo JSON
    with open('enlacesAfiliadoAmz.json', 'w') as json_file:
        json.dump(enlaces_afiliados, json_file, indent=4)

    driver.quit()

def process_enlaces():
    fecha_actual = datetime.now().strftime('%d-%m-%y')
    nombre_archivo_noafiliados = f"{fecha_actual} Noafiliados.json"
    
    try:
        # Procesar los enlaces y generar enlacesafiliadosamz.json
        enlaces = load_enlaces_from_json()
        enlaces_afiliados = []
        
        for enlace in enlaces:
            # ... proceso existente de enlaces ...
            enlace_afiliado = convert_to_affiliate(enlace)
            enlaces_afiliados.append(enlace_afiliado)
        
        # Guardar enlaces afiliados
        with open(f"{fecha_actual} enlacesafiliadosamz.json", 'w') as f:
            json.dump(enlaces_afiliados, f, indent=4)
        
        # Una vez terminado todo el proceso, eliminar el archivo Noafiliados.json
        if os.path.exists(nombre_archivo_noafiliados):
            os.remove(nombre_archivo_noafiliados)
            print(f"Archivo {nombre_archivo_noafiliados} eliminado exitosamente.")
            
    except Exception as e:
        print(f"Error durante el proceso: {e}")

if __name__ == "__main__":
    main()