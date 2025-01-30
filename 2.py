from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
# Configurar User-Agent y opciones para evitar detección
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f"--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

try:
    driver.get('https://amzn.to/3Cu0A5r')  # Espera estática (puedes ajustar o eliminar esto)

    # Espera explícita para asegurarte de que el contenido esté cargado
    driver.implicitly_wait(10)  # Espera hasta 10 segundos para que los elementos estén disponibles

    response = requests.get('https://amzn.to/3Cu0A5r')
    soup = BeautifulSoup(response.content, 'html.parser')

    core_price_divs = soup.find_all('div', id='corePrice_feature_div')
    for div in core_price_divs:
        price_spans = div.find_all('span', class_='a-price a-text-price a-size-medium')
        if price_spans:  # Si se encuentra al menos un span de precio
            for price_span in price_spans:
                hidden_spans = price_span.find_all('span', attrs={'aria-hidden': 'true'})
                for hidden_span in hidden_spans:
                    print(hidden_span.text)
        else:  # Si no se encuentra ningún span de precio
            hidden_spans = div.find_all('span', attrs={'aria-hidden': 'true'})
            for hidden_span in hidden_spans:
                print(hidden_span.text)

    # Buscar todos los elementos con la clase 'a-section a-spacing-micro'
    section_divs = soup.find_all('div', class_='a-section a-spacing-micro')
    for div in section_divs:
        print(f'Texto encontrado en div con clase "a-section a-spacing-micro": {div.text.strip()}')

finally:
    driver.quit()