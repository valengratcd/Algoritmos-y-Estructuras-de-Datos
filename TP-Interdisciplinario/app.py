import lib
import pandas as pd
import matplotlib.pyplot as plt
from sqlqueries import *

# Paso 3: Limpieza y Preparación de Datos (EDA)
df_RESPUESTAS = lib.obtener_dataframe_desde_mysql(QUERY_RESPUESTAS)

# 1. revisar tipos de datos
print(df_RESPUESTAS.info())
print("")

# 2. estandarizar tiempo de respuesta a formato minutos/segundos
df_RESPUESTAS["Tiempo_total_convertido"] = lib.formato_tiempo_legible(df_RESPUESTAS["Tiempo_total"])

# 3. verificar nulos y modificarlos
lib.modificar_na(df_RESPUESTAS)

# Paso 4: Análisis Estadístico y Generación de Gráficos
# 1. Top 10 - Mejores Puntajes:
df_mejores_puntajes = lib.obtener_dataframe_desde_mysql(QUERY_MEJORES_PUNTAJES)
plt.barh(df_mejores_puntajes["nombre"].head(10), df_mejores_puntajes["puntaje_total_grupal"].head(10))
lib.personalizar_grafico(
    titulo="top 10 mejores puntajes",
    dir="./graficos",
    etiqueta_x="puntajes", 
    etiqueta_y="nombres",
    nombre_archivo="mejores_puntajes.png"
)

# 2. Top 10 - Alumnos Más Veloces (Mejor Tiempo de Respuesta):
df_mas_veloces = lib.obtener_dataframe_desde_mysql(QUERY_MAS_VELOCES)
plt.barh(df_mas_veloces["nombre"].head(10), df_mas_veloces["tiempo_total_segundos"].head(10))
lib.personalizar_grafico(
    titulo="top 10 alumnos mas veloces",
    dir="./graficos",
    etiqueta_x="velocidad (segundos)", 
    etiqueta_y="nombres",
    nombre_archivo="mejores_velocidades.png"
)

# 3. Ganadores por Fechas:
df_puntaje_X_fecha = lib.obtener_dataframe_desde_mysql(QUERY_PUNTAJE_FECHA)
df_puntaje_X_fecha['Fecha'] = pd.to_datetime(df_puntaje_X_fecha['Fecha'])
plt.plot(df_puntaje_X_fecha["Fecha"], df_puntaje_X_fecha["puntaje_ganador"])
lib.personalizar_grafico(
    titulo="puntaje más alto por fecha",
    dir="./graficos",
    etiqueta_x="fecha", 
    etiqueta_y="puntajes",
    no_superponer=df_puntaje_X_fecha["Fecha"],
    nombre_archivo="puntajes_X_fecha.png"
)

# 4. Distribución de Puntajes:
puntajes_avg = df_mejores_puntajes["puntaje_total_grupal"].mean()
puntajes_med = df_mejores_puntajes["puntaje_total_grupal"].median()
puntajes_std = df_mejores_puntajes["puntaje_total_grupal"].std()
mejor_puntaje = df_mejores_puntajes["puntaje_total_grupal"].max()
peor_puntaje = df_mejores_puntajes["puntaje_total_grupal"].min()
print(f"Puntaje promedio: {puntajes_avg}")
print(f"Puntaje mediano: {puntajes_med}")
print(f"Desviacion estandar del puntaje: {puntajes_std}")
print(f"Mejor puntajes: {mejor_puntaje}")
print(f"Peor puntaje: {peor_puntaje}")

df_mejores_puntajes.hist()
lib.personalizar_grafico(
    titulo="cantidad de alumnos por puntaje",
    dir="./graficos",
    etiqueta_x="puntajes", 
    etiqueta_y="cantidad de alumnos",
    nombre_archivo="alumnos_X_puntaje.png"
)
