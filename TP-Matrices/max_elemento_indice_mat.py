def max_elemento_indice_mat(mat) -> int:
    if not mat:
        return -100
    
    fila = [[0, 0], mat[0][0]]

    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] > fila[1]:
                fila[1] = mat[i][j]
                fila[0] = i + 1, j + 1

    return fila[0]

def main():
    matrix = [
        [1,2,3],
        [4,5,6],
        [3,8,9]
    ]
    print(max_elemento_indice_mat(matrix))

if __name__ == "__main__":
    main()