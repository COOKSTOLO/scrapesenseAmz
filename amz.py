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
from datetime import datetime
import os

def process_url(driver, url):
    driver.get(url)
    time.sleep(5)
    action = ActionChains(driver)
    action.move_by_offset(100, 100).perform()
    
    try:
        language_menu = driver.find_element(By.CLASS_NAME, "languageMenuText")
        language_menu.click()
        
        time.sleep(2)
        language_option = driver.find_element(By.XPATH, "//span[@rel='domain' and @setting='11']")
        language_option.click()
        time.sleep(2)
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        links = soup.find_all('a', href=True)
        count = 0
        for link in links:
            if 'https://dyn.keepa' in link['href']:
                print(link['href'])
                count += 1
                if count == 5:
                    break
        
        external_amazon_elements = soup.find_all('span', class_='externalAmazon')
        enlaces = []
        count = 0
        for element in external_amazon_elements:
            href = element.get('href')
            if href:
                enlaces.append(href)
                count += 1
                if count == 5:
                    break
        
        return enlaces
    except Exception as e:
        print(f"Error al hacer clic en el elemento: {e}")
        return []

def buscar_links_mercadolibre():
    url_descuentos_amz = "https://www.descuento.com.mx/buscar?keyword=amazon"
    try:
        respuesta_descuentos = requests.get(url_descuentos_amz)
        respuesta_descuentos.raise_for_status()
        soup_descuentos = BeautifulSoup(respuesta_descuentos.text, 'html.parser')
        elementos_descuentos = soup_descuentos.find_all('a', class_='badge badge-info price', href=True)
        links_amz_descuentos = [elemento['href'] for elemento in elementos_descuentos][:5]
        
        if links_amz_descuentos:
            print("Enlaces de amazon encontrados en la página de descuentos:")
        else:
            print("No se encontraron enlaces de amazon en la página de descuentos.")
        
        # Load existing links from JSON
        with open('enlaces_amz_noafilidos.json', 'r') as file:
            existing_links = json.load(file)
        
        # Append new links
        all_links = existing_links + links_amz_descuentos
        
        # Save updated links back to JSON
        with open('enlaces_amz_noafilidos.json', 'w') as file:
            json.dump(all_links, file, indent=4)
    
    except requests.RequestException as e:
        print(f"Error al obtener los enlaces de descuentos: {e}")

options = Options()
options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

urls = [
    'https://keepa.com/#!deals/%7B"page"%3A0%2C"domainId"%3A"11"%2C"excludeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"includeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B599382031%5D%2C%5B%5D%2C%5B9482640011%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"priceTypes"%3A%5B0%5D%2C"deltaRange"%3A%5B0%2C2147483647%5D%2C"deltaPercentRange"%3A%5B20%2C80%5D%2C"salesRankRange"%3A%5B-1%2C-1%5D%2C"currentRange"%3A%5B10000%2C3100000%5D%2C"minRating"%3A-1%2C"isLowest"%3Afalse%2C"isLowest90"%3Afalse%2C"isLowestOffer"%3Afalse%2C"isOutOfStock"%3Afalse%2C"titleSearch"%3A""%2C"isRangeEnabled"%3Atrue%2C"isFilterEnabled"%3Afalse%2C"filterErotic"%3Atrue%2C"singleVariation"%3Atrue%2C"hasReviews"%3Afalse%2C"isPrimeExclusive"%3Afalse%2C"mustHaveAmazonOffer"%3Afalse%2C"mustNotHaveAmazonOffer"%3Afalse%2C"sortType"%3A4%2C"dateRange"%3A"0"%2C"warehouseConditions"%3A%5B1%2C2%2C3%2C4%2C5%5D%2C"settings"%3A%7B"viewTyp"%3A0%7D%2C"perPage"%3A150%7D',
    'https://keepa.com/#!deals/%7B"page"%3A0%2C"domainId"%3A"11"%2C"excludeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"includeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B599382031%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"priceTypes"%3A%5B0%5D%2C"deltaRange"%3A%5B0%2C2147483647%5D%2C"deltaPercentRange"%3A%5B20%2C80%5D%2C"salesRankRange"%3A%5B-1%2C-1%5D%2C"currentRange"%3A%5B10000%2C3100000%5D%2C"minRating"%3A-1%2C"isLowest"%3Afalse%2C"isLowest90"%3Afalse%2C"isLowestOffer"%3Afalse%2C"isOutOfStock"%3Afalse%2C"titleSearch"%3A""%2C"isRangeEnabled"%3Atrue%2C"isFilterEnabled"%3Afalse%2C"filterErotic"%3Atrue%2C"singleVariation"%3Atrue%2C"hasReviews"%3Afalse%2C"isPrimeExclusive"%3Afalse%2C"mustHaveAmazonOffer"%3Afalse%2C"mustNotHaveAmazonOffer"%3Afalse%2C"sortType"%3A3%2C"dateRange"%3A"0"%2C"warehouseConditions"%3A%5B1%2C2%2C3%2C4%2C5%5D%2C"settings"%3A%7B"viewTyp"%3A0%7D%2C"perPage"%3A150%7D',
    'https://keepa.com/?&#!deals/%7B"page"%3A0%2C"domainId"%3A"11"%2C"excludeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"includeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B9482640011%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"priceTypes"%3A%5B0%5D%2C"deltaRange"%3A%5B0%2C2147483647%5D%2C"deltaPercentRange"%3A%5B10%2C80%5D%2C"salesRankRange"%3A%5B-1%2C-1%5D%2C"currentRange"%3A%5B15500%2C2147483647%5D%2C"minRating"%3A-1%2C"isLowest"%3Afalse%2C"isLowest90"%3Afalse%2C"isLowestOffer"%3Afalse%2C"isOutOfStock"%3Afalse%2C"titleSearch"%3A""%2C"isRangeEnabled"%3Atrue%2C"isFilterEnabled"%3Afalse%2C"filterErotic"%3Atrue%2C"singleVariation"%3Atrue%2C"hasReviews"%3Afalse%2C"isPrimeExclusive"%3Afalse%2C"mustHaveAmazonOffer"%3Afalse%2C"mustNotHaveAmazonOffer"%3Afalse%2C"sortType"%3A3%2C"dateRange"%3A"4"%2C"warehouseConditions"%3A%5B1%2C2%2C3%2C4%2C5%5D%2C"settings"%3A%7B"viewTyp"%3A0%7D%2C"perPage"%3A150%7D',
    'https://keepa.com/?&#!deals/%7B"page"%3A0%2C"domainId"%3A"11"%2C"excludeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"includeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B11260452011%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"priceTypes"%3A%5B0%5D%2C"deltaRange"%3A%5B0%2C2147483647%5D%2C"deltaPercentRange"%3A%5B10%2C80%5D%2C"salesRankRange"%3A%5B-1%2C-1%5D%2C"currentRange"%3A%5B15500%2C2147483647%5D%2C"minRating"%3A-1%2C"isLowest"%3Afalse%2C"isLowest90"%3Afalse%2C"isLowestOffer"%3Afalse%2C"isOutOfStock"%3Afalse%2C"titleSearch"%3A""%2C"isRangeEnabled"%3Atrue%2C"isFilterEnabled"%3Afalse%2C"filterErotic"%3Atrue%2C"singleVariation"%3Atrue%2C"hasReviews"%3Afalse%2C"isPrimeExclusive"%3Afalse%2C"mustHaveAmazonOffer"%3Afalse%2C"mustNotHaveAmazonOffer"%3Afalse%2C"sortType"%3A3%2C"dateRange"%3A"0"%2C"warehouseConditions"%3A%5B1%2C2%2C3%2C4%2C5%5D%2C"settings"%3A%7B"viewTyp"%3A0%7D%2C"perPage"%3A150%7D',
    'https://keepa.com/?&#!deals/%7B"page"%3A0%2C"domainId"%3A"11"%2C"excludeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"includeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B9482558011%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"priceTypes"%3A%5B18%5D%2C"deltaRange"%3A%5B0%2C2147483647%5D%2C"deltaPercentRange"%3A%5B10%2C80%5D%2C"salesRankRange"%3A%5B-1%2C-1%5D%2C"currentRange"%3A%5B15500%2C2147483647%5D%2C"minRating"%3A-1%2C"isLowest"%3Afalse%2C"isLowest90"%3Afalse%2C"isLowestOffer"%3Afalse%2C"isOutOfStock"%3Afalse%2C"titleSearch"%3A""%2C"isRangeEnabled"%3Atrue%2C"isFilterEnabled"%3Afalse%2C"filterErotic"%3Atrue%2C"singleVariation"%3Atrue%2C"hasReviews"%3Afalse%2C"isPrimeExclusive"%3Afalse%2C"mustHaveAmazonOffer"%3Afalse%2C"mustNotHaveAmazonOffer"%3Afalse%2C"sortType"%3A3%2C"dateRange"%3A"0"%2C"warehouseConditions"%3A%5B1%2C2%2C3%2C4%2C5%5D%2C"settings"%3A%7B"viewTyp"%3A0%7D%2C"perPage"%3A150%7D',
    'https://keepa.com/?&#!deals/%7B"page"%3A0%2C"domainId"%3A"11"%2C"excludeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"includeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B9482558011%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"priceTypes"%3A%5B0%5D%2C"deltaRange"%3A%5B0%2C2147483647%5D%2C"deltaPercentRange"%3A%5B10%2C80%5D%2C"salesRankRange"%3A%5B-1%2C-1%5D%2C"currentRange"%3A%5B15500%2C2147483647%5D%2C"minRating"%3A-1%2C"isLowest"%3Afalse%2C"isLowest90"%3Afalse%2C"isLowestOffer"%3Afalse%2C"isOutOfStock"%3Afalse%2C"titleSearch"%3A""%2C"isRangeEnabled"%3Atrue%2C"isFilterEnabled"%3Afalse%2C"filterErotic"%3Atrue%2C"singleVariation"%3Atrue%2C"hasReviews"%3Afalse%2C"isPrimeExclusive"%3Afalse%2C"mustHaveAmazonOffer"%3Afalse%2C"mustNotHaveAmazonOffer"%3Afalse%2C"sortType"%3A3%2C"dateRange"%3A"0"%2C"warehouseConditions"%3A%5B1%2C2%2C3%2C4%2C5%5D%2C"settings"%3A%7B"viewTyp"%3A0%7D%2C"perPage"%3A150%7D',
]

# Process Keepa URLs
all_enlaces = []

for url in urls:
    enlaces = process_url(driver, url)
    all_enlaces.extend(enlaces)

# Eliminar duplicados convirtiendo la lista a un conjunto y luego de nuevo a una lista
all_enlaces = list(set(all_enlaces))

# Guarda todos los enlaces en un archivo JSON
with open('enlaces_amz_noafilidos.json', 'w') as json_file:
    json.dump(all_enlaces, json_file, indent=4)

# Crear un archivo Excel con los enlaces
fecha_actual = datetime.now().strftime('%d-%m-%y')
nombre_archivo = f"{fecha_actual} Noafiliados.xlsx"
df = pd.DataFrame(all_enlaces, columns=["Enlaces"])
df.to_excel(nombre_archivo, index=False)

# Eliminar el archivo JSON después de crear el Excel

# Call the function to search for MercadoLibre links
buscar_links_mercadolibre()

os.remove('enlaces_amz_noafilidos.json')

driver.quit()




