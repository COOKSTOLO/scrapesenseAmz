import requests
from bs4 import BeautifulSoup
import json
import random
import pandas as pd
from datetime import datetime
import os
import time
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from prueba import extraer_hrefs

# URLs de las páginas
urls = [
    "https://meliprice.com.mx/computacion/descuento-mayor",
    "https://meliprice.com.mx/celulares-y-telefonia/descuento-mayor",
    "https://meliprice.com.mx/belleza-y-cuidado-personal/descuento-mayor",
    "https://meliprice.com.mx/electrodomesticos/descuento-mayor",
    "https://meliprice.com.mx/electronica-audio-y-video/descuento-mayor",
    "https://meliprice.com.mx/hogar-muebles-y-jardin/descuento-mayor",
    "https://meliprice.com.mx/consolas-y-videojuegos/descuento-mayor",
    "https://meliprice.com.mx/joyas-y-relojes/descuento-mayor",
    "https://meliprice.com.mx/deportes-y-fitness/descuento-mayor",
    "https://meliprice.com.mx/accesorios-para-vehiculos/descuento-mayor",
]

def obtener_enlaces(url, limite=13, categoria=None):
    try:
        response = requests.get(url)
        response.raise_for_status()
        hrefs = []
        soup = BeautifulSoup(response.content, "html.parser")
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if href.startswith("https://meliprice.com.mx/precio/historico"):
                hrefs.append(href)
                if categoria == "belleza" and len(hrefs) >= 2:
                    break
                if categoria == "vehiculos" and len(hrefs) >= 2:
                    break
                if categoria == "joyas" and len(hrefs) >= 3:
                    break
                if len(hrefs) >= limite:
                    break
        return hrefs
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a {url}. Detalles: {e}")
        return []

# Procesar URLs y obtener enlaces
enlaces = []
for url in urls:
    print(f"Procesando URL: {url}")
    if "belleza-y-cuidado-personal" in url:
        enlaces_categoria = obtener_enlaces(url, categoria="belleza")
    elif "joyas-y-relojes" in url:
        enlaces_categoria = obtener_enlaces(url, categoria="joyas")
    elif "accesorios-para-vehiculos" in url:
        enlaces_categoria = obtener_enlaces(url, categoria="vehiculos")
    elif "deportes-y-fitness" in url:
        enlaces_categoria = obtener_enlaces(url, limite=2)
    elif "hogar-muebles-y-jardin" in url:
        enlaces_categoria = obtener_enlaces(url, limite=11)
    else:
        enlaces_categoria = obtener_enlaces(url)
    enlaces.extend(enlaces_categoria)
    print(f"Se agregaron {len(enlaces_categoria)} enlaces.")

# Obtener enlaces de descuentos.com.mx
url_descuentos = "https://www.descuento.com.mx/buscar?keyword=mercadolibre"
try:
    respuesta_descuentos = requests.get(url_descuentos)
    respuesta_descuentos.raise_for_status()
    soup_descuentos = BeautifulSoup(respuesta_descuentos.text, 'html.parser')
    elementos_descuentos = soup_descuentos.find_all('a', class_='badge badge-info price', href=True)
    links_mercadolibre_descuentos = [elemento['href'] for elemento in elementos_descuentos[:15]]
    enlaces.extend(links_mercadolibre_descuentos)
    print(f"Se agregaron {len(links_mercadolibre_descuentos)} enlaces en 'descuentos'.")
except Exception as e:
    print(f"Error en descuentos.com.mx: {e}")

# Mezclar enlaces y guardar en JSON
random.shuffle(enlaces)
with open("enlaces.json", "w", encoding="utf-8") as file:
    json.dump(enlaces, file, ensure_ascii=False, indent=4)

# Procesar enlaces con BeautifulSoup y Selenium
enlaces_mercadolibre = []
all_hrefs = []

# Procesar URLs de MercadoLibre
urls_ml = [
    "https://listado.mercadolibre.com.mx/_Container_iluminacion-aon_promotion*type_deal*of*the*day",
    "https://listado.mercadolibre.com.mx/_Container_hogar-2024-organizacion-y-almacenamiento",
    "https://listado.mercadolibre.com.mx/accesorios-camaras/lentes-filtros/_NoIndex_True",
    "https://www.mercadolibre.com.mx/ofertas?category=MLM438284",
    "https://listado.mercadolibre.com.mx/_Container_ao-computo-audifonos-gamer_promotion*type_deal*of*the*day",
    "https://listado.mercadolibre.com.mx/_Discount_26-100_Container_ao-computo-componentes",
    "https://www.mercadolibre.com.mx/ofertas?category=MLM1144&promotion_type=deal_of_the_day",
    "https://listado.mercadolibre.com.mx/_Container_flag-hogar-aon-home-office",
    "https://listado.mercadolibre.com.mx/joyas-relojes/_Discount_10-100",
    "https://listado.mercadolibre.com.mx/_Container_ao-toys-coleccionables",
    "https://listado.mercadolibre.com.mx/_Container_tendencias-sports",
]

for url in urls_ml: 
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.select('div.andes-card.poly-card.poly-card--grid-card.andes-card--flat.andes-card--padding-0.andes-card--animated')
        hrefs = []
        for card in cards:
            links = card.find_all('a')
            for link in links:
                hrefs.append(link.get('href'))
                if len(hrefs) >= 2:
                    break
            if len(hrefs) >= 2:
                break
        all_hrefs.extend(hrefs)
    except Exception as e:
        print(f"Error procesando {url}: {e}")

# Añadir enlaces de Promodescuentos
try:
    options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get("https://www.promodescuentos.com/")
    time.sleep(15)
    with open('PromoDescuento.pkl', 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    
    driver.get("https://www.promodescuentos.com/search/ofertas?merchant-id=142&hide_expired=true")
    wait = WebDriverWait(driver, 22)
    
    ofertas = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, 'div.threadListCard-footer a.threadListCard-mainButton')
    ))[:20]
    
    storepage_links = [oferta.get_attribute('href') for oferta in ofertas 
                      if '/visit/storepage' in oferta.get_attribute('href')]
    
    for link in storepage_links:
        try:
            driver.get(link)
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ui-ms-polycard-container'))
            )
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            product_cards = soup.find_all('div', class_='ui-ms-polycard-container')
            for card in product_cards:
                title_link = card.find('a', class_='poly-component__title')
                if title_link and title_link.has_attr('href'):
                    enlaces_mercadolibre.append(title_link['href'])
            time.sleep(random.choice([10, 7, 12]))
        except Exception as e:
            print(f"Error en {link}: {e}")
            continue

finally:
    driver.quit()
    print("Scraping de Promodescuentos completado")

# Combinar todos los enlaces
for enlace in enlaces:
    try:
        hrefs_encontrados = extraer_hrefs(enlace)
        enlaces_mercadolibre.extend(hrefs_encontrados)
    except Exception as e:
        print(f"Error procesando {enlace}: {e}")

enlaces_mercadolibre.extend(all_hrefs)
enlaces_mercadolibre.append("finish")

# Guardar en Excel
fecha_actual = datetime.now().strftime('%d-%m-%y')
nombre_archivo = f"{fecha_actual} Noafiliados.xlsx"
pd.DataFrame(enlaces_mercadolibre, columns=["Enlaces"]).to_excel(nombre_archivo, index=False)

# Limpiar archivos temporales
if os.path.exists("enlaces.json"):
    os.remove("enlaces.json")

print("Proceso completado exitosamente!")