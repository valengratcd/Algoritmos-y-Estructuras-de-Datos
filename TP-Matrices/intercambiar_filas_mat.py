def intercambiar_filas(mat, inx1: int, inx2: int) -> int:
    if inx1 is None or inx2 is None or inx1 >= len(mat) or inx2 >= len(mat) or not mat[inx1] or not mat[inx2]:
        return -100
    
    mat[inx1], mat[inx2] = mat[inx2], mat[inx1]

    return mat

def main():
    matrix = [
        [1,2,3],
        [4,5,6],
        [3,8,9]
    ]
    print(intercambiar_filas(matrix, 1, 2))

if __name__ == "__main__":
    main()