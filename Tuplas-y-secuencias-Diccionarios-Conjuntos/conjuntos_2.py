def eliminar_impares(con: set) -> set:
    con = list(con)
    for i, elemento in enumerate(con):
        if elemento & 1:
            con.pop(i)
    con = set(con)
    return con

def main():
    a = {1, 2, 3, 4, 5}
    print(eliminar_impares(a))

if __name__ == "__main__":
    main()    