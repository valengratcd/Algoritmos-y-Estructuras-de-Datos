def devolver_numeros_pares(tupla: tuple) -> tuple:
    tupla = list(tupla)
    for i, elemento in enumerate(tupla):
        if elemento & 1:
            tupla.pop(i)

    return tuple(tupla)

def main():
    numeros = (1, 2, 3, 4, 5)
    print(devolver_numeros_pares(numeros))

if __name__ == "__main__":
    main()