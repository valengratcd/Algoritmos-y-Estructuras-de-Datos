from typing import List
from math import pi

def multiplicarPorPI(lista1: List[int]) -> List[int]:
    return [round(i * pi, 3) for i in lista1]

def main():
    print(multiplicarPorPI([1,2,3]))
    return 0

if __name__ == "__main__":
    main()