from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import nest_asyncio  
import asyncio
import re
import json
import os

nest_asyncio.apply()   

# Definición del bloqueo asincrónico
procesar_lock = asyncio.Lock()

def format_price(price: str) -> str:
    price = re.sub(r"[^\d,\.]", "", price)
    price = price.replace(',', '.')
    try:
        float_price = float(price)
        str_price = f"{float_price:.6f}"
        whole_part, decimal_part = str_price.split('.')
        if len(whole_part) > 3 and not re.match(r"^\d{1,3}(\.\d{3})*$", whole_part):
            whole_part = whole_part[:3]
        if len(whole_part) <= 2:
            formatted_price = f"{whole_part},{decimal_part[:3]}"
        elif len(whole_part) > 3:
            formatted_price = f"{whole_part},{decimal_part[:3]}"
        else:
            formatted_price = f"{whole_part},{decimal_part[:2]}"
        return formatted_price
    except ValueError:
        return price

def sanitize_text(text: str) -> str:
    return text.encode('utf-8', 'ignore').decode('utf-8')

import random

def get_price_and_title(link: str) -> str:
    try:  
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser') 
        # Seleccionar el contenedor principal
        contenedor = soup.select_one('div.ui-ms-polycard-container')

        if contenedor:
            # Buscar el título dentro del contenedor
            titulo = contenedor.select_one('a.poly-component__title')
            
            # Buscar el precio actual dentro del contenedor
            precio = contenedor.select_one('div.poly-price__current span.andes-money-amount__fraction')
            
            # Buscar el precio original dentro del contenedor
            precio_original = contenedor.select_one('s.andes-money-amount.andes-money-amount--previous.andes-money-amount--cents-dot span.andes-money-amount__fraction')
            
            # Buscar el descuento dentro del contenedor
            descuento = contenedor.select_one('span.andes-money-amount__discount')
            
            # Buscar los meses sin intereses dentro del contenedor
            meses_sin_intereses = contenedor.select_one('span.poly-price__installments.poly-text-positive')
        else:
            print("No se encontró el contenedor principal.")
            titulo = precio = precio_original = descuento = meses_sin_intereses = None

        if titulo:
            titulo_texto = sanitize_text(titulo.get_text(strip=True))
        else:
            titulo_texto = "No se pudo encontrar el título."
        
        if precio:
            precio_texto = sanitize_text(precio.text.strip())
        else:
            precio_texto = "No se pudo encontrar el precio."
        
        if precio_original:
            precio_original_texto = sanitize_text(precio_original.text.strip())
        else:
            precio_original_texto = None  # Cambiar a None para indicar que no se encontró

        if descuento:
            descuento_texto = sanitize_text(descuento.text.strip())
            descuento_texto = f"Con {descuento_texto} 🔥🔥"
        else:
            descuento_texto = ""
        if meses_sin_intereses:
            meses_texto = sanitize_text(meses_sin_intereses.text.strip())
            meses_emojis = ['🫣', '❗', '😱']
            meses_texto = f"{meses_texto} {random.choice(meses_emojis)}"
        else:
            meses_texto = ""

        # Nuevo bloque para prevenir duplicación de precios
        if precio_original_texto:
            precio_formatted = f"De ${precio_original_texto} a ${precio_texto}"
        else:
            precio_formatted = f"Precio: ${precio_texto}"
        
        # Construir el mensaje final con un salto de línea antes del descuento
        mensaje = f"{titulo_texto}\n\nENLACE:\n{link}\n\n{precio_formatted}"
        
        if descuento_texto:
            # Cambiado de espacio a salto de línea
            mensaje += f"\n{descuento_texto}"
        
        if meses_texto:
            mensaje += f"\n\n{meses_texto}"
        
        # Imprimir los resultados en consola
        print("Título:", titulo.get_text(strip=True) if titulo else "No se encontró el título")
        print("Precio actual:", precio.get_text(strip=True) if precio else "No se encontró el precio actual")
        print("Precio original:", precio_original.get_text(strip=True) if precio_original else "No se encontró el precio original")
        print("Descuento:", descuento.get_text(strip=True) if descuento else "No se encontró el descuento")
        print("Meses sin intereses:", meses_sin_intereses.get_text(strip=True) if meses_sin_intereses else "No se encontraron meses sin intereses")

        return mensaje

    except Exception as e:
        return f"Error al procesar el enlace: {e}"

def get_image_and_info(link: str):
    try:
        driver = webdriver.Chrome() 
        driver.get(link)

        image_element = driver.find_element(By.CLASS_NAME, 'poly-component__picture')
        image_url = image_element.get_attribute('src')

        response = requests.get(image_url)
        if response.status_code == 200:
            return response.content  
        else:
            return None
    except Exception as e:
        print(f"Error al obtener la imagen: {e}")
        return None
    finally:
        driver.quit()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    link = update.message.text.strip()
    chat_id = "-1002302040412"  

    if "mercadolibre.com" in link:
        image_data = get_image_and_info(link)
        resultado = get_price_and_title(link)

        if image_data:
            await context.bot.send_photo(chat_id=chat_id, photo=image_data, caption=resultado)
        else:
            await update.message.reply_text("No se pudo obtener la imagen del producto.")
    else:
        await update.message.reply_text("Por favor, envíame un enlace válido de MercadoLibre.")

async def procesar_enlaces_auto(app: Application) -> None:
    async with procesar_lock:
        file_path = 'enlaces_recopilados.json'
        
        if not os.path.exists(file_path):
            print("No se encontró el archivo enlaces_recopilados.json.")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                enlaces_recopilados = json.load(f)
            except json.JSONDecodeError:
                print("Error al leer el archivo enlaces_recopilados.json.")
                return
        
        if not enlaces_recopilados:
            print("La lista de enlaces está vacía.")
            return
        
        chat_id = "-1002302040412"  # Asegúrate de que este ID es correcto
        
        for enlace in enlaces_recopilados:
            # Procesar cada enlace utilizando las funciones existentes
            image_data = get_image_and_info(enlace)
            resultado = get_price_and_title(enlace)
            
            if image_data:
                await app.bot.send_photo(chat_id=chat_id, photo=image_data, caption=resultado)
            else:
                await app.bot.send_message(chat_id=chat_id, text=f"No se pudo obtener la imagen del producto para el enlace: {enlace}")
            
            await asyncio.sleep(380)  # 13 minutos en segundos
        
        try:
            os.remove(file_path)
            print(f"Archivo {file_path} eliminado exitosamente.")
            # await app.bot.send_message(chat_id=chat_id, text=f"Archivo {file_path} eliminado exitosamente.")
        except OSError as e:
            print(f"Error al eliminar el archivo {file_path}: {e}")
            # await app.bot.send_message(chat_id=chat_id, text=f"Error al eliminar el archivo {file_path}: {e}")

async def procesar_enlaces(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await procesar_enlaces_auto(context.application)

async def main():
    TOKEN = "7227911386:AAF-OyBnbcRfSrd7XMmk1Qq2-YZGXXRIbME"
    app = Application.builder().token(TOKEN).build()
    
    # Agregar el manejador para mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Agregar el manejador para el comando /procesar_enlaces
    app.add_handler(CommandHandler("procesar_enlaces", procesar_enlaces))
    
    print("El bot está en ejecución...")

    # Programar la ejecución automática de procesar_enlaces
    asyncio.create_task(procesar_enlaces_auto(app))
    
    await app.run_polling()

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except RuntimeError as e:
        if str(e) == "This event loop is already running":
            print("Reutilizando el bucle de eventos existente...")
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            raise 

        ## por si acaso