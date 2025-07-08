# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 14:57:49 2025

@author: Morgan
"""
#----------------------------------------------------------
#----- Unificacion de datos erroneos en un solo df --------
#----------------------------------------------------------

import pandas as pd
import os

# Ruta de la carpeta donde están los 10 archivos
carpeta = r"C:\Users"

# Crear lista para acumular los errores
errores = []

# Buscar archivos .xlsx en la carpeta
for archivo in os.listdir(carpeta):
    if archivo.endswith(".xlsx"):
        ruta = os.path.join(carpeta, archivo)
        try:
            df = pd.read_excel(ruta)

            # Filtrar filas donde la columna "Telefono" es "Error"
            df_error = df[df["Telefono"] == "Error"].copy()
            if not df_error.empty:
                df_error["Archivo"] = archivo  # opcional: para saber de qué archivo vino
                errores.append(df_error)

        except Exception as e:
            print(f"❌ Error al procesar {archivo}: {e}")

# Concatenar todos los errores encontrados
if errores:
    df_final = pd.concat(errores, ignore_index=True)
    
    # Ruta de salida
    salida = os.path.join(carpeta, "CUIT_con_error_unificados.xlsx")
    df_final.to_excel(salida, index=False)
    print(f"✅ Archivo generado con {len(df_final)} registros con error: {salida}")
else:
    print("🎉 No se encontraron errores.")
