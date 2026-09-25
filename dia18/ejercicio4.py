# Solicitamos los tres números al usuario
a = float(input("Ingrese el primer número: "))
b = float(input("Ingrese el segundo número: "))
c = float(input("Ingrese el tercer número: "))

# Determinamos el mayor con max()
mayor = max(a, b, c)

print(f"El número mayor es: {mayor}")