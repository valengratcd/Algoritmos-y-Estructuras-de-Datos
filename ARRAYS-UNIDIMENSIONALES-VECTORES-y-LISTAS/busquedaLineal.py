from typing import List, Any

def busquedaLineal(lista1: List[int], n: int) -> Any:
    for i in range(len(lista1)):
        if n == lista1[i]:
            return i
    return None

def main():
    print(busquedaLineal([1,2,3], 2))
    return 0

if __name__ == "__main__":
    main()