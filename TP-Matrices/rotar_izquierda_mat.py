def rotar_izquierda_mat(mat) -> int:
    for i in range(len(mat)):
        mat[i].reverse()

    transpuesta = list(list(i)for i in zip(*mat))

    return transpuesta

def main():
    matrix = [
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]
    matrix = rotar_izquierda_mat(matrix)
    for i in matrix:
        print(i)

if __name__ == "__main__":
    main()