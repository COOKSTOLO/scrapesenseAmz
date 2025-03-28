import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configurar opciones de Chrome
options = Options()
options.add_argument("--start-maximized")  # Inicia el navegador maximizado (opcional)
# Puedes agregar más configuraciones si es necesario

# Usar webdriver-manager para obtener el driver automáticamente
service = Service(ChromeDriverManager().install())

# Inicializar el webdriver con el servicio y las opciones
driver = webdriver.Chrome(service=service, options=options)

# Abrir la página para iniciar sesión
driver.get("https://dyn.keepa.com/r/?type=amazon&smile=0&domain=11&asin=B08YZ9NMB5&source=website&path=dealsOverlay/AMAZON")

# Inicia sesión manualmente
print("Inicia sesión manualmente y presiona ENTER aquí cuando termines.")
input()

# Guardar cookies en un archivo
cookies_file = "cookies.pkl"  # Archivo donde se guardarán las cookies
with open(cookies_file, "wb") as file:
    pickle.dump(driver.get_cookies(), file)

print("Cookies guardadas exitosamente.")
driver.quit()
