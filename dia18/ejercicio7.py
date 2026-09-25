# Creámos una lista vacía para guardar los números
numeros = []

# Pedimos 5 números al usuario
for i in range(5):
    num = float(input(f"Ingrese el número {i + 1}: "))
    numeros.append(num)

# Mostramos la lista completa y la suma total
print("Lista de números:", numeros)
print("Suma de los números:", sum(numeros))