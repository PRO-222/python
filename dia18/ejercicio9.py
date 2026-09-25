# Creamos el diccionario con los estudiantes y sus notas
notas = {"Juan": 85, "María": 90, "Pedro": 78, "Ana": 92}

# Solicitamos el nombre al usuario y formateamos la primera letra en mayúscula
nombre = input("Ingrese el nombre del estudiante: ").strip().capitalize()

# Verificamos si el nombre existe en el diccionario
if nombre in notas:
    print(f"La nota de {nombre} es {notas[nombre]}")
else:
    print("Estudiante no encontrado.")