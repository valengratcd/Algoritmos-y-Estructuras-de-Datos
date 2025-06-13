from typing import List
from reverso import reverso

def productoEscalarConInverso(lista1: List[int], lista2: List[int]) -> List[int]:
    if len(lista1) != len(lista2):
        raise ValueError("no coinciden las longitudes de los arreglos")
    
    reverso(lista2)
    nuevo_arreglo = [0] * len(lista1)
    for i in range(len(lista1)):
        nuevo_arreglo[i] = lista1[i] * lista2[i]
    return nuevo_arreglo

def main():
    arr1 = [1, 5, 8, 2, 7]
    arr2 = [3, 9, 4, 6, 0]
    print(productoEscalarConInverso(arr1,arr2))
    return 0

if __name__ == "__main__":
    main()