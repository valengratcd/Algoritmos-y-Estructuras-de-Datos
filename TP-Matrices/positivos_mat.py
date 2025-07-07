def positivos_mat(mat) -> int:
    positivos = 0
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] >= 0:
                positivos += 1
    return positivos

def main():
    matrix = [
        [1,2,3],
        [4,-5,6],
        [7,8,9]
    ]
    print(positivos_mat(matrix))

if __name__ == "__main__":
    main()  