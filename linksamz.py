import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

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
        all_links = links_amz_descuentos 
        
        if all_links:
            all_links.append("finish")
            df = pd.DataFrame(all_links, columns=['Enlaces'])
            fecha_actual = datetime.now().strftime('%d/%m/%y').replace('/', '-')
            nombre_archivo = f"{fecha_actual} NoafiliadosAmz.xlsx"
            df.to_excel(nombre_archivo, index=False)
            print(f"Los enlaces se han guardado en el archivo: {nombre_archivo}")
        else:
            print("No se encontraron enlaces para guardar.")
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
buscar_links_mercadolibre()
