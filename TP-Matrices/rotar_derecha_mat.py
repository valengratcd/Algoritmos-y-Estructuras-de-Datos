def rotar_derecha_mat(mat) -> int:
    transpuesta = list(list(i)for i in zip(*mat))

    for i in range(len(transpuesta)):
        transpuesta[i].reverse()
    return transpuesta

def main():
    matrix = [
        [1,2,3],
        [4,5,6],
        [3,8,9]
    ]
    print(rotar_derecha_mat(matrix))

if __name__ == "__main__":
    main()