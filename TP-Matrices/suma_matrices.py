def suma_matrices(mat1, mat2):
    suma = []
    for i in range(3):
        suma.append([])

    for i in range(len(mat1)):
        for j in range(len(mat1[0])):
            suma[i].append(mat1[i][j] + mat2[i][j])

    return suma

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

    matrix = suma_matrices(matrix1, matrix2)
    for i in matrix:
        print(i)

if __name__ == "__main__":
    main()