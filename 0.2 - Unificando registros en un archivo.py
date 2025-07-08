# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 19:30:01 2025

@author: Morgan
"""

import os
import pandas as pd

# Ruta de la carpeta donde están los archivos
carpeta = r"C:\Users"

# Lista para guardar los DataFrames
dataframes = []

# Recorremos todos los archivos .xlsx de la carpeta
for archivo in os.listdir(carpeta):
    if archivo.endswith(".xlsx"):
        ruta_archivo = os.path.join(carpeta, archivo)
        try:
            # Leemos la hoja 'Sheet1' y solo las columnas necesarias
            df = pd.read_excel(
                ruta_archivo,
                sheet_name='Sheet1',
                usecols=['CUIT', 'RAZON_SOCIAL', 'REGION', 'INCIDENCIAS', 'archivo', 'hoja'],
                engine="openpyxl"
            )
            df["ARCHIVO_ORIGEN"] = archivo  # (opcional) Para trazabilidad
            dataframes.append(df)
        except Exception as e:
            print(f"⚠️ Error al leer {archivo}: {e}")

# Concatenamos todos los DataFrames
df_total = pd.concat(dataframes, ignore_index=True)

# Guardamos en un nuevo archivo Excel
archivo_salida = os.path.join(carpeta, "unificado_final.xlsx")
df_total.to_excel(archivo_salida, index=False, engine="openpyxl")

print(f"✅ Archivo unificado guardado como: {archivo_salida}")
