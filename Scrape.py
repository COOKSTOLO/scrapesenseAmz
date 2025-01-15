from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time  # Asegúrate de importar el módulo time
import re  # Asegúrate de importar el módulo re

url = "https://amzn.to/4jwsDC7"
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
    
    # Buscar todos los elementos <span> con el atributo aria-hidden="true" y las clases especificadas usando Selenium
    discount_elements = driver.find_elements(By.XPATH, '//span[@aria-hidden="true" and contains(@class, "a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage")]')
    if discount_elements:  # Verificar si hay elementos encontrados
        print("Descuento:", discount_elements[0].text)  # Imprimir solo el primer descuento encontrado
    else:
        print("No se encontraron elementos con las clases de descuento especificadas.")
    
    # Buscar el precio original usando Selenium
    original_price_elements = driver.find_elements(By.XPATH, '//span[@aria-hidden="true" and contains(text(), "$")]')
    if original_price_elements:  # Verificar si hay elementos encontrados
        print("Precio original:", original_price_elements[0].text)  # Imprimir solo el primer precio original encontrado
    else:
        print("No se encontraron elementos con el precio original especificado.")
    
    # Buscar todos los elementos <div> con el id 'installmentCalculator_feature_div'
    installment_elements = driver.find_elements(By.ID, 'installmentCalculator_feature_div')
    if installment_elements:  # Verificar si hay elementos encontrados
        for element in installment_elements:
            if "intereses" in element.text.lower():  # Verificar si el texto contiene la palabra "intereses"
                # Excluir la parte "Ver 2 planes de pago"
                filtered_text = element.text.replace("Ver 2 planes de pago", "").strip()
                print("Meses:", filtered_text)  # Imprimir el texto filtrado
    else:
        print("No se encontraron elementos con el id 'installmentCalculator_feature_div'.")
    
    
else:
    print("Error al acceder a la página:", response.status_code)


driver.quit()







