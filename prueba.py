from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configura el controlador del navegador (asegúrate de tener el controlador adecuado para tu navegador)
options = Options()
options.add_argument("--start-maximized")

# Inicializar el controlador de Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Abre la página web
url = 'https://keepa.com/#!deals/%7B"page"%3A0%2C"domainId"%3A"11"%2C"excludeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"includeCategories"%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B599382031%5D%2C%5B%5D%2C%5B9482640011%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C"priceTypes"%3A%5B0%5D%2C"deltaRange"%3A%5B0%2C2147483647%5D%2C"deltaPercentRange"%3A%5B20%2C80%5D%2C"salesRankRange"%3A%5B-1%2C-1%5D%2C"currentRange"%3A%5B10000%2C3100000%5D%2C"minRating"%3A-1%2C"isLowest"%3Afalse%2C"isLowest90"%3Afalse%2C"isLowestOffer"%3Afalse%2C"isOutOfStock"%3Afalse%2C"titleSearch"%3A""%2C"isRangeEnabled"%3Atrue%2C"isFilterEnabled"%3Afalse%2C"filterErotic"%3Atrue%2C"singleVariation"%3Atrue%2C"hasReviews"%3Afalse%2C"isPrimeExclusive"%3Afalse%2C"mustHaveAmazonOffer"%3Afalse%2C"mustNotHaveAmazonOffer"%3Afalse%2C"sortType"%3A4%2C"dateRange"%3A"0"%2C"warehouseConditions"%3A%5B1%2C2%2C3%2C4%2C5%5D%2C"settings"%3A%7B"viewTyp"%3A0%7D%2C"perPage"%3A150%7D'
driver.get(url)

# Espera a que la página se cargue
time.sleep(5)

# Simula un movimiento del ratón
action = ActionChains(driver)
action.move_by_offset(100, 100).perform()


try:
    language_menu = driver.find_element(By.CLASS_NAME, "languageMenuText")
    language_menu.click()
    
    # Espera a que el menú se despliegue
    time.sleep(5)  # Ajusta el tiempo según sea necesario

    # Encuentra el elemento específico dentro del menú y haz clic
    language_option = driver.find_element(By.XPATH, "//span[@rel='domain' and @setting='11']")
    language_option.click()
except Exception as e:
    print(f"Error al hacer clic en el elemento: {e}")
    
# Espera un poco para ver el efecto
time.sleep(500)

# Encuentra el elemento por su clase y haz c

# Cierra el navegador
driver.quit()


