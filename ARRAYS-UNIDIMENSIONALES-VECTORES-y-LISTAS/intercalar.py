from typing import List

def intercalar(arr: List[int], num: int) -> List[int]:
    arr[-1] = num
    for i in range(len(arr)):
        if num < arr[-(i + 1)]:
            arr[-i], arr[-(i + 1)] = arr[-(i + 1)], arr[-i]
    return arr

def main():
    arreglo = [1, 5, 10, 0]
    print(intercalar(arreglo, 2))

if __name__ == "__main__":
    main()