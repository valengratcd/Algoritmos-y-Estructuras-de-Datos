def max_fila_mat(mat, i_columna) -> int:
    if not mat or i_columna < 0 or i_columna >= len(mat):
        return -100
    
    transpuesta = list(zip(*mat))

    columna_seleccionada = transpuesta[i_columna]

    if not columna_seleccionada:
        return -1
    
    max_valor = [0, columna_seleccionada[0]]

    for i in range(1,len(columna_seleccionada)):
        if columna_seleccionada[i] > max_valor[1]:
            max_valor[1] = columna_seleccionada[i]
            max_valor[0] = i

    return max_valor[0]

def main():
    matrix = [
        [1,2,3],
        [4,5,6],
        [3,8,9]
    ]
    print(max_fila_mat(matrix, 0))

if __name__ == "__main__":
    main()