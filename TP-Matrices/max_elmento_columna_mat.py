def max_elmento_columna_mat(mat) -> int:
    if not mat:
        return -100
    
    transpuesta = list(zip(*mat))

    columna = [0, transpuesta[0][0]]

    for i in range(len(transpuesta)):
        for j in range(len(transpuesta[0])):
            if i == 0 and j == 0:
                 continue
            elif transpuesta[i][j] > columna[1]:
                columna[1] = transpuesta[i][j]
                columna[0] = i + 1
    return columna[0]

def main():
    matrix = [
        [1,2,3],
        [4,5,6],
        [3,8,9]
    ]
    print(max_elmento_columna_mat(matrix))

if __name__ == "__main__":
    main()