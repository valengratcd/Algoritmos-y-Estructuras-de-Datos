def max_columna_mat(mat, i_fila) -> int:
    if not mat or i_fila < 0 or i_fila >= len(mat):
        return -100
    
    fila_seleccionada = mat[i_fila]

    if not fila_seleccionada:
        return -1
    
    max_valor = [0, fila_seleccionada[0]]

    for i in range(1,len(fila_seleccionada)):
        if fila_seleccionada[i] > max_valor[1]:
            max_valor[1] = fila_seleccionada[i]
            max_valor[0] = i

    return max_valor[0]

def main():
    matrix = [
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]
    print(max_columna_mat(matrix, 1))

if __name__ == "__main__":
    main()