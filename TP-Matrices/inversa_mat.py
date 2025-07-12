def inversa_mat(mat):
    filas = len(mat)

    for fila in mat:
        if len(fila) != filas:
            return -100

    A = [fila[:] for fila in mat]
    identidad = [[float(i == j) for j in range(filas)] for i in range(filas)]

    for i in range(filas):
        pivote = A[i][i]
        if pivote == 0:
            for k in range(i + 1, filas):
                if A[k][i] != 0:
                    A[i], A[k] = A[k], A[i]
                    identidad[i], identidad[k] = identidad[k], identidad[i]
                    pivote = A[i][i]
                    break
            else:
                return None

        for j in range(filas):
            A[i][j] /= pivote
            identidad[i][j] /= pivote

        for k in range(filas):
            if k != i:
                factor = A[k][i]
                for j in range(filas):
                    A[k][j] -= factor * A[i][j]
                    identidad[k][j] -= factor * identidad[i][j]

    return identidad

def main():
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [3, 8, 9]
    ]
    print(inversa_mat(matrix))

if __name__ == "__main__":
    main()