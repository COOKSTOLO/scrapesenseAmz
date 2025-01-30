import os
import time
import random
import pickle
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

options = Options()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.promodescuentos.com/")
time.sleep(15)
with open('PromoDescuento.pkl', 'rb') as file:
    cookies = pickle.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)

driver.get("https://www.promodescuentos.com/search/ofertas?merchant-id=85")
wait = WebDriverWait(driver, 22)

ofertas = wait.until(EC.presence_of_all_elements_located(
    (By.CSS_SELECTOR, 'div.threadListCard-footer a.threadListCard-mainButton')
))[:20]

storepage_links = [oferta.get_attribute('href') for oferta in ofertas 
                  if '/visit/storepage' in oferta.get_attribute('href')]

enlaces_mercadolibre = []  # Inicializar la lista de enlaces de Mercadolibre
all_hrefs = []  # Inicializar la lista de todos los hrefs

# Iterar sobre cada URL
for oferta in ofertas:
    try:
        href = oferta.get_attribute('href')
        if '/visit/storepage' in href:
            enlaces_mercadolibre.append(href)  # Agregar el enlace directamente
    except Exception as e:
        print(f"Error al procesar la oferta: {e}")
        continue  # Continúa con el siguiente enlace

enlaces_mercadolibre.extend(all_hrefs)
enlaces_mercadolibre.append("finish")

# Guardar en Excel
fecha_actual = datetime.now().strftime('%d-%m-%y')
nombre_archivo = f"{fecha_actual} Noafiliados.xlsx"
pd.DataFrame(enlaces_mercadolibre, columns=["Enlaces"]).to_excel(nombre_archivo, index=False)

# Limpiar archivos temporales
if os.path.exists("enlaces.json"):
    os.remove("enlaces.json")

