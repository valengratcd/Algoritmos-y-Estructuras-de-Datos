import pandas as pd

import mysql.connector
from mysql.connector import Error

# --- 1. Definir los parámetros de conexión (REEMPLAZAR con tus datos) ---
DB_CONFIG = {
    "host": "localhost",  # O la IP de tu servidor MySQL
    "user": "mi_usuario",
    "password": "mi_password_segura",
    "database": "CUESTIONARIO"  # La BD con la que quieres trabajar
}

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

# --- EJEMPLOS DE USO ---

# 1. Consulta SELECT (Lectura de datos)
select_query = "SELECT IdRespuesta, Tiempo_Total FROM RESPUESTAS;"
personas_mayores = conectar_y_ejecutar_consulta(select_query, es_select=True)

if personas_mayores:
    print("\n--- Resultados de la Consulta SELECT ---")
    for row in personas_mayores:
        print(row)
    print("---------------------------------------")
