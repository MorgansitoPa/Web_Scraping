# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 19:05:14 2025

@author: Morgan
"""
#----------------------------------------------------------
#----- Unificacion de datos pertinentes en un solo df -----
#----------------------------------------------------------

import os
import pandas as pd
from openpyxl.utils.exceptions import InvalidFileException
import warnings
import unicodedata

warnings.simplefilter("ignore", UserWarning)

carpeta_raiz = r"C:\Users"

#lista de hojas a procesar
hojas_permitidas = ["COMPETENCIA", "Competencia", "competencia", "COMPETENCIA", "COMPETENCIAA", "COMPETENCI"]  

# Mapeo robusto de nombres de columnas (todas en minúsculas sin acento ni espacios)
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
    
    'region': 'REGION',
    'subregion': 'SUBREGION',
    'provincia': 'PROVINCIA',
    'asignacion': 'ASIGNACION',

    # todas las variantes conocidas o posibles errores de "incidencias"
    'incidencias': 'INCIDENCIAS',
    'inc': 'INCIDENCIAS',
    'incid': 'INCIDENCIAS',
    'incidencia': 'INCIDENCIAS',
    'inci': 'INCIDENCIAS',
    'incidncias': 'INCIDENCIAS',
}


def normalizar_nombre(col):
    col = str(col).strip().lower()
    col = ''.join(c for c in unicodedata.normalize('NFD', col) if unicodedata.category(c) != 'Mn')
    col = col.replace(" ", "").replace("_", "")
    return col

def procesar_excel(path_archivo):
    try:
        xl = pd.ExcelFile(path_archivo)
    except (InvalidFileException, ValueError, FileNotFoundError):
        print(f"⚠️ No se pudo leer el archivo: {path_archivo}")
        return []

    dataframes = []
    for hoja in xl.sheet_names:
        if hoja not in hojas_permitidas:
            continue
        
        try:
            df = xl.parse(hoja, dtype=str)
            df.columns = [str(c).strip() for c in df.columns]

            # Crear diccionario de columnas mapeadas automáticamente
            columnas_map = {}
            for col in df.columns:
                col_norm = normalizar_nombre(col)
                if col_norm in columnas_deseadas:
                    columnas_map[col] = columnas_deseadas[col_norm]

            if not columnas_map:
                continue

            df_filtrado = df[list(columnas_map.keys())].rename(columns=columnas_map)
            df_filtrado["archivo"] = os.path.basename(path_archivo)
            df_filtrado["hoja"] = hoja
            dataframes.append(df_filtrado)

        except Exception as e:
            print(f"❌ Error leyendo {path_archivo} - hoja '{hoja}': {e}")
            continue

    return dataframes


todos_los_dataframes = []
for root, dirs, files in os.walk(carpeta_raiz):
    for file in files:
        if file.endswith((".xlsx", ".xls")):
            full_path = os.path.join(root, file)
            dataframes = procesar_excel(full_path)
            todos_los_dataframes.extend(dataframes)

if todos_los_dataframes:
    df_final = pd.concat(todos_los_dataframes, ignore_index=True)
    df_final.to_excel("encuestas_unificadas.xlsx", index=False)
    print("✅ Archivo generado: encuestas_unificadas.xlsx")
else:
    print("⚠️ No se encontraron datos relevantes.")
