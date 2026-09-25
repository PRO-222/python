import os
import tkinter as tk


def abrir_calculadora():
    os.system("calc")


# Creación de la ventana principal
ventana = tk.Tk()
ventana.title("Abrir Calculadora")

# Creación del botón que ejecuta la función
boton = tk.Button(
    ventana, text="Abrir Calculadora", command=abrir_calculadora
)
boton.pack(pady=20)

# Bucle principal de la interfaz
ventana.mainloop()