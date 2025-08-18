def inscritos_cursos(curso, est):
    inscritos = []

    for key, conj in est.items():
        conj = list(conj)
        for conjunto in conj:
            if conjunto == curso:
                inscritos.append(key)
        conj = set(conj)

    return inscritos

def main():
    estudiantes = {
        'Ana': {'matematicas', 'historia', 'literatura'},
        'Luis': {'quimica', 'fisica'},
        'María': {'biologia', 'matematicas'},
        'Jorge': {'arte', 'musica'}
    }
    print("Estudiantes inscritos a matematicas: ", inscritos_cursos("matematicas", estudiantes))

if __name__ == "__main__":
    main()
