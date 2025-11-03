import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

import mysql.connector
from mysql.connector import Error

# --- 1. Definir los parámetros de conexión (REEMPLAZAR con tus datos) ---
DB_CONFIG = {
    "host": "localhost",  # O la IP de tu servidor MySQL
    "user": "mi_usuario",
    "password": "mi_password_segura",
    "database": "CUESTIONARIO"  # La BD con la que quieres trabajar
}

def formato_tiempo_legible(series_timedelta: pd.Series) -> pd.Series:
    """
    Convierte una Series de pandas con dtype timedelta64[ns] 
    a una Series de cadenas de texto con formato "Xh Ym Zs".
    Se normaliza a la unidad más grande que tenga un valor > 0.

    Args:
        series_timedelta: Una Series de pandas con valores Timedelta.

    Returns:
        Una Series de cadenas de texto con el tiempo formateado.
    """
    
    def convertir_segundos(total_segundos):
        if pd.isna(total_segundos):
            return ""  # Manejar valores NaN
        
        # Convertir a entero, ya que los segundos totales son un float
        segundos = int(total_segundos)
        
        # Calcular horas, minutos y segundos restantes
        horas = segundos // 3600
        segundos %= 3600
        minutos = segundos // 60
        segundos %= 60
        
        partes = []
        if horas > 0:
            partes.append(f"{horas}h")
        if minutos > 0 or (horas == 0 and segundos == 0): # Incluir minutos si hay, o si solo hay minutos
            partes.append(f"{minutos}m")
        # Incluir segundos si hay, o si todo es cero (para mostrar "0s" si el tiempo es 0)
        if segundos > 0 or (not partes and horas == 0 and minutos == 0):
             partes.append(f"{segundos}s")

        # La lógica anterior es compleja. Simplifiquemos para el requerimiento:
        # Mostrar la unidad más grande Y la siguiente, o solo la que tiene valor.

        formato_final = []
        if horas > 0:
            formato_final.append(f"{horas}h")
            if minutos > 0:
                 formato_final.append(f"{minutos}m")
        elif minutos > 0:
            formato_final.append(f"{minutos}m")
            if segundos > 0:
                formato_final.append(f"{segundos}s")
        elif segundos > 0:
            formato_final.append(f"{segundos}s")
        else:
            return "0s"

        return " ".join(formato_final)


    # Aplicar la función de conversión a los segundos totales de la Series
    return series_timedelta.dt.total_seconds().apply(convertir_segundos)

def modificar_na(df: pd.DataFrame) -> None:
    """
    Verifica valores nulos por cada columna numerica del dataframe 
    y los modifica por el valor promedio (Mean).

    Args:
        df (pd.DataFrame): El dataframe a remplazar.
    
    Returns:
        None: El dataframe remplazado por los promedios.
    """
    for s in df.columns:
        # s_numeric = pd.to_numeric(s, errors='coerce')
        es_numerico = is_numeric_dtype(df[s].dtype)
        if es_numerico:
            promedio = df[s].mean()
            df[s].fillna(promedio, inplace=True)

def obtener_dataframe_desde_mysql(query):
    """
    Establece la conexión, ejecuta una consulta SELECT y devuelve los resultados 
    como un DataFrame de Pandas.
    
    Args:
        query (str): La sentencia SQL SELECT a ejecutar.
    
    Returns:
        pd.DataFrame: El DataFrame con los resultados, o un DataFrame vacío si hay error.
    """
    conexion = None
    
    try:
        # 2. Establecer la conexión
        conexion = mysql.connector.connect(**DB_CONFIG)
        
        if conexion.is_connected():
            print("Conexión a MySQL exitosa. Generando DataFrame...")
            
            # 3. Usar pd.read_sql() para ejecutar la consulta y obtener el DataFrame
            # Esta función maneja el cursor y la extracción de filas automáticamente.
            df = pd.read_sql(query, conexion)
            
            print("DataFrame creado con éxito.")
            return df
            
        else:
            print("No se pudo conectar a la base de datos.")
            return pd.DataFrame()

    except Error as e:
        print(f"Error al conectar o ejecutar la consulta: {e}")
        return pd.DataFrame()

    finally:
        # 4. Cerrar la conexión
        if conexion is not None and conexion.is_connected():
            conexion.close()
            print("Conexión a MySQL cerrada")

def conectar_y_ejecutar_consulta(query, es_select=True, datos=None):
    """
    Establece la conexión, ejecuta una consulta y maneja la desconexión.
    
    Args:
        query (str): La sentencia SQL a ejecutar.
        es_select (bool): True si es una consulta SELECT (para devolver resultados).
        datos (tuple o list): Los datos a insertar/actualizar (si la consulta los requiere).
    
    Returns:
        list: Los resultados si es una consulta SELECT, o None.
    """
    conexion = None
    cursor = None
    resultados = None

    try:
        # 2. Establecer la conexión
        conexion = mysql.connector.connect(**DB_CONFIG)
        
        if conexion.is_connected():
            print("Conexión a MySQL exitosa")
            
            # 3. Crear un objeto cursor
            cursor = conexion.cursor()
            
            # 4. Ejecutar la consulta
            if datos:
                cursor.execute(query, datos)
            else:
                cursor.execute(query)
            
            # 5. Manejar los resultados o la confirmación (commit)
            if es_select:
                resultados = cursor.fetchall()
            else:
                conexion.commit() # Confirmar cambios (INSERT, UPDATE, DELETE)
                print(f"{cursor.rowcount} fila(s) afectada(s).")
                
        else:
            print("No se pudo conectar a la base de datos.")

    except Error as e:
        print(f"Error al conectar o ejecutar la consulta: {e}")

    finally:
        # 6. Cerrar el cursor y la conexión
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()
            print("Conexión a MySQL cerrada")
            
    return resultados