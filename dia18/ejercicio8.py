# Definimos la tupla con los meses del año
meses = (
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
)

# Solicitamos un número al usuario
num_mes = int(input("Ingrese un número del 1 al 12: "))

# Verificamos que el número esté dentro del rango válido
if 1 <= num_mes <= 12:
    print(f"El mes correspondiente es {meses[num_mes - 1]}")
else:
    print("Número inválido.")