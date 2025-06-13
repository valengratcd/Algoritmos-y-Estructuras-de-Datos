from typing import List

def productoDeArreglos(lista1: List[int], lista2: List[int]) -> List[int]:
    if len(lista1) != len(lista2):
        raise ValueError("no coinciden las longitudes de los arreglos")
    
    lista3 = [0] * len(lista1)

    for i in range(len(lista1)):
        lista3[i] = lista1[i] * lista2[len(lista1) - (i + 1)]

    return lista3
def main():
    arr1 = [10, 11, 12, 13, 14]
    arr2 = [20, 21, 22, 23, 24]

    print(productoDeArreglos(arr1, arr2))
    return 0

if __name__ == "__main__":
    main()