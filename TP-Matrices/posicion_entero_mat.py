def posicion_entero_mat(mat, num: int) -> int:
    if not mat or num is None:
        return -100
    
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == num:
                return i + 1, j + 1
    return -1

def main():
    matrix = [
        [1,2,3],
        [4,5,6],
        [3,8,9]
    ]
    print(posicion_entero_mat(matrix, 1))

if __name__ == "__main__":
    main()