from typing import List

def estrictamenteCreciente(arr: List) -> int:
    rompe_orden = 0
    for i in range(1,len(arr[1:])):
        if arr[i] >= arr[i + 1]:
            rompe_orden += 1
    return rompe_orden

def main():
    arreglo1 = [1,4,4,6,4]
    print(estrictamenteCreciente(arreglo1))

if __name__ == "__main__":
    main()