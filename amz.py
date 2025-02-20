import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
from datetime import datetime, timedelta
import os 
import random
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def process_url(driver, url):
    driver.get(url)
    time.sleep(5)
    
    try:
        # Verificar si el elemento está visible
        language_menu = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "languageMenuText"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", language_menu)  # Desplazar hacia el elemento
        language_menu.click()
        
        time.sleep(2)
        language_option = driver.find_element(By.XPATH, "//span[@rel='domain' and @setting='11']")
        language_option.click()
        time.sleep(2)
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        links = soup.find_all('a', href=True)
        count = 0
        
        # Verificar si el URL es el específico para mascotas
        #mascotas
        if url == 'https://keepa.com/#!deals/%7B"page"%3A0%2C"domainId"%3A"11"%2C"excludeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"includeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B599382031%5D%2C%5B%5D%2C%5B9482640011%5D%2C%5B11782336011%5D%2C%5B11782336011%5D%2C%5B%5D%5D%2C"priceTypes"%3A%5B18%5D%2C"deltaRange"%3A%5B0%2C2147483647%5D%2C"deltaPercentRange"%3A%5B20%2C80%5D%2C"salesRankRange"%3A%5B-1%2C-1%5D%2C"currentRange"%3A%5B3300%2C2147483647%5D%2C"minRating"%3A40%2C"isLowest"%3Atrue%2C"isLowest90"%3Atrue%2C"isLowestOffer"%3Afalse%2C"isOutOfStock"%3Afalse%2C"titleSearch"%3A""%2C"isRangeEnabled"%3Atrue%2C"isFilterEnabled"%3Afalse%2C"filterErotic"%3Atrue%2C"singleVariation"%3Atrue%2C"hasReviews"%3Afalse%2C"isPrimeExclusive"%3Afalse%2C"mustHaveAmazonOffer"%3Afalse%2C"mustNotHaveAmazonOffer"%3Afalse%2C"sortType"%3A3%2C"dateRange"%3A"0"%2C"warehouseConditions"%3A%5B1%2C2%2C3%2C4%2C5%5D%2C"settings"%3A%7B"viewTyp"%3A0%7D%2C"perPage"%3A150%7D':
            for link in links:
                if 'https://dyn.keepa' in link['href']:
                    print(link['href'])
                    count += 1
                    if count == 2:  # Solo 2 enlaces para este caso
                        break
                    #electronicos general
        elif url == 'https://keepa.com/?&#!deals/%7B"page"%3A0%2C"domainId"%3A"11"%2C"excludeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"includeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B9482558011%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"priceTypes"%3A%5B7%5D%2C"deltaRange"%3A%5B0%2C2147483647%5D%2C"deltaPercentRange"%3A%5B10%2C80%5D%2C"salesRankRange"%3A%5B-1%2C-1%5D%2C"currentRange"%3A%5B15500%2C2147483647%5D%2C"minRating"%3A40%2C"isLowest"%3Atrue%2C"isLowest90"%3Afalse%2C"isLowestOffer"%3Afalse%2C"isOutOfStock"%3Afalse%2C"titleSearch"%3A""%2C"isRangeEnabled"%3Atrue%2C"isFilterEnabled"%3Atrue%2C"filterErotic"%3Atrue%2C"singleVariation"%3Atrue%2C"hasReviews"%3Afalse%2C"isPrimeExclusive"%3Afalse%2C"mustHaveAmazonOffer"%3Afalse%2C"mustNotHaveAmazonOffer"%3Afalse%2C"sortType"%3A3%2C"dateRange"%3A"0"%2C"warehouseConditions"%3A%5B1%2C2%2C3%2C4%2C5%5D%2C"settings"%3A%7B"viewTyp"%3A0%7D%2C"perPage"%3A150%7D':
            for link in links:
                if 'https://dyn.keepa' in link['href']:
                    print(link['href'])
                    count += 1
                    if count == 5:  # Solo 6 enlaces para este caso
                        break
                    #electronicos amz
        elif url == 'https://keepa.com/?&#!deals/%7B"page"%3A0%2C"domainId"%3A"11"%2C"excludeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"includeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B9482558011%5D%2C%5B9482558011%5D%2C%5B%5D%2C%5B%5D%5D%2C"priceTypes"%3A%5B0%5D%2C"deltaRange"%3A%5B0%2C2147483647%5D%2C"deltaPercentRange"%3A%5B10%2C80%5D%2C"salesRankRange"%3A%5B-1%2C-1%5D%2C"currentRange"%3A%5B15500%2C2147483647%5D%2C"minRating"%3A40%2C"isLowest"%3Atrue%2C"isLowest90"%3Afalse%2C"isLowestOffer"%3Afalse%2C"isOutOfStock"%3Afalse%2C"titleSearch"%3A""%2C"isRangeEnabled"%3Atrue%2C"isFilterEnabled"%3Atrue%2C"filterErotic"%3Atrue%2C"singleVariation"%3Atrue%2C"hasReviews"%3Afalse%2C"isPrimeExclusive"%3Afalse%2C"mustHaveAmazonOffer"%3Afalse%2C"mustNotHaveAmazonOffer"%3Afalse%2C"sortType"%3A3%2C"dateRange"%3A"0"%2C"warehouseConditions"%3A%5B1%2C2%2C3%2C4%2C5%5D%2C"settings"%3A%7B"viewTyp"%3A0%7D%2C"perPage"%3A150%7D':
            for link in links:
                if 'https://dyn.keepa' in link['href']:
                    print(link['href'])
                    count += 1
                    if count == 5:  # Solo 5 enlaces para este caso
                        break
                #luces tiras
        elif url == 'https://keepa.com/#!deals/%7B"page"%3A0%2C"domainId"%3A"11"%2C"excludeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"includeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B599382031%5D%2C%5B%5D%2C%5B9482640011%5D%2C%5B9939347011%5D%2C%5B%5D%2C%5B%5D%5D%2C"priceTypes"%3A%5B10%5D%2C"deltaRange"%3A%5B0%2C2147483647%5D%2C"deltaPercentRange"%3A%5B10%2C70%5D%2C"salesRankRange"%3A%5B-1%2C-1%5D%2C"currentRange"%3A%5B7700%2C4997700%5D%2C"minRating"%3A-1%2C"isLowest"%3Afalse%2C"isLowest90"%3Afalse%2C"isLowestOffer"%3Afalse%2C"isOutOfStock"%3Afalse%2C"titleSearch"%3A""%2C"isRangeEnabled"%3Atrue%2C"isFilterEnabled"%3Afalse%2C"filterErotic"%3Atrue%2C"singleVariation"%3Atrue%2C"hasReviews"%3Afalse%2C"isPrimeExclusive"%3Afalse%2C"mustHaveAmazonOffer"%3Afalse%2C"mustNotHaveAmazonOffer"%3Afalse%2C"sortType"%3A3%2C"dateRange"%3A"0"%2C"warehouseConditions"%3A%5B1%2C2%2C3%2C4%2C5%5D%2C"settings"%3A%7B"viewTyp"%3A0%7D%2C"perPage"%3A150%7D':
            for link in links:
                if 'https://dyn.keepa' in link['href']:
                    print(link['href'])
                    count += 1
                    if count == 2:  # Solo 2 enlaces para este caso
                        break
        # Nuevo elif para lámparas de escritorio
        elif url == 'https://keepa.com/?&#!deals/%7B"page"%3A0%2C"domainId"%3A"11"%2C"excludeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"includeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B9482558011%5D%2C%5B50603379011%5D%2C%5B50603379011%5D%2C%5B%5D%2C%5B%5D%5D%2C"priceTypes"%3A%5B18%5D%2C"deltaRange"%3A%5B0%2C2147483647%5D%2C"deltaPercentRange"%3A%5B10%2C80%5D%2C"salesRankRange"%3A%5B-1%2C-1%5D%2C"currentRange"%3A%5B15500%2C2147483647%5D%2C"minRating"%3A40%2C"isLowest"%3Atrue%2C"isLowest90"%3Afalse%2C"isLowestOffer"%3Afalse%2C"isOutOfStock"%3Afalse%2C"titleSearch"%3A""%2C"isRangeEnabled"%3Atrue%2C"isFilterEnabled"%3Atrue%2C"filterErotic"%3Atrue%2C"singleVariation"%3Atrue%2C"hasReviews"%3Afalse%2C"isPrimeExclusive"%3Afalse%2C"mustHaveAmazonOffer"%3Afalse%2C"mustNotHaveAmazonOffer"%3Afalse%2C"sortType"%3A3%2C"dateRange"%3A"0"%2C"warehouseConditions"%3A%5B1%2C2%2C3%2C4%2C5%5D%2C"settings"%3A%7B"viewTyp"%3A0%7D%2C"perPage"%3A150%7D':
            for link in links:
                if 'https://dyn.keepa' in link['href']:
                    print(link['href'])
                    count += 1
                    if count == 2:  # Solo 2 enlaces para este caso
                        break
        else:
            for link in links:
                if 'https://dyn.keepa' in link['href']:
                    print(link['href'])
                    count += 1
                    if count == 4:  # 4 enlaces para otros casos
                        break
        
        external_amazon_elements = soup.find_all('span', class_='externalAmazon')
        enlaces = []
        count = 0
        for element in external_amazon_elements:
            href = element.get('href')
            if href:
                enlaces.append(href)
                count += 1
                if count == 4:
                    break
        
        return enlaces
    except Exception as e:
        print(f"Error al hacer clic en el elemento: {e}")
        return []

def buscar_links_mercadolibre():
    fecha_actual = datetime.now().strftime('%d-%m-%y')
    nombre_archivo_json = f"{fecha_actual} Noafiliados.json"
    url_descuentos_amz = "https://www.descuento.com.mx/buscar?keyword=amazon"
    try:
        respuesta_descuentos = requests.get(url_descuentos_amz)
        respuesta_descuentos.raise_for_status()
        soup_descuentos = BeautifulSoup(respuesta_descuentos.text, 'html.parser')
        elementos_descuentos = soup_descuentos.find_all('a', class_='badge badge-info price', href=True)
        links_amz_descuentos = [elemento['href'] for elemento in elementos_descuentos][:20]
        
        # Verificar si el archivo Noafiliados.json existe, si no, crear uno vacío
        if not os.path.exists(nombre_archivo_json):
            with open(nombre_archivo_json, 'w') as file:
                json.dump([], file)  # Crear un archivo JSON vacío

        # Cargar enlaces existentes desde Noafiliados.json
        with open(nombre_archivo_json, 'r') as file:
            existing_links = json.load(file)

        # Append new links directly to Noafiliados.json
        all_links = existing_links + links_amz_descuentos

        # Save updated links back to Noafiliados.json
        with open(nombre_archivo_json, 'w') as file:
            json.dump(all_links, file, indent=4)

    except requests.RequestException as e:
        print(f"Error al obtener los enlaces de descuentos: {e}")

# Configuración inicial de Selenium para Keepa
options_keepa = Options()
options_keepa.add_argument("--start-maximized")
service_keepa = Service(ChromeDriverManager().install())
driver_keepa = webdriver.Chrome(service=service_keepa, options=options_keepa)

# Procesar URLs de Keepa
urls_keepa = [
    'https://keepa.com/#!deals/%7B"page"%3A0%2C"domainId"%3A"11"%2C"excludeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"includeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B599382031%5D%2C%5B%5D%2C%5B9482640011%5D%2C%5B17608484011%5D%2C%5B%5D%2C%5B%5D%5D%2C"priceTypes"%3A%5B1%5D%2C"deltaRange"%3A%5B0%2C2147483647%5D%2C"deltaPercentRange"%3A%5B20%2C80%5D%2C"salesRankRange"%3A%5B-1%2C-1%5D%2C"currentRange"%3A%5B3300%2C4993300%5D%2C"minRating"%3A40%2C"isLowest"%3Atrue%2C"isLowest90"%3Atrue%2C"isLowestOffer"%3Afalse%2C"isOutOfStock"%3Afalse%2C"titleSearch"%3A""%2C"isRangeEnabled"%3Atrue%2C"isFilterEnabled"%3Afalse%2C"filterErotic"%3Atrue%2C"singleVariation"%3Atrue%2C"hasReviews"%3Afalse%2C"isPrimeExclusive"%3Afalse%2C"mustHaveAmazonOffer"%3Afalse%2C"mustNotHaveAmazonOffer"%3Afalse%2C"sortType"%3A3%2C"dateRange"%3A"0"%2C"warehouseConditions"%3A%5B1%2C2%2C3%2C4%2C5%5D%2C"settings"%3A%7B"viewTyp"%3A0%7D%2C"perPage"%3A150%7D',
    'https://keepa.com/?&#!deals/%7B"page"%3A0%2C"domainId"%3A"11"%2C"excludeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"includeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B9482640011%5D%2C%5B%5D%2C%5B9482558011%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"priceTypes"%3A%5B0%5D%2C"deltaRange"%3A%5B0%2C2147483647%5D%2C"deltaPercentRange"%3A%5B10%2C80%5D%2C"salesRankRange"%3A%5B-1%2C-1%5D%2C"currentRange"%3A%5B15500%2C2147483647%5D%2C"minRating"%3A40%2C"isLowest"%3Afalse%2C"isLowest90"%3Atrue%2C"isLowestOffer"%3Afalse%2C"isOutOfStock"%3Afalse%2C"titleSearch"%3A""%2C"isRangeEnabled"%3Atrue%2C"isFilterEnabled"%3Atrue%2C"filterErotic"%3Atrue%2C"singleVariation"%3Atrue%2C"hasReviews"%3Afalse%2C"isPrimeExclusive"%3Afalse%2C"mustHaveAmazonOffer"%3Afalse%2C"mustNotHaveAmazonOffer"%3Afalse%2C"sortType"%3A3%2C"dateRange"%3A"0"%2C"warehouseConditions"%3A%5B1%2C2%2C3%2C4%2C5%5D%2C"settings"%3A%7B"viewTyp"%3A0%7D%2C"perPage"%3A150%7D',
]


# Process Keepa URLs
all_enlaces = []
for url in urls_keepa:
    enlaces = process_url(driver_keepa, url)
    all_enlaces.extend(enlaces)

all_enlaces = list(set(all_enlaces))

# Obtener enlaces de descuentos.com.mx
buscar_links_mercadolibre()

driver_keepa.quit()  # Cerrar el driver de Keepa

# Configuración para PromoDescuentos
options_promo = Options()
service_promo = Service(ChromeDriverManager().install())
driver_promo = webdriver.Chrome(service=service_promo, options=options_promo)

driver_promo.get("https://www.promodescuentos.com/")
time.sleep(15)

# Cargar cookies para mantener la sesión
with open('PromoDescuento.pkl', 'rb') as file:
    cookies = pickle.load(file)
    for cookie in cookies:
        driver_promo.add_cookie(cookie)
# Navegar a ofertas de Amazon en PromoDescuentos
driver_promo.get("https://www.promodescuentos.com/search/ofertas?merchant-id=85")
wait = WebDriverWait(driver_promo, 22)
ofertas = wait.until(EC.presence_of_all_elements_located(
    (By.CSS_SELECTOR, 'div.threadListCard-footer a.threadListCard-mainButton')
))[:20]

# Extraer enlaces relevantes
enlaces_promodescuentos = [
    oferta.get_attribute('href') 
    for oferta in ofertas 
    if '/visit/storepage' in oferta.get_attribute('href')
]

driver_promo.quit()

# Combinar todos los enlaces y eliminar duplicados
all_enlaces.extend(enlaces_promodescuentos)
all_enlaces = list(set(all_enlaces))

# Generar archivo JSON final
fecha_actual = datetime.now().strftime('%d-%m-%y')
nombre_archivo_json = f"{fecha_actual} Noafiliados.json"
with open(nombre_archivo_json, 'w') as file:
    json.dump(all_enlaces, file, indent=4)

# Cargar títulos del día anterior
fecha_anterior = (datetime.now() - timedelta(days=1)).strftime('%d-%m-%y')
nombre_archivo_titulos_anterior = f"{fecha_anterior} titulos.json"

# Guardar enlaces actualizados en noafiliados.json
with open(nombre_archivo_json, 'w') as file:
    json.dump(all_enlaces, file, indent=4)






