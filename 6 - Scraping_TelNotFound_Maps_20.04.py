# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 22:12:45 2025

@author: famas
"""
#----------------------------------------------------
#----- Scraping de telefonos con datos erroneos -----
#----------------------------------------------------

import pandas as pd
import re
import time
import os
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

# -------- CONFIGURAR NAVEGADOR --------
def configurar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")

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
    print(f"[INFO] User-Agent: {user_agent}")

    return webdriver.Chrome(options=options)

# -------- BUSCAR TELÉFONO --------
def buscar_telefono_google(empresa, driver):
    telefono = "Error"
    estado = "Error"

    try:
        driver.get("https://www.google.com/maps/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchboxinput")))

        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.clear()
        search_box.send_keys(empresa)
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchboxinput"))
        )
        time.sleep(2)

        # Click en primer resultado si lo hay
        try:
            primer_resultado = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".Nv2PK"))
            )
            primer_resultado.click()
            time.sleep(3)
        except:
            pass  # No hay múltiples resultados

        # CAPTCHA
        if "detectar tráfico inusual" in driver.page_source.lower():
            return "CaptchaDetectado", "CaptchaDetectado"

        # Intentar con botón
        try:
            telefono_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Teléfono')]"))
            )
            telefono = telefono_element.get_attribute("aria-label").replace("Teléfono: ", "").strip()
            estado = "OK"
            return telefono, estado
        except:
            pass

        # Intentar extraer desde el texto visible (regex)
        try:
            page_text = driver.find_element(By.TAG_NAME, "body").text
            posibles_telefonos = re.findall(r"\(?\d{2,4}\)?[\s\-]?\d{3,4}[\s\-]?\d{4}", page_text)
            if posibles_telefonos:
                telefono = posibles_telefonos[0].strip()
                estado = "Regex"
        except Exception as e:
            with open("errores.log", "a", encoding="utf-8") as f:
                f.write(f"⚠️ Regex error para {empresa}: {e}\n")

    except Exception as e:
        estado = "Error"
        with open("errores.log", "a", encoding="utf-8") as f:
            f.write(f"❌ {empresa}: {type(e).__name__} - {e}\n")
            f.write(traceback.format_exc() + "\n")

    return telefono, estado

# -------- EJECUTAR PROCESO --------
def ejecutar_proceso_filtrado(archivo_entrada, archivo_salida):
    df = pd.read_excel(archivo_entrada)

    if "Estado" not in df.columns:
        df["Estado"] = ""

    df_filtrado = df[df["Telefono"].isin(["No encontrado", "Error", None, ""])].copy()

    if df_filtrado.empty:
        print("✅ No hay registros pendientes.")
        return

    driver = configurar_driver()

    for index, row in df_filtrado.iterrows():
        empresa = row.get("RAZON_SOCIAL") or row.get("Nuevo nombre empresa")
        if not isinstance(empresa, str): continue

        print(f"🔍 Buscando teléfono para: {empresa}")
        telefono, estado = buscar_telefono_google(empresa, driver)

        df_filtrado.at[index, "Telefono"] = telefono
        df_filtrado.at[index, "Estado"] = estado

        time.sleep(random.uniform(3, 6))

        if index > 0 and index % 30 == 0:
            print("💾 Guardando avance...")
            df_filtrado.to_excel(archivo_salida, index=False)

        if index > 0 and index % 150 == 0:
            print("🔄 Reiniciando navegador...")
            driver.quit()
            time.sleep(5)
            driver = configurar_driver()

    driver.quit()
    df_filtrado.to_excel(archivo_salida, index=False)
    print("✅ Proceso finalizado. Archivo guardado en:", archivo_salida)

# -------- RUTAS --------
entrada = r"C:\Users"
carpeta_salida = r"C:\Users"

# Obtener nombre base
nombre_base = os.path.splitext(os.path.basename(entrada))[0]  # fragmento_1_telefonos
salida = os.path.join(carpeta_salida, f"{nombre_base}_errores.xlsx")

ejecutar_proceso_filtrado(entrada, salida)
