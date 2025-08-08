from time import sleep
from os import system, name

estudiantes = []

while True:
    print("\n--- SISTEMA DE GESTIÓN DE ESTUDIANTES ---")
    print("1. Registrar nuevo estudiante")
    print("2. Mostrar todos los estudiantes")
    print("3. Calcular promedio general")
    print("4. Buscar estudiante por nombre")
    print("5. Mostrar estudiantes con nota mayor al promedio")
    print("6. Mostrar mejor y peor nota")
    print("7. Eliminar estudiante por nombre")
    print("8. Salir")

    opcion = input("Elige una opción: ")

    match opcion:
        case "1":
            nombre = str(input("Nombre del estudiante: "))
            try:
                edad = int(input("Edad: "))
                nota = float(input("Nota (0-10): "))
            except ValueError:
                print("Edad o nota inválidas. Intenta de nuevo.")
                continue

            if edad <= 0 or nota < 0 or nota > 10:
                print("Datos inválidos. Intenta de nuevo.")
            else:
                nuevo_estudiante = {
                    "nombre": nombre,
                    "edad": edad,
                    "nota": nota
                }
                estudiantes.append(nuevo_estudiante)
                print(f"Estudiante {nombre} registrado con éxito.")

        case "2":
            if not estudiantes:
                print("No hay estudiantes registrados aún.")
                continue

            print("\nEstudiantes registrados:")
            print("-------------------------")
            for i, estudiante in enumerate(estudiantes, 1):
                print(f"{i}. Nombre: {estudiante['nombre']}")
                print(f"   Edad: {estudiante['edad']}")
                print(f"   Nota: {estudiante['nota']}")
                print("-------------------------")

        case "3":
            if not estudiantes:
                print("No hay estudiantes registrados.")
                continue

            suma_notas = sum(e["nota"] for e in estudiantes)
            promedio = suma_notas / len(estudiantes)
            print(f"El promedio general de notas es: {promedio:.2f}")
        
        case "4":
            if not estudiantes:
                print("No hay estudiantes registrados.")
                continue

            objetivo = str(input("que estudiante desea buscar: "))
            for i, estudiante in enumerate(estudiantes):
                if estudiante["nombre"] == objetivo:
                    print(f"{objetivo} en {i} elemento")
                    continue
            print("Estudiante no encontrado")
        
        case "5":
            if not estudiantes:
                print("No hay estudiantes registrados.")
                continue

            suma_notas = sum(e["nota"] for e in estudiantes)
            promedio = suma_notas / len(estudiantes)

            for i, estudiante in enumerate(estudiantes):
                if estudiante["nota"] > promedio:
                    print(f"Estudiante {estudiante["nombre"]} tiene una nota mayor al promedio")
                
        case "6":
            if not estudiantes:
                print("No hay estudiantes registrados.")
                continue

            max_nota = 0
            min_nota = 0

            for i, estudiante in enumerate(estudiantes):
                if estudiante["nombre"] > max_nota:
                    max_nota = estudiante["nombre"]
                else:
                    min_nota = estudiante["nombre"]
            
            print(f"Mayor nota {max_nota}, menor nota {min_nota}")

        case "7":
            if not estudiantes:
                print("No hay estudiantes registrados.")
                continue

            nombre = str(input("Estudiante: "))

            for i, estudiante in enumerate(estudiantes):
                if estudiante["nombre"] == nombre:
                    del estudiante["nombre"]
                    print(f"Estudiante {nombre} eliminado")
                    continue

        case "8":
            print("Saliendo del programa...")
            break

        case _:
            print("Opción no válida. Intenta otra vez.")
    
    sleep(3)
    if name == "nt":
        system("cls")
    else:
        system("clear")