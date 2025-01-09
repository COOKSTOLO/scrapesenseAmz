import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def buscar_links_mercadolibre():
    url_descuentos_amz = "https://www.descuento.com.mx/buscar?keyword=amazon"
    url_amz = "https://www.amazon.com.mx/gp/goldbox?ref_=nav_em_0_1_1_35"
    
    try:
        respuesta_descuentos = requests.get(url_descuentos_amz)
        respuesta_descuentos.raise_for_status()

        soup_descuentos = BeautifulSoup(respuesta_descuentos.text, 'html.parser')
        elementos_descuentos = soup_descuentos.find_all('a', class_='badge badge-info price', href=True)
        links_amz_descuentos = [elemento['href'] for elemento in elementos_descuentos]

        if links_amz_descuentos:
            print("Enlaces de amazon encontrados en la página de descuentos:")
        else:
            print("No se encontraron enlaces de amazon en la página de descuentos.")

            # aqui saca los links de amz ofertas despues

        respuesta_amz = requests.get(url_amz)
        respuesta_amz.raise_for_status()

        soup_amz = BeautifulSoup(respuesta_amz.text, 'html.parser')
        elementos_mercadolibre = soup_amz.find_all('a', class_='ProductCard-module__card_uyr_Jh7WpSkPx4iEpn4w', href=True)
        # Limitamos a solo 15 enlaces de Mercado Libre
        links_mercadolibre_mercadolibre = [elemento['href'] for elemento in elementos_mercadolibre][:15]

        if links_mercadolibre_mercadolibre:
            print("\nEnlaces de Mercado Libre encontrados en la página de Mercado Libre:")
        else:
            print("No se encontraron enlaces de Mercado Libre en la página de Mercado Libre.")
        
        # Unir los enlaces encontrados
        all_links = links_amz_descuentos + links_mercadolibre_mercadolibre
        
        if all_links:
            # Unir el mensaje "finish" al final de los enlaces
            all_links.append("finish")
            
            # Crear DataFrame de pandas con los enlaces
            df = pd.DataFrame(all_links, columns=['Enlaces'])
            
            # Obtener la fecha actual para el nombre del archivo
            fecha_actual = datetime.now().strftime('%d/%m/%y').replace('/', '-')
            nombre_archivo = f"{fecha_actual} NoafiliadosAmz.xlsx"
            
            # Guardar el DataFrame en un archivo Excel
            df.to_excel(nombre_archivo, index=False)
            print(f"Los enlaces se han guardado en el archivo: {nombre_archivo}")
        else:
            print("No se encontraron enlaces para guardar.")

    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")

buscar_links_mercadolibre()
