import os

while True:
    print(f"1. Bloc \n2. Calculadora \n3. Apagar  \n4. Cancelar Apagado \n0. Salir")

    resp = input ("Elige: ")
    if resp == "1":
        os.system("notepad")
    elif resp == "2":
        os.system("calc")
    elif resp == "3":
        os.system("shutdown -s -t 300")
    elif resp == "4":
        os.system("shutdown -a")
    elif resp == "0":
        break
    else:
        print("No se entiende la orden")