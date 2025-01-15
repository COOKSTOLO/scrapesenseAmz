import pickle
import pyperclip
import os  # Importar el módulo os
import time  # Importar el módulo time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime, timedelta  # Asegúrate de importar timedelta
import requests
import json  # Importar el módulo json




options = Options()
options.add_argument("--start-maximized")

# Inicializar el controlador de Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


# Abre el enlace en el navegador
driver.get("https://dyn.keepa.com/r/?type=amazon&smile=0&domain=11&asin=B08YZ9NMB5&source=website&path=dealsOverlay/AMAZON")

# Mantén la página abierta durante 15 segundos
time.sleep(9000)


