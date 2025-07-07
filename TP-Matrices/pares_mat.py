def pares_mat(mat) -> int:
    pares = 0
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if not mat[i][j] & 1:
                pares += 1
    return pares

def main():
    matrix = [
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]
    print(pares_mat(matrix))

if __name__ == "__main__":
    main()  