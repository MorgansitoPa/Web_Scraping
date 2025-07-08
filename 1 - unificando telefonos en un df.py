# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 17:39:05 2025

@author: Morgan
"""
#----------------------------------------------------------
#----- Unificacion de telefonos en un solo df -------------
#----- para comparacion con datos scrapeados --------------
#----------------------------------------------------------

import os
import pandas as pd

# ------------------ Configuración ------------------

# Carpeta donde están todos los archivos
carpeta = r"C:\Users"

# Lista de hojas permitidas a procesar
hojas_permitidas = ["COMPETENCIA", "Competencia", "competencia", "COMPETENCIAA", "COMPETENCI"]

# Mapeo de columnas posibles hacia nombres estandarizados
columnas_deseadas = {
    'id': 'ID',
    'cuit': 'CUIT',
    'cuil': 'CUIT',

    'razonsocial': 'RAZON_SOCIAL',
    'apeynomds': 'RAZON_SOCIAL',
    'razon_social': 'RAZON_SOCIAL',
    'razonsoc': 'RAZON_SOCIAL',
    'razon': 'RAZON_SOCIAL',
    'rsocial': 'RAZON_SOCIAL',
    'RAZ_SOC': 'RAZON_SOCIAL',
    'RS': 'RAZON_SOCIAL',
    'rs': 'RAZON_SOCIAL',
    'RAZONSOCIAL': 'RAZON_SOCIAL',
    'RAZON_SOCIAL': 'RAZON_SOCIAL',
    'RAZON SOCIAL': 'RAZON_SOCIAL',
    'Razon Social': 'RAZON_SOCIAL',
    'Razon_Social': 'RAZON_SOCIAL',
    'APEYNOM_DS': 'RAZON_SOCIAL',
    'razón social': 'RAZON_SOCIAL',
    'razon social': 'RAZON_SOCIAL',

    # Teléfonos
    'tel_1': 'TEL_1',
    'telefono1': 'TEL_1',
    'tel1': 'TEL_1',
    'numtel': 'TEL_1',
    'numero': 'TEL_1',

    'tel_2': 'TEL_2',
    'telefono2': 'TEL_2',
    'tel2': 'TEL_2',

    'tel_3': 'TEL_3',
    'telefono3': 'TEL_3',
    'tel3': 'TEL_3',

    'cel': 'CELULAR',
    'celular': 'CELULAR',
    'movil': 'CELULAR',
}

# ------------------ Función para procesar cada archivo ------------------

def procesar_archivo(ruta_archivo):
    dfs = []
    xls = pd.ExcelFile(ruta_archivo)

    for hoja in xls.sheet_names:
        if hoja.strip().upper() in [h.upper() for h in hojas_permitidas]:
            try:
                df = xls.parse(hoja)
                df.columns = [str(col).strip().lower().replace(" ", "").replace("á", "a").replace("é", "e")
                              .replace("í", "i").replace("ó", "o").replace("ú", "u") for col in df.columns]

                columnas_renombradas = {}
                for col in df.columns:
                    if col in columnas_deseadas:
                        columnas_renombradas[col] = columnas_deseadas[col]

                df = df.rename(columns=columnas_renombradas)

                columnas_finales = ['CUIT', 'TEL_1', 'TEL_2', 'TEL_3', 'CELULAR']
                df_final = df[[col for col in columnas_finales if col in df.columns]].copy()

                dfs.append(df_final)

            except Exception as e:
                print(f"⚠️ Error procesando hoja '{hoja}' en '{ruta_archivo}': {e}")
    
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

# ------------------ Proceso principal ------------------

todos_los_dfs = []

for archivo in os.listdir(carpeta):
    if archivo.endswith(".xlsx") or archivo.endswith(".xls"):
        ruta = os.path.join(carpeta, archivo)
        print(f"📄 Procesando: {archivo}")
        df = procesar_archivo(ruta)
        if not df.empty:
            todos_los_dfs.append(df)

# Concatenar todo en un único DataFrame final
df_final = pd.concat(todos_los_dfs, ignore_index=True)
print("✅ Consolidación completa. Registros:", len(df_final))

# Guardar en nuevo Excel
salida = os.path.join(carpeta, "telefonos_unificados.xlsx")
df_final.to_excel(salida, index=False)
print(f"📁 Archivo generado: {salida}")
