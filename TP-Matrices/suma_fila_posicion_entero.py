def posicion_entero_mat(mat, num: int) -> int:
    if not mat[num] or num is None:
        return -100
    
    suma = 0

    for i in range(len(mat[num])):
        suma += mat[num][i] 
    return suma

def main():
    matrix = [
        [1,2,3],
        [4,5,6],
        [3,8,9]
    ]
    print(posicion_entero_mat(matrix, 1))

if __name__ == "__main__":
    main()