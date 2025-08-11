def mayor_cien(dicc: dict) -> dict:
    nuevo = {}
    for i in dicc:
        if float(dicc[i]) > 100.0:
            nuevo.update({i: dicc[i]})
    return nuevo

def main():
    productos = {
        "Manzanas": 1.20,
        "Pan": 0.90,
        "Leche": 1.50,
        "Huevos": 1000,
        "Arroz": 1.10,
        "Queso": 3.75
    }
    print(mayor_cien(productos))

if __name__ == "__main__":
    main()