# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 15:03:40 2025

@author: Morgan
"""
#------------------------------------------------------------
#----- Unificacion de telefonos obtenidos en un solo df -----
#------------------------------------------------------------

import pandas as pd
import os

# Ruta de la carpeta con tus archivos
carpeta = r"C:\Users"

# Lista para acumular los registros encontrados
resultados_ok = []

for archivo in os.listdir(carpeta):
    if archivo.endswith(".xlsx"):
        ruta = os.path.join(carpeta, archivo)
        try:
            df = pd.read_excel(ruta)

            # Filtrar los que tienen un número válido
            df_ok = df[
                (~df["Telefono"].isin(["Error", "No encontrado", "", None])) &
                (df["Telefono"].notna())
            ].copy()

            if not df_ok.empty:
                df_ok["Archivo"] = archivo  # opcional: Columna para saber de qué archivo proviene
                resultados_ok.append(df_ok)

        except Exception as e:
            print(f"❌ Error al procesar {archivo}: {e}")

# Concatenar y guardar si hay datos
if resultados_ok:
    df_final = pd.concat(resultados_ok, ignore_index=True)
    
    # Ruta de salida
    salida = os.path.join(carpeta, "Telefonos_encontrados.xlsx")
    df_final.to_excel(salida, index=False)
    print(f"✅ Archivo generado con {len(df_final)} teléfonos encontrados: {salida}")
else:
    print("📭 No se encontraron registros con teléfonos válidos.")
