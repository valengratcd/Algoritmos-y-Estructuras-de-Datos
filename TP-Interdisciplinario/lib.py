import os

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
import matplotlib.pyplot  as plt
import mysql.connector
from mysql.connector import Error

# --- 1. Definir los parámetros de conexión (REEMPLAZAR con tus datos) ---
DB_CONFIG = {
    "host": "localhost",  # O la IP de tu servidor MySQL
    "user": "mi_usuario",
    "password": "mi_password_segura",
    "database": "CUESTIONARIO"  # La BD con la que quieres trabajar
}

cantidad_graficos = 0

def personalizar_grafico(
    titulo: str,
    etiqueta_x: str,
    etiqueta_y: str,
    nombre_archivo: str = None,
    dir: str = None,
    mostrar_leyenda: bool = False,
    dpi: int = 300,
    usar_cuadricula: bool = True,
    no_superponer = None
):
    """
    Aplica configuraciones estéticas y de guardado a un gráfico de Matplotlib.

    Args:
        titulo (str): Título principal del gráfico.
        etiqueta_x (str): Etiqueta del eje X.
        etiqueta_y (str): Etiqueta del eje Y.
        nombre_archivo (str, optional): Nombre del archivo para guardar. Si es None, no se guarda.
        dir (str, optional): Nombre del directorio para guardar. Si es None, no se guarda o se usa la ruta determinada
        mostrar_leyenda (bool): Si es True, muestra la leyenda del gráfico.
        dpi (int): Resolución (puntos por pulgada) para la exportación.
        usar_cuadricula (bool): Si es True, añade una cuadrícula.
        no_superponer: Asegurar que se muestre los valores pasados.
    """
    # 1. Títulos y Etiquetas
    plt.title(titulo, fontsize=16, fontweight='bold')
    plt.xlabel(etiqueta_x, fontsize=12)
    plt.ylabel(etiqueta_y, fontsize=12)

    # 2. Configuración Estética
    if usar_cuadricula:
        # Añade una cuadrícula suave y de fondo
        plt.grid(True, linestyle='--', alpha=0.6)
        
    if mostrar_leyenda:
        # Muestra la leyenda si se han definido labels en el plot()
        plt.legend(loc='best', frameon=True) # frameon=True pone un marco alrededor de la leyenda

    if no_superponer is not None:
        plt.xticks(no_superponer, rotation=45, ha='right')

    # Ajustar el diseño para que los títulos y etiquetas no se solapen
    plt.tight_layout()

    # 3. Exportación
    if nombre_archivo:
        global cantidad_graficos
        cantidad_graficos += 1
        ruta_completa = nombre_archivo
        
        if dir:
            if not os.path.exists(dir):
                 os.makedirs(dir)
            ruta_completa = os.path.join(dir, nombre_archivo)
        
        try:
            plt.savefig(ruta_completa, dpi=dpi, bbox_inches='tight')
            print(f"Gráfico N°{cantidad_graficos} guardado como: {ruta_completa}")

        except Exception as e:
            print(f"Error al guardar el archivo '{nombre_archivo}': {e}")
            
    plt.close()

def extraer_porcentaje_como_entero(serie_str: pd.Series) -> pd.Series:
    """
    Toma una Series de strings con formato "NUMERO%", elimina el símbolo "%" 
    y convierte los valores restantes a enteros.

    Args:
        serie_str (pd.Series): Series de pandas con strings (ej: "15%", "50%").

    Returns:
        pd.Series: Series de enteros (ej: 15, 50).
    """
    
    # Asegurarse de que los valores sean tratados como strings
    # Luego, usa .str.replace('%', '') para eliminar el símbolo
    serie_limpia = serie_str.astype(str).str.replace('%', '', regex=False)
    
    # Convertir los valores limpios a enteros.
    # Usamos errors='coerce' para convertir cualquier valor no numérico 
    # (por si hubiera errores o NaNs) a NaN, y luego los convertimos a int.
    # Nota: Los NaNs requieren que la Series sea float o Int64, no int64 estándar.
    
    # 1. Convertir a numérico (float, para manejar NaNs si existen)
    serie_numerica = pd.to_numeric(serie_limpia, errors='coerce')
    
    # 2. Convertir a entero (usamos Int64 para preservar NaNs)
    # Si quieres un int estándar y estás seguro que no habrá NaNs, usa .astype('int64')
    serie_entera = serie_numerica.astype('Int64') 
    
    return serie_entera

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
            
            # 3. Usar pd.read_sql() para ejecutar la consulta y obtener el DataFrame
            # Esta función maneja el cursor y la extracción de filas automáticamente.
            df = pd.read_sql(query, conexion)
            
            return df
            
        else:
            return pd.DataFrame()

    except Error as e:
        return pd.DataFrame()

    finally:
        # 4. Cerrar la conexión
        if conexion is not None and conexion.is_connected():
            conexion.close()
