from typing import List

def reverso(arr: List[int]) -> None:
    arr[:] = arr[::-1]

def main():
    arr1 = [1,2,3]
    reverso(arr1)
    print(arr1)
    return 0

if __name__ == "__main__":
    main()