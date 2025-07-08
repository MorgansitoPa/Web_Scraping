# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 14:23:11 2025

@author: Morgan
"""

import pandas as pd
import os

# Configurá esto según tu archivo original
archivo_origen = r"C:\Users\Morgan\Desktop\laboral\proyectos\prvkrs\flujo de trabajo\SCRAPING\0.1 - unificado_final - sin cuit duplicados.xlsx"
directorio_salida = r"C:\Users\Morgan\Desktop\laboral\proyectos\prvkrs\flujo de trabajo\fragmentos"
cantidad_partes = 5  # Cambiá este número si querés más o menos fragmentos

# Crear carpeta de salida si no existe
os.makedirs(directorio_salida, exist_ok=True)

# Cargar datos
df = pd.read_excel(archivo_origen)
total_filas = len(df)
filas_por_parte = total_filas // cantidad_partes + (total_filas % cantidad_partes > 0)

# Dividir y guardar cada parte
for i in range(cantidad_partes):
    inicio = i * filas_por_parte
    fin = min(inicio + filas_por_parte, total_filas)
    df_fragmento = df.iloc[inicio:fin]

    nombre_archivo = f"fragmento_{i+1}.xlsx"
    ruta_salida = os.path.join(directorio_salida, nombre_archivo)
    df_fragmento.to_excel(ruta_salida, index=False)

    print(f"✔ Fragmento {i+1} guardado: {ruta_salida} ({len(df_fragmento)} filas)")
