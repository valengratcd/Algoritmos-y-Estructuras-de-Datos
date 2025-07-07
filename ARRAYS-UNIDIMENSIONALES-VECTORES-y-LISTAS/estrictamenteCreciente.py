from typing import List

def estrictamenteCreciente(arr: List) -> int:
    orden = arr[1] - arr[0]
    rompe_orden = 0
    for i in range(1,len(arr[1:])):
        if (arr[i + 1] - arr[i]) != orden:
            rompe_orden += 1
    return rompe_orden

def main():
    arreglo1 = [1,4,4,6]
    print(estrictamenteCreciente(arreglo1))

if __name__ == "__main__":
    main()