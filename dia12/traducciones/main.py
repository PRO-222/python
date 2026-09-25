from controller import ControladorTraduccion

controlador = ControladorTraduccion()

while True:
    print("1. Cargar palabra: ")
    print("2. Traducir: ")
    print("3. Salir")
    opcion = input("Elige: ")

    if opcion == "1":
        esp = input("Escribe la palabra en español: ")
        ing = input("Escribe la palabra en inglés: ")
        controlador.cargar_palabra(esp, ing)

    elif opcion == "2":
        palabra = input("Escriba la palabra a traducir: ")
        print(f"{palabra} : {controlador.traducir(palabra)}")

    elif opcion == "3":
        break