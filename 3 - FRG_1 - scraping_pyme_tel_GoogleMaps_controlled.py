# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 18:53:30 2025

@author: famas
"""
#-------------------------------------------------------
#----- Se scrapea nros de telefono en formato Batch ----
#----- replicar el archivo x cantidad de batches -------
#-------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
import random
import os

# Configurar el navegador
def configurar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Modo sin interfaz para mejor rendimiento
    options.add_argument("--disable-blink-features=AutomationControlled")  # Evitar detección de bot

# Lista de user-agents comunes
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",

        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/15.1 Safari/605.1.15",

        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",

        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",

        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1"
    ]

    user_agent = random.choice(user_agents)
    options.add_argument(f"user-agent={user_agent}")
    print(f"[INFO] User-Agent seleccionado: {user_agent}")

    driver = webdriver.Chrome(options=options)
    return driver

# Cargar datos desde Excel
def cargar_datos_excel(archivo):
    df = pd.read_excel(archivo)
    df["Telefono"] = ""  # Nueva columna para los teléfonos
    return df

# Buscar teléfono en Google Maps
def buscar_telefono_google(empresa, driver):
    driver.get("https://www.google.com/maps/")

    try:
        # Esperar campo de búsqueda
        search_box = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.ID, "searchboxinput"))
        )
        search_box.clear()
        search_box.send_keys(empresa)
        search_box.send_keys(Keys.RETURN)

        # Esperar hasta 7 segundos la carga de resultado individual
        WebDriverWait(driver, 7).until(
            EC.any_of(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Teléfono')]")),
                EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Resultados de búsqueda')]"))
            )
        )

        # Verificar si hay ficha directa con teléfono
        try:
            telefono_element = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Teléfono')]")
            telefono = telefono_element.get_attribute("aria-label").replace("Teléfono: ", "")
        except:
            telefono = "No encontrado"

    except Exception as e:
        telefono = "Error"
        print(f"Error al buscar teléfono para {empresa}: {type(e).__name__} - {e}")

    return telefono

# Guardar resultados en Excel
def actualizar_excel(df, archivo_salida):
    df.to_excel(archivo_salida, index=False)

# Ejecutar el proceso
def ejecutar_proceso(archivo_entrada, archivo_salida):
    df = cargar_datos_excel(archivo_entrada)
    driver = configurar_driver()

    for index, row in df.iterrows():
        empresa = row["RAZON_SOCIAL"]
        print(f"Buscando teléfono para: {empresa}")  # Mensaje de depuración
        telefono = buscar_telefono_google(empresa, driver)
        df.at[index, "Telefono"] = telefono
        
        # Espera aleatoria entre búsquedas para evitar detección
        time.sleep(random.uniform(3, 6))
        
        # Guardar el archivo cada 10 registros
        if index % 30 == 0 and index != 0:
            print(f"Guardando los primeros {index+1} registros...")
            actualizar_excel(df, archivo_salida)

        # Reiniciar el navegador cada 150 registros
        if index > 0 and index % 150 == 0:
            print("Reiniciando navegador para evitar saturación...")
            driver.quit()
            time.sleep(5)  # Espera antes de reiniciar
            driver = configurar_driver()

    driver.quit()
    actualizar_excel(df, archivo_salida)
    print("Proceso finalizado. Datos guardados en:", archivo_salida)

# Ejecutar
archivo_entrada = r"C:\Users\Morgan\Desktop\laboral\proyectos\prvkrs\flujo de trabajo\SCRAPING\fragmento 1\fragmento_1.xlsx"
carpeta_salida = r"C:\Users\Morgan\Desktop\laboral\proyectos\prvkrs\flujo de trabajo\SCRAPING\Fragmentos_salida"

# Obtener nombre del archivo de entrada (sin extensión)
nombre_base = os.path.splitext(os.path.basename(archivo_entrada))[0]

# Crear ruta de salida automáticamente
archivo_salida = os.path.join(carpeta_salida, f"{nombre_base}_telefonos.xlsx")

# Ejecutar
ejecutar_proceso(archivo_entrada, archivo_salida)
