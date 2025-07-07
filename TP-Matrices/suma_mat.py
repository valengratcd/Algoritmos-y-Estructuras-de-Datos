def suma_mat(mat) -> int:
    suma = 0
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            suma += mat[i][j]
    return suma

def main():
    matrix = [
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]
    print(suma_mat(matrix))

if __name__ == "__main__":
    main()  