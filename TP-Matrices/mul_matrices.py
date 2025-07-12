def mul_matrices(mat1, mat2):
    if len(mat1[0]) != len(mat2):
        return -100
    
    filas = len(mat1)
    columnas = len(mat2[0])
    intermedia = len(mat2)

    producto = [[0 for _ in range(columnas)] for _ in range(filas)]

    print(producto)

    for i in range(filas):
        for j in range(columnas):
            for k in range(intermedia):
                producto[i][j] += mat1[i][k] * mat2[k][j]

    return producto

def main():
    matrix1 = [
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]
    matrix2 = [
        [9, 8, 7],
        [6, 5, 4],
        [3, 2, 1]
    ]

    matrix = mul_matrices(matrix1, matrix2)
    for i in matrix:
        print(i)

if __name__ == "__main__":
    main()