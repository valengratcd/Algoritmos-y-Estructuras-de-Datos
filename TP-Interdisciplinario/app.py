import lib

# Paso 3: Limpieza y Preparación de Datos (EDA)
select_query = "SELECT * FROM RESPUESTAS;"
df = lib.obtener_dataframe_desde_mysql(select_query)

df["Tiempo_total_convertido"] = lib.formato_tiempo_legible(df["Tiempo_total"])

print(df.info())
print("")
print(df["Tiempo_total"])
print("")
lib.modificar_na(df)
