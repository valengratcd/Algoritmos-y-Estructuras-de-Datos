import random

def simulacion_de_operaciones(inventario, cantidad_inicial):
    cantidad_actual = [len(inventario[categoria]) for categoria in inventario.keys()]
    clave_categoria = random.choice(list(inventario.keys()))
    producto = random.randint(0, len(inventario[clave_categoria]) - 1)
    inventario[clave_categoria].pop(producto)

    cantidad_actual = [len(inventario[categoria]) for categoria in inventario.keys()]

    for (i_v, cantidad_v), cantidad_n in zip(enumerate(cantidad_inicial), cantidad_actual):
        if cantidad_v[0] > cantidad_n:
            match cantidad_v[1]:
                case "computadoras":
                    inventario[cantidad_v[1]].append(tuple(["desktop HP Pavilion", 900]))
                case "accesorios":
                    inventario[cantidad_v[1]].append(tuple(["mousepad gamer", 20]))
                case _:
                    inventario[cantidad_v[1]].append(tuple(["impresora multifuncional", 120]))

def main():
    inventario = {
        'computadoras': [
            ("laptop Dell XPS 13", 1200),
            ("laptop MacBook Pro", 2500),
            ("laptop Lenovo ThinkPad", 1000)
        ],
        'accesorios': [
            ("cargador portátil", 25),
            ("funda para laptop", 40),
            ("adaptador USB-C", 15)
        ],
        'periféricos': [
            ("teclado mecánico", 45),
            ("mouse inalámbrico", 30),
            ("monitor 24 pulgadas", 150)
        ]
    }
    cantidad_inicial = [(len(inventario[categoria]), categoria) for categoria in inventario.keys()]

    for i in range(3):
        simulacion_de_operaciones(inventario, cantidad_inicial)
    
    for categoria, productos in inventario.items():
        print(f"Categoría: {categoria.capitalize()}")
        for nombre, precio in productos:
            print(f"  - {nombre}: ${precio}")
        print()


if __name__ == "__main__":
    main()