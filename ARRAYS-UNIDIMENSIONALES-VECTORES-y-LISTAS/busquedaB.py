from typing import List

def busquedaB(arr: List[int], num: int) -> int:
    # checkeo que no esten vacios ni el array ni el numero esten vacios
    if not arr or num is None:
        return -1
    
    # checkeo si esta ordenado
    for i in range(len(arr) - 1):
        print(i, arr[i], arr[i + 1])
        if arr[i] > arr[i + 1]:
            return -1
     
    del i
    # implementacion 
    indice_final = len(arr) - 1
    indice_inicial = 0
    while indice_inicial <= indice_final:
        medio = (indice_inicial + indice_final) // 2
        if num == arr[medio]:
            return medio
        elif num < arr[medio]:
            indice_final = medio - 1
        else:
            indice_inicial = medio + 1
    return -3


def main():
    arreglo1 = [1,2,3]
    print(busquedaB(arreglo1, 4))

if __name__ == "__main__":
    main()