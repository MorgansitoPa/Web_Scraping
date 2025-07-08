# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 18:16:20 2025

@author: Morgan
"""
#----------------------------------------------------------
#----- Comparacion entre nros proporcionados --------------
#--------------- y nros scrapeados ------------------------
#----------------------------------------------------------

import pandas as pd

archivo_1 = r"C:\Users"
archivo_2 = r"C:\Users"

df1 = pd.read_excel(archivo_1, dtype=str)
df2 = pd.read_excel(archivo_2, dtype=str)

# Limpiamos espacios y convertimos a str
telefonos_1 = df1['Telefono'].dropna().astype(str).str.strip()

# Columnas base a comparar
cols_base = ['TEL_1', 'TEL_2', 'TEL_3', 'CELULAR']

# Concatenamos todas las columnas base en una sola serie
telefonos_2 = pd.Series(dtype=str)
for col in cols_base:
    if col in df2.columns:
        telefonos_2 = pd.concat([telefonos_2, df2[col].dropna().astype(str).str.strip()])
    else:
        print(f"⚠️ La columna {col} no está en el archivo base.")

telefonos_2 = telefonos_2.drop_duplicates()

# Convertimos a set para búsqueda rápida
set_telefonos_2 = set(telefonos_2)

# Comparamos y creamos la columna de resultado
df1['Existe_en_base'] = telefonos_1.apply(lambda x: x in set_telefonos_2)

# Guardamos resultado
df1.to_excel(r"C:\Users", index=False)

print("✅ Comparación realizada. Archivo resultado_comparacion.xlsx creado.")
