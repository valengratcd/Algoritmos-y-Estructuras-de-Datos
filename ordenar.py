from typing import List
from random import randint

def ordenar(arr: List[int]) -> List[int]:
    tamaño = len(arr)

    for i in range(tamaño):
        camio_o_no = False
        for j in range(tamaño - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                camio_o_no = True
        if not camio_o_no:
            return arr

def main() -> None:
    # generar 100 numeros random del 1 al 10
    arreglo = [randint(1,10) for _ in range(100)]
    print(ordenar(arreglo))
    return 0

if __name__ == "__main__":
    main()