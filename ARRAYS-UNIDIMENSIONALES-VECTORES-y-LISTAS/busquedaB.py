from typing import List

def busquedaB(arr: List[int], num: int) -> int:
    # checkeo que no esten vacios ni el array ni el numero esten vacios
    if not arr or not num:
        return -1
    
    # checkeo si esta ordenado
    for i in range(len(arr)):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                return -2
     
    del i, j
    # implementacion 
    indice_final = len(arr) - 1
    while arr[0] <= arr[len(arr) - 1]:
        if num == arr[indice_final]:
            return indice_final
        elif num < arr[indice_final]:
            indice_final = indice_final // 2
        else:
            indice_final = (indice_final // 2) + indice_final


def main():
    arreglo1 = [1,2,3,4,5,6]
    print(busquedaB(arreglo1, 3))

if __name__ == "__main__":
    main()