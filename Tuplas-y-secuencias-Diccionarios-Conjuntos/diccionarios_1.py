persona = {
    "nombre": "Ana",
    "edad": 25,
    "profesion": "Ingeniera"
}

persona.update({"edad": 18, "ciudad": "CABA"})
persona.pop("profesion")
print(persona)
