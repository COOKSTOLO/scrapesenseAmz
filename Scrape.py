from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time  # Asegúrate de importar el módulo time

url = "https://amzn.to/3C9aut3"
response = requests.get(url)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)


# Buscar todos los elementos <span> con la clase 'a-price-whole'
spans = driver.find_elements(By.CLASS_NAME, 'a-price-whole')
if spans:  # Verificar si hay elementos encontrados
    print("Precio actual:", spans[0].text)  # Imprimir solo el primer elemento
else:
    print("No se encontraron elementos con la clase 'a-price-whole'.")


if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find('span', id='productTitle')
    if title:
        print("Título:", title.get_text(strip=True))
    else:
        print("No se encontró el título del producto.")
    
    # Buscar el precio anterior
    
else:
    print("Error al acceder a la página:", response.status_code)

# Inicializar el controlador de Selenium


# Cerrar el controlador
driver.quit()





