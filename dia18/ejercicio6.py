# Solicitamos al usuario un número entero positivo
num = int(input("Ingrese un número entero positivo: "))

# Generamos la tabla de multiplicar del 1 al 10
for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")