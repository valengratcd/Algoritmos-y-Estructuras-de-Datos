def suma_columna_posicion_entero(mat, num: int) -> int:
    if (num >= len(mat)) or (not mat[num]) or (num is None):
        return -100
    
    transpuesta = list(zip(*mat))

    suma = 0

    for i in mat[num]:
        suma += i
    return suma

def main():
    matrix = [
        [1,2,3],
        [4,5,6],
        [3,8,9]
    ]
    print(suma_columna_posicion_entero(matrix, 2))

if __name__ == "__main__":
    main()