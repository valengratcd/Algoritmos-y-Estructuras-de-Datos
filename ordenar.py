from typing import List

def ordenar(arr: List[int]) -> List[int]:
    nuevo_arr = [0] * len(arr)
    for i in range(len(arr)):
        for j in range(len(arr)):
            if arr[j] < arr[i]:
                nuevo_arr[i] = arr[j]
                break
        
    print(nuevo_arr)

ordenar([3,4,1,7,5])