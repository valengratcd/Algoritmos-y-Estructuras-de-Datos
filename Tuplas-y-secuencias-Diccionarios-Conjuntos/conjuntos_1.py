curso_a = {"Ana", "Luis", "Carlos", "Marta", "Elena"}
curso_b = {"Pedro", "Marta", "Jorge", "Ana", "Lucía"}

print(f"Estudiantes que están en ambos cursos {curso_a & curso_b}")
print(f"Estudiantes que solo se encuentran en el curso_a {curso_a - curso_b}")
print(f"Estudiantes combinados (sin repetir) {curso_a | curso_b}")
